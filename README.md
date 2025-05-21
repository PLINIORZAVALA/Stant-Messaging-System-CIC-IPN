# DID Management API

**Last updated date:** 15/05/2025
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
- **Python 3.12.3 or higher**: [Download Python](https://www.python.org/downloads/)
- **Pip**: Python Package Manager (comes included with Python 3.4+).
- **WSL**: Ubuntu-24.04 versión need for SignDID whit OpenSSL version 3.x.x.x.

### Facility

1. Clone the branch repository:
   ```bash
   https://github.com/PLINIORZAVALA/Stant-Messaging-System-CIC-IPN/tree/test
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

## Upgrade Steps 

### Main Document Structure

- **`DIDProvider3.py`**: You must paste all the code provided for the backend.
- **`README.md`**: Update this file with instructions based on the code's functionality.
- **`venv`**: These are the virtual environment directories where the backend runs (they do not require manual modification).
- **`requirements.txt`**: List of dependencies required for installation (run `pip install -r requirements.txt`).
- **`walletTools`**: Folder containing the key management scripts.

#### Initial structure of the `walletTools` folder

- **`generateKeys.sh`**: Paste the complete code for the key generation script here.
- **`signDID.sh`**: Paste the complete code for the DID signing script here.

#### Final Post-Execution Files

Follow these steps to generate the final structure:

1. **Navigate to the correct folder**:  
   ```bash
   cd pocDavid/walletTools
   ```  
2. **Grant execute permissions** (only once):  
   ```bash
   chmod +x generateKeys.sh
   ```  
3. **Run the script**:
   ```bash
   ./generateKeys.sh
   ```  

#### Expected Output:

#### **Key Files**
| File | Description |
|---------|-------------|
| `ed25519.jwk` | Ed25519 key in JWK (JSON Web Key) format. |
| `ed25519_priv.pem` | Ed25519 private key in PEM format. |
| `ed25519_pub.pem` | Ed25519 public key in PEM format. |
| `x25519.jwk` | X25519 key (for ECDH) in JWK format. |
| `x25519_priv.pem` | X25519 private key in PEM format. |
| `x25519_pub.pem` | X25519 public key in PEM format. |

#### Verificación:  

- Use `ls` to confirm that the files were created:
  ```bash
  ls -l
  ```

### **Key Notes**
- **Ed25519**: Used for digital signatures.
- **X25519**: Used for key exchange (ECDH).
- **JWK vs. PEM**:
- `JWK` (JSON Web Key): Standard format for keys in web environments.
- `PEM`: Traditional (base64) format used in OpenSSL.
  
---

## Using the API

### Create a DID
**Endpoint:** `POST /CreateDID`

Creates a new DID and stores it in the registry. A public key in PEM format is required.

**Request example:**
```
wget --method=POST \
  --header="Content-Type: application/json" \
  --body-data='{
    "jwk_auth": {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "z9yQ7eAiZg9DgSI9QhIDhkd3blOvFHmIo-Dqg0PHpZA"
    },
    "jwk_enc": {
      "kty": "OKP",
      "crv": "X25519",
      "x": "lzeH6SSSyArkVUoEbTyif6xptkGtuoUUMit205-w0D0"
    }
  }' \
  http://localhost:5000/CreateDID
```

**Answer in did_registry.json:**
```json
{
    "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC": {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/suites/ed25519-2020/v1",
            "https://w3id.org/security/suites/x25519-2020/v1"
        ],
        "id": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC",
        "verificationMethod": [
            {
                "id": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC#auth-key",
                "type": "Ed25519VerificationKey2020",
                "controller": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC",
                "publicKeyMultibase": "z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC"
            },
            {
                "id": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC#enc-key",
                "type": "X25519KeyAgreementKey2020",
                "controller": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC",
                "publicKeyMultibase": "z2D7H2TMK2FWCmFG9uxzcAsBjdTAMfjHBjjVtWshJrJRzZL"
            }
        ],
        "authentication": [
            "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC#auth-key"
        ],
        "keyAgreement": [
            "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC#enc-key"
        ],
        "service": [
            {
                "id": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC#didcomm",
                "type": "DIDCommMessaging",
                "serviceEndpoint": "https://example.com/didcomm",
                "accept": [
                    "didcomm/v2"
                ]
            }
        ]
    }
}

```

### Get a DID
**Endpoint:** `GET /DIDRegistryGet`

Get if a DID exists in the registry.

**Parameters:**
- `did`: The DID to verify.

**Request example:**
```
wget --method=GET \
  --output-document=did_response.json \
"http://localhost:5000/DIDRegistryGet?did=did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb"
```

**Answer in did_response.json:**
```json
{
  "DID_Document": {
    "@context": [
      "https://www.w3.org/ns/did/v1",
      "https://w3id.org/security/suites/ed25519-2020/v1",
      "https://w3id.org/security/suites/x25519-2020/v1"
    ],
    "authentication": [
      "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC#auth-key"
    ],
    "id": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC",
    "keyAgreement": [
      "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC#enc-key"
    ],
    "service": [
      {
        "accept": [
          "didcomm/v2"
        ],
        "id": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC#didcomm",
        "serviceEndpoint": "https://example.com/didcomm",
        "type": "DIDCommMessaging"
      }
    ],
    "verificationMethod": [
      {
        "controller": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC",
        "id": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC#auth-key",
        "publicKeyMultibase": "z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC",
        "type": "Ed25519VerificationKey2020"
      },
      {
        "controller": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC",
        "id": "did:key:z6Mkh3pN8SDcZkpbivbPu34747ZMpzuUdjJWFCQgSuxYj1xC#enc-key",
        "publicKeyMultibase": "z2D7H2TMK2FWCmFG9uxzcAsBjdTAMfjHBjjVtWshJrJRzZL",
        "type": "X25519KeyAgreementKey2020"
      }
    ]
  }
}

