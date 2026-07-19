#!/usr/bin/env bash
# Stranger install smoke: pin fetchable + root layout + thin-PATH launchers.
# Does not require a live `grok` binary — simulates what Grok verifies after clone.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MKT="$ROOT/.grok-plugin/marketplace.json"
FAIL=0

# Archetypes: T1 MCP, T2 uv, skill-only, hooks+skill
ARCHETYPES=(amnesia total-recall project-prospector screen-mcp searxng)

python3 - "$MKT" "${ARCHETYPES[@]}" <<'PY' || exit 1
import json, re, subprocess, sys
from pathlib import Path

mkt = Path(sys.argv[1])
want = set(sys.argv[2:])
data = json.loads(mkt.read_text())
by = {p["name"]: p for p in data["plugins"]}
missing = want - set(by)
if missing:
    print("ERROR: archetypes missing from catalog:", missing)
    sys.exit(1)
for name in sorted(want):
    p = by[name]
    url, sha = p["source"]["url"], p["source"]["sha"]
    print(f"== {name} ==")
    # pin must match origin HEAD (same contract as check-grok-pins-fresh.py)
    head = subprocess.check_output(
        ["git", "ls-remote", url, "HEAD"], text=True, timeout=30
    ).split()[0].lower()
    if head != sha.lower():
        print(f"FAIL pin stale for {name}: pin={sha[:12]} HEAD={head[:12]}")
        sys.exit(1)
    print(f"  pin==HEAD {sha[:12]}")
print("catalog archetypes OK")
PY

# Layout + launcher checks against sources/ when present (dev machine / CI with sources)
check_src() {
  local name="$1" repo="$2"
  local d="$ROOT/sources/$repo"
  if [[ ! -d "$d" ]]; then
    echo "SKIP sources/$repo (not checked out)"
    return 0
  fi
  echo "== layout $name ($repo) =="
  test -f "$d/.claude-plugin/plugin.json" || { echo "FAIL no root plugin.json $repo"; FAIL=1; return; }
  test ! -f "$d/plugin.json" || { echo "FAIL orphan root plugin.json $repo"; FAIL=1; return; }
  if [[ -f "$d/scripts/run-python.sh" ]]; then
    env -i HOME="$HOME" PATH="/usr/bin:/bin" bash "$d/scripts/run-python.sh" -c 'import sys; assert sys.version_info >= (3, 10)' \
      || { echo "FAIL thin PATH run-python $repo"; FAIL=1; return; }
    echo "  run-python thin PATH OK"
  fi
  if [[ -f "$d/scripts/mcp-server.sh" ]]; then
    bash -n "$d/scripts/mcp-server.sh" || { echo "FAIL bash -n mcp-server $repo"; FAIL=1; return; }
    echo "  mcp-server.sh syntax OK"
  fi
  # smoke if fast
  if [[ -f "$d/tests/smoke.sh" ]]; then
    (cd "$d" && bash tests/smoke.sh) >/tmp/stranger-smoke-"$name".log 2>&1 \
      && echo "  smoke OK" \
      || { echo "FAIL smoke $name (see /tmp/stranger-smoke-$name.log)"; FAIL=1; }
  fi
}

check_src amnesia amnesia
check_src total-recall total-recall
check_src project-prospector project-prospector
check_src screen-mcp screen-mcp
check_src searxng searxng-mcp

if [[ "$FAIL" -ne 0 ]]; then
  echo "stranger-smoke FAILED"
  exit 1
fi
echo "stranger-smoke PASSED"
