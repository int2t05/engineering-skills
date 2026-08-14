---
name: a11y-review
description: Use when reviewing changes for accessibility — WCAG conformance, axe-core findings, keyboard and screen-reader support, contrast. Triggers on "accessibility", "a11y", "WCAG", "screen reader", "无障碍", "可访问性". Not for general code quality (use code-review), machine-detectable lint (use linting), or runtime behavior bugs (use debugging).
---

# Accessibility Review

Accessibility is a verify-phase audit, the same shape as `security-review`: define the
conformance target, run the automated layer, walk the manual checks, triage each finding
to fix or accept-with-rationale. Automated tools (axe-core) catch ~30–40% of issues; the
rest require a keyboard and screen-reader walkthrough. A page that passes axe but fails
keyboard nav is not accessible.

## When to use

- Reviewing a UI change (new page, component, form, interaction) before merge.
- A feature touches focus order, dynamic content, media, or color-only signaling.
- Hitting a conformance requirement (WCAG 2.1/2.2 AA is the legal/commercial default; AA is the target here unless stated).
- An automated a11y scan (axe, Lighthouse) surfaced findings to triage.

**Not for:** general code-quality review (use `code-review`); machine-detectable lint/style (use `linting`); runtime behavior bugs (use `debugging`). a11y-review is the human-judgment + tool-assisted audit layer.

## Steps

### 1. Confirm the conformance target and scope

WCAG 2.2 AA is the default (covers 2.1 AA + new criteria). AAA is opt-in and only for specific surfaces. Scope: which pages/components are in this review? A full-site audit is different from a single-PR review — state the boundary.

### 2. Run the automated layer

axe-core (or Lighthouse a11y audit) catches the machine-detectable class: missing alt text, empty buttons, insufficient contrast (ratio < 4.5:1 for text), duplicate IDs, missing form labels, invalid ARIA roles. Run it against the rendered DOM, not the source — client-rendered content needs a real browser. Capture every finding with its rule ID.

### 3. Walk the manual WCAG checks

Automated tools miss the structural and interaction issues. Check per page/component — see [references/wcag-checklist.md](references/wcag-checklist.md) for the criterion-by-criterion list. The high-value manual checks:

- **Keyboard** — every interactive element reachable in logical order via Tab; no keyboard traps; visible focus indicator on every focusable element.
- **Focus management** — route changes and modal opens move focus; modals trap focus correctly and return it on close.
- **Heading order** — `<h1>`→`<h2>`→`<h3>` without skipping levels; one `<h1>` per view.
- **Color independence** — information isn't conveyed by color alone (error states have text/icon, not just red); links are distinguishable beyond color.
- **Dynamic content** — `aria-live` regions announce updates; loading and error states are perceivable by AT.
- **Media** — images have alt (decorative = `alt=""`); video has captions; audio has transcript.

### 4. Keyboard + screen-reader walkthrough

Navigate the flow with the keyboard only (no mouse). Then run a screen-reader (NVDA/VoiceOver) through the critical path: land in the page, find the main content, complete the primary task, perceive errors and confirmations. This catches what axe can't: reading order vs visual order, landmark navigation, live-region announcements, form-error association.

### 5. Triage — fix or accept with rationale

Each finding is either **fix** (the default for AA-level issues) or **accept with a documented rationale** (AAA, or a genuine constraint with a mitigation). Record the WCAG criterion, severity, and the fix or rationale per finding — never silently drop a finding.

## Red flags

- A PR adding interactive UI with no keyboard-focus test; modals that don't trap or return focus; `div`/`span` used as a button without `role` and `tabindex`; error states signaled by color alone; `aria-live` missing on dynamic updates; images with meaningful content marked `alt=""`; a contrast ratio just under 4.5:1 left "because it looks fine"; automated scan green but no manual keyboard walkthrough done.

**Output:** `docs/a11y-report.md` — findings by WCAG criterion / axe rule, severity, and the fix or accept rationale per finding. Mirrors `docs/security-report.md`.

## Verify

- [ ] Conformance target stated (default WCAG 2.2 AA); scope boundary defined
- [ ] axe-core / Lighthouse run against rendered DOM; every finding captured with rule ID
- [ ] Full keyboard pass completed — every interactive element reachable, no traps, focus visible
- [ ] Focus management checked on route changes and modals (trap + return)
- [ ] Heading order has no skipped levels; one `<h1>` per view
- [ ] No information conveyed by color alone; links distinguishable beyond color
- [ ] Screen-reader walkthrough completed on the critical path
- [ ] Every finding triaged to fix or accept-with-rationale; none silently dropped
- [ ] `docs/a11y-report.md` produced with criterion, severity, and resolution per finding

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, surgical scope)
- [references/wcag-checklist.md](references/wcag-checklist.md) — WCAG 2.2 AA criterion-by-criterion checklist mapped to axe-core rules, with the manual checks automated tools miss
