<div align="center">

# 88plug

  <h3>Curated plugins for AI coding assistants. One marketplace. Two commands.</h3>

  [![marketplace](https://img.shields.io/badge/marketplace-88plug-000?style=for-the-badge)](https://github.com/88plug/claude-code-plugins)
  [![license](https://img.shields.io/badge/license-MIT-000?style=for-the-badge)](./LICENSE)
  [![plugins](https://img.shields.io/badge/plugins-4%20shipping-000?style=for-the-badge)](#plugins)

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
```

That's the whole install. No environment variables, no API keys — uses your existing AI coding tool setup.

## Plugins

| Plugin | What it does | Surfaces | Install |
| :--- | :--- | :--- | :--- |
| [**amnesia**](https://github.com/88plug/amnesia)&nbsp;`v0.2.3` | Seamless context continuity across compaction — capture and restore the agent's working state on every `/compact` and resume, invisible to you | `5 hooks` · `1 skill` · `4 commands` · `1 agent` | `/plugin install amnesia@88plug` |
| [**caveman-plus**](https://github.com/88plug/caveman-plus) | Talk like caveman. Cut ~75% tokens. Keep all technical accuracy | `1 output style` | `/plugin install caveman-plus@88plug` |
| [**total-recall**](https://github.com/88plug/total-recall)&nbsp;`v0.6.1` | Cross-session, cross-CLI memory. Mines transcripts from 8 CLI clients; surfaces operator identity, standing decisions, bans, goals, and past corrections so the model stops re-asking | `4 hooks` · `2 skills` · `15 commands` · `23 MCP tools` | `/plugin install total-recall@88plug` |
| [**searxng**](https://github.com/88plug/searxng-mcp)&nbsp;`v0.2.0` | Privacy-respecting metasearch over 70+ engines via a self-hosted SearXNG instance. Token-efficient tool responses, stdio + streamable-http, optional rendered (Playwright) fetch for JS-heavy pages | `1 MCP server` | `/plugin install searxng@88plug` |

## Philosophy

Plugins should be invisible until you need them. Each one in this marketplace earns its slot by closing a specific failure mode in long-horizon AI-assisted work:

- **amnesia** — the model forgets what it was doing across compaction
- **caveman-plus** — the model spends 4× more tokens than the answer needs
- **total-recall** — the model keeps relearning who the operator is and what they've already decided
- **searxng** — the model can't do real web research without leaking queries to surveillance-capitalism search engines

All four are local-first and respect your privacy by default.

## License

MIT. See [LICENSE](./LICENSE).

## Contributing

PRs welcome. New plugin submissions should:

1. Live in their own `88plug/<plugin-name>` repository.
2. Ship a valid `.claude-plugin/plugin.json` at repo root.
3. Open a PR here that adds an entry to `.claude-plugin/marketplace.json` (github source).

Plugin code itself never lives in this repo — only the marketplace index.
