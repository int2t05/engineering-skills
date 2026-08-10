# Skills Archive Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate 83 skills across three unmanaged collections into one unified, normalized, lifecycle-organized collection of 33 canonical skills with shared engineering principles.

**Architecture:** In-place refactor at `C:\Users\int2t\Desktop\skills`. 9 numbered SDLC phase directories + `meta/` + shared `references/` + `archive/` for the two upstream repos (read-only). Each skill is a lean `SKILL.md` (15-150 lines) with progressive disclosure via in-skill `references/`. Recurring discipline distilled once into `references/engineering-principles.md`, linked from every skill.

**Tech Stack:** Markdown skill files, YAML frontmatter, pure-bash validator (Git Bash on Windows).

**Spec:** `docs/superpowers/specs/2026-08-10-skills-archive-refactor-design.md`

## Global Constraints

- **Working dir:** `C:\Users\int2t\Desktop\skills` (Windows, Git Bash). Use forward slashes in paths.
- **Skill filename:** `SKILL.md` (uppercase) — no exceptions. Fixes the lone lowercase `test-generator/skill.md`.
- **Frontmatter fields allowed:** `name`, `description`, `disable-model-invocation` (optional only). All other fields (`license`, `metadata`, `category`, `priority`, `agents`, `dependencies`, `tags`, `validation`, `origin`, `allowed-tools`, `model`, `user-invocable`, `argument-hint`) are forbidden.
- **Skill body sections (in order):** `## When to use`, `## Steps`, `## Verify`, `## References`.
- **Every skill** links `../../references/engineering-principles.md` (or `../references/...` for `meta/`) in `## References`.
- **Language:** English-primary bodies; preserve/add Chinese trigger phrases in `## When to use` where a skill serves a Chinese workflow.
- **Skill count:** exactly 33 (1 meta + 32 phase). Any addition/removal requires updating the spec.
- **Two upstream repos** become read-only under `archive/upstream-addyosmani/` and `archive/upstream-mattpocock/` — preserve their git history (move the whole folder, do not flatten).
- **Plan routing:** no custom plan skill. Skills/README point to Claude Code's built-in plan mode (EnterPlanMode/ExitPlanMode).
- **Frequent commits:** one commit per task. Commit message prefix `refactor:` for moves, `feat:` for new content.

---

## File Structure

### Created (collection skeleton)
- `README.md` — root catalog: 9-phase table + install + conventions
- `CLAUDE.md` — collection-level agent conventions
- `scripts/validate-skills.sh` — schema validator (dependency-free bash)
- `references/engineering-principles.md` — distilled 8 principles
- `references/skill-anatomy.md` — format spec + skill-writing guide
- `references/definition-of-done.md` — project-wide completion bar
- `references/clean-code.md` — Uncle Bob coding discipline (from root `clean-code`)
- `references/mermaid-diagrams.md` — Mermaid syntax + examples (from root `mermaid-diagrams`)
- `meta/using-skills/SKILL.md` — router/meta-skill
- `<phase>/<skill-name>/SKILL.md` × 32 — the phase skills
- `<phase>/<skill-name>/references/*.md` — progressive-disclosure docs (per skill, as needed)

### Moved (archived, read-only)
- `agent-skills/` → `archive/upstream-addyosmani/`
- `skills/` → `archive/upstream-mattpocock/`

### Deleted (after migration verified)
- The 24 original root skill folders (content merged into the new structure or archived)

### Source-path conventions (for migration tasks)
- **Root skills** (read in place during their task, then deleted): `<name>/SKILL.md` at repo root.
- **Addy sources:** `archive/upstream-addyosmani/skills/<name>/SKILL.md` (after Task 3).
- **Matt sources:** `archive/upstream-mattpocock/skills/<bucket>/<name>/SKILL.md` (after Task 3).

---

## Task 1: Scaffold structure + git init + validator

**Files:**
- Create: `scripts/validate-skills.sh`
- Create (dirs): `references/`, `meta/`, `01-product/`, `02-research/`, `03-design/`, `04-develop/`, `05-tune/`, `06-test/`, `07-verify/`, `08-ship/`, `09-operate/`, `archive/`
- Init: git repo at `C:\Users\int2t\Desktop\skills`

**Interfaces:**
- Produces: `scripts/validate-skills.sh` (exit 0 = all skills valid, exit non-zero = failures). Used by every subsequent skill task as the test gate.

- [ ] **Step 1: Initialize git repo**

```bash
cd "C:/Users/int2t/Desktop/skills"
git init
git config user.email "local@skills" 2>/dev/null; git config user.name "skills" 2>/dev/null
```

- [ ] **Step 2: Create the directory skeleton**

```bash
cd "C:/Users/int2t/Desktop/skills"
mkdir -p references meta archive docs/superpowers/plans
for p in 01-product 02-research 03-design 04-develop 05-tune 06-test 07-verify 08-ship 09-operate; do mkdir -p "$p"; done
```

- [ ] **Step 3: Write the validator**

Create `scripts/validate-skills.sh` with this exact content:

```bash
#!/usr/bin/env bash
# Validate every SKILL.md against the collection schema. Dependency-free (bash + awk + grep).
set -euo pipefail
cd "$(dirname "$0")/.."

phases="meta 01-product 02-research 03-design 04-develop 05-tune 06-test 07-verify 08-ship 09-operate"
errors=0
count=0

for phase in $phases; do
  for skill_dir in "$phase"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_md="$skill_dir/SKILL.md"
    if [ ! -f "$skill_md" ]; then
      echo "FAIL: $skill_dir has no SKILL.md (lowercase filename?)"
      errors=$((errors+1)); continue
    fi
    count=$((count+1))
    head -1 "$skill_md" | grep -q '^---' || { echo "FAIL: $skill_md missing frontmatter opener"; errors=$((errors+1)); }
    grep -q '^name:' "$skill_md" || { echo "FAIL: $skill_md missing name:"; errors=$((errors+1)); }
    grep -q '^description:' "$skill_md" || { echo "FAIL: $skill_md missing description:"; errors=$((errors+1)); }
    fm=$(awk 'NR==1{next} /^---$/{exit} {print}' "$skill_md")
    bad=$(echo "$fm" | grep -iE '^(license|metadata|category|priority|agents|dependencies|tags|validation|origin|allowed-tools|model|user-invocable|argument-hint):' || true)
    [ -z "$bad" ] || { echo "FAIL: $skill_md disallowed frontmatter: $bad"; errors=$((errors+1)); }
    grep -q '^## When to use' "$skill_md" || { echo "FAIL: $skill_md missing ## When to use"; errors=$((errors+1)); }
    grep -q '^## Steps' "$skill_md" || { echo "FAIL: $skill_md missing ## Steps"; errors=$((errors+1)); }
    grep -q '^## Verify' "$skill_md" || { echo "FAIL: $skill_md missing ## Verify"; errors=$((errors+1)); }
    grep -q '^## References' "$skill_md" || { echo "FAIL: $skill_md missing ## References"; errors=$((errors+1)); }
    grep -q 'engineering-principles' "$skill_md" || { echo "FAIL: $skill_md doesn't link engineering-principles"; errors=$((errors+1)); }
  done
done

echo "Skills found: $count (expected 33)"
[ "$count" -eq 33 ] || { echo "FAIL: expected 33 skills, found $count"; errors=$((errors+1)); }
echo "Total errors: $errors"
exit $errors
```

