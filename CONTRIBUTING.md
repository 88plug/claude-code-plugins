# Contributing to 88plug plugins

Thanks for considering a contribution. This repo is the **marketplace index**
— individual plugin code lives in its own `88plug/<plugin>` repository. Where
you contribute depends on what you want to do.

## What you want to do

### Add a NEW plugin to the marketplace

1. Build your plugin in its own GitHub repo. Ship a valid `.claude-plugin/plugin.json`
   at the root (or under a `path` subdirectory).
2. License it however you choose — 88plug recommends FSL-1.1-ALv2 for IP-bearing
   plugins, MIT for thin wrappers, but the choice is yours.
3. Open a pull request here that **adds an entry** to
   `.claude-plugin/marketplace.json` referencing your repo via the
   `{"source": "github", "repo": "..."}` block. Do not commit plugin code into
   this hub repo — the hub ships the index only.
4. Sign the [CLA](#contributor-license-agreement) on your first PR.

### Improve an EXISTING 88plug plugin

Find the plugin's own repo at `https://github.com/88plug/<plugin>` and open
the PR there. The CLA bot will gate the merge.

| Plugin | Repo |
|---|---|
| amnesia | https://github.com/88plug/amnesia |
| caveman-plus | https://github.com/88plug/caveman-plus |
| total-recall | https://github.com/88plug/total-recall |
| searxng | https://github.com/88plug/searxng-mcp |
| deepwiki | https://github.com/88plug/deepwiki |

### Fix something in THIS hub repo

(Typos, broken links, README rephrasing, marketplace.json edits.) Just PR
this repo directly. No CLA required since the hub is MIT and contains no
substantive IP.

## Contributor License Agreement

Pull requests against IP-bearing 88plug repositories (amnesia, total-recall,
searxng-mcp) trigger our CLA Assistant bot. Sign once, all future PRs from
the same GitHub account auto-pass.

The CLA text lives at: https://gist.github.com/88plug/de8629bdb714949a9ea9a47323d8468e

Key terms:

- Your contribution stays your copyright. You grant 88plug a sublicensable
  license to distribute it under current and future license terms (including
  commercial licenses).
- You waive moral rights (relevant in EU jurisdictions).
- You confirm the contribution is your original work or appropriately
  authorized.
- 88plug is not obligated to merge anything.

The CLA is adapted from SAP's lawyer-reviewed open-source CLA (Apache-2.0
licensed text). See the full 9-clause version at the gist link above.

## What 88plug plugins typically look like

Two structural patterns, both legitimate:

**Pure plugin** — hooks, skills, slash commands, output styles, agents. May
or may not embed an MCP server. Examples: `amnesia`, `total-recall`,
`caveman-plus`.

**MCP wrapper** — minimal `.claude-plugin/plugin.json` that points at an
existing MCP server (either local stdio via `uvx`/`npx` or a remote SSE/HTTP
endpoint). Examples: `searxng`, `deepwiki`.

Either pattern is accepted. The marketplace tag prefix (`type:plugin` or
`type:mcp`) signals which to the hub README.

## Naming conventions

- **Plugin repository name on GitHub**: free choice, but the convention is
  - bare service name for plugin-first repos (e.g. `amnesia`, `total-recall`)
  - `<service>-mcp` suffix for pure-MCP-first repos (e.g. `searxng-mcp`)
- **Plugin name** (in `plugin.json` + marketplace entry): always bare service
  name. Drop `-mcp` even if the repo has it. Matches Anthropic's official
  marketplace convention.

## Quality bar

A plugin earns a slot in this marketplace by closing a real failure mode in
AI-assisted work. Vague utility plugins are politely declined. Concretely:

- It should do one specific thing well.
- It should be local-first (or transparently disclose remote dependencies).
- It should not require an API key or paid service for the basic use case
  (third-party paid services are OK but must be optional and disclosed).
- It should not leak data the user did not intend to leak.

## Questions

Open an issue, or email claude@cryptoandcoffee.com.
