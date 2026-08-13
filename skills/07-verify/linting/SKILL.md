---
name: linting
description: Use when fixing machine-detectable code issues — run linters and static analyzers (ESLint, Ruff, Clippy, golangci-lint), resolve findings, suppress false positives with justification, tighten config. Automated quality gate, distinct from human-judgment review. Triggers on "lint", "linting", "fix eslint", "static analysis", "lint 修复", "静态分析", "格式检查", "代码规范检查". Not for human-judgment code review (use code-review), runtime behavior bugs (use debugging), or behavior-preserving structural refactoring (use refactoring).
---

# Linting

Fix machine-detectable code issues — run the project's linters and static analyzers, resolve or
justifiably suppress findings, and tighten config so real issues surface and noise dies down. This
is the automated quality gate, not a substitute for human review.

## When to use

- Fixing a failing lint/static-analysis gate in CI or a pre-commit hook
- Tightening lint rules — turning on stricter rules, removing broad ignores, paying down `eslint-disable` debt
- Running static analysis (type checkers, security linters, complexity analyzers) and triaging findings
- Establishing lint config for a new project or after a toolchain migration
- Triggers on "lint", "linting", "fix eslint", "static analysis", "lint 修复", "静态分析", "格式检查", "代码规范检查"

**Not for:** human-judgment review of a diff — smells, spec faithfulness, design (use `code-review`); diagnosing runtime behavior bugs (use `debugging`); behavior-preserving structural moves like extracting or splitting modules (use `refactoring`).

## Steps

### 1. Detect the toolchain

Read the project before running anything. Don't impose a linter the project doesn't use.

- Find lint config and scripts: `package.json` (`lint` script, `eslint`/`biome`/`prettier` config), `pyproject.toml`/`setup.cfg` (`ruff`/`flake8`/`mypy`), `Cargo.toml` (`clippy`), `.golangci.yml`, `.editorconfig`.
- Find the CI gate — what command does CI actually run? Lint locally with the same command, or you'll fix issues CI doesn't see and miss issues CI blocks on.
- If no toolchain exists, ask before introducing one — adding a linter is a project decision, not a drive-by.

### 2. Run and capture all findings

Run the linter/analyzer and capture the full output. Don't fix as you go — get the complete picture
first so you can triage by category, not react to the first error.

- Run with the project's configured command. For a first pass, also run with `--max-warnings 0` (or equivalent) so warnings don't slip past.
- Capture the raw output; note the rule code for every finding (e.g. `@typescript-eslint/no-explicit-any`, `F401`, `E501`). The rule code is how you triage and how you suppress.

### 3. Triage — fix, suppress, or tighten

Sort every finding into one of three buckets. Never blanket-silence (`eslint-disable *`, `# noqa: noqa`, broad `ignorePatterns`) — that's the failure mode this skill exists to prevent.

- **Fix** — the finding is real. Fix the code. This is the default; most findings are real.
- **Suppress with reason** — the finding is a false positive or an intentional, justified exception. Suppress at the narrowest scope (inline, not file-level) and write the reason in the suppression comment. A suppression without a reason is noise that hides future real issues.
- **Tighten config** — the same noisy false positive recurs across the codebase. Rather than suppress everywhere, adjust the rule config (narrow its scope, set a threshold) so it fires only on real cases. This pays down the noise permanently.

If a finding is real but fixing it now is too risky (large behavior-touching change), suppress *with a TODO and a reason* and file it — don't silently disable.

### 4. Fix incrementally — re-run after each batch

Fix by rule category, not file-by-file at random. Resolving all `no-unused-vars` together is
reviewable; mixing five rule fixes into one change is not. Re-run the linter after each batch to
confirm the category is clear before moving on.

- Fix a category → re-run → clean for that category → next category.
- If a fix triggers new findings (common when tightening types), resolve those before moving on — don't leave the tree noisier than you found it.

### 5. Verify clean and config improved

- Full lint run is clean (or only justified suppressions remain).
- Every suppression carries a reason. No blanket silences, no file-level disables without justification.
- Config is tighter than before — recurring noise addressed at the config level, not suppressed ad hoc.
- The fix command matches what CI runs.

## Verify

- [ ] Lint/static-analysis run is clean — no unresolved findings, or only narrow suppressions with reasons
- [ ] Every suppression has a written reason; no blanket silences (`eslint-disable *`, `# noqa: noqa`, broad ignores)
- [ ] Config tightened where noise recurred — recurring false positives fixed at the rule level, not suppressed everywhere
- [ ] Local fix command matches the CI gate command
- [ ] Fixes grouped by rule category, each batch re-run clean before moving on
- [ ] No behavior change introduced by fixes (if a lint fix requires behavior change, it's suppressed with TODO + filed, not forced)

**Red flags:** blanket-disabling a rule to make the gate pass; file-level or project-level suppressions without reasons; fixing lint findings by editing the lint config to permit the smell; introducing a linter the project doesn't use without asking; a "lint fix" PR that also changes behavior; leaving the tree with more findings than it started because a fix triggered new ones.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, fix root causes not symptoms, surgical scope)
