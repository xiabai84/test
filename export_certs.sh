#!/bin/bash

JKS_FILE="${1:-keystore.jks}"
STOREPASS="${2:-changeit}"
OUTPUT_DIR="${3:-./certs_output}"

# --- Validate inputs ---
if [ ! -f "$JKS_FILE" ]; then
  echo "ERROR: JKS file not found: $JKS_FILE"
  echo "Usage: $0 <keystore.jks> [password] [output_dir]"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "================================================"
echo " JKS Certificate Exporter"
echo "================================================"
echo " Keystore : $JKS_FILE"
echo " Output   : $OUTPUT_DIR"
echo "------------------------------------------------"

# --- Extract all aliases ---
aliases=$(keytool -list -keystore "$JKS_FILE" -storepass "$STOREPASS" 2>/dev/null \
  | grep -E "PrivateKeyEntry|trustedCertEntry" \
  | awk -F',' '{print $1}' \
  | xargs)

if [ -z "$aliases" ]; then
  echo "ERROR: No certificates found. Check the JKS path or password."
  exit 1
fi

success=0
fail=0

# --- Export each certificate as PEM ---
for alias in $aliases; do
  safe_name=$(echo "$alias" | tr ' /:' '___')
  out_file="$OUTPUT_DIR/${safe_name}.pem"

  keytool -exportcert \
    -keystore "$JKS_FILE" \
    -storepass "$STOREPASS" \
    -alias "$alias" \
    -rfc \
    -file "$out_file" 2>/dev/null

  if [ $? -eq 0 ]; then
    echo "[OK]   $alias -> $out_file"
    ((success++))
  else
    echo "[FAIL] $alias -> export failed"
    ((fail++))
  fi
done

echo "------------------------------------------------"
echo " Done: $success exported, $fail failed"
echo "================================================"