- [ ] **Step 4: Make validator executable and run it (expect 0 skills, 0 errors)**

```bash
cd "C:/Users/int2t/Desktop/skills"
chmod +x scripts/validate-skills.sh
bash scripts/validate-skills.sh
```
Expected output: `Skills found: 0 (expected 33)` then `FAIL: expected 33 skills, found 0` and `Total errors: 1`. This is correct — no skills exist yet. The validator itself works (exit non-zero only because count is 0, which later tasks fix).

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/int2t/Desktop/skills"
cat > .gitignore <<'EOF'
archive/upstream-addyosmani/.git
archive/upstream-mattpocock/.git
EOF
git add scripts/validate-skills.sh .gitignore
git commit -m "feat: scaffold directory structure and skill validator"
```

---

## Task 2: Write the shared reference docs + CLAUDE.md

These docs are foundational — every skill task links them. Write them before any skill.

**Files:**
- Create: `references/engineering-principles.md`
- Create: `references/skill-anatomy.md`
- Create: `references/definition-of-done.md`
- Create: `references/clean-code.md` (content from root `clean-code/SKILL.md`)
- Create: `references/mermaid-diagrams.md` (content from root `mermaid-diagrams/SKILL.md` + its `references/`)
- Create: `CLAUDE.md`

**Interfaces:**
- Produces: 5 reference docs + `CLAUDE.md`. Every skill task's `## References` links `engineering-principles.md`; skill-anatomy is the spec skills conform to.

- [ ] **Step 1: Write `references/engineering-principles.md`**

Content — the 8 distilled principles, each with a one-line elaboration. These come from the spec §7. Write them as a referenced doc (no frontmatter — it's a reference, not a skill):

```markdown
# Engineering Principles

Recurring discipline for every skill in this collection. Each skill links this file
rather than repeating these rules. Apply them at all times.

## 1. Surface assumptions before implementing
List assumptions explicitly before non-trivial work; ask for correction before proceeding.
Don't silently fill ambiguous requirements.

## 2. Manage confusion actively
When you hit inconsistencies or unclear specs: STOP. Name the confusion. Ask. Wait.
Never plow ahead with a guess. (Absorbs the old "wait-what" reflex.)

## 3. Push back when warranted
No sycophancy. If an approach has clear problems, say so, quantify the downside,
propose an alternative, and accept the human's override with full information.

## 4. Enforce simplicity
Minimum code that solves the problem. Abstractions must earn their complexity.
If 100 lines would do what 1000 do, you have failed. Prefer the boring, obvious solution.

## 5. Surgical scope
Touch only what the task requires. Don't refactor adjacent code, "clean up" orthogonal
code, or delete things you don't fully understand. Match existing style.

## 6. Verify, don't assume
Evidence before assertions. "Seems right" is never sufficient — passing tests, build
output, or runtime data. See definition-of-done.md for the project-wide bar.

## 7. Plan with built-in plan mode
No custom plan skill. Use Claude Code's EnterPlanMode/ExitPlanMode for planning.
The spec is its input. For work breakdown into tickets, use the `breakdown` skill.

## 8. Goal-driven execution
Transform tasks into verifiable goals ("write a test that reproduces it, then make it
pass"). Loop until the goal is verified, not until it "looks done."
```

- [ ] **Step 2: Write `references/skill-anatomy.md`**

Content — the format spec from spec §6, framed as the skill-writing guide (folds in matt `writing-for-agents`):

```markdown
# Skill Anatomy

How to write a skill in this collection. Every skill conforms to this spec; the
validator (scripts/validate-skills.sh) enforces it.

## Folder layout
<phase>/<skill-name>/SKILL.md            # lean core, always loaded
<phase>/<skill-name>/references/<x>.md   # progressive disclosure, loaded on demand

## Frontmatter (minimal, enforced)
---
name: kebab-case-name
description: Use when [trigger]. [What it does]. [Optional: triggers on "中文短语".]
disable-model-invocation: true   # OPTIONAL — only for skills that must be typed by the user
---
Allowed fields: name, description, disable-model-invocation. Nothing else.

## Body sections (in order)
## When to use    — 2-4 trigger conditions; include Chinese phrases where relevant
## Steps          — numbered, each step independently verifiable
## Verify         — concrete completion check (evidence, not "looks right")
## References     — link ../../references/engineering-principles.md + skill-specific docs

## Progressive disclosure
Keep SKILL.md lean (target 15-150 lines, matching function complexity). Move
encyclopedic data, long examples, and platform-specific detail into references/
subfiles the skill loads only when needed.

## User-invoked vs model-invoked
- Model-invoked (default): rich trigger phrasing so the model reaches for it.
- User-invoked: set disable-model-invocation: true. Must be typed (e.g. /brainstorm, /handoff).
Use sparingly — only when auto-activation would cause false positives.
```

- [ ] **Step 3: Write `references/definition-of-done.md`**

```markdown
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
```

- [ ] **Step 4: Write `references/clean-code.md` (from root `clean-code`)**

Read `clean-code/SKILL.md` at repo root. Rewrite as a reference doc: strip the YAML frontmatter, keep the Clean Code principles content, reframe the heading as `# Clean Code` (reference, not skill). Drop any "Use when..." framing that assumes it's a skill. The body becomes the coding-discipline reference that `04-develop/implement` and `engineering-principles` link.

- [ ] **Step 5: Write `references/mermaid-diagrams.md` (from root `mermaid-diagrams`)**

Read `mermaid-diagrams/SKILL.md` AND its `mermaid-diagrams/references/` (7 diagram-type files). Merge into one reference doc `references/mermaid-diagrams.md`: strip frontmatter, keep the syntax guide + all diagram-type examples. `03-design/architecture`, `07-verify/code-review`, etc. link it on demand.

- [ ] **Step 6: Write `CLAUDE.md` (collection-level agent conventions)**

```markdown
# CLAUDE.md

This is a curated collection of agent skills organized by the software development
lifecycle. See README.md for the full catalog.

## Conventions
- Skills live under meta/ + 9 numbered phase dirs (01-product through 09-operate).
- Every skill is a folder with SKILL.md (uppercase). See references/skill-anatomy.md.
- Every skill links references/engineering-principles.md — the distilled discipline.
- Planning uses Claude Code's built-in plan mode (EnterPlanMode/ExitPlanMode), not a skill.
- Validate the collection: bash scripts/validate-skills.sh

## Skill discovery
Run /using-skills (meta) to route a task to the right phase skill, or invoke a skill
directly by name.
```

- [ ] **Step 7: Commit**

```bash
cd "C:/Users/int2t/Desktop/skills"
git add references/ CLAUDE.md
# Note: clean-code/ and mermaid-diagrams/ root folders still exist until their
# deletion task — that's fine, the references/ copies are the canonical ones now.
git commit -m "feat: shared reference docs and collection CLAUDE.md"
```

---

## Task 3: Archive the two upstream repos (read-only)

**Files:**
- Move: `agent-skills/` → `archive/upstream-addyosmani/`
- Move: `skills/` → `archive/upstream-mattpocock/`

**Interfaces:**
- Produces: `archive/upstream-addyosmani/skills/<name>/SKILL.md` and `archive/upstream-mattpocock/skills/<bucket>/<name>/SKILL.md` — the source paths all skill-migration tasks read from.

- [ ] **Step 1: Move both repos into archive/, preserving their internal .git**

```bash
cd "C:/Users/int2t/Desktop/skills"
mkdir -p archive
git mv agent-skills archive/upstream-addyosmani
git mv skills archive/upstream-mattpocock
```

If `git mv` complains the dirs aren't tracked yet (they aren't — repo just initialized), use plain moves then `git add`:

