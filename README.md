<div align="center">

# 88plug

  <h3>Curated plugins for AI coding assistants. One marketplace. Two commands.</h3>

  [![marketplace](https://img.shields.io/badge/marketplace-88plug-000?style=for-the-badge)](https://github.com/88plug/claude-code-plugins)
  [![license](https://img.shields.io/badge/license-MIT-000?style=for-the-badge)](./LICENSE)
  [![plugins](https://img.shields.io/badge/plugins-9%20shipping-000?style=for-the-badge)](#plugins)
  [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/88plug/claude-code-plugins)

</div>

---

## Install

```sh
# 1. Add the marketplace (once per machine)
/plugin marketplace add 88plug/claude-code-plugins

# 2. Install any plugin from the catalog
/plugin install amnesia@88plug
/plugin install caveman-plus@88plug
/plugin install total-recall@88plug
/plugin install scientific-method@88plug
/plugin install drive-remote-terminal@88plug
/plugin install project-prospector@88plug
/plugin install searxng@88plug
/plugin install deepwiki@88plug
/plugin install screen-mcp@88plug
```

That's the whole install. No environment variables, no API keys — uses your existing AI coding tool setup.

## Plugins

Two structural categories. Both install the same way.

### Plugins — Claude Code UX surfaces (hooks, skills, commands, output styles)

| Plugin | What it does | Surfaces | Install |
| :--- | :--- | :--- | :--- |
| [**amnesia**](https://github.com/88plug/amnesia)&nbsp;`v0.3.0` | Seamless context continuity across compaction — capture and restore the agent's working state on every `/compact` and resume, invisible to you | `5 hooks` · `1 skill` · `4 commands` · `1 agent` · `1 MCP (embedded)` | `/plugin install amnesia@88plug` |
| [**total-recall**](https://github.com/88plug/total-recall)&nbsp;`v2.1.0` | Cross-session, cross-CLI memory. Mines transcripts from 8 CLI clients; surfaces operator identity, standing decisions, bans, goals, and past corrections so the model stops re-asking. Zero host-python prereq — bootstraps its own `uv` + python in `$CLAUDE_PLUGIN_DATA` on first run | `4 hooks` · `2 skills` · `15 commands` · `23 MCP tools` | `/plugin install total-recall@88plug` |
| [**caveman-plus**](https://github.com/88plug/caveman-plus) | Talk like caveman. Cut ~75% tokens. Keep all technical accuracy | `1 output style` | `/plugin install caveman-plus@88plug` |
| [**scientific-method**](https://github.com/88plug/scientific-method)&nbsp;`v1.7.2` | Falsification-first investigation + invention — turn every claim into a labeled hypothesis, predict before measuring, run controlled experiments, REFUTE-first verification, and a persistent ledger so killed ideas stay killed | `1 skill` · `7 commands` · `5 agents` · `1 hook` | `/plugin install scientific-method@88plug` |
| [**drive-remote-terminal**](https://github.com/88plug/drive-remote-terminal)&nbsp;`v1.0.0` | Operate an interactive full-screen TUI on a remote machine over tmux/screen + SSH like a human: type with send-keys, screenshot with capture-pane, in a type-wait-screenshot-read loop | `1 skill` | `/plugin install drive-remote-terminal@88plug` |
| [**project-prospector**](https://github.com/88plug/project-prospector)&nbsp;`v1.0.0` | Discover, catalog, and rank everything you've built or sketched on a machine — a two-pass parallel read-only sweep into a tiered novelty/leverage ranking with idea/live/dormant tags | `1 skill` | `/plugin install project-prospector@88plug` |

### MCP wrappers — single MCP server, one-command install

| Plugin | What it does | Backend | Install |
| :--- | :--- | :--- | :--- |
| [**searxng**](https://github.com/88plug/searxng-mcp)&nbsp;`v0.2.0` | Privacy-respecting metasearch over 70+ engines via a self-hosted SearXNG instance. Token-efficient tool responses, stdio + streamable-http, optional rendered (Playwright) fetch | local (uvx) | `/plugin install searxng@88plug` |
| [**deepwiki**](https://github.com/88plug/deepwiki)&nbsp;`v0.1.0` | Chat with any public GitHub repo's auto-generated documentation — read-only research into codebases without cloning | remote (Cognition AI) | `/plugin install deepwiki@88plug` |
| [**screen-mcp**](https://github.com/88plug/screen-mcp)&nbsp;`v1.3.2` | Eyes and hands on a Linux Wayland desktop: screenshot any monitor and click/type/scroll/drag/read any visible app over xdg-desktop-portal, with optional OCR + icon grounding. Ships the MCP server + a drive-screen skill. CPU-only | local (Wayland/GNOME) | `/plugin install screen-mcp@88plug` |

## Philosophy

Plugins should be invisible until you need them. Each one in this marketplace earns its slot by closing a specific failure mode in long-horizon AI-assisted work:

- **amnesia** — the model forgets what it was doing across compaction
- **caveman-plus** — the model spends 4× more tokens than the answer needs
- **total-recall** — the model keeps relearning who the operator is and what they've already decided
- **scientific-method** — the model asserts ceilings, root causes, and "novel" inventions without ever proving them
- **drive-remote-terminal** — the model can't operate an interactive TUI (Claude Code, vim, installers, REPLs) over SSH
- **project-prospector** — you lose track of everything you've half-built, and which ideas are worth resuming
- **searxng** — the model can't do real web research without leaking queries to surveillance-capitalism search engines
- **deepwiki** — the model can't navigate an unfamiliar GitHub repo without cloning, grepping, and burning context
- **screen-mcp** — the model can't see or act on what's actually on your screen

All are local-first except **deepwiki**, a thin wrapper around a hosted third-party service (Cognition AI) — included for the productivity win, with the dependency disclosed up-front.

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
