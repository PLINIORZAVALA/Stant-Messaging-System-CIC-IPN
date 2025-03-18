
# DID Management API

**Fecha de última actualización:** 18/03/2025
**Colaboradores:** 4

## Introducción

Este repositorio contiene una API desarrollada en Flask para la gestión de Identificadores Descentralizados (DIDs). La API permite crear, verificar y actualizar DIDs utilizando criptografía asimétrica (RSA). Los DIDs se almacenan en un registro local en formato JSON.

### Tecnologías utilizadas
- **Flask**: Framework web para Python.
- **Cryptography**: Librería para operaciones criptográficas.
- **RSA**: Algoritmo de criptografía asimétrica para la generación de claves y firmas.

---

## Empezando

### Prerrequisitos

Asegúrate de tener instalado lo siguiente en tu sistema:
- **Python 3.8 o superior**: [Descargar Python](https://www.python.org/downloads/)
- **Pip**: Gestor de paquetes de Python (viene incluido con Python 3.4+).

### Instalación

1. Clona el repositorio:
   ```bash
   https://github.com/PLINIORZAVALA/Stant-Messaging-System-CIC-IPN.git
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd tu-repositorio
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución

Para iniciar la API, ejecuta:
```bash
python3 DIDProvider3.py
```

La API estará disponible en `http://localhost:5000`.

---

## Uso de la API

### Crear un DID
**Endpoint:** `POST /CreateDID`

Crea un nuevo DID y lo almacena en el registro. Se requiere proporcionar una clave pública en formato PEM.

**Ejemplo de solicitud:**
```json
{
    "entity": "Example Corp",
    "name": "Example DID",
    "purpose": "Authentication",
    "publicKey": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
}
```

**Respuesta:**
```json
{
    "DID": "did:key:123e4567-e89b-12d3-a456-426614174000",
    "DID_Document": {
        "id": "did:key:123e4567-e89b-12d3-a456-426614174000",
        "controller": "Example Corp",
        "name": "Example DID",
        "purpose": "Authentication",
        "publicKey": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
    }
}
```

### Verificar un DID
**Endpoint:** `GET /VerifyDID`

Verifica si un DID existe en el registro.

**Parámetros:**
- `did`: El DID a verificar.

**Ejemplo de solicitud:**
```
GET /VerifyDID?did=did:key:123e4567-e89b-12d3-a456-426614174000
```

**Respuesta:**
```json
{
    "verified": true,
    "DID": "did:key:123e4567-e89b-12d3-a456-426614174000"
}
```

### Obtener el DID Document
**Endpoint:** `GET /DIDRegistryGet`

Retorna el DID Document y la clave pública asociada a un DID.

**Parámetros:**
- `did`: El DID a consultar.

**Ejemplo de solicitud:**
```
GET /DIDRegistryGet?did=did:key:123e4567-e89b-12d3-a456-426614174000
```

**Respuesta:**
```json
{
    "DID_Document": {
        "id": "did:key:123e4567-e89b-12d3-a456-426614174000",
        "controller": "Example Corp",
        "name": "Example DID",
        "purpose": "Authentication",
        "publicKey": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
    },
    "PublicKey": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
}
```

### Actualizar un DID
**Endpoint:** `POST /UpdateDID`

Actualiza el DID Document si la firma RSA es válida.

**Ejemplo de solicitud:**
```json
{
    "did": "did:key:123e4567-e89b-12d3-a456-426614174000",
    "signature": "base64-encoded-signature",
    "updates": {
        "purpose": "New Purpose"
    }
}
```

**Respuesta:**
```json
{
    "status": "DID Document updated",
    "DIDDocument": {
        "id": "did:key:123e4567-e89b-12d3-a456-426614174000",
        "controller": "Example Corp",
        "name": "Example DID",
        "purpose": "New Purpose",
        "publicKey": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
    }
}
```

---

## Contribuir

¡Agradecemos tu interés en contribuir a este proyecto! Por favor, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu contribución:
   ```bash
   git checkout -b nombre-de-tu-rama
   ```
3. Realiza tus cambios y asegúrate de que las pruebas pasen.
4. Envía un pull request con una descripción detallada de tus cambios.

### Reportar problemas

Si encuentras algún problema, por favor [abre un issue](https://github.com/PLINIORZAVALA) en nuestro repositorio.


### Notas adicionales:
- Asegúrate de reemplazar `tu-usuario` y `tu-repositorio` con los valores correctos de tu repositorio.
- Si tienes pruebas unitarias o documentación adicional, agrega secciones específicas para ellas.
