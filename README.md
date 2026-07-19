<div align="center">

# 88plug

**Claude Code + Grok Build plugin marketplace — curated plugins, agent skills, and MCP servers. Two commands to install.**

[![sync](https://github.com/88plug/claude-code-plugins/actions/workflows/sync-plugins.yml/badge.svg)](https://github.com/88plug/claude-code-plugins/actions/workflows/sync-plugins.yml)
[![License: FSL-1.1-ALv2](https://img.shields.io/badge/license-FSL--1.1--ALv2-blue?style=flat)](./LICENSE)
[![plugins](https://img.shields.io/badge/plugins-18-1f2328?style=flat)](#plugins)
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

### [recover-from-false-positive](https://github.com/88plug/recover-from-false-positive)
[`v2026.7.34`](https://github.com/88plug/recover-from-false-positive/commit/c65574744b9d "commit c655747") · 1 skill · hooks

Recover Claude Code sessions after an Anthropic API output-classifier false positive (the "cyber-related safeguards" / "appears to violate our Usage Policy" hard failure).

```text
# Claude Code
/plugin install recover-from-false-positive@88plug

# Grok Build
grok plugin install recover-from-false-positive@88plug --trust
```

### [amnesia](https://github.com/88plug/amnesia)
[`v2026.7.54`](https://github.com/88plug/amnesia/commit/b5674a5cfa4a "commit b5674a5") · MCP server · 1 skill · 8 commands · 1 agent · hooks

Seamless context continuity across Claude Code compaction.

```text
# Claude Code
/plugin install amnesia@88plug

# Grok Build
grok plugin install amnesia@88plug --trust
```

### [caveman-plus](https://github.com/88plug/caveman-plus)
[`v2026.7.217`](https://github.com/88plug/caveman-plus/commit/c3f10e4f3aa2 "commit c3f10e4") · 7 skills · 3 agents

Ultra-compressed communication mode.

```text
# Claude Code
/plugin install caveman-plus@88plug

# Grok Build
grok plugin install caveman-plus@88plug --trust
```

### [total-recall](https://github.com/88plug/total-recall)
[`v2026.7.155`](https://github.com/88plug/total-recall/commit/4001c4766bb1 "commit 4001c47") · MCP server · 3 skills · 15 commands · hooks

Cross-session, cross-CLI memory for AI coding assistants.

```text
# Claude Code
/plugin install total-recall@88plug

# Grok Build
grok plugin install total-recall@88plug --trust
```

### [scientific-method](https://github.com/88plug/scientific-method)
[`v2026.7.31`](https://github.com/88plug/scientific-method/commit/4b0920508d9c "commit 4b09205") · 1 skill · 7 commands · 5 agents · hooks

Falsification-first investigation workflow: convert every assertion into a labeled falsifiable hypothesis, predict before measuring, run controlled experiments, verify…

```text
# Claude Code
/plugin install scientific-method@88plug

# Grok Build
grok plugin install scientific-method@88plug --trust
```

### [drive-remote-terminal](https://github.com/88plug/drive-remote-terminal)
[`v2026.7.26`](https://github.com/88plug/drive-remote-terminal/commit/2e51b54adbb6 "commit 2e51b54") · 1 skill

Operate and observe an interactive full-screen TUI on a REMOTE machine over tmux/screen + SSH by driving it like a human: type with send-keys, screenshot with…

```text
# Claude Code
/plugin install drive-remote-terminal@88plug

# Grok Build
grok plugin install drive-remote-terminal@88plug --trust
```

### [project-prospector](https://github.com/88plug/project-prospector)
[`v2026.7.25`](https://github.com/88plug/project-prospector/commit/68facd487238 "commit 68facd4") · 1 skill

Discover, catalog, and rank everything you've built or sketched on a machine via a two-pass parallel read-only sweep: a clustered project catalog plus blind-spot agents…

```text
# Claude Code
/plugin install project-prospector@88plug

# Grok Build
grok plugin install project-prospector@88plug --trust
```

### [deepwiki-index](https://github.com/88plug/deepwiki-index)
[`v2026.7.17`](https://github.com/88plug/deepwiki-index/commit/fcd0bc1b6289 "commit fcd0bc1") · 1 skill

Index a public GitHub repo's DeepWiki (the page the 'Ask DeepWiki' badge links to) hands-free, and do it autonomously after publishing or updating a repo — no human…

```text
# Claude Code
/plugin install deepwiki-index@88plug

# Grok Build
grok plugin install deepwiki-index@88plug --trust
```

### [addlightness](https://github.com/88plug/addlightness)
[`v2026.7.15`](https://github.com/88plug/addlightness/commit/6828e78fd17e "commit 6828e78") · 3 skills · 2 agents

Simplify, then add lightness.

```text
# Claude Code
/plugin install addlightness@88plug

# Grok Build
grok plugin install addlightness@88plug --trust
```

### [drift-detector](https://github.com/88plug/drift-detector)
[`v2026.7.42`](https://github.com/88plug/drift-detector/commit/4f9fb2449f65 "commit 4f9fb24") · MCP server · 1 skill · 6 commands

Detects when Claude drifts away from your active output contract (a terse persona, hard formatting/length rules, an in-character voice) and quietly steers it back.

```text
# Claude Code
/plugin install drift-detector@88plug

# Grok Build
grok plugin install drift-detector@88plug --trust
```

### [trigger-my-training](https://github.com/88plug/trigger-my-training)
[`v2026.7.24`](https://github.com/88plug/trigger-my-training/commit/1195236f9742 "commit 1195236") · 1 skill · 6 commands · 1 agent · hooks

A ground-first reflex: the agent judges (from its own training, any domain) when a request is complex/irreversible, grounds before acting, and is hard-blocked from the…

```text
# Claude Code
/plugin install trigger-my-training@88plug

# Grok Build
grok plugin install trigger-my-training@88plug --trust
```

### [be-the-whole-bitch](https://github.com/88plug/be-the-whole-bitch)
[`v2026.7.29`](https://github.com/88plug/be-the-whole-bitch/commit/9b88c44969ab "commit 9b88c44") · 1 skill · 3 commands · hooks

Enforce full agent authority on reversible work: run commands yourself, never yield instructions back to the operator.

```text
# Claude Code
/plugin install be-the-whole-bitch@88plug

# Grok Build
grok plugin install be-the-whole-bitch@88plug --trust
```

### [dehumanize](https://github.com/88plug/dehumanize)
[`v2026.7.26`](https://github.com/88plug/dehumanize/commit/52e46f0b6aa7 "commit 52e46f0") · 1 skill · 4 commands · hooks

Makes AI work like AI — no human time estimates, no asking for accessible data, no emotional labor.

```text
# Claude Code
/plugin install dehumanize@88plug

# Grok Build
grok plugin install dehumanize@88plug --trust
```

## MCP servers

*A single MCP server — Claude or Grok, one command each.*

### [searxng](https://github.com/88plug/searxng-mcp)
[`v2026.7.45`](https://github.com/88plug/searxng-mcp/commit/5c4597e55283 "commit 5c4597e") · MCP server

Fast, token-efficient MCP for SearXNG metasearch.

```text
# Claude Code
/plugin install searxng@88plug

# Grok Build
grok plugin install searxng@88plug --trust
```

### [deepwiki](https://github.com/88plug/deepwiki)
[`v2026.7.27`](https://github.com/88plug/deepwiki/commit/09e017b7e73a "commit 09e017b") · MCP server

Talk to any public GitHub repo's auto-generated documentation via Cognition's hosted DeepWiki MCP.

```text
# Claude Code
/plugin install deepwiki@88plug

# Grok Build
grok plugin install deepwiki@88plug --trust
```

### [screen-mcp](https://github.com/88plug/screen-mcp)
[`v2026.7.43`](https://github.com/88plug/screen-mcp/commit/df7853a2882c "commit df7853a") · MCP server · 1 skill

Eyes and hands on a Linux Wayland desktop: screenshot any monitor and click, type, scroll, drag, and read any visible app over xdg-desktop-portal (RemoteDesktop +…

```text
# Claude Code
/plugin install screen-mcp@88plug

# Grok Build
grok plugin install screen-mcp@88plug --trust
```

### [os-control-mcp](https://github.com/88plug/os-control-mcp)
[`v2026.7.22`](https://github.com/88plug/os-control-mcp/commit/9d298c6642a3 "commit 9d298c6") · MCP server · 1 skill

The sanctioned OS 'motor cortex' for an agent on a Linux box: control systemd services/timers, query journald, read host resources/processes, send desktop notifications…

```text
# Claude Code
/plugin install os-control-mcp@88plug

# Grok Build
grok plugin install os-control-mcp@88plug --trust
```

### [use-latest-version](https://github.com/88plug/use-latest-version-mcp)
[`v2026.7.40`](https://github.com/88plug/use-latest-version-mcp/commit/58b93cb6d683 "commit 58b93cb") · MCP server

Stop suggesting stale package versions from training data.

```text
# Claude Code
/plugin install use-latest-version@88plug

# Grok Build
grok plugin install use-latest-version@88plug --trust
```

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
