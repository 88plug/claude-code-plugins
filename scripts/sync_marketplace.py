#!/usr/bin/env python3
"""Sync each plugin entry in .claude-plugin/marketplace.json from its SOURCE
repo's .claude-plugin/plugin.json, so the marketplace always tracks the latest
plugin metadata instead of hand-maintained static copy.

For every plugin whose source is a github repo, this pulls the live
description (and homepage) from the source plugin manifest and writes it back.
Idempotent: exits 0 with 'no changes' when already in sync.
"""
from __future__ import annotations
import json, os, sys, urllib.request, urllib.error
from pathlib import Path

MKT = Path(__file__).resolve().parent.parent / ".claude-plugin" / "marketplace.json"
REFS = ("HEAD", "main", "master")
_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

import re as _re


def _headers():
    h = {"User-Agent": "88plug-sync"}
    if _TOKEN:
        h["Authorization"] = f"Bearer {_TOKEN}"
    return h


def _auto_version(repo):
    """Friendly hands-free version for a rolling (version-less) plugin:
    YEAR.MONTH.BUILD, where BUILD is the repo's total commit count. One request
    yields the latest commit (for the date) and, via the Link header's last page,
    the commit count. Monotonic and unique per push, so users see a readable
    version that increases on every release instead of a bare commit hash."""
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/commits?per_page=1", headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            link = r.headers.get("Link", "")
            items = json.loads(r.read().decode())
    except Exception:
        return None
    if not items:
        return None
    commit = items[0].get("commit", {})
    date = (commit.get("committer", {}).get("date")
            or commit.get("author", {}).get("date", ""))
    if len(date) < 7:
        return None
    m = _re.search(r'[?&]page=(\d+)>;\s*rel="last"', link)
    count = int(m.group(1)) if m else len(items)
    return f"{date[:4]}.{int(date[5:7])}.{count}"
def _repo_of(src):
    """Resolve owner/repo from a github, git-subdir, or url source (None otherwise)."""
    if src.get("source") == "github" and src.get("repo"):
        return src["repo"]
    if src.get("source") in ("git-subdir", "url") and src.get("url"):
        m = _re.search(r"github\.com[:/]+([^/]+/[^/.]+)", src["url"])
        return m.group(1) if m else None
    return None


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
        repo = _repo_of(src)
        if not repo:
            continue
        man = _fetch_plugin_manifest(repo, entry["name"])
        if not man:
            print(f"  WARN  {entry['name']}: could not fetch source manifest ({repo})", file=sys.stderr)
            continue
        for field in ("description", "homepage"):
            new = man.get(field)
            if new and entry.get(field) != new:
                entry[field] = new
                changed.append(f"{entry['name']}.{field}")
        # Version shown in the catalog + `claude plugin list`. If the source
        # declares a semver, mirror it. If not (rolling), stamp a friendly
        # auto-version YEAR.MONTH.BUILD so users see a readable, monotonically
        # increasing version instead of a bare commit hash. Refreshed every sync.
        ver = man.get("version") or _auto_version(repo)
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
