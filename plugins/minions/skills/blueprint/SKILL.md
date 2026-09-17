---
name: blueprint
description: >-
  Apply BEFORE structuring any multi-step agentic task. Use when the work
  has at least two distinct phases (gather context / implement / verify) or
  when the task will run unattended. Teaches how to alternate deterministic
  steps with agentic nodes to maximise reliability, minimise token spend, and
  guarantee a hard retry cap. Especially valuable for coding tasks triggered
  by external signals (issues, tickets, Slack threads) and for recurring
  task patterns you want to codify into a reusable Blueprint.
---

# Blueprint

A Blueprint is a state machine that drives an unattended coding agent to
reliable completion. It alternates two types of nodes:

```
[D] Deterministic  →  [A] Agentic  →  [D] Deterministic  →  [A?] Agentic  →  [D] Report
```

Modeled after Stripe's Minions architecture (1,300+ unattended PRs/week).

---

## Node types

### [D] Deterministic node

- Hard-coded, scripted, no LLM
- Predictable: same inputs → same outputs every time
- Examples: fetch a GitHub issue, run a linter, push a branch, parse a config,
  create a PR from a template, time a timeout
- Use for: setup, context gathering, verification, submission, any decision
  with < 4 concrete branches

### [A] Agentic node

- Full LLM loop with tool access
- Handles ambiguity, judgment, creative work
- Examples: implement a feature, triage test failures, write a PR description
- Use for: the work that genuinely requires intelligence — nothing else
- Must receive a pre-assembled context packet from preceding D nodes
- Must have a crisp exit condition (a specific artifact, not "when done")

---

## The standard coding Blueprint

Every coding task follows this sequence. Deviate only with explicit justification.

```
Step 1  [D]  Pre-hydrate
             ↓ fetch all linked issues, tickets, docs, PRs before agent starts
Step 2  [A]  Implement
             ↓ one focused LLM pass with full tool access
Step 3  [D]  Lint / verify
             ↓ run the project's own checkers deterministically
Step 4  [D]  Assess: all pass? → jump to Step 6
             any fail caused by this change? → Step 5
             pre-existing fail? → Step 6 with caveat
Step 5  [A]  Fix   ← HARD CAP: one retry only
             ↓ minimal targeted fix, re-run same checkers
Step 6  [D]  Report structured result
```

**Hard cap = 2 agentic passes total.** Diminishing marginal returns after
that. If 2 passes are not enough, the task needs human intervention, not more
retries.

---

## Design axioms

1. **Front-load determinism.** Gather every piece of context the agent will
   need *before* the first agentic node. An agent that fetches its own context
   mid-run is a design defect.

2. **Minimise agentic surface.** The agentic node should know *exactly* what to
   do and receive *only* the context it needs. It should decide *how*, never
   *what*.

3. **Encode small decisions deterministically.** If you can script it, script it.
   Don't spend LLM tokens on `if package.json exists run npm else run pip`.

4. **Epilogue is always deterministic.** The agent never decides to push, commit,
   or open a PR. Those actions are in D nodes at the end of the Blueprint.

5. **Submission authority ≠ merge authority.** Agents propose; humans approve.
   A Blueprint ends with "report + stage for review", never with "merge".

6. **One-shot isolation.** Each Blueprint run is fresh: no memory carried between
   runs, no state on disk from a previous invocation. Idempotent by design.

---

## Pre-hydration recipe

Before any agentic node, deterministically fetch all references in the task:

| Reference type | Command |
|---|---|
| GitHub issue | `gh issue view <number> --json title,body,labels,comments` |
| GitHub PR | `gh pr view <number> --json title,body,state,reviews,files` |
| URL | `WebFetch` → strip to plain text |
| Local file | `Read` |
| Jira / Linear ticket | MCP tool or `curl` + token if configured |

Assemble into a compact context packet:
```
Task: <one-line summary>
Acceptance criteria: <extracted from issue/ticket>
Linked artifacts: <list of fetched summaries>
Affected files: <glob/grep sweep result>
Constraints: <any explicit don'ts>
```

Pass this packet verbatim as the opening context for the agentic node.

---

## Verification recipe

After every agentic node that touches source files, run the project's own tools:

```bash
# Detect toolchain
[ -f package.json ]        && npm run lint --if-present && npm test
[ -f pyproject.toml ]      && (ruff check . ; pytest -x -q)
[ -f Cargo.toml ]          && cargo clippy && cargo test
[ -f go.mod ]              && go vet ./... && go test ./...
[ -f Gemfile ]             && bundle exec rubocop && bundle exec rspec
[ -f Makefile ]            && make lint test
```

Rules:
- Run the project's tools, never invent new ones
- Capture full stdout+stderr per tool
- Classify each failure: caused by this change, or pre-existing?
- Pre-existing failures → document, do not fix (out of scope)
- Failures caused by this change → one fix pass, then report regardless

---

## Report format

Every Blueprint run ends with this block:

```
## Minion result

**Task**: <one-line summary>
**Status**: ✅ ready / ⚠️ ready with caveats / ❌ blocked

**Changes**:
- <file>: <what changed and why>

**Verification**:
- <tool>: PASS
- <tool>: FAIL (pre-existing) — <first error line>

**Notes**: <assumptions made, edge cases skipped, follow-ups>

**Next step**: Review the diff, then `git add -p && git commit`.
```

No prose padding. No apologies. The human reads the status first; the rest
is supporting evidence.

---

## When to use a Blueprint vs. free-form exploration

| Use Blueprint | Use free-form |
|---|---|
| Task is well-defined before starting | Task needs clarification first |
| Task runs unattended | Human is pairing step-by-step |
| Task has a clear done condition | Exploring, debugging, investigating |
| Same task pattern repeats | One-off research or analysis |
| Failure has real cost (CI, production) | Low-stakes experimentation |

---

## Recurring Blueprint patterns

Store reusable Blueprints for your project as `.minions/<name>.blueprint.md`.
The `/blueprint` command can list, show, and design them.

Common patterns worth codifying:
- `dependency-upgrade`: bump a package, migrate breakage, verify, PR
- `add-api-endpoint`: scaffold route + handler + test + docs
- `fix-flaky-test`: investigate failure pattern, add retry/isolation, verify
- `backfill-migration`: write migration, run on shadow DB, verify data shape
- `translate-copy`: extract strings, translate via API, update locale files
