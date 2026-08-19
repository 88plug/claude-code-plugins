---
description: "Manage and design Blueprints — reusable state machines for recurring unattended task patterns."
argument-hint: "[list | show <name> | design <task description>]"
---

Manage Blueprints for this project.

**Usage**

```
/blueprint list                          — list all stored Blueprints in .minions/
/blueprint show <name>                   — display a stored Blueprint
/blueprint design <task description>     — design a new Blueprint using the blueprint-architect agent
```

**What is a Blueprint?**

A Blueprint is a state machine that alternates deterministic steps (scripted,
no LLM) with agentic nodes (LLM loops) to drive an unattended coding agent to
reliable completion. Modeled after Stripe's Minions architecture.

Blueprints live in `.minions/<name>.blueprint.md` at the project root.

**Examples**

```
/blueprint list
/blueprint show dependency-upgrade
/blueprint design bump a Python dependency, migrate breaking changes, run tests, PR
/blueprint design add a REST endpoint with handler + test + OpenAPI spec
```

If $ARGUMENTS starts with "list" or is empty: scan `.minions/*.blueprint.md` and
list them with a one-line summary each. If none exist, print a tip to run
`/blueprint design <description>` to create the first one.

If $ARGUMENTS starts with "show": read and display `.minions/<name>.blueprint.md`.

If $ARGUMENTS starts with "design": spawn the `blueprint-architect` agent with
the remaining text as the task class description, and save the resulting Blueprint
to `.minions/<slug>.blueprint.md` where slug is a kebab-case version of the name
the architect assigns.
