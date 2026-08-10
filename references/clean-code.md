# Clean Code

Coding discipline from Robert C. Martin's "Clean Code." Loaded on demand by `implement`,
`simplify`, `code-review`, and `tdd`. Transform "code that works" into "code that is clean."

> "Code is clean if it can be read, and enhanced by a developer other than its original author." — Grady Booch

## 1. Meaningful Names
- **Intention-revealing**: `elapsedTimeInDays` not `d`.
- **No disinformation**: don't call it `accountList` if it's a `Map`.
- **Meaningful distinctions**: avoid `ProductData` vs `ProductInfo`.
- **Pronounceable/searchable**: avoid `genymdhms`.
- **Class names**: nouns (`Customer`, `WikiPage`); avoid `Manager`, `Data`.
- **Method names**: verbs (`postPayment`, `deletePage`).

## 2. Functions
- **Small** — smaller than you think.
- **Do one thing** — and do it well.
- **One level of abstraction** — don't mix business logic with low-level details like regex.
- **Descriptive names** — `isPasswordValid` beats `check`.
- **Arguments** — 0 ideal, 1-2 okay, 3+ needs strong justification.
- **No side effects** — don't secretly mutate global state.

## 3. Comments
- **Don't comment bad code — rewrite it.** Most comments signal a failure to express intent in code.
- **Explain in code**: `if employee.isEligibleForFullBenefits():` beats a comment explaining flags.
- **Good comments**: legal, informative (regex intent), clarification (external libs), TODOs.
- **Bad comments**: mumbling, redundant, misleading, mandated, noise, position markers.

## 4. Formatting
- **Newspaper metaphor**: high-level at top, details at bottom.
- **Vertical density**: related lines stay close.
- **Distance**: declare variables near their usage.
- **Indentation**: essential for structural readability.

## 5. Objects and Data Structures
- **Data abstraction**: hide implementation behind interfaces.
- **Law of Demeter**: don't reach through objects — avoid `a.getB().getC().doSomething()`.
- **DTOs**: public data, no behavior.

## 6. Error Handling
- **Exceptions over return codes** — keeps logic clean.
- **Write try-catch-finally first** — defines the operation's scope.
- **Don't return null** — forces every caller to check.
- **Don't pass null** — invites `NullPointerException`.

## 7. Unit Tests
- **Three Laws of TDD**:
  1. No production code until a failing unit test exists.
  2. No more test than sufficient to fail.
  3. No more production code than sufficient to pass.
- **F.I.R.S.T.**: Fast, Independent, Repeatable, Self-validating, Timely.

## 8. Classes
- **Small** — single responsibility (SRP).
- **Stepdown rule** — code reads like a top-down narrative.

## 9. Smells and Heuristics
- **Rigidity** — hard to change.
- **Fragility** — breaks in many places.
- **Immobility** — hard to reuse.
- **Viscosity** — hard to do the right thing.
- Needless complexity; needless repetition.

## Checklist
- [ ] Function under 20 lines?
- [ ] Does exactly one thing?
- [ ] Names searchable and intention-revealing?
- [ ] Avoided comments by making code clearer?
- [ ] Too many arguments?
- [ ] Failing test for this change?
