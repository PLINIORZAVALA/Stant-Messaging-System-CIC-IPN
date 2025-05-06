#!/usr/bin/env bash
# gen_keys.sh: Genera claves Ed25519/X25519 en PEM y JWK (OKP)
# Uso: ./gen_keys.sh

set -euo pipefail

# 1) Generar claves PEM
openssl genpkey -algorithm Ed25519 -out ed25519_priv.pem
openssl pkey -in ed25519_priv.pem -pubout -out ed25519_pub.pem

openssl genpkey -algorithm X25519 -out x25519_priv.pem
openssl pkey -in x25519_priv.pem -pubout -out x25519_pub.pem

echo "Claves PEM generadas:"
echo "  - ed25519_priv.pem"
echo "  - ed25519_pub.pem"
echo "  - x25519_priv.pem"
echo "  - x25519_pub.pem"

# 2) Convertir cada pública a JWK
for curve in ed25519 x25519; do
  # Extraer 32 bytes raw (últimos del DER)
  raw=$(openssl pkey -in "${curve}_pub.pem" -pubin -outform DER | tail -c 32)
  # Base64url sin padding
  xb64=$(printf '%s' "${raw}" | base64 | tr '+/' '-_' | tr -d '=')
  # Escribir JWK
  cat > "${curve}.jwk" <<EOF
{
  "kty": "OKP",
  "crv": "${curve^^}",
  "x": "${xb64}"
}
EOF
  echo "JWK generado: ${curve}.jwk"
done