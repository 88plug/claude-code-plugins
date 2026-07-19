#!/usr/bin/env python3
"""Generate .grok-plugin/marketplace.json from the 88plug Claude catalog.

Keeps the Grok-native catalog in sync with the authoritative
.claude-plugin/marketplace.json while resolving full commit SHAs for
content-addressable installs (Grok re-verifies HEAD == sha after clone).

Grok Build contract (validated vs xai-org/grok-build + plugin-marketplace):

  Publisher (required for remote url sources):
    - Full 40-char lowercase hex `sha` on every url entry (official validate-catalog.py)
    - Grok CLI re-verifies HEAD == sha after clone when pin present

  Runtime (git_install / installer):
    - Pin present → fetch-by-sha + ShaMismatch guard
    - Pin absent → mutable ref clone (fallback); require_sha can refuse

  Dual catalog: Grok prefers `.grok-plugin/`; Claude catalog may stay rolling (no sha).
  keywords = matcher; tags = display; optional domains = URL-paste matching.
  plugin-index sha must match catalog pin or TUI hides components.

Run manually or from CI before generate-grok-plugin-index.py.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

CLAUDE_MKT = Path(".claude-plugin/marketplace.json")
GROK_DIR = Path(".grok-plugin")
GROK_MKT = GROK_DIR / "marketplace.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
GITHUB_REPO_RE = re.compile(r"github\.com[:/]+([^/]+/[^/.]+)")

# Product hosts for Grok URL-paste matching (optional; skip github.com noise).
PRODUCT_DOMAINS: dict[str, list[str]] = {
    "deepwiki": ["deepwiki.com"],
}


def resolve_sha(repo: str) -> str:
    """Resolve full commit SHA for github.com/<owner>/<repo> HEAD."""
    url = f"https://github.com/{repo}.git"
    try:
        out = subprocess.check_output(
            ["git", "ls-remote", url, "HEAD"],
            text=True,
            timeout=30,
        )
    except Exception as exc:
        raise RuntimeError(f"could not resolve sha for {repo}: {exc}") from exc
    if not out.strip():
        raise RuntimeError(f"empty ls-remote for {repo}")
    sha = out.split()[0].strip().lower()
    if not SHA_RE.match(sha):
        raise RuntimeError(f"invalid sha for {repo}: {sha!r}")
    return sha


def keywords_from_entry(name: str, entry: dict) -> list[str]:
    """Grok matcher keywords — not the same as Claude hub tags.

    Prefer explicit keywords; else derive from tags (drop type:* prefixes)
    and always include the install name.
    """
    seen: set[str] = set()
    out: list[str] = []

    def add(term: str) -> None:
        t = term.strip()
        if not t:
            return
        key = t.casefold()
        if key in seen:
            return
        seen.add(key)
        out.append(t)

    for kw in entry.get("keywords") or []:
        if isinstance(kw, str):
            add(kw)

    for tag in entry.get("tags") or []:
        if not isinstance(tag, str):
            continue
        if tag.startswith("type:"):
            continue
        add(tag)

    add(name)
    # Niche install names that differ from repo (matcher convenience)
    if name == "searxng":
        add("searxng-mcp")
        add("web search")
    elif name == "use-latest-version":
        add("use-latest-version-mcp")
        add("dependency versions")

    return out


def repo_from_source(src: dict) -> tuple[str | None, str | None]:
    """Return (github owner/repo, optional subdir path)."""
    repo = None
    subdir_path = None
    if src.get("source") == "github" and src.get("repo"):
        repo = src["repo"]
    elif src.get("source") in ("git-subdir", "url") and src.get("url"):
        m = GITHUB_REPO_RE.search(src["url"])
        if m:
            repo = m.group(1).removesuffix(".git")
        if src.get("source") == "git-subdir":
            subdir_path = src.get("path")
        elif src.get("path"):
            subdir_path = src.get("path")
    return repo, subdir_path


def main() -> int:
    if not CLAUDE_MKT.is_file():
        print(f"ERROR: missing {CLAUDE_MKT}", file=sys.stderr)
        return 1

    claude = json.loads(CLAUDE_MKT.read_text(encoding="utf-8"))
    claude_plugins = claude.get("plugins", [])
    if not isinstance(claude_plugins, list) or not claude_plugins:
        print("ERROR: Claude catalog has no plugins", file=sys.stderr)
        return 1

    grok_plugins = []
    errors: list[str] = []

    for entry in claude_plugins:
        name = entry.get("name")
        if not name:
            errors.append("catalog entry without name")
            continue

        src = entry.get("source") or {}
        if not isinstance(src, dict):
            errors.append(f"{name}: source must be an object")
            continue

        repo, subdir_path = repo_from_source(src)
        if not repo:
            errors.append(f"{name}: no github repo in source")
            continue

        try:
            sha = resolve_sha(repo)
        except RuntimeError as e:
            errors.append(str(e))
            continue

        grok_entry: dict = {
            "name": name,
            "description": entry.get("description", ""),
            "category": entry.get("category", "productivity"),
            "author": {"name": "88plug"},
            "source": {
                "source": "url",
                "url": f"https://github.com/{repo}.git",
                "sha": sha,
            },
            "homepage": entry.get("homepage", f"https://github.com/{repo}"),
            "keywords": keywords_from_entry(name, entry),
        }

        if subdir_path:
            grok_entry["source"]["path"] = subdir_path

        # Keep tags for TUI display (Grok IndexEntry.tags)
        if "tags" in entry and entry["tags"]:
            grok_entry["tags"] = entry["tags"]

        # Optional domains (Grok IndexEntry.domains — URL paste matching)
        domains = entry.get("domains") or PRODUCT_DOMAINS.get(name)
        if domains:
            grok_entry["domains"] = list(domains)

        grok_plugins.append(grok_entry)

    if errors:
        print("ERROR: Grok catalog generation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    if len(grok_plugins) != len(claude_plugins):
        print(
            f"ERROR: Grok plugin count {len(grok_plugins)} != Claude {len(claude_plugins)}",
            file=sys.stderr,
        )
        return 1

    GROK_DIR.mkdir(exist_ok=True)
    data = {
        "name": "88plug",
        "description": "Curated plugins by 88plug for Grok Build and Claude Code.",
        "owner": {"name": "88plug"},
        "plugins": grok_plugins,
    }

    GROK_MKT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {GROK_MKT} with {len(grok_plugins)} plugins (all url+sha)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
