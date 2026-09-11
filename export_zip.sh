#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
OUT_FILE="${1:-$PARENT_DIR/learning_langgraph.zip}"

cd "$PARENT_DIR"
rm -f "$OUT_FILE"
zip -r -q "$OUT_FILE" "$(basename "$SCRIPT_DIR")" \
  -x "*.DS_Store" \
  -x "*/__pycache__/*"

echo "Created: $OUT_FILE"
echo "Size: $(du -h "$OUT_FILE" | cut -f1)"
