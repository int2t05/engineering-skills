---
name: spec
description: Use when starting a new project, feature, or significant change. Writes a spec/PRD covering objectives, commands, structure, code style, testing, and boundaries before any code. Triggers on "write spec", "create prd", "spec out", "to spec".
---

# Spec

Write a structured specification before any code. The spec is the shared source of truth —
it defines what we're building, why, and how we'll know it's done. Code without a spec is
guessing.

## When to use

- Starting a new project, feature, or significant change.
- Requirements are ambiguous or only exist as a vague idea.
- The change touches multiple files or modules.
- User says "write spec", "create prd", "spec out", "to spec", or 写规格.

**Not for:** single-line fixes, typos, or changes where requirements are unambiguous.

## Steps

1. **Surface assumptions.** Before writing any spec content, list what you're assuming
   (tech stack, auth model, database, target environment). Ask the user to correct before
   proceeding. Don't silently fill ambiguous requirements.

2. **Ask 3–5 clarifying questions** where the prompt is ambiguous — problem/goal, core
   functionality, scope, success criteria. Offer lettered options (A/B/C/D) so the user
   can respond "1A, 2C, 3B" for quick iteration. Only ask what's actually ambiguous.

3. **Write the spec** using the template below. Reframe vague requirements as testable
   success criteria ("make the dashboard faster" → "LCP < 2.5s on 4G; initial load < 500ms").

4. **Publish.** Save to `tasks/spec-[feature-name].md` (or a user-specified path). If the
   project has an issue tracker, publish there with a `ready-for-agent` label. Commit the
   spec — it's a living document, not a one-time artifact. Update it when decisions or
   scope change; reference it in PRs.

5. **User review gate.** Ask the user to review the written spec before any implementation.
   If they request changes, make them and re-verify. Only proceed once approved.

**Spec template:**

```markdown
# Spec: [Project/Feature Name]

## Objective
[What we're building and why. User stories with verifiable acceptance criteria.]

## Project Structure
[Directory layout with descriptions — where source, tests, docs live.]

## Commands
[Build, test, lint, dev — full executable commands with flags.]

## Code Style
[One real code snippet showing conventions. Naming, formatting, key patterns.]

## Testing Strategy
[Framework, test locations, coverage expectations, which test levels for which concerns.]

## Boundaries
- Always: [run tests before commits, validate inputs, follow naming conventions]
- Ask first: [schema changes, new dependencies, CI config changes]
- Never: [commit secrets, edit vendor dirs, remove failing tests without approval]

## Non-Goals
[What this feature will NOT include. Makes scope trade-offs explicit.]

## Open Questions
[Unresolved items needing human input.]
```

Planning the implementation FROM this spec uses Claude Code's built-in plan mode
(see engineering-principles §7) — no custom plan skill. The spec is plan mode's input.

## Verify

- The spec file exists on disk and is committed to version control.
- It covers all sections: Objective, Structure, Commands, Code Style, Testing, Boundaries, Non-Goals.
- Success criteria are specific and testable, not vague.
- Boundaries (Always / Ask first / Never) are defined.
- The user has reviewed and approved the spec.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline shared by every skill; §7 covers plan mode for implementation planning.
