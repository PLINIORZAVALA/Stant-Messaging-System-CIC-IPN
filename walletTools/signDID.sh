#!/usr/bin/env bash
# sign_did.sh: Firma un DID con una clave privada Ed25519
# Uso: ./signDID.sh -k <privkey.pem> -d <DID> [-o <out_file>]

set -euo pipefail

authUsage() {
  echo "Usage: $0 -k <privkey.pem> -d <DID> [-o <out_file>]"
  exit 1
}

privkey=""
did=""
out=""

while getopts "k:d:o:" opt; do
  case "$opt" in
    k) privkey="$OPTARG" ;;  
    d) did="$OPTARG" ;;      
    o) out="$OPTARG" ;;      
    *) authUsage ;;              
  esac
done
shift $((OPTIND-1))

# Verificar parámetros
[[ -z "$privkey" || -z "$did" ]] && authUsage

# Crear archivo temporal para el DID
tmpfile=$(mktemp)
echo -n "$did" > "$tmpfile"

# Firmar el DID usando rawin desde archivo
signature=$(openssl pkeyutl -sign -inkey "$privkey" -rawin -in "$tmpfile" \
  | openssl base64 -A)

# Eliminar temporal
rm -f "$tmpfile"

# Salida
if [[ -n "$out" ]]; then
  echo "$signature" > "$out"
  echo "Firma guardada en $out"
else
  echo "$signature"
fi