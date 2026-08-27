"""Cookbook loader for netcore-cd-agent (see ARCHITECTURE.md §2.3).

This agent carries its OWN cookbook (``cookbook/cookbook.yaml`` at the repo root),
scoped to .NET Core CD only. A CD recipe is keyed by app-pattern (web-service /
worker) and declares the deploy shape (Harness blue/green strategy, health type,
approval envs, the shared Harness template name). GENERATE is cookbook-first: it
loads the recipe for the app-pattern and stamps the generated pipeline with the
recipe's declared strategy/pattern/approvals; it falls back to built-in defaults
when no recipe matches.

No ``agent_core`` dependency, so the loader/renderer can be unit-tested offline.

NOTE (backlog): the CD cookbook is a first-cut scaffold not yet confirmed against
the architect's real Harness template, so today the recipe drives pipeline
metadata (labels/annotations) rather than the full Argo template body. Deepening
that is tracked in cookbook/README.md and ARCHITECTURE.md §6.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

import yaml


def find_cookbook() -> Optional[Path]:
    override = os.getenv("COOKBOOK_PATH")
    if override:
        p = Path(override)
        return p if p.is_file() else None
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "cookbook" / "cookbook.yaml"
        if candidate.is_file():
            return candidate
    return None


def load_cookbook() -> Optional[dict]:
    path = find_cookbook()
    if not path:
        return None
    with path.open() as fh:
        return yaml.safe_load(fh)


def get_recipe(app_pattern: str = "web-service") -> Optional[dict]:
    """Return the CD recipe for an app-pattern, or None to fall back."""
    cb = load_cookbook()
    if not cb:
        return None
    recipe = (cb.get("recipes") or {}).get(app_pattern)
    return dict(recipe) if recipe else None


def _q(v: Any) -> str:
    s = str(v)
    if "'" in s:
        return '"' + s.replace('"', '\\"') + '"'
    return f"'{s}'"


def render_metadata(recipe: Optional[dict], app_pattern: str) -> str:
    """Render metadata labels+annotations (2-space indent) from a recipe, or ''."""
    if not recipe:
        return ""
    lines = [
        "  labels:",
        f"    deploy-strategy: {_q(recipe.get('deploy_strategy', 'blue-green'))}",
        f"    app-pattern: {_q(app_pattern)}",
    ]
    if recipe.get("health_type"):
        lines.append(f"    health-type: {_q(recipe['health_type'])}")
    lines.append("  annotations:")
    if recipe.get("harness_template"):
        lines.append(f"    cookbook/harness-template: {_q(recipe['harness_template'])}")
    approvals = recipe.get("approval_envs") or []
    if approvals:
        lines.append(f"    cookbook/approval-envs: {_q(','.join(approvals))}")
    return "\n".join(lines) + "\n"