```

### Signature example:
1. **Navigate to the correct folder**:  
   ```bash
   cd pocDavid/walletTools
   ```  
2. **Grant execute permissions** (only once):  
   ```bash
   chmod +x signDID.sh
   ```  
3. **Signature:**
   
   Signature format
   ```
   ./ signDID.sh -k <privkey.pem> -d <DID> [-o <out_file>]
   ```
   Example Singnature:
   ```
   ./signDID.sh -k ed25519_priv.pem -d did:key:z6MkuCWyYtNs3Jw1QRN8E7F1uQvJuGJMDm3v9Q8rkoQ3PHPQ -o signature.txt
   ```
   Example Answer:
   ```
   8Zb6iM2ysBAxiIstjX1USJWKvldzAwM7lP9IqY9kurWagEnT3UJHcG3lrZMCCic5B8vX4mvSwnxDLjaeQPjpAQ==
   ```
4. **Answer in CreateDID.json:**
   
   This file serves as backup metadata or evidence of which DID and public keys were used when signing a message or document.
```json
{
  "DID": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb",
  "DID_Document": {
    "@context": [
      "https://www.w3.org/ns/did/v1",
      "https://w3id.org/security/suites/ed25519-2020/v1",
      "https://w3id.org/security/suites/x25519-2020/v1"
    ],
    "authentication": [
      "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#auth-key"
    ],
    "id": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb",
    "keyAgreement": [
      "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#enc-key"
    ],
    "service": [
      {
        "accept": [
          "didcomm/v2"
        ],
        "id": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#didcomm",
        "serviceEndpoint": "https://example.com/didcomm",
        "type": "DIDCommMessaging"
      }
    ],
    "verificationMethod": [
      {
        "controller": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb",
        "id": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#auth-key",
        "publicKeyMultibase": "z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb",
        "type": "Ed25519VerificationKey2020"
      },
      {
        "controller": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb",
        "id": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#enc-key",
        "publicKeyMultibase": "z6LSmrTqdDxHJdefaTwcS5AHZ3o7qcQQuDpyioVESbUDB6LC",
        "type": "X25519KeyAgreementKey2020"
      }
    ]
  }
}

```
### VerifySignedDID
**Endpoint:** `POST /VerifySignedDID`

POST if a DID exists in the registry.

**Parameters:**
- `did`: The DID to verify.

**Request example:**
```
wget --method=POST \
  --header="Content-Type: application/json" \
  --body-data='{
    "did": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb",
    "signature": "8Zb6iM2ysBAxiIstjX1USJWKvldzAwM7lP9IqY9kurWagEnT3UJHcG3lrZMCCic5B8vX4mvSwnxDLjaeQPjpAQ=="
  }' \
  http://localhost:5000/VerifySignedDID   
```
**Answer in verifySignedDID.json**
```json
{
  "DID": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb",
  "verified": true
}
```
### VerifySignedDID
**Endpoint:** `POST /UpdateDID`

POST updates DID Document if the RSA signature is valid.
**Request example:**
```
wget --method=POST \
  --header="Content-Type: application/json" \
  --body-data='{
    "did": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb",
    "signature": "8Zb6iM2ysBAxiIstjX1USJWKvldzAwM7lP9IqY9kurWagEnT3UJHcG3lrZMCCic5B8vX4mvSwnxDLjaeQPjpAQ==",
    "updates": {
      "service": [
        {
          "id": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#mi-servicio",
          "type": "DIDCommMessaging",
          "serviceEndpoint": "https://nuevo-ejemplo.com/endpoint",
          "accept": ["didcomm/v2"],
          "routingKeys": ["did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#enc-key"]
        }
      ]
    }
  }' \
  http://localhost:5000/UpdateDID
```
**Answer in did_registry.json**
```json
{
    "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb": {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/suites/ed25519-2020/v1",
            "https://w3id.org/security/suites/x25519-2020/v1"
        ],
        "id": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb",
        "verificationMethod": [
            {
                "id": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#auth-key",
                "type": "Ed25519VerificationKey2020",
                "controller": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb",
                "publicKeyMultibase": "z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb"
            },
            {
                "id": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#enc-key",
                "type": "X25519KeyAgreementKey2020",
                "controller": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb",
                "publicKeyMultibase": "z6LSmrTqdDxHJdefaTwcS5AHZ3o7qcQQuDpyioVESbUDB6LC"
            }
        ],
        "authentication": [
            "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#auth-key"
        ],
        "keyAgreement": [
            "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#enc-key"
        ],
        "service": [
            {
                "id": "did:key:z6MktSfWTatv5dUtfQjt3Q2WjsrWMJFcuqTGRumSgbKNaUzb#didcomm",
                "type": "DIDCommMessaging",
                "serviceEndpoint": "https://example.com/didcomm",
                "accept": [
                    "didcomm/v2"
                ]
            }
        ]
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

