# Definition of Done

The project-wide bar. Applies to every change regardless of which skill is active.
Complements each task's per-skill Verify step, not replaces it.

A task is done when ALL hold:
- Tests pass (existing + any new).
- No regressions introduced.
- Behavior verified at runtime, not just at the type/test level.
- Docs updated to match the change (no drift).
- The change is committed with a clear message.

"Seems right" is never sufficient. If you cannot produce evidence, the task is not done.
