#!/usr/bin/env python3
"""Sync each plugin entry in .claude-plugin/marketplace.json from its SOURCE
repo's .claude-plugin/plugin.json, so the marketplace always tracks the latest
plugin metadata instead of hand-maintained static copy.

For every plugin whose source is a github repo, this pulls the live
description (and homepage) from the source plugin manifest and writes it back.
Idempotent: exits 0 with 'no changes' when already in sync.
"""
from __future__ import annotations
import json, sys, urllib.request, urllib.error
from pathlib import Path

MKT = Path(__file__).resolve().parent.parent / ".claude-plugin" / "marketplace.json"
REFS = ("HEAD", "main", "master")


def _fetch_plugin_manifest(repo: str) -> dict | None:
    for ref in REFS:
        url = f"https://raw.githubusercontent.com/{repo}/{ref}/.claude-plugin/plugin.json"
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (404,):
                continue
        except Exception:
            continue
    return None


def main() -> int:
    data = json.loads(MKT.read_text())
    changed = []
    for entry in data.get("plugins", []):
        src = entry.get("source", {})
        if src.get("source") != "github" or not src.get("repo"):
            continue
        man = _fetch_plugin_manifest(src["repo"])
        if not man:
            print(f"  WARN  {entry['name']}: could not fetch source manifest ({src['repo']})", file=sys.stderr)
            continue
        for field in ("description", "homepage"):
            new = man.get(field)
            if new and entry.get(field) != new:
                entry[field] = new
                changed.append(f"{entry['name']}.{field}")
        # surface the latest declared version for visibility (does not pin install)
        ver = man.get("version")
        if ver and entry.get("version") != ver:
            entry["version"] = ver
            changed.append(f"{entry['name']}.version->{ver}")
    if changed:
        MKT.write_text(json.dumps(data, indent=2) + "\n")
        print("synced:", ", ".join(changed))
        return 0
    print("no changes — marketplace already tracks all sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
