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
/plugin install searxng@88plug
/plugin install deepwiki@88plug
/plugin install scientific-method@88plug
/plugin install drive-remote-terminal@88plug
/plugin install project-prospector@88plug
/plugin install screen-mcp@88plug
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
| [**amnesia**](https://github.com/88plug/amnesia)&nbsp;`rolling` | Seamless context continuity across Claude Code compaction. Four background layers (continuous tool-call capture, mechanical PostCompact handoff, async Opus 4.7 enrichment at --effort max, async Stop-hook refinement, and preemptive snapshot before the next compact) keep the agent's working state intact across every compaction and resume. All summarization is isolated from CLAUDE.md/auto-memory and invisible to the user. | `MCP server · 1 skill · 8 commands · 1 agent · hooks` | `/plugin install amnesia@88plug` |
| [**caveman-plus**](https://github.com/88plug/caveman-plus)&nbsp;`rolling` | Ultra-compressed communication mode. Cuts ~75% of tokens while keeping full technical accuracy by speaking like a caveman. | `7 skills · 3 agents` | `/plugin install caveman-plus@88plug` |
| [**total-recall**](https://github.com/88plug/total-recall)&nbsp;`v2.1.2` | Cross-session, cross-CLI memory for AI coding assistants. Mines transcripts from 8 supported CLI clients. Surfaces operator identity / decisions / bans / corrections / goals / voice via 26 MCP tools, 6 hooks (SessionStart signpost + SessionStart compact-restore + UserPromptSubmit retrieval + Stop/PostCompact re-index + PreCompact continuity-seed), 15 slash commands, and 3 skills. gte-modernbert hybrid recall; worktree-aware project scoping; post-compaction coding-continuity packet. Optional local-LLM refinement ([llm] extra, ollama, off by default). The operator becomes the source of truth; the model stops re-asking what they already told it. | `MCP server · 3 skills · 15 commands · hooks` | `/plugin install total-recall@88plug` |
| [**scientific-method**](https://github.com/88plug/scientific-method)&nbsp;`rolling` | Falsification-first investigation workflow: convert every assertion into a labeled falsifiable hypothesis, predict before measuring, run controlled experiments, verify findings adversarially (REFUTE-first), and persist verdicts in a hypothesis ledger so killed ideas are never re-attacked | `1 skill · 7 commands · 5 agents · hooks` | `/plugin install scientific-method@88plug` |
| [**drive-remote-terminal**](https://github.com/88plug/drive-remote-terminal)&nbsp;`rolling` | Operate and observe an interactive full-screen TUI on a REMOTE machine over tmux/screen + SSH by driving it like a human: type with send-keys, screenshot with capture-pane, in a type-wait-screenshot-read loop. For the Claude Code TUI, vim, top, curses installers, REPLs, or any program that needs a real PTY over SSH. | `1 skill` | `/plugin install drive-remote-terminal@88plug` |
| [**project-prospector**](https://github.com/88plug/project-prospector)&nbsp;`rolling` | Discover, catalog, and rank everything you've built or sketched on a machine via a two-pass parallel read-only sweep: a clustered project catalog plus blind-spot agents (transcripts, other agent CLIs, running services, research artifacts, beyond-home), synthesized into a tiered novelty/leverage ranking with idea/live/dormant tags and evidence-anchored rationale. | `1 skill` | `/plugin install project-prospector@88plug` |

### MCP wrappers — single MCP server, one-command install

| Plugin | What it does | Surfaces | Install |
| :--- | :--- | :--- | :--- |
| [**searxng**](https://github.com/88plug/searxng-mcp)&nbsp;`rolling` | Fast, token-efficient MCP for SearXNG metasearch. Privacy-respecting search across 70+ engines with stdio + streamable-http transports, Docker, and optional rendered (Playwright) fetch for JS-heavy pages. Self-hostable. The underlying server is also usable independently of Claude Code via `uvx --from git+https://github.com/88plug/searxng-mcp searxng-mcp`. | `MCP server` | `/plugin install searxng@88plug` |
| [**deepwiki**](https://github.com/88plug/deepwiki)&nbsp;`v0.1.2` | Talk to any public GitHub repo's auto-generated documentation via Cognition's hosted DeepWiki MCP. Read-only research into codebases without cloning. Note: this plugin wraps a remote MCP server hosted by Cognition AI at mcp.deepwiki.com; 88plug does not operate the underlying service. | `MCP server` | `/plugin install deepwiki@88plug` |
| [**screen-mcp**](https://github.com/88plug/screen-mcp)&nbsp;`rolling` | Eyes and hands on a Linux Wayland desktop: screenshot any monitor and click, type, scroll, drag, and read any visible app over xdg-desktop-portal (RemoteDesktop + ScreenCast), with optional OCR + OmniParser icon grounding. Pure-Python, CPU-only. GNOME/Wayland only. Ships the MCP server plus a drive-screen skill that encodes the locate-ground-act-confirm loop. | `MCP server · 1 skill` | `/plugin install screen-mcp@88plug` |

## Philosophy

Plugins should be invisible until you need them. Each one in this marketplace earns its slot by closing a specific failure mode in long-horizon AI-assisted work:

- **amnesia** — Seamless context continuity across Claude Code compaction
- **caveman-plus** — Ultra-compressed communication mode
- **total-recall** — Cross-session, cross-CLI memory for AI coding assistants
- **searxng** — Fast, token-efficient MCP for SearXNG metasearch
- **deepwiki** — Talk to any public GitHub repo's auto-generated documentation via Cognition's hosted DeepWiki MCP
- **scientific-method** — Falsification-first investigation workflow
- **drive-remote-terminal** — Operate and observe an interactive full-screen TUI on a REMOTE machine over tmux/screen + SSH by driving it like a human
- **project-prospector** — Discover, catalog, and rank everything you've built or sketched on a machine via a two-pass parallel read-only sweep
- **screen-mcp** — Eyes and hands on a Linux Wayland desktop

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
