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


def _fetch_plugin_manifest(repo: str, name: str) -> dict | None:
    # Try the plugin at the repo root first, then at a monorepo subpath
    # (plugins/<name>/.claude-plugin/plugin.json) so single-plugin repos AND
    # multi-plugin monorepos (e.g. amnesia) both sync.
    paths = (".claude-plugin/plugin.json", f"plugins/{name}/.claude-plugin/plugin.json")
    for ref in REFS:
        for path in paths:
            url = f"https://raw.githubusercontent.com/{repo}/{ref}/{path}"
            try:
                with urllib.request.urlopen(url, timeout=20) as r:
                    return json.loads(r.read().decode())
            except urllib.error.HTTPError as e:
                if e.code == 404:
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
        man = _fetch_plugin_manifest(src["repo"], entry["name"])
        if not man:
            print(f"  WARN  {entry['name']}: could not fetch source manifest ({src['repo']})", file=sys.stderr)
            continue
        for field in ("description", "homepage"):
            new = man.get(field)
            if new and entry.get(field) != new:
                entry[field] = new
                changed.append(f"{entry['name']}.{field}")
        # Track the source's declared version. If the source has NO version, the
        # plugin is in the commit-SHA regime (every commit ships); strip any stale
        # entry version so resolution falls through to the source commit SHA.
        ver = man.get("version")
        if ver:
            if entry.get("version") != ver:
                entry["version"] = ver
                changed.append(f"{entry['name']}.version->{ver}")
        elif "version" in entry:
            del entry["version"]
            changed.append(f"{entry['name']}.version removed (rolling / commit-SHA)")
    if changed:
        MKT.write_text(json.dumps(data, indent=2) + "\n")
        print("synced:", ", ".join(changed))
        return 0
    print("no changes — marketplace already tracks all sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
