#!/usr/bin/env bash
# minion-prehydrate.sh
#
# UserPromptSubmit hook — runs before every user prompt.
# When the prompt triggers a /minion run (detected by CLAUDE_TOOL_INPUT or
# CLAUDE_HOOK_EVENT env vars), pre-fetches referenced GitHub issues/PRs and
# injects them into the context window via stdout.
#
# Outputs a JSON object with an "inject" key if context was fetched, or exits
# silently (empty output) when no pre-hydration is needed. The Claude Code hook
# system ignores empty output and honours non-empty output as a context injection.
#
# Required env (set by Claude Code):
#   CLAUDE_HOOK_EVENT_JSON  — JSON blob of the full hook event
#
# Soft-required (for GitHub fetches):
#   GH_TOKEN / GITHUB_TOKEN  — GitHub API token (falls back to gh CLI auth)

set -euo pipefail

event="${CLAUDE_HOOK_EVENT_JSON:-}"
if [[ -z "$event" ]]; then
  exit 0
fi

# Extract the user prompt text
prompt=$(echo "$event" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    # UserPromptSubmit shape: {prompt: str} or {message: {content: str}}
    print(d.get('prompt') or d.get('message', {}).get('content') or '')
except Exception:
    print('')
" 2>/dev/null || true)

if [[ -z "$prompt" ]]; then
  exit 0
fi

# Only pre-hydrate when the prompt looks like a /minion invocation
if ! echo "$prompt" | grep -qiE '^/minion\b|minion[[:space:]]+run|run[[:space:]]+minion'; then
  exit 0
fi

# Collect GitHub issue/PR references: #123, owner/repo#123, full URLs
refs=$(echo "$prompt" | grep -oE \
  'https://github\.com/[^/]+/[^/]+/(issues|pull)/[0-9]+|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[0-9]+|#[0-9]+' \
  || true)

if [[ -z "$refs" ]]; then
  exit 0
fi

# Check for gh CLI
if ! command -v gh &>/dev/null; then
  exit 0
fi

output=""
while IFS= read -r ref; do
  [[ -z "$ref" ]] && continue

  # Normalise: strip URL to owner/repo#number
  if echo "$ref" | grep -qE '^https://github\.com/'; then
    owner_repo=$(echo "$ref" | sed -E 's|https://github\.com/([^/]+/[^/]+)/(issues\|pull)/([0-9]+).*|\1#\3|')
    ref="$owner_repo"
  fi

  # Determine type: issue or PR (try issue first, fallback to PR)
  repo_part=$(echo "$ref" | cut -d'#' -f1)
  number=$(echo "$ref" | cut -d'#' -f2)

  # If no repo_part, use current repo from git remote
  if [[ -z "$repo_part" ]] || [[ "$repo_part" == "$number" ]]; then
    repo_part=$(git remote get-url origin 2>/dev/null \
      | sed -E 's|.*github\.com[:/]([^/]+/[^.]+)(\.git)?$|\1|' || true)
  fi

  [[ -z "$repo_part" || -z "$number" ]] && continue

  # Fetch as issue, fall back to PR
  fetched=$(gh issue view "$number" --repo "$repo_part" \
    --json number,title,body,labels,state \
    2>/dev/null || \
    gh pr view "$number" --repo "$repo_part" \
    --json number,title,body,state,baseRefName,headRefName \
    2>/dev/null || true)

  [[ -z "$fetched" ]] && continue

  title=$(echo "$fetched" | python3 -c \
    "import sys,json; d=json.load(sys.stdin); print(d.get('title',''))" 2>/dev/null || true)
  body=$(echo "$fetched" | python3 -c \
    "import sys,json; d=json.load(sys.stdin); print((d.get('body') or '')[:1200])" 2>/dev/null || true)

  output+="
--- pre-hydrated: ${repo_part}#${number} ---
Title: ${title}
${body}
---
"
done <<< "$refs"

if [[ -n "$output" ]]; then
  python3 -c "
import sys, json
print(json.dumps({'inject': sys.argv[1]}))
" "$output"
fi
