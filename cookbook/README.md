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

## Status (backlog)
This is a **first-cut scaffold**, not yet confirmed against the architect's actual
.NET Core Harness template, and the agent does **not yet read it** (ARCHITECTURE.md
§6). Remaining work: confirm the recipe fields against the real template and wire
`GENERATE` to consume this cookbook-first with the LLM as fallback.