```bash
cd "C:/Users/int2t/Desktop/skills"
mv agent-skills archive/upstream-addyosmani
mv skills archive/upstream-mattpocock
```

- [ ] **Step 2: Verify the source paths exist for migration**

```bash
cd "C:/Users/int2t/Desktop/skills"
test -f archive/upstream-addyosmani/skills/planning-and-task-breakdown/SKILL.md && echo "addy OK"
test -f archive/upstream-mattpocock/skills/engineering/implement/SKILL.md && echo "matt OK"
```
Expected: `addy OK` then `matt OK`.

- [ ] **Step 3: Verify .git history preserved inside each archived repo**

```bash
cd "C:/Users/int2t/Desktop/skills/archive/upstream-addyosmani"
git log --oneline -1 2>/dev/null && echo "addy git OK"
cd "C:/Users/int2t/Desktop/skills/archive/upstream-mattpocock"
git log --oneline -1 2>/dev/null && echo "matt git OK"
```
Expected: a commit line + `git OK` for each. (The inner .git folders are gitignored by Task 1's .gitignore so the outer repo doesn't nest them.)

- [ ] **Step 4: Commit**

```bash
cd "C:/Users/int2t/Desktop/skills"
git add archive/
git commit -m "refactor: archive upstream addyosmani and mattpocock repos as read-only"
```

---

## Skill Migration Tasks (Tasks 4-36)

Each skill task follows this 5-step template. **Read the per-task Sources/Files/Frontmatter/Extract block, then apply the template.**

**Template:**
- [ ] **Step 1: Read sources** — Read each source path listed; note which sections carry the canonical content (per the merge note).
- [ ] **Step 2: Write `<target>/SKILL.md`** — Use the frontmatter block below. Body: 4 sections (When to use / Steps / Verify / References). Lean to the line target. `## References` MUST link `../../references/engineering-principles.md` (for phase skills) plus any extracted refs.
- [ ] **Step 3: Extract references** (skip if "none") — Move the listed encyclopedic content into `<target>/references/<x>.md`; replace it in SKILL.md with a one-line link.
- [ ] **Step 4: Validate** — Run `bash scripts/validate-skills.sh`; the only allowed failure is the count (33) until all skills exist. This skill's own checks (frontmatter, sections, link) must pass.
- [ ] **Step 5: Delete original root source + commit** — If a root skill was a source, delete its original folder: `rm -rf <root-skill-name>/`. Then commit: `git add <target> && git rm -r <root-skill-name>/ 2>/dev/null; git commit -m "feat: migrate <skill-name> to <phase>"`.

**Merge rule (applies to all):** Preserve each source's精华. Drop verbose intros, anti-rationalization tables (those live in engineering-principles.md now), and per-skill license/origin cruft. Keep concrete steps, verification gates, and reference material.

---

## Task 4: meta/using-skills (router)

**Sources:**
- `find-skills/SKILL.md` (root)
- `using-superpowers/SKILL.md` (root) + its `references/` (codex-tools, copilot-tools, gemini-tools)
- `archive/upstream-addyosmani/skills/using-agent-skills/SKILL.md`
- `archive/upstream-mattpocock/skills/engineering/ask-matt/SKILL.md`

**Files:** Create `meta/using-skills/SKILL.md` + `meta/using-skills/references/phase-tree.md`

**Frontmatter:**
```yaml
---
name: using-skills
description: Use when starting a session or deciding which skill applies. Maps incoming work to the right skill across the 9 SDLC phases (product → research → design → develop → tune → test → verify → ship → operate).
---
```

**Body:** Lean router. `## When to use`: start of session, or unsure which skill fits. `## Steps`: a decision tree by phase (product/brainstorm-or-spec → research → design → develop → tune → test → verify → ship → operate), each branch naming the concrete skill. Move the full ASCII decision tree into `references/phase-tree.md` (progressive disclosure) and keep a compact phase-list in SKILL.md. `## Verify`: the routed skill activates and matches the task. `## References`: engineering-principles + phase-tree + (optionally) the platform-tool refs from using-superpowers if still relevant.

**Extract:** full decision tree → `references/phase-tree.md`; platform-tool reference files (codex/copilot/gemini) → `meta/using-skills/references/` only if you keep multi-platform notes, else drop (this is a Claude Code collection).

**Line target:** ~80.

Apply the 5-step template. Root sources to delete after: `find-skills/`, `using-superpowers/`.

---

## Task 5: 01-product/brainstorm

**Sources:**
- `brainstorming/SKILL.md` (root) + its `scripts/`, `visual-companion.md`, `spec-document-reviewer-prompt.md`
- `archive/upstream-addyosmani/skills/idea-refine/SKILL.md` + its `examples.md`, `frameworks.md`, `refinement-criteria.md`
- `archive/upstream-addyosmani/skills/interview-me/SKILL.md`
- `archive/upstream-mattpocock/skills/productivity/grill-me/SKILL.md`
- `archive/upstream-mattpocock/skills/productivity/grilling/SKILL.md`
- `archive/upstream-mattpocock/skills/engineering/grill-with-docs/SKILL.md`
- `archive/upstream-mattpocock/skills/productivity/to-questionnaire/SKILL.md`

**Files:** Create `01-product/brainstorm/SKILL.md` + `01-product/brainstorm/references/techniques.md`

**Frontmatter:**
```yaml
---
name: brainstorm
description: Use before any creative work, or when the ask is underspecified. One-question-at-a-time dialogue that sharpens a vague idea into a concrete proposal. Triggers on "brainstorm", "grill me", "interview me", "refine this idea".
disable-model-invocation: true
---
```

**Body:** Merge the one-question-at-a-time discipline (interview-me, grilling, grill-me) with divergent/convergent thinking (idea-refine) and the spec-review loop (brainstorming). `## When to use`: underspecified asks, new features, "refine this." `## Steps`: establish intent → ask ONE question → converge → repeat until ~95% confidence → propose. `## Verify`: user confirms the proposal captures intent; spec is writable. `## References`: engineering-principles + techniques (the frameworks/examples from idea-refine).

