from flask import Flask, request, jsonify
import uuid
import json
import os
import base64
import base58
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

app = Flask(__name__)
DID_REGISTRY_FILE = 'did_registry.json'

# Carga o inicializa el registro de DID Documents
if os.path.exists(DID_REGISTRY_FILE):
    with open(DID_REGISTRY_FILE, 'r') as f:
        did_registry = json.load(f)
else:
    did_registry = {}

def save_registry():
    with open(DID_REGISTRY_FILE, 'w') as f:
        json.dump(did_registry, f, indent=4)

def decode_multibase_base58(mb_str: str) -> bytes:
    """Elimina prefijo 'z' y decodifica Base58."""
    if not mb_str.startswith('z'):
        raise ValueError('Cadena no usa multibase Base58 (falta prefijo z)')
    return base58.b58decode(mb_str[1:])

def verify_ed25519_signature(public_mb: str, signature_b64: str, message: bytes):
    """Verifica firma Ed25519 en mensaje usando clave multibase Base58."""
    data = decode_multibase_base58(public_mb)
    # El multicodec de ed25519-pub es 0xed01
    if not data.startswith(b'\xed\x01'):
        raise ValueError('Clave no es Ed25519 (multicodec inválido)')
    raw_pk = data[2:]
    pub_key = Ed25519PublicKey.from_public_bytes(raw_pk)
    sig = base64.b64decode(signature_b64)
    pub_key.verify(sig, message)

@app.route('/CreateDID', methods=['POST'])
def create_did():
    """
    Crea un DID:key a partir de dos JWKs (Ed25519 y X25519).
    Parámetros JSON esperados:
      - jwk_auth: JWK OKP Ed25519 ({kty, crv, x})
      - jwk_enc:  JWK OKP X25519 ({kty, crv, x})
    """
    data = request.json or {}
    jwk_auth = data.get('jwk_auth')
    jwk_enc = data.get('jwk_enc')
    if not jwk_auth or not jwk_enc:
        return jsonify({'error': 'Faltan jwk_auth o jwk_enc'}), 400

    # Validar formato de JWKs
    if jwk_auth.get('kty') != 'OKP' or jwk_auth.get('crv') != 'Ed25519' or 'x' not in jwk_auth:
        return jsonify({'error': 'jwk_auth inválido'}), 400
    if jwk_enc.get('kty') != 'OKP' or jwk_enc.get('crv') != 'X25519' or 'x' not in jwk_enc:
        return jsonify({'error': 'jwk_enc inválido'}), 400

    # Decodificar 'x' base64url y producir multibase Base58BTC
    raw_auth = base64.urlsafe_b64decode(jwk_auth['x'] + '==')
    mb_auth = 'z' + base58.b58encode(b'\xed\x01' + raw_auth).decode('utf-8')

    raw_enc = base64.urlsafe_b64decode(jwk_enc['x'] + '==')
    mb_enc = 'z' + base58.b58encode(b'\xec\x01' + raw_enc).decode('utf-8')

    # El DID se deriva de la clave de autenticación
    did = f"did:key:{mb_auth}"

    did_doc = {
        '@context': [
            'https://www.w3.org/ns/did/v1',
            'https://w3id.org/security/suites/ed25519-2020/v1',
            'https://w3id.org/security/suites/x25519-2020/v1'
        ],
        'id': did,
        'verificationMethod': [
            {
                'id': f'{did}#auth-key',
                'type': 'Ed25519VerificationKey2020',
                'controller': did,
                'publicKeyMultibase': mb_auth
            },
            {
                'id': f'{did}#enc-key',
                'type': 'X25519KeyAgreementKey2020',
                'controller': did,
                'publicKeyMultibase': mb_enc
            }
        ],
        'authentication': [f'{did}#auth-key'],
        'keyAgreement': [f'{did}#enc-key'],
        'service': [
            {
                'id': f'{did}#didcomm',
                'type': 'DIDCommMessaging',
                'serviceEndpoint': 'https://example.com/didcomm',
                'accept': ['didcomm/v2']
            }
        ]
    }

    # Guardar DID Document
    did_registry[did] = did_doc
    save_registry()

    return jsonify({'DID': did, 'DID_Document': did_doc}), 201

@app.route('/DIDRegistryGet', methods=['GET'])
def get_did_registry():
    """Devuelve el DID Document almacenado."""
    did = request.args.get('did')
    if not did or did not in did_registry:
        return jsonify({'error': 'DID no encontrado'}), 404
    return jsonify({'DID_Document': did_registry[did]}), 200

@app.route('/VerifySignedDID', methods=['POST'])
def verify_signed_did():
    """Verifica firma Ed25519 en el DID."""
    data = request.json or {}
    did = data.get('did')
    signature = data.get('signature')
    if not did or not signature or did not in did_registry:
        return jsonify({'error': 'Faltan did o signature'}), 400

    did_doc = did_registry[did]
    # Localizar clave auth-key
    auth_vm = next((vm for vm in did_doc['verificationMethod'] if vm['id'] == f'{did}#auth-key'), None)
    if not auth_vm:
        return jsonify({'error': 'verificationMethod auth-key no encontrado'}), 404

    try:
        verify_ed25519_signature(auth_vm['publicKeyMultibase'], signature, did.encode('utf-8'))
    except Exception as e:
        return jsonify({'verified': False, 'error': str(e)}), 403

    return jsonify({'verified': True, 'DID': did}), 200

@app.route('/UpdateDID', methods=['POST'])
def update_did():
    """Actualiza un DID Document tras verificar firma Ed25519."""
    data = request.json or {}
    did = data.get('did')
    signature = data.get('signature')
    updates = data.get('updates', {})
    if not did or not signature or did not in did_registry:
        return jsonify({'error': 'Faltan did o signature'}), 400

    did_doc = did_registry[did]
    auth_vm = next((vm for vm in did_doc['verificationMethod'] if vm['id'] == f'{did}#auth-key'), None)
    if not auth_vm:
        return jsonify({'error': 'verificationMethod auth-key no encontrado'}), 404

    try:
        verify_ed25519_signature(auth_vm['publicKeyMultibase'], signature, did.encode('utf-8'))
    except Exception as e:
        return jsonify({'error': 'Firma inválida', 'details': str(e)}), 403

    # Aplicar actualizaciones al DID Document (puede alterar secciones permitidas)
    did_doc.update(updates)
    did_registry[did] = did_doc
    save_registry()

    return jsonify({'status': 'DID Document updated', 'DIDDocument': did_doc}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
