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