**Extract:** idea-refine's `examples.md` + `frameworks.md` + `refinement-criteria.md` → `references/techniques.md`; brainstorming's `visual-companion.md` → `references/visual-companion.md` (keep if useful); the `scripts/` (server) → drop unless you use the visual companion.

**Line target:** ~120.

Apply template. Root source to delete: `brainstorming/`.

---

## Task 6: 01-product/spec

**Sources:**
- `prd/SKILL.md` (root)
- `archive/upstream-addyosmani/skills/spec-driven-development/SKILL.md`
- `archive/upstream-mattpocock/skills/engineering/to-spec/SKILL.md`

**Files:** Create `01-product/spec/SKILL.md`

**Frontmatter:**
```yaml
---
name: spec
description: Use when starting a new project, feature, or significant change. Writes a spec/PRD covering objectives, commands, structure, code style, testing, and boundaries before any code. Triggers on "write spec", "create prd", "spec out", "to spec".
---
```

**Body:** Merge prd's PRD structure with addy's spec-driven gates and matt's to-spec publish step. `## When to use`: new project/feature/change. `## Steps`: objectives → structure → commands → code style → testing → boundaries → publish. `## Verify`: spec file exists, covers all sections, user approves. `## References`: engineering-principles. Note: planning the implementation from this spec uses built-in plan mode (principle 7).

**Extract:** none.

**Line target:** ~100.

Apply template. Root source to delete: `prd/`.

---

## Task 7: 01-product/oss-strategy

**Sources:**
- `open-source-strategy/SKILL.md` (root)

**Files:** Create `01-product/oss-strategy/SKILL.md`

**Frontmatter:**
```yaml
---
name: oss-strategy
description: Use when the user wants open source strategy, OSS commercialization, open core, COSS, open source to paid, GitHub stars strategy, or open source growth/business model. Triggers on "open source strategy", "OSS 策略".
---
```

**Body:** Keep the strategy/business content (COSS, open core, commercialization, growth). This is strategy only — GitHub-presence beautification lives in `08-ship/oss-polish`. `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~90.

Apply template. Root source to delete: `open-source-strategy/`.

---

## Task 8: 02-research/research

**Sources:**
- `research-to-md/SKILL.md` (root) + its `pressure-scenarios.md`, `agents/openai.yaml`
- `archive/upstream-mattpocock/skills/engineering/research/SKILL.md`

**Files:** Create `02-research/research/SKILL.md` + `02-research/research/references/pressure-scenarios.md`

**Frontmatter:**
```yaml
---
name: research
description: Use when the user asks for deep web research, source-backed investigation, current technical/tool comparison, or a cited Markdown research artifact.
---
```

**Body:** Merge research-to-md's cited-artifact workflow with matt's minimal research loop. `## Steps`: frame question → fan-out search → fetch sources → adversarially verify claims → synthesize cited Markdown. `## Verify`: artifact has citations; claims verified. `## References`: engineering-principles + pressure-scenarios.

**Extract:** `pressure-scenarios.md` → `references/pressure-scenarios.md`. Drop `agents/openai.yaml` (Codex integration, out of scope).

**Line target:** ~110.

Apply template. Root source to delete: `research-to-md/`.

---

## Task 9: 02-research/market-research

**Sources:** `market-research/SKILL.md` (root)

**Files:** Create `02-research/market-research/SKILL.md`

**Frontmatter:**
```yaml
---
name: market-research
description: Use when the user wants market sizing, competitor comparisons, investor due diligence, industry intelligence, fund research, or technology scans that inform business decisions.
---
```

**Body:** Keep the market/competitor/duediligence methodology with source attribution. Drop `origin: ECC` frontmatter (forbidden field). `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~75.

Apply template. Root source to delete: `market-research/`.

---

## Task 10: 02-research/tech-selection

**Sources:** `github-tech-selection-research/SKILL.md` (root)

**Files:** Create `02-research/tech-selection/SKILL.md`

**Frontmatter:**
```yaml
---
name: tech-selection
description: Use when choosing or comparing a technology stack, library, framework, open-source project, or repository for a concrete requirement. Triggers on "技术选型", "方案对比", "选哪个", "tech stack", "library comparison".
---
```

**Body:** Keep the GitHub-driven selection/comparison methodology. Preserve Chinese triggers. `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~150.

Apply template. Root source to delete: `github-tech-selection-research/`.

---

## Task 11: 03-design/architecture

**Sources:**
- `architecture-designer/SKILL.md` (root) + its `references/` (adr-template, architecture-patterns, database-selection, nfr-checklist, system-design)

**Files:** Create `03-design/architecture/SKILL.md` + `03-design/architecture/references/` (adr-template.md, architecture-patterns.md, database-selection.md, nfr-checklist.md, system-design.md)

**Frontmatter:**
```yaml
---
name: architecture
description: Use when designing high-level system architecture, reviewing existing designs, or making architectural decisions. Produces ADRs, architecture diagrams, and evaluates scalability/NFR trade-offs.
---
```

**Body:** Keep the system-level architecture workflow. `## Steps`: identify NFRs → evaluate patterns → design components → record ADR. `## Verify`: ADR written; diagram renders; NFRs addressed. `## References`: engineering-principles + the 5 reference docs + mermaid-diagrams (../../references/mermaid-diagrams.md).

**Extract:** the 5 reference files move into `03-design/architecture/references/` (rename to lowercase-kebab if needed). Drop `license: MIT` and `metadata:` frontmatter.

**Line target:** ~120.

Apply template. Root source to delete: `architecture-designer/`.

---

## Task 12: 03-design/domain-modeling

**Sources:**
- `archive/upstream-mattpocock/skills/engineering/domain-modeling/SKILL.md` + its `ADR-FORMAT.md`, `CONTEXT-FORMAT.md`

**Files:** Create `03-design/domain-modeling/SKILL.md` + `03-design/domain-modeling/references/` (context-format.md, adr-format.md)

**Frontmatter:**
```yaml
---
name: domain-modeling
description: Use when building or sharpening a project's domain model — challenging terms, stress-testing with scenarios, and updating CONTEXT.md and ADRs inline to establish a shared ubiquitous language.
---
```

**Body:** Keep matt's domain-modeling discipline (challenge terms, scenarios, update CONTEXT.md + ADRs). `## References`: engineering-principles + context-format + adr-format.

**Extract:** `CONTEXT-FORMAT.md` → `references/context-format.md`; `ADR-FORMAT.md` → `references/adr-format.md`.

**Line target:** ~80.

Apply template. No root source to delete (matt source is already in archive).

---

## Task 13: 03-design/api-design

**Sources:** `archive/upstream-addyosmani/skills/api-and-interface-design/SKILL.md`

**Files:** Create `03-design/api-design/SKILL.md`

