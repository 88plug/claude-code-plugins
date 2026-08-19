---
description: "Run a task end-to-end using the Minion Blueprint: pre-hydrate context, implement, verify, fix once, report."
argument-hint: "<task description, issue URL, or issue #number>"
---

Run the `minion` agent on $ARGUMENTS.

The minion will:
1. Pre-hydrate all context referenced in the task (issues, PRs, URLs, files)
2. Implement the change in one shot, touching only what the task requires
3. Run the project's linters and tests deterministically
4. If any checker fails due to the change, apply one targeted fix pass
5. Report a structured result (status, changed files, verification output)

The agent will not ask for confirmation mid-run. It will not push, commit, or
open a PR — it hands back a diff and a report for you to review and merge.

If the task description is ambiguous, the agent will make a reasonable
interpretation, state it in the report, and proceed.

To design a reusable Blueprint for a recurring task pattern: `/blueprint design <description>`
