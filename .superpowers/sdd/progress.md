# Skills Archive Refactor — Progress Ledger

Tracking execution of `docs/superpowers/plans/2026-08-10-skills-archive-refactor.md`.
After compaction, trust this ledger + `git log` over recollection. Resume at the
first task not marked complete.

## Status

- [x] T1: Scaffold + git + validator — commit 48800e8
- [x] T2: Shared refs + CLAUDE.md — commit 2bcec2f
- [x] T3: Archive upstream repos — commit f2ec37b (335 archive files; inner .git removed as tradeoff)
- [x] T4-36: Migrate 33 skills — commits 0839173..ce0e75a (per-skill table below)
- [x] T37: Root README catalog — commit 78f95d5
- [x] T38: Final verify + audit — 33 skills, 0 errors, overlap clean
- [x] Final whole-branch review — APPROVED_WITH_MINOR; fixes applied commit 2799393
- [x] Fix subagent — 4 Important + 6 Minor fixes, validator still 33/0

## DONE — refactor complete
Final validator: `bash scripts/validate-skills.sh` → 33 skills, 0 errors, exit 0.
15 commits total on master.

## Per-skill migration (T4-36)

| # | Task | Skill | Phase | Model | Status |
|---|---|---|---|---|---|
| 4 | T4 | using-skills | meta | sonnet | pending |
| 5 | T5 | brainstorm | 01-product | sonnet | pending |
| 6 | T6 | spec | 01-product | haiku | pending |
| 7 | T7 | oss-strategy | 01-product | haiku | pending |
| 8 | T8 | research | 02-research | haiku | pending |
| 9 | T9 | market-research | 02-research | haiku | pending |
| 10 | T10 | tech-selection | 02-research | haiku | pending |
| 11 | T11 | architecture | 03-design | sonnet | pending |
| 12 | T12 | domain-modeling | 03-design | haiku | pending |
| 13 | T13 | api-design | 03-design | haiku | pending |
| 14 | T14 | codebase-design | 03-design | opus | pending |
| 15 | T15 | frontend-design | 03-design | opus | pending |
| 16 | T16 | prototype | 03-design | haiku | pending |
| 17 | T17 | implement | 04-develop | sonnet | pending |
| 18 | T18 | breakdown | 04-develop | haiku | pending |
| 19 | T19 | context-engineering | 04-develop | haiku | pending |
| 20 | T20 | performance | 05-tune | haiku | pending |
| 21 | T21 | simplify | 05-tune | haiku | pending |
| 22 | T22 | tdd | 06-test | sonnet | pending |
| 23 | T23 | test-generation | 06-test | haiku | pending |
| 24 | T24 | api-testing | 06-test | sonnet | pending |
| 25 | T25 | e2e-testing | 06-test | sonnet | pending |
| 26 | T26 | code-review | 07-verify | sonnet | pending |
| 27 | T27 | debugging | 07-verify | haiku | pending |
| 28 | T28 | security-review | 07-verify | haiku | pending |
| 29 | T29 | shipping | 08-ship | haiku | pending |
| 30 | T30 | git-workflow | 08-ship | sonnet | pending |
| 31 | T31 | ci-cd | 08-ship | haiku | pending |
| 32 | T32 | deprecation-migration | 08-ship | haiku | pending |
| 33 | T33 | oss-polish | 08-ship | opus | pending |
| 34 | T34 | observability | 09-operate | haiku | pending |
| 35 | T35 | documentation-audit | 09-operate | haiku | pending |
| 36 | T36 | handoff | 09-operate | haiku | pending |

## Completion log

(appended as tasks complete: `Task N: complete (commits <base7>..<head7>, review clean)`)

- Task 4 (using-skills, meta): complete — commit 0839173, validator clean
- Task 20 (performance, 05-tune): complete — commit 0839173, validator clean
- Task 21 (simplify, 05-tune): complete — commit 0839173, validator clean
- Task 34 (observability, 09-operate): complete — commit 302ac85, validator clean
- Task 35 (documentation-audit, 09-operate): complete — commit 302ac85, validator clean
- Task 36 (handoff, 09-operate): complete — commit 302ac85, validator clean
- Task 17 (implement, 04-develop): complete — commit 93dbdfb, validator clean
- Task 18 (breakdown, 04-develop): complete — commit 93dbdfb, validator clean
- Task 19 (context-engineering, 04-develop): complete — commit 93dbdfb, validator clean
- Task 5 (brainstorm, 01-product): complete — commit 44e2120, validator clean
- Task 6 (spec, 01-product): complete — commit 44e2120, validator clean
- Task 7 (oss-strategy, 01-product): complete — commit 44e2120, validator clean
- Task 33 (oss-polish, 08-ship): complete — commit 200f830, validator clean
- Task 11 (architecture, 03-design): complete — commit 4d1285d, validator clean
- Task 12 (domain-modeling, 03-design): complete — commit 4d1285d, validator clean
- Task 13 (api-design, 03-design): complete — commit 4d1285d, validator clean
- Task 16 (prototype, 03-design): complete — commit 4d1285d, validator clean
- Task 26 (code-review, 07-verify): complete — commit d08cada, validator clean
- Task 27 (debugging, 07-verify): complete — commit d08cada, validator clean
- Task 28 (security-review, 07-verify): complete — commit d08cada, validator clean
- Task 8 (research, 02-research): complete — commit d08cada, validator clean
- Task 9 (market-research, 02-research): complete — commit d08cada, validator clean
- Task 10 (tech-selection, 02-research): complete — commit d08cada, validator clean
- Task 29 (shipping, 08-ship): complete — commit 2645665, validator clean
- Task 30 (git-workflow, 08-ship): complete — commit 2645665, validator clean
- Task 31 (ci-cd, 08-ship): complete — commit 2645665, validator clean
- Task 32 (deprecation-migration, 08-ship): complete — commit 2645665, validator clean
- Task 22 (tdd, 06-test): complete — commit 6ed760d, validator clean
- Task 23 (test-generation, 06-test): complete — commit 6ed760d, validator clean
- Task 24 (api-testing, 06-test): complete — commit 6ed760d, validator clean
- Task 25 (e2e-testing, 06-test): complete — commit 6ed760d, validator clean

## Deployability refactor (packaging as plugin) — DONE

Pivot after confirming Claude Code discovery rules (via claude-code-guide):
- discovery is flat (direct children) — nested phase dirs need a plugin's skills[] array
- relative ../../ shared-ref links unreliable — must use ${CLAUDE_PLUGIN_ROOT}
- ambient principles need a SessionStart hook (not CLAUDE.md)
- => package as a plugin (the superpowers-pack model)

Commits:
- 81cabf8: .claude-plugin/plugin.json + skills[] array (33 nested paths)
- 2f19fa5: convert 40 shared-ref links to ${CLAUDE_PLUGIN_ROOT}/references/
- ccdbcf6: hooks/ SessionStart — injects engineering-principles.md as ambient context (tested: valid JSON, 2287 chars)
- 5057633: move phase dirs under skills/ (convention), marketplace.json, README install docs, validator manifest-sync check

Final: 33 skills, 0 errors; plugin structurally complete.
REMAINING (user must do): live install test — `claude --plugin-dir "C:/Users/int2t/Desktop/skills"` and confirm 33 skills + ambient principles load. Also clear ~/.claude/skills/ old 24 skills to avoid redundancy.