**Frontmatter:**
```yaml
---
name: api-design
description: Use when designing APIs or interfaces — REST/GraphQL contracts, request/response shapes, versioning, error models, and interface ergonomics.
---
```

**Body:** Keep addy's API/interface design content. `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~150.

Apply template. No root source to delete.

---

## Task 14: 03-design/codebase-design

**Sources:**
- `archive/upstream-mattpocock/skills/engineering/codebase-design/SKILL.md` + its `DEEPENING.md`, `DESIGN-IT-TWICE.md`
- `archive/upstream-mattpocock/skills/engineering/improve-codebase-architecture/SKILL.md` + its `HTML-REPORT.md`
- `improve-codebase-architecture/SKILL.md` (root) + its `DEEPENING.md`, `HTML-REPORT.md`, `INTERFACE-DESIGN.md`, `LANGUAGE.md`

**Files:** Create `03-design/codebase-design/SKILL.md` + `03-design/codebase-design/references/` (deepening.md, design-it-twice.md, html-report.md, interface-design.md, language.md)

**Frontmatter:**
```yaml
---
name: codebase-design
description: Use when designing deep modules, finding refactoring or deepening opportunities, or making a codebase more testable and AI-navigable. Presents deepening opportunities and works through the one you pick.
---
```

**Body:** Merge matt's codebase-design (deep modules, design-it-twice) with both improve-codebase-architecture variants (deepening scan + HTML report). `## Steps`: scan for deepening opportunities → present → pick one → grill through it. `## References`: engineering-principles + the 5 reference docs.

**Extract:** consolidate the UPPERCASE reference files into lowercase-kebab `references/` files (dedupe the two DEEPENING.md / HTML-REPORT.md copies — keep the richer one).

**Line target:** ~110.

Apply template. Root source to delete: `improve-codebase-architecture/`.

---

## Task 15: 03-design/frontend-design

**Sources:**
- `frontend-design/SKILL.md` (root)
- `ui-ux-pro-max/SKILL.md` (root) — encyclopedic (658 lines: 50+ styles, 161 palettes, 57 fonts, 161 product types, 99 UX guidelines, 25 charts)
- `apple-hig-design/SKILL.md` (root)
- `archive/upstream-addyosmani/skills/frontend-ui-engineering/SKILL.md`

**Files:** Create `03-design/frontend-design/SKILL.md` + `03-design/frontend-design/references/` (palettes.md, font-pairings.md, styles.md, ux-guidelines.md, apple-hig.md)

**Frontmatter:**
```yaml
---
name: frontend-design
description: Use when building web components, pages, or applications with distinctive, production-grade design quality. Covers color, typography, layout, interaction states, and platform conventions. Triggers on "frontend", "UI", "design", "界面设计".
---
```

**Body:** This is the critical progressive-disclosure task. SKILL.md stays lean (~120 lines): the design method (form heuristic, color formula, mark specs, interaction rules) + when-to-use + steps + verify + refs. ALL encyclopedic data (161 palettes, 57 fonts, 50+ styles, 99 UX guidelines, Apple HIG specs) moves to `references/`. `## Steps`: define element/project → pick style → apply color formula → typography pairing → interaction states → verify. `## References`: engineering-principles + palettes + font-pairings + styles + ux-guidelines + apple-hig.

**Extract:** palettes → `references/palettes.md`; fonts → `references/font-pairings.md`; styles → `references/styles.md`; UX guidelines → `references/ux-guidelines.md`; apple-hig content → `references/apple-hig.md`. Drop `license:` frontmatter from frontend-design and apple-hig sources.

**Line target:** ~120 (SKILL.md only — refs hold the bulk).

Apply template. Root sources to delete: `frontend-design/`, `ui-ux-pro-max/`, `apple-hig-design/`.

---

## Task 16: 03-design/prototype

**Sources:** `archive/upstream-mattpocock/skills/engineering/prototype/SKILL.md` + its `LOGIC.md`, `UI.md`

**Files:** Create `03-design/prototype/SKILL.md` + `03-design/prototype/references/` (logic.md, ui.md)

**Frontmatter:**
```yaml
---
name: prototype
description: Use when a design question is best answered by a throwaway prototype — a single shareable HTML file for state/logic, or several toggleable UI variations to compare.
---
```

**Body:** Keep matt's prototype discipline (throwaway, single HTML, or toggleable variations). `## References`: engineering-principles + logic + ui.

**Extract:** `LOGIC.md` → `references/logic.md`; `UI.md` → `references/ui.md`.

**Line target:** ~40.

Apply template. No root source to delete.

---

## Task 17: 04-develop/implement

**Sources:**
- `archive/upstream-mattpocock/skills/engineering/implement/SKILL.md`
- `archive/upstream-addyosmani/skills/incremental-implementation/SKILL.md`
- `archive/upstream-addyosmani/skills/source-driven-development/SKILL.md`
- `archive/upstream-addyosmani/skills/doubt-driven-development/SKILL.md`

**Files:** Create `04-develop/implement/SKILL.md`

**Frontmatter:**
```yaml
---
name: implement
description: Use when implementing the work described by a spec or tickets. Drives TDD at pre-agreed seams, runs typechecks and tests regularly, and closes with code-review before committing. Incremental, source-driven, doubt-driven.
---
```

**Body:** Merge matt's lean implement shell (drive /tdd at seams, typecheck, full suite at end, /code-review, commit) with addy's incremental-implementation (one slice at a time), source-driven (doc-verified code), and doubt-driven (high-stakes/unfamiliar code). `## Steps`: read spec/tickets → implement one slice via tdd → typecheck → run affected tests → full suite at end → code-review → commit. `## Verify`: tests pass; code-review clean; committed. `## References`: engineering-principles + ../../references/clean-code.md.

**Extract:** none (clean-code is already a shared reference).

**Line target:** ~90.

Apply template. No root source to delete.

---

## Task 18: 04-develop/breakdown

**Sources:**
- `archive/upstream-mattpocock/skills/engineering/to-tickets/SKILL.md`
- `archive/upstream-mattpocock/skills/engineering/wayfinder/SKILL.md`

**Files:** Create `04-develop/breakdown/SKILL.md`

**Frontmatter:**
```yaml
---
name: breakdown
description: Use when breaking a plan, spec, or conversation into tracer-bullet tickets, each declaring its blocking edges. For work too large for one session, builds a shared map of decision tickets resolved one at a time.
---
```

**Body:** Merge to-tickets (tracer-bullet tickets with blocking edges) and wayfinder (huge-work decision map). `## Verify`: tickets written with blocking edges; map resolves to a clear path. `## References`: engineering-principles. Note: the plan itself comes from built-in plan mode (principle 7); this skill breaks the result into tickets.

**Extract:** none.

**Line target:** ~90.

Apply template. No root source to delete.

---

## Task 19: 04-develop/context-engineering

**Sources:** `archive/upstream-addyosmani/skills/context-engineering/SKILL.md`

**Files:** Create `04-develop/context-engineering/SKILL.md`

