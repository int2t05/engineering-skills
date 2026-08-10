# Dispatch Brief — Shared Preamble (for all skill-migration subagents)

You are migrating skills as part of a refactor consolidating 83 → 33 skills.
Working dir: `C:/Users/int2t/Desktop/skills` (Windows, Git Bash).

## FIRST: read the format spec
Read `references/skill-anatomy.md` and `references/engineering-principles.md` to learn the
schema every skill must follow. Then do your assigned tasks below.

## GLOBAL CONSTRAINTS (enforced by `scripts/validate-skills.sh`)
- Each skill is a folder `<phase>/<skill-name>/SKILL.md` (uppercase `SKILL.md` — no exceptions).
- Frontmatter fields ALLOWED: `name`, `description`, `disable-model-invocation` (optional only).
  FORBIDDEN (drop if present in sources): `license`, `metadata`, `category`, `priority`,
  `agents`, `dependencies`, `tags`, `validation`, `origin`, `allowed-tools`, `model`,
  `user-invocable`, `argument-hint`.
- Body sections IN ORDER: `## When to use`, `## Steps`, `## Verify`, `## References`.
- `## References` MUST link `../../references/engineering-principles.md`
  (every skill is two levels deep: `<phase>/<skill>/SKILL.md` → `../../references/` = root `references/`).
- Keep `SKILL.md` LEAN (hit the per-task line target). Move encyclopedic data, long examples,
  platform-specific detail into `<skill>/references/<x>.md` (progressive disclosure); replace
  the inlined bulk with a one-line link in `## References`.
- English-primary bodies. Preserve and add Chinese trigger phrases in `## When to use` where
  the skill serves a Chinese workflow.

## MERGE RULES (apply to every task)
- Preserve each source's精华 — concrete steps, verification gates, reference material.
- DROP: verbose intros, anti-rationalization tables, "Core Operating Behaviors" boilerplate
  (that discipline now lives in `engineering-principles.md`, which every skill links — do NOT
  repeat it), per-skill license/origin cruft, Codex `agents/openai.yaml` files.
- When merging multiple sources, synthesize one coherent skill — don't stitch sections verbatim.

## PROCESS PER TASK
1. Read each source `SKILL.md` (and supporting files) listed in the task.
2. Write the target `SKILL.md` per its frontmatter + merge intent + line target.
3. Extract the listed encyclopedic content into `<target>/references/<x>.md`; link from SKILL.md.
4. Delete the listed root source folders: `rm -rf <root-skill-name>/` (root sources only; never
   delete anything under `archive/`).
5. Run the validator: `bash scripts/validate-skills.sh` (from repo root). It reports skills-found
   count and per-skill errors. YOUR skills' own checks (frontmatter fields, 4 sections,
   engineering-principles link, uppercase filename) MUST pass. The total count will be partial
   until all phases are done — that is expected; ignore the count mismatch.

## DO NOT
- Do NOT `git add` or `git commit` — the coordinator commits centrally after reviewing your report.
- Do NOT edit anything under `archive/` (read-only upstream sources).
- Do NOT touch skills outside your assigned list.

## REPORT (return as your final message, concise + structured)
For each skill produced:
- target path + line count
- refs extracted (paths)
- root sources deleted (paths)
- validator result for this skill's checks (pass / which failures)
Then: any concerns, ambiguities you resolved, or decisions you made. Keep it tight.
