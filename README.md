<div align="center">

# 88plug

**Curated plugins for AI coding assistants. One marketplace. Two commands.**

[![marketplace](https://img.shields.io/badge/marketplace-88plug-1f2328?style=flat-square)](https://github.com/88plug/claude-code-plugins)
[![license](https://img.shields.io/badge/license-MIT-1f2328?style=flat-square)](./LICENSE)
[![plugins](https://img.shields.io/badge/plugins-10-1f2328?style=flat-square)](#plugins)

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

### [amnesia](https://github.com/88plug/amnesia)
[`v2026.6.28`](https://github.com/88plug/amnesia/commit/0603a0f7114a "commit 0603a0f") · MCP server · 1 skill · 8 commands · 1 agent · hooks

Seamless context continuity across Claude Code compaction.

```sh
/plugin install amnesia@88plug
```

### [caveman-plus](https://github.com/88plug/caveman-plus)
[`v2026.6.194`](https://github.com/88plug/caveman-plus/commit/a9b3f76ce560 "commit a9b3f76") · 7 skills · 3 agents

Ultra-compressed communication mode.

```sh
/plugin install caveman-plus@88plug
```

### [total-recall](https://github.com/88plug/total-recall)
[`v2026.6.85`](https://github.com/88plug/total-recall/commit/2623b3ed7d6b "commit 2623b3e") · MCP server · 3 skills · 15 commands · hooks

Cross-session, cross-CLI memory for AI coding assistants.

```sh
/plugin install total-recall@88plug
```

### [scientific-method](https://github.com/88plug/scientific-method)
[`v2026.6.11`](https://github.com/88plug/scientific-method/commit/f6de673112df "commit f6de673") · 1 skill · 7 commands · 5 agents · hooks

Falsification-first investigation workflow: convert every assertion into a labeled falsifiable hypothesis, predict before measuring, run controlled experiments, verify…

```sh
/plugin install scientific-method@88plug
```

### [drive-remote-terminal](https://github.com/88plug/drive-remote-terminal)
[`v2026.6.6`](https://github.com/88plug/drive-remote-terminal/commit/ce825bbd0d79 "commit ce825bb") · 1 skill

Operate and observe an interactive full-screen TUI on a REMOTE machine over tmux/screen + SSH by driving it like a human: type with send-keys, screenshot with…

```sh
/plugin install drive-remote-terminal@88plug
```

### [project-prospector](https://github.com/88plug/project-prospector)
[`v2026.6.6`](https://github.com/88plug/project-prospector/commit/8459b0888fb6 "commit 8459b08") · 1 skill

Discover, catalog, and rank everything you've built or sketched on a machine via a two-pass parallel read-only sweep: a clustered project catalog plus blind-spot agents…

```sh
/plugin install project-prospector@88plug
```

### [recover-from-false-positive](https://github.com/88plug/recover-from-false-positive)
[`v2026.6.2`](https://github.com/88plug/recover-from-false-positive/commit/99f6d7437df5 "commit 99f6d74") · 1 skill · hooks

Recover Claude Code sessions after an Anthropic API output-classifier false positive (the "cyber-related safeguards" / "appears to violate our Usage Policy" hard failure).

```sh
/plugin install recover-from-false-positive@88plug
```

## MCP servers

*A single MCP server, one-command install.*

### [searxng](https://github.com/88plug/searxng-mcp)
[`v2026.6.17`](https://github.com/88plug/searxng-mcp/commit/7a21c172615e "commit 7a21c17") · MCP server

Fast, token-efficient MCP for SearXNG metasearch.

```sh
/plugin install searxng@88plug
```

### [deepwiki](https://github.com/88plug/deepwiki)
[`v2026.6.9`](https://github.com/88plug/deepwiki/commit/6e132fa9544e "commit 6e132fa") · MCP server

Talk to any public GitHub repo's auto-generated documentation via Cognition's hosted DeepWiki MCP.

```sh
/plugin install deepwiki@88plug
```

### [screen-mcp](https://github.com/88plug/screen-mcp)
[`v2026.6.7`](https://github.com/88plug/screen-mcp/commit/4a444cb86207 "commit 4a444cb") · MCP server · 1 skill

Eyes and hands on a Linux Wayland desktop: screenshot any monitor and click, type, scroll, drag, and read any visible app over xdg-desktop-portal (RemoteDesktop +…

```sh
/plugin install screen-mcp@88plug
```

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

MIT. See [LICENSE](./LICENSE).

<sub>Generated from <code>.claude-plugin/marketplace.json</code> by <code>scripts/build_readme.py</code>. Don't edit by hand — edit the catalog (or the plugin's manifest) and the sync action regenerates it.</sub>
