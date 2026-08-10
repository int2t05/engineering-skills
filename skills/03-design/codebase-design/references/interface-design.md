# Interface Design

Criteria for designing and evaluating a module's interface. Use with
[design-it-twice.md](design-it-twice.md) when exploring alternative interfaces. Assumes the
vocabulary in [language.md](language.md) — **module**, **interface**, **seam**, **adapter**,
**leverage**.

## What an interface includes

Everything a caller must know to use the module correctly — not just the type signature:

- Types, methods, parameters
- Invariants the caller must respect
- Ordering constraints (call A before B)
- Error modes and failure semantics
- Required configuration
- Performance characteristics

If a caller needs to know it, it is part of the interface, even if it is not expressed in the type
system.

## Depth: the design goal

A module is **deep** when a large amount of behaviour sits behind a small interface. A module is
**shallow** when the interface is nearly as complex as the implementation.

When designing an interface, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

**Deletion test:** imagine deleting the module. If complexity vanishes, it was a pass-through. If
complexity reappears across N callers, it was earning its keep.

## Designing for testability

Good interfaces make testing natural — the interface is the test surface.

1. **Accept dependencies, don't create them.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Small surface area.** Fewer methods = fewer tests needed. Fewer params = simpler test setup.

If you want to test *past* the interface, the module is probably the wrong shape.

## Comparing alternative interfaces

When evaluating designs produced by [design-it-twice.md](design-it-twice.md), contrast them on:

- **Depth** — leverage at the interface. Which design hides the most behaviour behind the smallest
  surface?
- **Locality** — where does change concentrate? Which design keeps bugs, knowledge, and
  verification in one place?
- **Seam placement** — where does the interface live? Does the seam sit at a natural boundary in
  the dependency graph?

Be opinionated. Give a recommendation: which design is strongest and why. If elements from
different designs would combine well, propose a hybrid. The user wants a strong read, not a menu.