**Frontmatter:**
```yaml
---
name: context-engineering
description: Use when the agent needs better context — assembling the right files, definitions, and prior decisions to feed into the working context before implementing.
---
```

**Body:** Keep addy's context-engineering content. `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~100.

Apply template. No root source to delete.

---

## Task 20: 05-tune/performance

**Sources:** `archive/upstream-addyosmani/skills/performance-optimization/SKILL.md`

**Files:** Create `05-tune/performance/SKILL.md`

**Frontmatter:**
```yaml
---
name: performance
description: Use when optimizing performance. Measure before you optimize — profile, identify bottlenecks, then improve. Triggers on "webperf", "performance regression", "慢", "性能优化".
---
```

**Body:** Keep addy's performance methodology (measure-first, profile, optimize). `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~150.

Apply template. No root source to delete.

---

## Task 21: 05-tune/simplify

**Sources:** `archive/upstream-addyosmani/skills/code-simplification/SKILL.md`

**Files:** Create `05-tune/simplify/SKILL.md`

**Frontmatter:**
```yaml
---
name: simplify
description: Use when the code is too complex. Clarity over cleverness — removes speculative abstractions, dead complexity, and earns-its-cost structures. Triggers on "simplify", "too complex", "refactor for clarity".
---
```

**Body:** Keep addy's code-simplification content. `## References`: engineering-principles + ../../references/clean-code.md.

**Extract:** none.

**Line target:** ~120.

Apply template. No root source to delete.

---

## Task 22: 06-test/tdd

**Sources:**
- `test-driven-development/SKILL.md` (root) + its `testing-anti-patterns.md`
- `archive/upstream-addyosmani/skills/test-driven-development/SKILL.md`
- `archive/upstream-mattpocock/skills/engineering/tdd/SKILL.md` + its `mocking.md`, `tests.md`

**Files:** Create `06-test/tdd/SKILL.md` + `06-test/tdd/references/` (testing-anti-patterns.md, mocking.md, good-tests.md)

**Frontmatter:**
```yaml
---
name: tdd
description: Use when implementing any feature or bugfix, before writing implementation code. Red-green-refactor loop, one vertical slice at a time. Triggers on "tdd", "test-driven", "red green refactor".
---
```

**Body:** Merge the three. addy's red-green-refactor loop + gates; matt's lean shell + mocking/tests refs; root's anti-patterns. `## Steps`: write failing test → run (red) → minimal impl → run (green) → refactor → commit. `## Verify`: test passes; behavior verified at runtime. `## References`: engineering-principles + testing-anti-patterns + mocking + good-tests.

**Extract:** root `testing-anti-patterns.md` → `references/testing-anti-patterns.md`; matt `mocking.md` → `references/mocking.md`; matt `tests.md` → `references/good-tests.md`.

**Line target:** ~120.

Apply template. Root source to delete: `test-driven-development/`.

---

## Task 23: 06-test/test-generation

**Sources:** `test-generator/skill.md` (root — NOTE the lowercase filename; this is the one being fixed)

**Files:** Create `06-test/test-generation/SKILL.md`

**Frontmatter:**
```yaml
---
name: test-generation
description: Use when asked to generate or write tests for a feature or bugfix. Language-agnostic, works with any test framework. Triggers on "generate tests", "create tests", "write tests for", "生成测试".
---
```

**Body:** Keep the test-generation methodology. Preserve Chinese triggers. `## References`: engineering-principles + ../../references/clean-code.md. Drop `user-invocable: true` frontmatter (forbidden; use disable-model-invocation only if needed — here leave it model-invoked).

**Extract:** none.

**Line target:** ~150.

Apply template. Root source to delete: `test-generator/` (the lowercase `skill.md` case issue is resolved by writing the new `SKILL.md` uppercase).

---

## Task 24: 06-test/api-testing

**Sources:** `api-testing-patterns/SKILL.md` (root) + its `templates/`, `scripts/`, `schemas/`, `evals/`, `config.json`

**Files:** Create `06-test/api-testing/SKILL.md` + `06-test/api-testing/references/` (templates, schemas — keep if useful)

**Frontmatter:**
```yaml
---
name: api-testing
description: Use when testing APIs or designing API test strategies — contract testing, REST/GraphQL testing, and integration testing.
---
```

**Body:** Keep the API testing patterns. `## References`: engineering-principles + templates/schemas refs. **Drop the entire custom frontmatter** (`category`, `priority`, `agents`, `dependencies`, `tags`, `validation`) — all forbidden fields.

**Extract:** keep `templates/` and `schemas/` as `references/` if they carry real content; drop `config.json` and `evals/` (collection-specific scaffolding).

**Line target:** ~150.

Apply template. Root source to delete: `api-testing-patterns/`.

---

## Task 25: 06-test/e2e-testing

**Sources:**
- `e2e-playwright-testing/SKILL.md` (root) + its `rules/` (10 files), `AGENTS.md`, `README.md`
- `archive/upstream-addyosmani/skills/browser-testing-with-devtools/SKILL.md`

**Files:** Create `06-test/e2e-testing/SKILL.md` + `06-test/e2e-testing/references/` (playwright-rules.md consolidated)

**Frontmatter:**
```yaml
---
name: e2e-testing
description: Use when writing end-to-end or browser tests — Playwright flows, form submission, user journeys, and DevTools-driven testing. Triggers on "playwright", "e2e test", "browser test", "end-to-end".
---
```

**Body:** Merge the Playwright patterns with addy's DevTools-driven testing. `## References`: engineering-principles + playwright-rules. Drop `license: MIT` and `metadata:` frontmatter.

**Extract:** consolidate the 10 `rules/` files into `references/playwright-rules.md` (or keep as a `references/rules/` subdir if distinct). Drop `AGENTS.md`, `README.md` (collection-specific).

**Line target:** ~150.

Apply template. Root source to delete: `e2e-playwright-testing/`.

---

## Task 26: 07-verify/code-review

**Sources:**
- `archive/upstream-addyosmani/skills/code-review-and-quality/SKILL.md`
- `archive/upstream-mattpocock/skills/engineering/code-review/SKILL.md`

**Files:** Create `07-verify/code-review/SKILL.md`

**Frontmatter:**
```yaml
---
name: code-review
description: Use when reviewing code before merge. Two-axis review: Standards (repo conventions + smell baseline) and Spec (faithful to the originating issue/spec). Run as parallel sub-agents for thoroughness.
---
```

**Body:** Merge addy's five-axis quality review with matt's two-axis (Standards + Spec) parallel-subagent approach. `## Steps`: diff since fixed point → Standards axis → Spec axis → synthesize findings. `## Verify`: findings verified adversarially; report delivered. `## References`: engineering-principles + ../../references/clean-code.md + ../../references/mermaid-diagrams.md.

**Extract:** none.

**Line target:** ~120.

Apply template. No root source to delete.

---

## Task 27: 07-verify/debugging

**Sources:**
- `archive/upstream-addyosmani/skills/debugging-and-error-recovery/SKILL.md`
- `archive/upstream-mattpocock/skills/engineering/diagnosing-bugs/SKILL.md` + its `scripts/hitl-loop.template.sh`

