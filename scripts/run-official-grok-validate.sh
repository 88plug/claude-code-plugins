#!/usr/bin/env bash
# Run xAI official validate-catalog against .grok-plugin only.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT
mkdir -p "$TMP/.grok-plugin"
cp "$ROOT/.grok-plugin/marketplace.json" "$TMP/.grok-plugin/"
# Official script uses CWD-relative paths
(
  cd "$TMP"
  python3 "$ROOT/scripts/vendor/xai-validate-catalog.py"
)
