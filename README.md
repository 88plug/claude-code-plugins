<div align="center">

# 88plug

**Claude Code plugin marketplace for AI coding agents — curated plugins, agent skills, and MCP servers. Two commands to install.**

[![sync](https://github.com/88plug/claude-code-plugins/actions/workflows/sync-plugins.yml/badge.svg)](https://github.com/88plug/claude-code-plugins/actions/workflows/sync-plugins.yml)
[![License: FSL-1.1-ALv2](https://img.shields.io/badge/license-FSL--1.1--ALv2-blue?style=flat)](./LICENSE)
[![plugins](https://img.shields.io/badge/plugins-18-1f2328?style=flat)](#plugins)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-8A2BE2?style=flat)](https://github.com/88plug/claude-code-plugins)
[![DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/88plug/claude-code-plugins)

</div>

## Install

Inside Claude Code, add the 88plug marketplace once, then install any plugin by name:

```text
/plugin marketplace add 88plug/claude-code-plugins
/plugin install <name>@88plug
```

No environment variables. No API keys. Uses your existing Claude Code setup.

> [!TIP]
> Enable auto-update once (`/plugin` → Marketplaces → **88plug** → Enable auto-update) and you always get the latest at startup.

## Why this marketplace

88plug is a curated Claude Code plugin marketplace for developers who run AI coding agents all day. You get productivity plugins (memory, compaction, guardrails, investigation) and MCP servers (search, desktop control, package versions) without cloning repos or wiring config by hand.

Each entry is a Claude Code plugin or MCP server in its own repo. This hub is only the catalog index — install with `/plugin install <name>@88plug`, then work. Versions are `YEAR.MONTH.BUILD`, auto-stamped so `claude plugin list` shows whether you are current.

## Features

| Area | What you get |
| --- | --- |
| Claude Code plugins | Hooks, skills, slash commands, and output styles for coding agents |
| MCP servers | One-command MCP install for search, DeepWiki, desktop, OS, package versions |
| Marketplace install | `/plugin marketplace add` once, then `/plugin install <name>@88plug` |
| Rolling versions | `YEAR.MONTH.BUILD` auto-stamped so `claude plugin list` stays current |
| Auto-update | Optional marketplace auto-update at Claude Code startup |
| Zero config | No env vars or API keys for the catalog path itself |

## Plugins

*Claude Code UX surfaces — hooks, skills, commands, output styles. Each version is
`YEAR.MONTH.BUILD`, auto-stamped and linked to the exact commit; it's what
`claude plugin list` shows, so you can tell at a glance if you're current.*

### [recover-from-false-positive](https://github.com/88plug/recover-from-false-positive)
`v2026.7.31`

Recover Claude Code sessions after an Anthropic API output-classifier false positive (the "cyber-related safeguards" / "appears to violate our Usage Policy" hard failure).

```sh
/plugin install recover-from-false-positive@88plug
```

### [amnesia](https://github.com/88plug/amnesia)
`v2026.7.50`

Seamless context continuity across Claude Code compaction.

```sh
/plugin install amnesia@88plug
```

### [caveman-plus](https://github.com/88plug/caveman-plus)
`v2026.7.214`

Ultra-compressed communication mode.

```sh
/plugin install caveman-plus@88plug
```

### [total-recall](https://github.com/88plug/total-recall)
`v2026.7.146`

Cross-session, cross-CLI memory for AI coding assistants.

```sh
/plugin install total-recall@88plug
```

### [scientific-method](https://github.com/88plug/scientific-method)
`v2026.7.28`

Falsification-first investigation workflow: convert every assertion into a labeled falsifiable hypothesis, predict before measuring, run controlled experiments, verify…

```sh
/plugin install scientific-method@88plug
```

### [drive-remote-terminal](https://github.com/88plug/drive-remote-terminal)
`v2026.7.23`

Operate and observe an interactive full-screen TUI on a REMOTE machine over tmux/screen + SSH by driving it like a human: type with send-keys, screenshot with…

```sh
/plugin install drive-remote-terminal@88plug
```

### [project-prospector](https://github.com/88plug/project-prospector)
`v2026.7.22`

Discover, catalog, and rank everything you've built or sketched on a machine via a two-pass parallel read-only sweep: a clustered project catalog plus blind-spot agents…

```sh
/plugin install project-prospector@88plug
```

### [deepwiki-index](https://github.com/88plug/deepwiki-index)
`v2026.7.14`

Index a public GitHub repo's DeepWiki (the page the 'Ask DeepWiki' badge links to) hands-free, and do it autonomously after publishing or updating a repo — no human…

```sh
/plugin install deepwiki-index@88plug
```

### [addlightness](https://github.com/88plug/addlightness)
`v2026.7.12`

Simplify, then add lightness.

```sh
/plugin install addlightness@88plug
```

### [drift-detector](https://github.com/88plug/drift-detector)
`v2026.7.38`

Detects when Claude drifts away from your active output contract (a terse persona, hard formatting/length rules, an in-character voice) and quietly steers it back.

```sh
/plugin install drift-detector@88plug
```

### [trigger-my-training](https://github.com/88plug/trigger-my-training)
`v2026.7.19`

A ground-first reflex: the agent judges (from its own training, any domain) when a request is complex/irreversible, grounds before acting, and is hard-blocked from the…

```sh
/plugin install trigger-my-training@88plug
```

### [be-the-whole-bitch](https://github.com/88plug/be-the-whole-bitch)
`v2026.7.25`

Enforce full agent authority on reversible work: run commands yourself, never yield instructions back to the operator.

```sh
/plugin install be-the-whole-bitch@88plug
```

### [dehumanize](https://github.com/88plug/dehumanize)
`v2026.7.22`

Makes AI work like AI — no human time estimates, no asking for accessible data, no emotional labor.

```sh
/plugin install dehumanize@88plug
```

## MCP servers

*A single MCP server, one-command install.*

### [searxng](https://github.com/88plug/searxng-mcp)
`v2026.7.42`

Fast, token-efficient MCP for SearXNG metasearch.

```sh
/plugin install searxng@88plug
```

### [deepwiki](https://github.com/88plug/deepwiki)
`v2026.7.24`

Talk to any public GitHub repo's auto-generated documentation via Cognition's hosted DeepWiki MCP.

```sh
/plugin install deepwiki@88plug
```

### [screen-mcp](https://github.com/88plug/screen-mcp)
`v2026.7.40`

Eyes and hands on a Linux Wayland desktop: screenshot any monitor and click, type, scroll, drag, and read any visible app over xdg-desktop-portal (RemoteDesktop +…

```sh
/plugin install screen-mcp@88plug
```

### [os-control-mcp](https://github.com/88plug/os-control-mcp)
`v2026.7.19`

The sanctioned OS 'motor cortex' for an agent on a Linux box: control systemd services/timers, query journald, read host resources/processes, send desktop notifications…

```sh
/plugin install os-control-mcp@88plug
```

### [use-latest-version](https://github.com/88plug/use-latest-version-mcp)
`v2026.7.36`

Stop suggesting stale package versions from training data.

```sh
/plugin install use-latest-version@88plug
```

<details>
<summary><b>Updating &amp; versioning</b></summary>

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
in managed settings. Versions are `YEAR.MONTH.BUILD` (auto-stamped, increasing every
release); the linked hash is the exact commit. If your installed version differs from the
one here, you're behind — update it.

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