**Files:** Create `07-verify/debugging/SKILL.md` + `07-verify/debugging/references/hitl-loop-template.sh`

**Frontmatter:**
```yaml
---
name: debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes. Disciplined diagnosis loop: build a red feedback loop → minimise → hypothesise → instrument → fix → regression-test.
---
```

**Body:** Merge addy's error-recovery with matt's diagnosing-bugs loop. `## Steps`: reproduce (go red) → minimise → hypothesise → instrument → fix → regression-test. `## Verify`: regression test passes; root cause identified (not symptom masked). `## References`: engineering-principles + hitl-loop-template.

**Extract:** `scripts/hitl-loop.template.sh` → `references/hitl-loop-template.sh`.

**Line target:** ~120.

Apply template. No root source to delete.

---

## Task 28: 07-verify/security-review

**Sources:** `archive/upstream-addyosmani/skills/security-and-hardening/SKILL.md`

**Files:** Create `07-verify/security-review/SKILL.md`

**Frontmatter:**
```yaml
---
name: security-review
description: Use when reviewing changes for security — secrets, auth, injection, access control, and hardening. Complete security review of pending changes.
---
```

**Body:** Keep addy's security-and-hardening content. `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~150.

Apply template. No root source to delete.

---

## Task 29: 08-ship/shipping

**Sources:** `archive/upstream-addyosmani/skills/shipping-and-launch/SKILL.md`

**Files:** Create `08-ship/shipping/SKILL.md`

**Frontmatter:**
```yaml
---
name: shipping
description: Use when deploying or launching to production. Faster is safer — checklist-driven launch with rollback readiness and launch-day verification.
---
```

**Body:** Keep addy's shipping-and-launch content. `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~120.

Apply template. No root source to delete.

---

## Task 30: 08-ship/git-workflow

**Sources:**
- `archive/upstream-addyosmani/skills/git-workflow-and-versioning/SKILL.md`
- `archive/upstream-mattpocock/skills/engineering/resolving-merge-conflicts/SKILL.md`
- `archive/upstream-mattpocock/skills/misc/git-guardrails-claude-code/SKILL.md` + its `scripts/block-dangerous-git.sh`
- `archive/upstream-mattpocock/skills/misc/setup-pre-commit/SKILL.md`

**Files:** Create `08-ship/git-workflow/SKILL.md` + `08-ship/git-workflow/references/` (block-dangerous-git.sh, pre-commit-setup.md)

**Frontmatter:**
```yaml
---
name: git-workflow
description: Use when committing, branching, resolving merge or rebase conflicts, or setting up git guardrails and pre-commit hooks. Resolves conflicts by intent traced to each side's source — never --abort.
---
```

**Body:** Merge addy's git-workflow-and-versioning (broad) with matt's resolving-merge-conflicts (hunk-by-hunk by intent), git-guardrails (dangerous-command blocking), and setup-pre-commit. `## References`: engineering-principles + block-dangerous-git + pre-commit-setup.

**Extract:** `scripts/block-dangerous-git.sh` → `references/block-dangerous-git.sh`; setup-pre-commit content → `references/pre-commit-setup.md`.

**Line target:** ~150.

Apply template. No root source to delete.

---

## Task 31: 08-ship/ci-cd

**Sources:** `archive/upstream-addyosmani/skills/ci-cd-and-automation/SKILL.md`

**Files:** Create `08-ship/ci-cd/SKILL.md`

**Frontmatter:**
```yaml
---
name: ci-cd
description: Use when working on CI/CD pipelines and automation — build, test, and deploy automation, pipeline design, and deployment strategies.
---
```

**Body:** Keep addy's ci-cd-and-automation content. `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~150.

Apply template. No root source to delete.

---

## Task 32: 08-ship/deprecation-migration

**Sources:**
- `archive/upstream-addyosmani/skills/deprecation-and-migration/SKILL.md`
- `archive/upstream-mattpocock/skills/misc/migrate-to-shoehorn/SKILL.md`

**Files:** Create `08-ship/deprecation-migration/SKILL.md`

**Frontmatter:**
```yaml
---
name: deprecation-migration
description: Use when deprecating old code or APIs, or migrating to a new system. Staged deprecation paths and migration strategies that preserve behavior across the transition.
---
```

**Body:** Merge addy's deprecation-and-migration with matt's migrate-to-shoehorn (concrete migration example). `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~120.

Apply template. No root source to delete.

---

## Task 33: 08-ship/oss-polish (开源项目美化)

**Sources:**
- `readme-generator/SKILL.md` (root) + its `references/badges.md`, `scripts/` (collect-site-metrics.py, validate-readme.py)
- `oss-project-polish/SKILL.md` (root)
- `github-topics/SKILL.md` (root) + its `src/` (python)
- `repo-story-time/SKILL.md` (root)

**Files:** Create `08-ship/oss-polish/SKILL.md` + `08-ship/oss-polish/references/` (badges.md, scripts/)

**Frontmatter:**
```yaml
---
name: oss-polish
description: Use when polishing an open source project's GitHub presence — README, topics/About description, commit-history narrative story, and trending-repo positioning. Triggers on "polish my repo", "开源项目美化", "优化项目展示".
---
```

**Body:** Merge the four into one OSS-beautification skill. `## Steps`: README (readme-generator method + badges) → topics/About (oss-project-polish) → narrative story (repo-story-time) → trending positioning (github-topics). `## Verify`: README conforms to best practices; topics set; narrative generates; validate-readme passes. `## References`: engineering-principles + badges + scripts.

**Extract:** `references/badges.md` → `references/badges.md`; `scripts/collect-site-metrics.py` + `scripts/validate-readme.py` → `references/scripts/`; github-topics `src/` python → `references/scripts/` (or drop if redundant). Drop `license: MIT` frontmatter from readme-generator.

**Line target:** ~150.

Apply template. Root sources to delete: `readme-generator/`, `oss-project-polish/`, `github-topics/`, `repo-story-time/`.

---

## Task 34: 09-operate/observability

**Sources:** `archive/upstream-addyosmani/skills/observability-and-instrumentation/SKILL.md`

**Files:** Create `09-operate/observability/SKILL.md`

**Frontmatter:**
```yaml
---
name: observability
description: Use when adding logs, metrics, alerts, or instrumentation to a system — making runtime behavior observable and debuggable in production.
---
```

**Body:** Keep addy's observability-and-instrumentation content. `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~100.

Apply template. No root source to delete.

---

## Task 35: 09-operate/documentation-audit

**Sources:** `documentation-audit/SKILL.md` (root)

**Files:** Create `09-operate/documentation-audit/SKILL.md`

**Frontmatter:**
```yaml
---
name: documentation-audit
description: Use when documentation drift is detected. Comprehensively audits the codebase and syncs Swagger, feature docs, and general documentation to match the code.
---
```

