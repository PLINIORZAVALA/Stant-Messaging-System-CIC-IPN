from flask import Flask, request, jsonify
import uuid
import json
import os
import base64

# Librerías de criptografía
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

app = Flask(__name__)

# Ruta para almacenar el registro de DIDs
DID_REGISTRY_FILE = 'did_registry.json'

# Cargar el registro si existe o inicializar uno nuevo
if os.path.exists(DID_REGISTRY_FILE):
    with open(DID_REGISTRY_FILE, 'r') as f:
        did_registry = json.load(f)
else:
    did_registry = {}

def save_registry():
    with open(DID_REGISTRY_FILE, 'w') as f:
        json.dump(did_registry, f, indent=4)

def generate_did():
    return f"did:key:{uuid.uuid4()}"

def generate_key_pair():
    """
    Genera un par de claves RSA (2048 bits) y devuelve
    la clave pública y la clave privada en formato PEM.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    return public_pem, private_pem

@app.route('/CreateDID', methods=['POST'])
def create_did():
    """
    Crea un DID, genera un par de claves RSA y
    almacena solo la clave pública en el servidor.
    """
    data = request.json

    # Validar que se proporcionen los datos básicos
    required_fields = ['entity', 'name', 'purpose']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Generar el DID y el par de claves RSA
    did = generate_did()
    public_pem, private_pem = generate_key_pair()

    did_document = {
        "id": did,
        "controller": data['entity'],
        "name": data['name'],
        "purpose": data['purpose'],
        "publicKey": public_pem
    }

    # Almacenar solo la clave pública
    did_registry[did] = {
        "did_document": did_document,
        "public_key": public_pem
    }

    save_registry()

    return jsonify({
        "DID": did,
        "DID_Document": did_document,
        "PublicKey": public_pem,
        "PrivateKey": private_pem  # Se envía al usuario, pero NO se almacena en el servidor
    }), 201

@app.route('/VerifyDID', methods=['GET'])
def verify_credential():
    """
    Verifica si un DID existe en el registro.
    """
    did = request.args.get('did')
    if not did or did not in did_registry:
        return jsonify({"error": "DID not found or invalid"}), 404

    return jsonify({"verified": True, "DID": did}), 200

@app.route('/DIDRegistryGet', methods=['GET'])
def get_did_registry():
    """
    Retorna el DID Document y la clave pública almacenada.
    """
    did = request.args.get('did')
    if not did or did not in did_registry:
        return jsonify({"error": "DID not found"}), 404

    entry = did_registry[did]
    return jsonify({
        "DID_Document": entry["did_document"],
        "PublicKey": entry["public_key"]
    }), 200

@app.route('/UpdateDID', methods=['POST'])
def update_did():
    """
    Actualiza el DID Document si la firma RSA es válida.
    Se espera:
      - did: El DID a actualizar
      - signature: Firma RSA (base64) de la cadena 'did' con la clave privada
      - updates: Campos que se quieren actualizar en el DID Document
    """
    data = request.json
    did = data.get('did')
    signature_b64 = data.get('signature')
    updates = data.get('updates', {})

    if not did or did not in did_registry:
        return jsonify({'error': 'DID not found'}), 404

    # Recuperar la public_key del registro
    public_pem = did_registry[did].get('public_key')
    if not public_pem:
        return jsonify({'error': 'No public key found for DID'}), 403

    # Verificar la firma
    try:
        public_key = serialization.load_pem_public_key(public_pem.encode('utf-8'))
        signature = base64.b64decode(signature_b64)
        # Se firma la cadena "did" (puede ajustarse según necesidad real)
        public_key.verify(
            signature,
            did.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except Exception as e:
        return jsonify({'error': 'Invalid signature', 'details': str(e)}), 403

    # Actualizar el DID Document con los campos recibidos
    did_registry[did]['did_document'].update(updates)
    save_registry()

    return jsonify({
        'status': 'DID Document updated',
        'DIDDocument': did_registry[did]['did_document']
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)