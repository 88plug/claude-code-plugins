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
    if src.get("source") == "git-subdir" and src.get("url"):
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


# Mobile-first layout (researched 2026): no wide tables — GitHub never reflows
# them, so they force horizontal scroll and clip columns on a phone. Each plugin
# is a vertical stanza (heading + metadata line + short description + fenced
# install block with a copy button). Catalog leads; the update essay collapses.
HEADER = """<div align="center">

# 88plug

**Curated plugins for AI coding assistants. One marketplace. Two commands.**

[![marketplace](https://img.shields.io/badge/marketplace-88plug-1f2328?style=flat-square)](https://github.com/88plug/claude-code-plugins)
[![license](https://img.shields.io/badge/license-FSL--1.1--ALv2-1f2328?style=flat-square)](./LICENSE)
[![plugins](https://img.shields.io/badge/plugins-{count}-1f2328?style=flat-square)](#plugins)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/88plug/claude-code-plugins)

</div>

---

## Install

```sh
# 1. Add the marketplace (once per machine)
/plugin marketplace add 88plug/claude-code-plugins

# 2. Install any plugin below
/plugin install <name>@88plug
```

No environment variables, no API keys — it uses your existing setup.

> [!TIP]
> Enable auto-update once (`/plugin` → Marketplaces → **88plug** → Enable auto-update) and you always get the latest at startup.

## Plugins

*Claude Code UX surfaces — hooks, skills, commands, output styles. Each version is
`YEAR.MONTH.BUILD`, auto-stamped and linked to the exact commit; it's what
`claude plugin list` shows, so you can tell at a glance if you're current.*

{plugin_blocks}

## MCP servers

*A single MCP server, one-command install.*

{mcp_blocks}

<details>
<summary><b>Updating &amp; versioning</b></summary>

Third-party marketplaces have auto-update **off by default**. Turn it on once
(`/plugin` → Marketplaces → **88plug** → Enable auto-update) and Claude Code refreshes
the catalog and updates installed plugins at startup, then prompts `/reload-plugins`.

Prefer to do it by hand:

```sh
/plugin marketplace update 88plug
/plugin update <name>@88plug
/reload-plugins
```

Org-wide, an admin can add `88plug` to `extraKnownMarketplaces` with auto-update enabled
in managed settings. Versions are `YEAR.MONTH.BUILD` (auto-stamped, increasing every
release); the linked hash is the exact commit. If your installed version differs from the
one here, you're behind — update it.

</details>

## Philosophy

Plugins should be invisible until you need them. Each one earns its slot by closing a
specific failure mode in long-horizon AI-assisted work.

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
            f"```sh\n/plugin install {name}@88plug\n```")


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