**Body:** Keep the documentation-audit methodology. **Drop `allowed-tools:` and `model: opus` frontmatter** (forbidden fields; model/tool scoping is not per-skill). `## References`: engineering-principles.

**Extract:** none.

**Line target:** ~150.

Apply template. Root source to delete: `documentation-audit/`.

---

## Task 36: 09-operate/handoff

**Sources:**
- `archive/upstream-mattpocock/skills/productivity/handoff/SKILL.md`
- `archive/upstream-mattpocock/skills/in-progress/claude-handoff/SKILL.md`

**Files:** Create `09-operate/handoff/SKILL.md`

**Frontmatter:**
```yaml
---
name: handoff
description: Use when handing off work to another session or agent. Produces a structured handoff brief capturing context, decisions, and next steps. Triggers on "handoff".
disable-model-invocation: true
---
```

**Body:** Merge matt's `handoff` (productivity) and `claude-handoff` (in-progress) — near-duplicates, pick the richer content. `## References`: engineering-principles. Drop `argument-hint:` frontmatter (forbidden).

**Extract:** none.

**Line target:** ~40.

Apply template. No root source to delete.

---

## Task 37: Root README.md (9-phase catalog)

**Files:** Create `README.md` at repo root.

**Interfaces:**
- Produces: the catalog index linking all 33 skills. Used by humans and the using-skills router for discovery.

- [ ] **Step 1: Write `README.md`**

Content — a 9-phase table (each row: phase name + the skills in it with one-line descriptions + their path), then conventions summary and the validator command. Structure:

```markdown
# Skills

A unified collection of 33 agent skills organized by the software development lifecycle.
Each skill is a lean workflow; shared engineering discipline lives in references/.

## Catalog

| Phase | Skills |
|---|---|
| meta | using-skills — route a task to the right skill |
| 01-product | brainstorm, spec, oss-strategy |
| 02-research | research, market-research, tech-selection |
| 03-design | architecture, domain-modeling, api-design, codebase-design, frontend-design, prototype |
| 04-develop | implement, breakdown, context-engineering |
| 05-tune | performance, simplify |
| 06-test | tdd, test-generation, api-testing, e2e-testing |
| 07-verify | code-review, debugging, security-review |
| 08-ship | shipping, git-workflow, ci-cd, deprecation-migration, oss-polish |
| 09-operate | observability, documentation-audit, handoff |

(Expand each skill name into a row with path + one-line description from its frontmatter.)

## Conventions
- Every skill: SKILL.md (uppercase), frontmatter name+description (+optional disable-model-invocation).
- Every skill links references/engineering-principles.md.
- Planning uses Claude Code's built-in plan mode.
- Validate: `bash scripts/validate-skills.sh`

## Archive
archive/upstream-addyosmani/ and archive/upstream-mattpocock/ hold the original source
repos (read-only) for provenance.
```

Write the full expanded table (each skill as its own row with `<phase>/<skill>` path + the description line from its frontmatter).

- [ ] **Step 2: Verify all 33 skill descriptions are represented**

```bash
cd "C:/Users/int2t/Desktop/skills"
# Count skills referenced in README vs actual
grep -c 'SKILL.md' README.md  # should be 33 (or count skill-name rows)
```

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/int2t/Desktop/skills"
git add README.md
git commit -m "feat: root README catalog of 33 skills"
```

---

## Task 38: Final verify + archive integrity

**Files:** none (verification only, plus a final commit if any stray files remain).

- [ ] **Step 1: Run the full validator — expect 33 skills, 0 errors**

```bash
cd "C:/Users/int2t/Desktop/skills"
bash scripts/validate-skills.sh
```
Expected: `Skills found: 33 (expected 33)` and `Total errors: 0`, exit code 0.

- [ ] **Step 2: Audit overlap — no two skills share a core function**

Skim the 33 `## When to use` sections. Confirm each skill has a distinct trigger domain. Spot-check the high-risk clusters: only one TDD skill (`06-test/tdd`), one brainstorm (`01-product/brainstorm`), one frontend-design (`03-design/frontend-design`), one code-review (`07-verify/code-review`). If overlap found, revise the skill's When-to-use to narrow it.

- [ ] **Step 3: Verify no original root skill folders remain (except archive/ and the new structure)**

```bash
cd "C:/Users/int2t/Desktop/skills"
# List top-level dirs; should be: archive, docs, meta, references, scripts, 01-09 phases, plus README/CLAUDE.md/.gitignore
ls -1d */ | grep -vE '^(archive|docs|meta|references|scripts|[0-9]{2}-)/'
```
Expected: empty output (no stray root skill folders).

- [ ] **Step 4: Verify archive integrity**

```bash
cd "C:/Users/int2t/Desktop/skills"
test -d archive/upstream-addyosmani/skills && echo "addy archive OK"
test -d archive/upstream-mattpocock/skills && echo "matt archive OK"
cd archive/upstream-addyosmani && git log --oneline -1 2>/dev/null && echo "addy git intact"
cd ../upstream-mattpocock && git log --oneline -1 2>/dev/null && echo "matt git intact"
```

- [ ] **Step 5: Verify every skill links engineering-principles (validator already checks, but spot-confirm path resolves)**

```bash
cd "C:/Users/int2t/Desktop/skills"
# Pick one skill from a deep path and confirm the relative link resolves
test -f 03-design/frontend-design/references/palettes.md && echo "progressive-disclosure OK"
grep -l 'engineering-principles' 01-product/*/SKILL.md | head -1
```

- [ ] **Step 6: Final commit (any remaining untracked files) + done**

```bash
cd "C:/Users/int2t/Desktop/skills"
git add -A
git status --porcelain  # should be empty or only intentional files
git commit -m "refactor: complete skills archive consolidation (83 -> 33)" 2>/dev/null || echo "nothing to commit — clean"
```

---

## Self-Review Notes (run after writing, before handoff)

**Spec coverage:** Every item in spec §5 roster (33 skills) maps to a task (Tasks 4-36). Spec §5.1 discarded skills: clean-code/mermaid-diagrams → Task 2 references; wait-what → engineering-principles §2; writing-for-agents → skill-anatomy; github-topics/repo-story-time → Task 33 (oss-polish). Spec §7 principles → Task 2 engineering-principles. Spec §6 schema → validator (Task 1) + skill-anatomy (Task 2). Spec §8 stages → Tasks 1-38. Spec §9 git init → Task 1. Spec §10 resolved decisions → reflected (git in Task 1; oss-polish in Task 33). ✓

**Placeholder scan:** No "TBD/TODO". Each skill task has concrete frontmatter (name+description written out), exact source paths, exact target path, refs to extract, line target, and the 5-step template. Body-prose synthesis is specified by per-skill merge notes (concrete merge intent, not placeholder). ✓

**Type consistency:** Skill names match across roster, frontmatter, task headings, and README. Paths consistent (`<phase>/<skill-name>/SKILL.md`). Relative link depth: phase skills use `../../references/...`; meta uses `../references/...` (noted in Task 4). ✓

---

*Plan complete. Execution handoff below.*
