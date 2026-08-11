# Writing Docs from Scratch

Sub-guide for the `documentation-audit` skill. Use when the task is writing
**new** documentation, not syncing drifted docs to code.

## When to use this sub-guide

- "Write a README for this project."
- "Document this feature."
- "Write user-facing docs for this endpoint/flow."
- No docs exist yet and you're starting from a blank page.

## When NOT to use

- Docs exist but are out of sync with code → main `documentation-audit` sync
  flow.
- Designing the API contract itself → `api-design`.
- Polishing an open source project's GitHub presence → `oss-polish`.

## Steps

1. **Identify the audience and what they need to do.** A README targets a
   new contributor (get running in 5 minutes). Feature docs target a user
   (accomplish a task). API docs target an integrator (call correctly). State
   the audience at the top before writing.
2. **Read the code to ground every claim.** Commands come from
   `package.json` / `Makefile`; the structure comes from the directory tree;
   the behavior comes from the entry points. Never document what you assume —
   document what you read.
3. **Pick the doc type's minimal complete structure:**
   - **README** — what it is, prerequisites, install, run, test, structure,
     license. Keep it short; link out to deeper docs.
   - **Feature doc** — what it does, how to use it (steps), configuration,
     gotchas.
   - **API doc** — endpoint, method, parameters, request/response shapes,
     errors, example call. (If an OpenAPI spec exists, point there instead of
     duplicating.)
4. **Write one runnable example.** A copy-pasteable command or request that
   works against the real system. One working example beats three paragraphs.
5. **Mark gaps honestly.** If a behavior isn't determinable from code, write
   "TODO: confirm with maintainer" rather than inventing it. Gaps are
   actionable; invented docs are defects.
6. **Cross-link, don't duplicate.** Point to the spec, ADRs, or API doc by
   path rather than restating their content.

## Quality bar

- Every command was read from the project's config (not guessed).
- Every structural claim maps to a real file or directory.
- At least one runnable example is present.
- No invented behavior — gaps are marked.

## When to escalate

- Writing reveals the API contract is unclear → `api-design`.
- The project has no structure to document → consider `spec` /
  `architecture` first.
- Docs are for an open source launch → `oss-polish` for README positioning +
  topics after the content is written here.

## Verify

- The audience is stated at the top.
- Every command runs (read from config, verified against the real project).
- One runnable example works.
- Gaps are marked, not fabricated.
