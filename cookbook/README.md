# Cookbook — netcore-cd-agent

This directory is **this agent's own cookbook**: deterministic CD recipes **scoped
to .NET Core only**. See `ARCHITECTURE.md` §2.3 for the platform-wide rule.

## How it's meant to work
`GENERATE` is **cookbook-first**: match the app-pattern to a recipe here and render
the **Harness blue/green** pipeline deterministically; the **LLM is only a fallback**
when no recipe matches. Generation is idempotent — reuse an existing shared template,
never fork it per application; add only what's missing.

## Files
- `cookbook.yaml` — starter recipes by app-pattern (web-service, worker), encoding
  the architect's authoritative CD design (Harness blue/green on AKS, shared template
  per pattern in a remote git repo, per-env input-sets, Nexus image per CI handoff,
  approval for staging/prod, rollback on health failure).

## Status — WIRED (metadata-level) ✓
`GENERATE` now reads this cookbook: `src/agent/cookbook.py` loads the recipe for the
`app_pattern` (web-service | worker) and `GenerateHarnessPipeline` stamps the
generated pipeline's `metadata.labels`/`annotations` with the recipe's declared
strategy, pattern, health type, shared-template name and approval envs. It reports
`generation_source` (`cookbook` | `builtin-fallback`).

Remaining (backlog): this is still a **first-cut scaffold**. The recipe currently
drives pipeline *metadata*, not the full Argo/Harness template body. Confirm the
recipe fields against the architect's real .NET Core Harness template, then thread
them (strategy, health path, approvals, target) through the template body, with an
LLM fallback that writes a missing recipe.
