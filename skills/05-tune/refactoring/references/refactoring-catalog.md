# Refactoring Move Catalog

Loaded on demand by `05-tune/refactoring/SKILL.md`. Triggers, before→after examples,
and characterization-test guidance for each move in the catalog.

## Contents

- [Extract](#extract)
- [Move](#move)
- [Split](#split)
- [Merge](#merge)
- [Change dependency](#change-dependency)
- [Characterization tests](#characterization-tests)

## Extract

**When to apply.** A function or class does two distinct jobs, or a cohesive responsibility
is buried inline where callers can't reach it. Smells: long method, mixed responsibilities.

```ts
// Before — pricing logic buried in checkout
function checkout(cart: Cart, customer: Customer): Receipt {
  const subtotal = cart.items.reduce((s, i) => s + i.price * i.qty, 0);
  const discount = customer.isMember ? subtotal * 0.1 : 0;
  const tax = (subtotal - discount) * TAX_RATE;
  return { subtotal, discount, tax, total: subtotal - discount + tax };
}
// After — extracted; checkout delegates (priceOrder has the same body, now isolated)
function checkout(cart: Cart, c: Customer): Receipt { return priceOrder(cart, c); }
function priceOrder(cart: Cart, c: Customer): Receipt { /* ...same body, now testable */ }
```

**Characterization test guidance.** Pin `checkout` outputs across member/non-member,
empty cart, single item, bulk — before the move. Same assertions must pass unmodified
after extraction. Direct tests on `priceOrder` come after; `checkout` suite is the net.

## Move

**When to apply.** A method reaches across to another module's data more than its own
(Feature Envy at the structure level). Smell: reads five fields from `B`, one from `A`.

```ts
// Before — Invoice formats itself using Customer's data
class Invoice {
  constructor(private customer: Customer, private amount: number) {}
  label(): string {
    return `${this.customer.fullName} — ${this.customer.region} — $${this.amount}`;
  }
}
// After — Customer owns its label; Invoice delegates
class Invoice {
  constructor(private customer: Customer, private amount: number) {}
  label(): string { return `${this.customer.shippingLabel()} — $${this.amount}`; }
}
class Customer {
  shippingLabel(): string { return `${this.fullName} — ${this.region}`; }
}
```

**Characterization test guidance.** Pin `Invoice.label()` outputs for every customer
variant (region, name length, empty fields). After the move, same outputs must hold —
the label string is the behavior surface, wherever the parts come from.

## Split

**When to apply.** A module exceeds ~300 lines of real logic, or co-locates unrelated
responsibilities. Smell: importing across six packages, changed for four unrelated
reasons. Split along a clean seam.

```ts
// Before — UserService handles persistence, email, and permissions
class UserService {
  create(user: User): void { /* save to db */ }
  notify(user: User, msg: string): void { /* send email */ }
  canAccess(user: User, res: string): boolean { /* check role */ }
}
// After — split along the persistence / notification / authz seam
class UserRepository { create(user: User): void { /* save to db */ } }
class Notifier { send(user: User, msg: string): void { /* send email */ } }
class AccessPolicy { canAccess(user: User, res: string): boolean { /* check role */ } }
```

**Characterization test guidance.** Pin every public method before the split. After,
callers use three smaller classes; same effects must hold. Golden master catches drift.

## Merge

**When to apply.** Two or more units implement near-identical logic with drift —
bug-fixed-in-one-not-the-other. Signal: <10% structural difference, diverged copy-paste.

```ts
// Before — two near-identical formatters; EUR forgot negative handling (drifted)
function formatPriceUSD(n: number): string {
  if (n < 0) return `-$${(-n).toFixed(2)}`;
  return `$${n.toFixed(2)}`;
}
function formatPriceEUR(n: number): string { return `€${n.toFixed(2)}`; }
// After — one canonical formatter; currency is a parameter
function formatMoney(amount: number, symbol: string): string {
  const sign = amount < 0 ? "-" : "";
  return `${sign}${symbol}${Math.abs(amount).toFixed(2)}`;
}
```

**Characterization test guidance.** Pin **both** formatters' outputs across the same
input set (positive, zero, negative, large, fractional). Where they diverged (negative
EUR), the pre-pin exposes it — pick correct behavior as a **separate** change, not in
the merge.

## Change dependency

**When to apply.** A high-level module imports a concrete low-level dependency, blocking
test or swap. Smells: can't unit-test `A` without `B`'s database. Invert the direction.

```ts
// Before — ReportLoader depends on concrete FileSystem; untestable without disk
class ReportLoader {
  constructor(private fs: FileSystem) {}
  load(name: string): string { return this.fs.readFile(`reports/${name}.txt`); }
}
// After — depends on a port; concrete adapter is injected
interface ReadStore { read(path: string): string; }
class ReportLoader {
  constructor(private store: ReadStore) {}
  load(name: string): string { return this.store.read(`reports/${name}.txt`); }
}
class FileSystemStore implements ReadStore {
  constructor(private fs: FileSystem) {}
  read(p: string): string { return this.fs.readFile(p); }
}
```

**Characterization test guidance.** Pin `ReportLoader.load` outputs for a set of report
names using the real `FileSystem` before inversion. After, same outputs must hold when
`FileSystemStore` is injected. A `FakeStore` is new coverage, not preservation.

## Characterization tests

**What they are.** Tests that pin current behavior — inputs → observed outputs — without
claiming the behavior is correct. If the refactor changes behavior, the test goes red.
You pin what the code *does* do, not what it *should* do.

**When to write them.** Always, when the existing suite is thin in the area you're about
to touch. If coverage of the target path is weak, add characterization tests before any
structural move (SKILL.md step 1).

**Three patterns.**

- **Golden master.** Feed a fixed input set through the target; capture outputs to a
  snapshot. Re-run and diff — any change is behavior shift. Best for many inputs.
- **Approval test.** Tool-supported: the framework diffs a serialized form (string, JSON,
  HTML) and prompts approve or reject. Good for complex outputs where hand-assertions
  are impractical.
- **Coverage check.** Run the suite with coverage on the target. If the lines you're about
  to move are uncovered, add targeted tests until they are. Minimum bar, not gold standard.

**Concrete example — pinning before a risky extract.**

```ts
// Extracting `priceOrder` from `checkout`. Only single-item member cart tested. Pin first:
describe("checkout (characterization — pins current behavior)", () => {
  const cases: Array<[Cart, Customer, number]> = [
    [singleItemCart(), member(), 90],
    [singleItemCart(), nonMember(), 100],
    [bulkCart(5), member(), 450],
    [emptyCart(), member(), 0],
    [singleItemCart(), memberInRegion("EU"), 90],  // pin whatever the tax is
  ];
  it.each(cases)("total matches pinned value", (cart, customer, expected) => {
    expect(checkout(cart, customer).total).toBe(expected);
  });
});
// Encodes CURRENT behavior — bugs included. Suspected bug? File it; don't fix
// inside the refactor. Assertions hold before and after; that's the contract.
```

After the move, run this suite unmodified. Any red means behavior shifted — revert the
step. Tests modified to pass mean behavior changed (a red flag in SKILL.md).

- See [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md §9](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — behavior-preserving change discipline: incremental test-pinned steps, separate refactor from feature work, Rule of 500, each step independently revertible.
