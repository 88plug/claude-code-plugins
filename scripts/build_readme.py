#!/usr/bin/env python3
"""Generate README.md entirely from .claude-plugin/marketplace.json.

No plugin data is hand-maintained in the README. The badge count, install list,
the two category tables (versions + descriptions + derived component "surfaces"),
and the philosophy list are all rendered from the marketplace catalog — which is
itself auto-synced from each plugin's source manifest by sync_marketplace.py.

Component "surfaces" (e.g. "1 skill · 7 commands · 5 agents · 1 hook · MCP") are
counted live from each plugin's source repo tree via the GitHub API, so adding or
restructuring a plugin updates the README with zero hand edits.

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


def _first_clause(desc: str) -> str:
    d = (desc or "").strip()
    for sep in (" — ", ". ", ": ", "; "):
        i = d.find(sep)
        if 0 < i < 140:
            return d[:i].rstrip(" .,:;—-")
    return d[:120].rstrip(" .,:;—-")


HEADER = """<div align="center">

# 88plug

  <h3>Curated plugins for AI coding assistants. One marketplace. Two commands.</h3>

  [![marketplace](https://img.shields.io/badge/marketplace-88plug-000?style=for-the-badge)](https://github.com/88plug/claude-code-plugins)
  [![license](https://img.shields.io/badge/license-MIT-000?style=for-the-badge)](./LICENSE)
  [![plugins](https://img.shields.io/badge/plugins-{count}%20shipping-000?style=for-the-badge)](#plugins)
  [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/88plug/claude-code-plugins)

</div>

---

## Install

```sh
# 1. Add the marketplace (once per machine)
/plugin marketplace add 88plug/claude-code-plugins

# 2. Install any plugin from the catalog
{install_lines}
```

That's the whole install. No environment variables, no API keys — uses your existing AI coding tool setup.

## Staying up to date

Third-party marketplaces have auto-update **off by default**, so turn it on once to
receive new plugin versions automatically at startup:

```sh
/plugin            # → Marketplaces → select 88plug → Enable auto-update
```

With it on, Claude Code refreshes this catalog and updates installed plugins at
startup, then prompts you to `/reload-plugins`. Prefer to do it by hand? Refresh the
catalog first, then update:

```sh
/plugin marketplace update 88plug
/plugin update <name>@88plug
/reload-plugins
```

(Org-wide: an admin can add `88plug` to `extraKnownMarketplaces` with `"autoUpdate": true`
in managed settings.) Plugins tagged **`rolling`** ship on every commit; **versioned**
plugins update when their version is bumped. Either way, with auto-update on you always
get the latest.

## Plugins

Two structural categories. Both install the same way.

### Plugins — Claude Code UX surfaces (hooks, skills, commands, output styles)

| Plugin | What it does | Surfaces | Install |
| :--- | :--- | :--- | :--- |
{plugin_rows}

### MCP wrappers — single MCP server, one-command install

| Plugin | What it does | Surfaces | Install |
| :--- | :--- | :--- | :--- |
{mcp_rows}

## Philosophy

Plugins should be invisible until you need them. Each one in this marketplace earns its slot by closing a specific failure mode in long-horizon AI-assisted work:

{philosophy}

## License

MIT. See [LICENSE](./LICENSE).

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full workflow, naming
convention, quality bar, and CLA terms. Short version:

1. Build your plugin in its own `88plug/<plugin>` repo with a valid
   `.claude-plugin/plugin.json`.
2. PR an entry to this hub's `.claude-plugin/marketplace.json` (github
   source).
3. Sign the [CLA](https://gist.github.com/88plug/de8629bdb714949a9ea9a47323d8468e)
   on your first PR (CLA Assistant gates merge).

Plugin code itself never lives in this repo — only the marketplace index.

<sub>This README is generated from <code>.claude-plugin/marketplace.json</code> by <code>scripts/build_readme.py</code>. Do not edit by hand — edit the catalog (or the plugin's own manifest) and the sync action regenerates it.</sub>
"""


def _row(p: str, name: str, ver, desc, surfaces) -> str:
    vtag = f"&nbsp;`v{ver}`" if ver else "&nbsp;`rolling`"
    s = surfaces or "—"
    return (f"| [**{name}**]({p})" + vtag + f" | {desc} | `{s}` | "
            f"`/plugin install {name}@88plug` |")


def main() -> int:
    data = json.loads(MKT.read_text())
    plugins = data.get("plugins", [])
    plugin_rows, mcp_rows, philo, installs = [], [], [], []
    n_repo = n_surfaced = 0
    for e in plugins:
        name = e["name"]
        repo = _repo_of(e.get("source", {}))
        homepage = e.get("homepage") or (f"https://github.com/{repo}" if repo else "")
        ver = e.get("version")
        desc = (e.get("description") or "").replace("\n", " ").strip()
        tag0 = (e.get("tags") or [""])[0]
        surfaces = _surfaces(repo, name) if repo else ""
        if repo:
            n_repo += 1
            n_surfaced += 1 if surfaces else 0
        row = _row(homepage, name, ver, desc, surfaces)
        (mcp_rows if tag0 == "type:mcp" else plugin_rows).append(row)
        installs.append(f"/plugin install {name}@88plug")
        philo.append(f"- **{name}** — {_first_clause(desc)}")
        print(f"  {name}: v{ver or '—'} [{tag0}] surfaces='{surfaces}'", file=sys.stderr)

    # Abort rather than commit a degraded README: if every repo-backed plugin
    # came back with empty surfaces, the GitHub API was unreachable/rate-limited.
    if n_repo >= 2 and n_surfaced == 0:
        print("ERROR: derived 0 surfaces for all plugins — GitHub API likely "
              "rate-limited/unreachable. Refusing to overwrite README.", file=sys.stderr)
        return 1

    out = HEADER.format(
        count=len(plugins),
        install_lines="\n".join(installs),
        plugin_rows="\n".join(plugin_rows),
        mcp_rows="\n".join(mcp_rows),
        philosophy="\n".join(philo),
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
