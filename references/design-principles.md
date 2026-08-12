# Design Principles

Recurring discipline for every UIUX skill in this collection (frontend-design, image-to-code,
imagegen-web, imagegen-mobile, brandkit, prototype). Each skill links this file rather than repeating
these rules. Apply them at all times — they sit alongside engineering-principles.md, not instead of it.

## 1. CRAP: Contrast, Repetition, Alignment, Proximity
Different things must look different (contrast); same things must look the same (repetition); elements
align along invisible lines (alignment); related elements sit close, unrelated far (proximity). These
four — Robin Williams' Non-Designer's Design Book — are the root of all visual organization. Every
layout decision traces back to one of them.

## 2. Hierarchy before decoration
Establish hierarchy via size, contrast, spacing, and position — never via decoration alone. The squint
test: blur your eyes; if you can still distinguish the primary from the secondary, hierarchy holds. The
5-second test: flash it to someone; can they name the main action? If hierarchy fails these, color and
ornament cannot rescue it.

## 3. Minimize cognitive load
More choices means slower decisions (Hick's Law). Progressive-disclose advanced options behind a toggle;
chunk long forms into steps; pre-fill defaults; remove distractions. Three load types — intrinsic (the
task is hard), extraneous (your interface adds friction), germane (learning). Kill extraneous; you
cannot remove intrinsic, only decide who bears it.

## 4. Design every state
Loading, error, empty, and partial — every interface hits all four. Skeleton screens beat spinners
(they show structure, not just "wait"). Empty states explain why empty and guide to the next action,
never just "No data." Errors state the cause in plain language and offer an actionable next step. A
screen designed only for the happy path is unfinished.

## 5. Accessibility is non-optional
WCAG 2.1 AA is the floor, not the ceiling: text contrast ≥ 4.5:1, large text ≥ 3:1, full keyboard
operability, visible focus, alt text on images. Accessibility is not a phase or a checklist bolted on at
the end — it is a constraint on every component decision. Target Lighthouse a11y ≥ 90; treat regressions
as bugs.

## 6. Consistency comes from systems, not hand-tuning
Token tiers — atomic (raw values) → semantic (role references) → component (component-scoped). Change an
atomic token and every dependent color shifts; hand-tuning hex per component creates drift you cannot
audit. Components reference semantic tokens, never raw values. The system enforces consistency; individual
judgment does not scale.

## 7. Mobile first, content out
Start from the smallest screen and the core content, then enhance outward. Responsive design is
progressive enhancement — add capability as space allows — not a desktop design shrunk to fit. Breakpoints
(sm 640 / md 768 / lg 1024 / xl 1280) define where layout adapts; the content-first baseline works below
all of them.

## 8. Recognize rather than recall
Show options and state visibly; don't force users to remember commands, labels, or prior steps. Visible
choices beat memorized ones (Nielsen #6). The interface carries the memory of what's possible — the
user's attention stays on their task, not on reconstructing the system's state.
