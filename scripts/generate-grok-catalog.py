#!/usr/bin/env python3
"""Generate .grok-plugin/marketplace.json from the 88plug Claude catalog.

This keeps the Grok-native catalog in sync with the authoritative
.claude-plugin/marketplace.json, while resolving current HEAD SHAs
for pinned reproducible installs and rich pre-install component display
in the Grok TUI.

Run manually or from CI before generate-grok-plugin-index.py.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

CLAUDE_MKT = Path(".claude-plugin/marketplace.json")
GROK_DIR = Path(".grok-plugin")
GROK_MKT = GROK_DIR / "marketplace.json"

def resolve_sha(repo: str) -> str:
    try:
        out = subprocess.check_output(
            ["git", "ls-remote", f"https://github.com/{repo}.git", "HEAD"],
            text=True,
            timeout=15,
        )
        return out.split()[0]
    except Exception as exc:
        print(f"WARNING: could not resolve sha for {repo}: {exc}")
        return "HEAD"

def main() -> int:
    claude = json.loads(CLAUDE_MKT.read_text(encoding="utf-8"))
    grok_plugins = []

    for entry in claude.get("plugins", []):
        src = entry.get("source", {})
        name = entry["name"]
        repo = None
        subdir_path = None

        # Claude catalog uses github | git-subdir | url (url preferred since
        # 2026-07 switch away from ambiguous github-type sources). All three
        # must resolve; skipping url left the Grok marketplace at 1 plugin.
        if src.get("source") == "github" and src.get("repo"):
            repo = src["repo"]
        elif src.get("source") in ("git-subdir", "url") and src.get("url"):
            m = re.search(r"github\.com[:/]+([^/]+/[^/.]+)", src["url"])
            if m:
                repo = m.group(1)
            if src.get("source") == "git-subdir":
                subdir_path = src.get("path")
            elif src.get("path"):
                # url + optional path (same shape as git-subdir)
                subdir_path = src.get("path")

        if not repo:
            print(f"Skipping {name}: no github repo")
            continue

        sha = resolve_sha(repo)

        grok_entry = {
            "name": name,
            "description": entry.get("description", ""),
            "category": entry.get("category", "productivity"),
            "source": {
                "source": "url",
                "url": f"https://github.com/{repo}.git",
                "sha": sha,
            },
            "homepage": entry.get("homepage", f"https://github.com/{repo}"),
        }

        if subdir_path:
            grok_entry["source"]["path"] = subdir_path

        if "tags" in entry:
            grok_entry["tags"] = entry["tags"]
        if "keywords" in entry:
            grok_entry["keywords"] = entry["keywords"]

        grok_plugins.append(grok_entry)

    GROK_DIR.mkdir(exist_ok=True)
    data = {
        "name": "88plug",
        "description": "Curated plugins by 88plug for Grok and Claude Code.",
        "owner": {"name": "88plug"},
        "plugins": grok_plugins,
    }

    GROK_MKT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {GROK_MKT} with {len(grok_plugins)} plugins")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
