# minions

**Unattended one-shot coding agents driven by Blueprints.**

[![marketplace](https://img.shields.io/badge/marketplace-88plug-1f2328?style=flat-square)](https://github.com/88plug/claude-code-plugins)
[![license](https://img.shields.io/badge/license-FSL--1.1--ALv2-1f2328?style=flat-square)](../../LICENSE)

---

## Install

```sh
/plugin install minions@88plug
```

## What it does

`minions` gives Claude Code an unattended, fire-and-forget coding mode modeled
after [Stripe's Minions architecture](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
(1,300+ unattended PRs merged per week at Stripe).

The core primitive is the **Blueprint** — a state machine that alternates
*deterministic nodes* (scripted, no LLM) with *agentic nodes* (LLM loops):

```
[D] Pre-hydrate context → [A] Implement → [D] Lint/test → [A?] Fix (once) → [D] Report
```

Key properties copied from Stripe's design:

| Property | What it means |
|---|---|
| **Unattended** | Runs to completion without asking for confirmation mid-task |
| **Pre-hydration** | Fetches all linked issues/PRs/docs *before* the agent loop starts |
| **Hard retry cap** | Max one fix pass — diminishing returns beyond that |
| **Submission authority** | Agent proposes a diff; human decides to commit and merge |
| **Deterministic epilogue** | Lint, verify, and report are always scripted — never left to the agent |

## Commands

### `/minion <task>`

Run a task unattended. The task can be:
- A plain description: `/minion refactor the UserService to use dependency injection`
- An issue number: `/minion #412`
- A GitHub URL: `/minion https://github.com/acme/api/issues/412`
- A mixed description: `/minion fix the race condition described in #412`

The minion pre-hydrates any referenced issues/PRs, implements the change,
runs your project's linters and tests, and hands back a structured result:

```
## Minion result

**Task**: Refactor UserService to use dependency injection
**Status**: ✅ ready

**Changes**:
- src/services/user.ts: extracted IUserRepository interface, injected via constructor
- src/services/user.test.ts: updated test setup to pass mock repository

**Verification**:
- tsc: PASS
- eslint: PASS
- jest: PASS (47 tests)

**Next step**: Review the diff above, then `git add -p && git commit`.
```

### `/blueprint [list | show <name> | design <description>]`

Manage reusable Blueprints for recurring task patterns:

```sh
/blueprint list                             # show all .minions/*.blueprint.md
/blueprint show dependency-upgrade          # display a stored Blueprint
/blueprint design bump a Python dep, migrate breakage, verify, PR
```

Blueprints are stored as `.minions/<name>.blueprint.md` at your project root —
check them in alongside your code so the whole team benefits.

## Agents

| Agent | Role |
|---|---|
| `minion` | Unattended task executor. Runs the standard coding Blueprint end-to-end. |
| `blueprint-architect` | Designs reusable Blueprints for recurring task classes. |

## Skill

**`blueprint`** — teaches Claude the Blueprint pattern and when to use it.
Loaded automatically when you use `/minion` or spawn the minion agent.

## Hooks

**`UserPromptSubmit`** — when a `/minion` invocation references GitHub issues
or PRs, the hook pre-fetches them via the `gh` CLI and injects the content into
the context window before the agent loop starts. This is the deterministic
pre-hydration step — the agent receives full context from the first token.

Requires `gh` CLI authenticated. Falls back silently if unavailable.

## Design rationale

Stripe's key insight: most of the cost and failure risk in autonomous coding
comes from the agent having to *discover* what to do while also *doing* it.
Separate the two. Gather everything deterministically first, then hand the
agent a precise instruction and a pre-assembled context packet.

A Blueprint is the formalization of that separation. By encoding the prologue
(pre-hydration), epilogue (lint + report), and all small branching decisions
as deterministic nodes, the agentic nodes are left to do only what LLMs are
actually good at: reading ambiguous specifications, writing idiomatic code, and
synthesizing information from multiple sources.

The 2-pass hard cap exists because empirically, if an LLM cannot fix its own
output in one retry, the problem is usually scope creep or a missing
precondition — not insufficient iterations. Capping retries forces good
Blueprint design upstream.

## References

- [Stripe Minions Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
- [Stripe Minions Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- [HazyResearch Minions](https://github.com/HazyResearch/minions) (local/cloud LLM coordination)
- [Block/Goose](https://github.com/block/goose) (the open-source agent harness Stripe forked)

## License

FSL-1.1-ALv2. See [LICENSE](../../LICENSE).
