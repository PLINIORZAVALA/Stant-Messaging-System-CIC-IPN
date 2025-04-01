
# DID Management API

**Last updated date:** 18/03/2025
**Collaborators:** 4

## Introduction

This repository contains a Flask-based API for managing decentralized identifiers (DIDs). The API allows you to create, verify, and update DIDs using asymmetric cryptography (RSA). DIDs are stored in a local registry in JSON format.

### Technologies used
- **Flask**: Web framework for Python.
- **Cryptography**: Library for cryptographic operations.
- **RSA**: Asymmetric cryptography algorithm for key and signature generation.

---

## Getting started

### Prerequisites

Make sure you have the following installed on your system:
- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **Pip**: Python Package Manager (comes included with Python 3.4+).

### Facility

1. Clone the repository:
   ```bash
   https://github.com/PLINIORZAVALA/Stant-Messaging-System-CIC-IPN.git
   ```
2. Navigate to the project directory:
   ```bash
   cd tu-repositorio
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Execution

To start the API, run:
```bash
python3 DIDProvider3.py
```

The API will be available at `http://localhost:5000`.

---

## Using the API

### Create a DID
**Endpoint:** `POST /CreateDID`

Creates a new DID and stores it in the registry. A public key in PEM format is required.

**Request example:**
```json
wget --header 'Content-Type: application/json' \
  --post-data '{
    "entity": "MiOrganizacion",
    "name": "MiIdentidadDigital",
    "purpose": "autenticacion",
    "publicKey": "-----BEGIN PUBLIC KEY-----\nTU_CLAVE_PUBLICA_AQUI\n-----END PUBLIC KEY-----"
  }' \
  -O - \
  http://localhost:5000/CreateDID
```

**Answer:**
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

### Verify a DID
**Endpoint:** `GET /VerifyDID`

Checks if a DID exists in the registry.

**Parameters:**
- `did`: The DID to verify.

**Request example:**
```
GET /VerifyDID?did=did:key:123e4567-e89b-12d3-a456-426614174000
```

**Answer:**
```json
{
    "verified": true,
    "DID": "did:key:123e4567-e89b-12d3-a456-426614174000"
}
```

### Get the Document DID
**Endpoint:** `GET /DIDRegistryGet`

Returns the Document DID and the public key associated with a DID.

**Parameters:**
- `did`: The DID to query.

**Request example:**
```
GET /DIDRegistryGet?did=did:key:123e4567-e89b-12d3-a456-426614174000
```

**Answer:**
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
### Signature DID
**Signature example:**
```bash
echo -n "did:key:f98fb796-f57c-464a-a1ee-e5e21b9f438f" | openssl dgst -sha256 -sign private_key.pem
```

### Update a DID
**Endpoint:** `POST /UpdateDID`

Updates the DID Document if the RSA signature is valid.

**Request example:**
```json
{
    "did": "did:key:123e4567-e89b-12d3-a456-426614174000",
    "signature": "base64-encoded-signature",
    "updates": {
        "purpose": "New Purpose"
    }
}
```

**Answer:**
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

## Contribute

Thank you for your interest in contributing to this project! Please follow these steps:

1. Fork the repository.
2. Create a branch for your contribution:
```bash
git checkout -b your-branch-name
```
3. Make your changes and make sure the tests pass.
4. Submit a pull request with a detailed description of your changes.

### Reporting Issues

If you encounter any issues, please open an issue in our repository.


### Additional Notes:
- Make sure to replace `your-username` and `your-repository` with the correct values ​​for your repository.
- If you have unit tests or additional documentation, add specific sections for them.
