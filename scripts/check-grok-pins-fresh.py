#!/usr/bin/env python3
"""Fail if any .grok-plugin url pin is not origin HEAD of that repo.

Run after generate-grok-catalog in CI, or against the committed catalog to
detect stale pins between syncs.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MKT = Path(".grok-plugin/marketplace.json")


def head_sha(url: str) -> str:
    out = subprocess.check_output(
        ["git", "ls-remote", url, "HEAD"], text=True, timeout=30
    )
    if not out.strip():
        raise RuntimeError(f"empty ls-remote for {url}")
    sha = out.split()[0].strip().lower()
    if not SHA_RE.match(sha):
        raise RuntimeError(f"bad HEAD sha for {url}: {sha!r}")
    return sha


def main() -> int:
    if not MKT.is_file():
        print(f"ERROR: missing {MKT}", file=sys.stderr)
        return 1
    data = json.loads(MKT.read_text(encoding="utf-8"))
    plugins = data.get("plugins") or []
    stale: list[str] = []
    errors: list[str] = []
    for p in plugins:
        name = p.get("name", "?")
        src = p.get("source") or {}
        if src.get("source") != "url":
            continue
        url = src.get("url") or ""
        pin = (src.get("sha") or "").lower()
        if not SHA_RE.match(pin):
            errors.append(f"{name}: invalid pin {pin!r}")
            continue
        try:
            head = head_sha(url)
        except Exception as e:
            errors.append(f"{name}: ls-remote failed: {e}")
            continue
        if head != pin:
            stale.append(f"{name}: pin={pin[:12]} HEAD={head[:12]}")
        else:
            print(f"  fresh {name} {pin[:12]}")
    if errors:
        print("Pin freshness ERRORS:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
    if stale:
        print("Pin freshness STALE (regenerate catalog / wait for hub sync):", file=sys.stderr)
        for s in stale:
            print(f"  - {s}", file=sys.stderr)
    if errors or stale:
        return 1
    print(f"All {len(plugins)} Grok pins match origin HEAD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
