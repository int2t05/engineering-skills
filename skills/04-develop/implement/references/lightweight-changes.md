# Lightweight Changes

Sub-guide for the `implement` skill. Use for changes too small to warrant a
full spec — small edits, mechanical renames, project scaffolding. The bar is:
the change has no open design question; if it did, you'd be in `spec`, not here.

## When to use this sub-guide

- "Change this config value / default."
- "Rename this module / function / file."
- "Move this file to a new directory."
- "Add a trivial field to a config or type."
- "Scaffold a new project (package.json, tooling config, dir structure)."

## When NOT to use

- The change requires a design decision → `spec`.
- The change has cross-cutting architectural impact → `architecture` or
  `codebase-design`.
- You're fixing a bug whose cause is unknown → `debugging` first.

## Steps

### Small edits (config, defaults, trivial fields)

1. Read the target file and any callers of the symbol/field you're changing.
2. Make the edit.
3. Run the typecheck and the directly affected tests.
4. Done — commit if the work session is complete.

### Mechanical renames / moves

1. Find every reference: `grep -r "<old-name>"` across the repo (exclude
   build output and dependencies).
2. Rename the declaration and every reference in one pass. Use the editor's
   rename-refactor when the language supports it; otherwise search-and-replace
   with the exact identifier.
3. For file moves, update import paths in every file that references the old
   path.
4. Run typecheck + full test suite — a missed reference surfaces here.
5. Verify no stale references remain: re-run the grep; expect zero hits.

### Project scaffolding

1. Confirm the stack with the user (language, framework, runtime version).
2. Create the minimum structure to make the project buildable and testable:
   entry point, one example module, one example test, tooling config
   (lint/format/typecheck), and a `.gitignore`.
3. Run build + test once to prove the skeleton works before adding real
   features.
4. Write a one-paragraph `README.md` stating what the project is and its run
   commands — enough for the next session to orient.

## When to escalate to a full spec

- The "small change" starts touching more than ~3 files or crosses module
  boundaries you don't fully understand → stop, switch to `spec`.
- The rename reveals a naming ambiguity that needs a decision → `spec`.
- Scaffolding grows into architecture decisions (DB choice, service
  boundaries) → `architecture`.

## Verify

- Typecheck passes.
- Affected tests pass (full suite for renames/moves; targeted for small edits).
- `grep` for the old name returns zero hits (for renames).
- For scaffolding: `build` and `test` both run green on the empty skeleton.
