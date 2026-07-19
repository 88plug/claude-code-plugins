#!/usr/bin/env python3
"""Generate README.md entirely from .claude-plugin/marketplace.json.

No plugin data is hand-maintained in the README. The badge count and the two
category sections — each a vertical per-plugin stanza (name, auto-version linked
to its commit, derived component "surfaces", a trimmed description, and a fenced
install command) — are rendered from the marketplace catalog, which
sync_marketplace.py keeps in step with each plugin's source manifest. Mobile-first
by design: no wide tables (GitHub never reflows them on a phone).

Component "surfaces" (e.g. "1 skill · 7 commands · 5 agents · hooks · MCP server")
are counted live from each plugin's source repo tree via the GitHub API, and each
rolling plugin's version is YEAR.MONTH.<commit-count>, so adding or updating a
plugin refreshes the README with zero hand edits.

Run order in CI: sync_marketplace.py  ->  build_readme.py  ->  commit both.
"""
from __future__ import annotations
import json, os, sys, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MKT = ROOT / ".claude-plugin" / "marketplace.json"
README = ROOT / "README.md"
REFS = ("HEAD", "main", "master")

def _repo_of(src):
    if src.get("source") == "github" and src.get("repo"):
        return src["repo"]
    if src.get("source") in ("git-subdir", "url") and src.get("url"):
        import re as _re
        m = _re.search(r"github\.com[:/]+([^/]+/[^/.]+)", src["url"])
        return m.group(1) if m else ""
    return ""
# Authenticate API calls when a token is present (GITHUB_TOKEN in CI). The GitHub
# trees API is rate-limited to 60/hr unauthenticated — on a shared CI runner IP
# that exhausts instantly and surfaces come back empty. With the token it's 5000/hr.
_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def _headers():
    h = {"User-Agent": "88plug-readme-builder"}
    if _TOKEN:
        h["Authorization"] = f"Bearer {_TOKEN}"
    return h


