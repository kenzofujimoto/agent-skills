---
name: {{SKILL_NAME}}
description: Describe the concrete outcome this skill produces and its trigger conditions.
---

# {{SKILL_TITLE}}

## When to use

Use this skill when the request requires its specialized workflow.

## When not to use

Do not use it for unrelated tasks or when required inputs are unavailable.

## Workflow

1. Inspect the available context and constraints.
2. Select the smallest safe approach.
3. Execute the work with explicit error handling.
4. Validate the result against the request.

## Rules

- Keep paths portable and inputs untrusted.
- Never embed credentials or private data.
- State assumptions that materially affect the result.

## References

Read only the files in `references/` needed for the task.

## Recipes

Use `recipes/` for repeatable implementation patterns.

## Scripts

Prefer the tested helpers in `scripts/` when applicable.

## QA

Verify correctness, safety, portability, and documentation.

## Deliverables

Return the completed artifact, validation results, and any remaining limitation.
