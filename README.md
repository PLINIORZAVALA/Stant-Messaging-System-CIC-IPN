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

### Upgrade Steps 

#### Main Document Structure

- **`DIDProvider3.py`**: You must paste all the code provided for the backend.
- **`README.md`**: Update this file with instructions based on the code's functionality.
- **`bin` and `lib`**: These are the virtual environment directories where the backend runs (they do not require manual modification).
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

- The following files will be generated in `walletTools`:
- Public/private keys (e.g., `key_public.pem`, `key_private.pem`).
- Signature files (e.g., `did_signed.json`). 

#### Verificación:  

- Use `ls` to confirm that the files were created:
  ```bash
  ls -l
  ```  