def _get(url: str):
    req = urllib.request.Request(url, headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def _latest_sha(repo: str):
    """Latest commit SHA on the source repo's default branch — the real version a
    rolling (version-less) plugin resolves to. Refreshed on every catalog sync."""
    for ref in REFS:
        c = _get(f"https://api.github.com/repos/{repo}/commits/{ref}")
        if c and c.get("sha"):
            return c["sha"][:12]
    return None


def _repo_tree(repo: str) -> list[str]:
    for ref in REFS:
        t = _get(f"https://api.github.com/repos/{repo}/git/trees/{ref}?recursive=1")
        if t and isinstance(t.get("tree"), list):
            return [n["path"] for n in t["tree"] if "path" in n]
    return []


def _plugin_root(paths: list[str], name: str) -> str | None:
    """Return the plugin root within the repo ('' for repo-root, 'plugins/<name>/'
    for a monorepo), or None if no manifest found."""
    if ".claude-plugin/plugin.json" in paths:
        return ""
    sub = f"plugins/{name}/.claude-plugin/plugin.json"
    if sub in paths:
        return f"plugins/{name}/"
    for p in paths:
        if p.endswith(".claude-plugin/plugin.json"):
            return p[: -len(".claude-plugin/plugin.json")]
    return None


def _manifest(repo: str, root: str):
    for ref in REFS:
        m = _get_raw(repo, ref, f"{root}.claude-plugin/plugin.json")
        if m is not None:
            return m
    return {}


def _get_raw(repo: str, ref: str, path: str):
    req = urllib.request.Request(
        f"https://raw.githubusercontent.com/{repo}/{ref}/{path}",
        headers=_headers(),
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def _surfaces(repo: str, name: str) -> str:
    paths = _repo_tree(repo)
    root = _plugin_root(paths, name) if paths else None
    if root is None:
        return ""

    def in_dir(d):
        pre = f"{root}{d}/"
        return [p for p in paths if p.startswith(pre)]

    nskills = len([p for p in in_dir("skills") if p.endswith("/SKILL.md")])
    ncmds = len([p for p in in_dir("commands") if p.endswith(".md")])
    nagents = len([p for p in in_dir("agents") if p.endswith(".md")])
    has_hooks = f"{root}hooks/hooks.json" in paths

    man = _manifest(repo, root) or {}
    has_mcp = bool(man.get("mcpServers")) or f"{root}.mcp.json" in paths
    # output styles
    nstyles = len([p for p in in_dir("output-styles") if p.endswith(".md")])

    def plural(n, word):
        return f"{n} {word}" + ("s" if n != 1 else "")

    parts = []
    if has_mcp:
        parts.append("MCP server")
    if nskills:
        parts.append(plural(nskills, "skill"))
    if ncmds:
        parts.append(plural(ncmds, "command"))
    if nagents:
        parts.append(plural(nagents, "agent"))
    if has_hooks:
        parts.append("hooks")
    if nstyles:
        parts.append(plural(nstyles, "output style"))
    return " · ".join(parts)


def _short(desc: str, limit: int = 170) -> str:
    """One-line description for the catalog: first sentence, else a word-boundary
    truncation. Full text stays in the catalog + each plugin's own repo."""
    d = (desc or "").replace("\n", " ").strip()
    first = d.split(". ", 1)[0].rstrip(" .")
    if first and len(first) <= limit:
        return first if first.endswith((".", "!", "?")) else first + "."
    if len(d) <= limit:
        return d
    return d[:limit].rsplit(" ", 1)[0].rstrip(" .,:;—-") + "…"


# Catalog layout: per-plugin vertical stanzas (mobile-friendly; GitHub never reflows
# wide tables). Marketplace-level features use a narrow ≤3-col table above the fold.
HEADER = """<div align="center">

# 88plug

**Claude Code + Grok Build plugin marketplace — curated plugins, agent skills, and MCP servers. Two commands to install.**

[![sync](https://github.com/88plug/claude-code-plugins/actions/workflows/sync-plugins.yml/badge.svg)](https://github.com/88plug/claude-code-plugins/actions/workflows/sync-plugins.yml)
[![License: FSL-1.1-ALv2](https://img.shields.io/badge/license-FSL--1.1--ALv2-blue?style=flat)](./LICENSE)
[![plugins](https://img.shields.io/badge/plugins-{count}-1f2328?style=flat)](#plugins)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-8A2BE2?style=flat)](https://github.com/88plug/claude-code-plugins)
[![Grok Build](https://img.shields.io/badge/Grok%20Build-marketplace-1f2328?style=flat)](https://github.com/xai-org/grok-build)
[![DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/88plug/claude-code-plugins)

</div>

## Install

### Claude Code

Add the 88plug marketplace once, then install any plugin by name:

```text
/plugin marketplace add 88plug/claude-code-plugins
/plugin install <name>@88plug
```

### Grok Build

Same catalog — Grok reads `.grok-plugin/marketplace.json` (SHA-pinned) automatically when you add this repo as a marketplace source:

```text
grok plugin marketplace add 88plug/claude-code-plugins
grok plugin install <name>@88plug --trust
```

Or in the TUI: `/marketplace` → add source `88plug/claude-code-plugins` → select a plugin → `i`.

No environment variables. No API keys for the catalog path. Uses your existing Claude Code or Grok Build setup.

> [!TIP]
> **Claude:** enable auto-update once (`/plugin` → Marketplaces → **88plug** → Enable auto-update).
> **Grok:** `grok plugin marketplace update` then `grok plugin update` to refresh pins and installed plugins.

### Hardened Grok installs (`require_sha`)

Every 88plug plugin is published with a **full commit SHA** in `.grok-plugin/marketplace.json`.
Grok re-verifies `HEAD == sha` after clone. To refuse unpinned remotes from *any* marketplace:

```toml
# ~/.grok/config.toml
[marketplace]
require_sha = true
```

or `GROK_MARKETPLACE_REQUIRE_SHA=1`. Default is off; 88plug catalogs already pin so this is safe for our entries.

## Why this marketplace

88plug is a curated plugin marketplace for developers who run AI coding agents all day — Claude Code and Grok Build. You get productivity plugins (memory, compaction, guardrails, investigation) and MCP servers (search, desktop control, package versions) without cloning repos or wiring config by hand.

Each entry is a full plugin or MCP server in its own repo. This hub is only the catalog index — install with `/plugin install <name>@88plug` (Claude) or `grok plugin install <name>@88plug --trust` (Grok), then work. Claude versions are `YEAR.MONTH.BUILD` (rolling). Grok installs pin the exact commit SHA from `.grok-plugin/marketplace.json` and re-verify it after clone.

## Features

| Area | What you get |
| --- | --- |
| Claude Code + Grok Build | Same catalog; Grok uses SHA-pinned `.grok-plugin/` entries |
| Plugins | Hooks, skills, slash commands, agents for coding agents |
| MCP servers | One-command MCP for search, DeepWiki, desktop, OS, package versions |
| Marketplace install | Add once, then install `<name>@88plug` |
| Rolling + pinned | Claude: `YEAR.MONTH.BUILD`; Grok: full commit `sha` on every url source |
| Zero config | No env vars or API keys for the catalog path itself |

## Plugins

*Hooks, skills, commands, output styles. Claude versions are `YEAR.MONTH.BUILD`
(what `claude plugin list` shows). Grok installs pin the full commit SHA from
`.grok-plugin/marketplace.json`. Each card has both install commands.*

{plugin_blocks}

## MCP servers

*A single MCP server — Claude or Grok, one command each.*

{mcp_blocks}

<details>
<summary><b>Updating &amp; versioning</b></summary>

### Claude Code

Third-party marketplaces have auto-update **off by default**. Turn it on once
(`/plugin` → Marketplaces → **88plug** → Enable auto-update) and Claude Code refreshes
the catalog and updates installed plugins at startup, then prompts `/reload-plugins`.

Prefer to do it by hand:

```text
/plugin marketplace update 88plug
/plugin update <name>@88plug
/reload-plugins
```

Org-wide, an admin can add `88plug` to `extraKnownMarketplaces` with auto-update enabled
in managed settings.

### Grok Build

Refresh the marketplace (new SHA pins), then update installed plugins:

```text
grok plugin marketplace update
grok plugin update
```

Or reinstall one plugin to the current catalog pin:

```text
grok plugin install <name>@88plug --trust
```

### Versions

Claude: `YEAR.MONTH.BUILD` (auto-stamped; linked hash is the exact commit).
Grok: full commit `sha` in `.grok-plugin/marketplace.json`, re-verified after clone.
If your installed version or pin differs from the catalog, update it.

</details>

## Philosophy

Plugins should be invisible until you need them. Each one earns its slot by closing a
specific failure mode in long-horizon AI-assisted work — compaction loss, stale package
versions, yield-back, classifier false positives, and similar agent failure modes.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full workflow, naming convention, quality
bar, and CLA terms. Short version: build your plugin in its own `88plug/<plugin>` repo with
a valid `.claude-plugin/plugin.json`, PR an entry to this hub's
`.claude-plugin/marketplace.json`, and sign the
[CLA](https://gist.github.com/88plug/de8629bdb714949a9ea9a47323d8468e) on your first PR.
Plugin code never lives in this repo — only the marketplace index.

## License

FSL-1.1-ALv2. See [LICENSE](./LICENSE).

<sub>Generated from <code>.claude-plugin/marketplace.json</code> by <code>scripts/build_readme.py</code>. Don't edit by hand — edit the catalog (or the plugin's manifest) and the sync action regenerates it.</sub>
"""


def _stanza(name, homepage, ver, desc, surfaces, repo=None, sha=None) -> str:
    head = f"### [{name}]({homepage})" if homepage else f"### {name}"
    bits = []
    if ver and sha and repo:
        bits.append(f'[`v{ver}`](https://github.com/{repo}/commit/{sha} "commit {sha[:7]}")')
    elif ver:
        bits.append(f"`v{ver}`")
    elif sha and repo:
        bits.append(f'[`{sha[:7]}`](https://github.com/{repo}/commit/{sha})&nbsp;rolling')
    if surfaces:
        bits.append(surfaces)
    meta = " · ".join(bits)
    return (f"{head}\n"
            f"{meta}\n\n"
            f"{_short(desc)}\n\n"
            f"```text\n"
            f"# Claude Code\n"
            f"/plugin install {name}@88plug\n"
            f"\n"
            f"# Grok Build\n"
            f"grok plugin install {name}@88plug --trust\n"
            f"```")


def main() -> int:
    data = json.loads(MKT.read_text())
    plugins = data.get("plugins", [])
    plugin_blocks, mcp_blocks = [], []
    n_repo = n_surfaced = 0
    for e in plugins:
        name = e["name"]
        repo = _repo_of(e.get("source", {}))
        homepage = e.get("homepage") or (f"https://github.com/{repo}" if repo else "")
        ver = e.get("version")
        desc = (e.get("description") or "").replace("\n", " ").strip()
        tag0 = (e.get("tags") or [""])[0]
        surfaces = _surfaces(repo, name) if repo else ""
        sha = _latest_sha(repo) if repo else None
        if repo:
            n_repo += 1
            n_surfaced += 1 if surfaces else 0
        block = _stanza(name, homepage, ver, desc, surfaces, repo=repo, sha=sha)
        (mcp_blocks if tag0 == "type:mcp" else plugin_blocks).append(block)
        print(f"  {name}: {('v'+ver) if ver else (sha or 'rolling')} [{tag0}] surfaces='{surfaces}'", file=sys.stderr)

    # Abort rather than commit a degraded README: if every repo-backed plugin
    # came back with empty surfaces, the GitHub API was unreachable/rate-limited.
    if n_repo >= 2 and n_surfaced == 0:
        print("ERROR: derived 0 surfaces for all plugins — GitHub API likely "
              "rate-limited/unreachable. Refusing to overwrite README.", file=sys.stderr)
        return 1

    out = HEADER.format(
        count=len(plugins),
        plugin_blocks="\n\n".join(plugin_blocks),
        mcp_blocks="\n\n".join(mcp_blocks),
    )
    old = README.read_text() if README.exists() else ""
    if out != old:
        README.write_text(out)
        print("README regenerated")
    else:
        print("README already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
