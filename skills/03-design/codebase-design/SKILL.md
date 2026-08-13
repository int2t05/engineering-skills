---
name: codebase-design
description: Use when designing deep modules, finding refactoring or deepening opportunities, or making a codebase more testable and AI-navigable. Presents deepening opportunities and works through the one you pick. Triggers on "deep modules", "refactor architecture", "deepening", "深化模块", "重构架构", "代码库设计".
---

# Codebase Design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam,
testable through that interface. Leverage for callers, locality for maintainers, testability for
everyone. This skill merges the deep-module vocabulary with a scan-and-grill workflow: surface
architectural friction as deepening opportunities, present them as a visual HTML report, then grill
through the one the user picks.

## When to use

- Designing a new module or restructuring an existing one — deciding where a seam goes, what hides behind it
- Finding refactoring or deepening opportunities across a codebase
- Making a codebase more testable or AI-navigable
- Consolidating tightly-coupled shallow modules into one deep module
- Triggers on "deep module", "seam", "refactoring opportunity", "架构改进", "模块设计", "deepening", "深化模块", "重构架构", "代码库设计"

**Not for:** code-level naming or function-extraction without architectural intent (use
`simplify`); greenfield system architecture (use `architecture`); feature-level API contracts (use
`api-design`).

## Steps

### 1. Scan for deepening opportunities

Read the project's domain glossary (`CONTEXT.md`) and any ADRs in the area you're touching first —
the domain language names good seams; ADRs record decisions not to re-litigate.

Scope before you scan — put weight on parts of the codebase that have recently changed. If the user
named a direction, take it. Otherwise walk the commit history (`git log --oneline`) to find hot
spots, then explore those paths first.

Spawn an `Explore` sub-agent to walk the codebase and note friction: where understanding one
concept requires bouncing between many small modules; where modules are **shallow** (interface
nearly as complex as the implementation); where pure functions were extracted just for testability
but bugs hide in how they're called; where tightly-coupled modules leak across seams; where code
is untested or hard to test through its current interface.

Apply the **deletion test** to anything suspect: would deleting it concentrate complexity, or just
move it? "Concentrates" is the signal.

- Load [references/language.md](references/language.md) for the glossary (module, interface, depth, seam, adapter, leverage, locality) and principles
- Load [references/deepening.md](references/deepening.md) for dependency categories and the replace-don't-layer testing strategy

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory (resolve from `$TMPDIR`, fall back to
`/tmp` or `%TEMP%`), at `<tmpdir>/architecture-review-<timestamp>.html`. Open it for the user
(`xdg-open` / `open` / `start`) and tell them the absolute path.

Each candidate is a card: Files, Problem, Solution, Benefits (in terms of locality and leverage),
a before/after visualisation, and a recommendation-strength badge (`Strong` / `Worth exploring` /
`Speculative`). End with a Top Recommendation section. Use CONTEXT.md vocabulary for the domain and
the glossary for the architecture — if CONTEXT.md defines "Order," say "the Order intake module,"
not "the FooBarHandler."

If a candidate contradicts an existing ADR, only surface it when the friction warrants reopening
the ADR; mark it clearly in the card.

- Load [references/html-report.md](references/html-report.md) for the full HTML scaffold, diagram patterns, and styling guidance

Do NOT propose interfaces yet. After the file is written, ask: "Which of these would you like to
explore?"

### 3. Grill through the chosen candidate

Once the user picks a candidate, walk the design tree: constraints, dependencies, the shape of the
deepened module, what sits behind the seam, what tests survive. Side effects happen inline as
decisions crystallize:

- Naming a deepened module after a concept not in `CONTEXT.md`? Add the term to `CONTEXT.md` (create it lazily if needed).
- Sharpening a fuzzy term? Update `CONTEXT.md` right there.
- User rejects the candidate with a load-bearing reason? Offer an ADR so future reviews don't re-suggest it.
- Want to explore alternative interfaces? Run the design-it-twice parallel sub-agent pattern.

- Load [references/interface-design.md](references/interface-design.md) for interface design criteria: depth, testability rules, seam placement
- Load [references/design-it-twice.md](references/design-it-twice.md) for the parallel sub-agent pattern when exploring alternative interfaces

**Output:** `docs/design/codebase-audit.md` — the deepening opportunities found (candidates with
problem/solution/benefit/strength), the one chosen, and the grilled result (defined interface, seam
placement, testing strategy). The HTML report (Step 2) is the visual presentation; this md is the
durable record that survives the temp file.

## Verify

- [ ] HTML report written to temp dir and opened for the user; absolute path communicated
- [ ] Every candidate card has Files, Problem, Solution, Benefits, before/after diagram, strength badge
- [ ] Glossary terms used exactly (module, interface, depth, seam, adapter) — no drift to "component," "service," "API," "boundary"
- [ ] Domain vocabulary from CONTEXT.md used for module names, not raw type names
- [ ] ADR conflicts flagged only when the friction warrants reopening
- [ ] After grilling: the chosen candidate has a defined interface, a seam placement, and a testing strategy

**Red flags:** proposing interfaces during the scan; listing every theoretical refactor an ADR
forbids; drifting to "component"/"service"/"API"/"boundary"; skipping the deletion test.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, push back, verify don't assume)
- [references/language.md](references/language.md) — glossary: module, interface, implementation, depth, seam, adapter, leverage, locality + principles (deletion test, interface is the test surface, one vs two adapters)
- [references/deepening.md](references/deepening.md) — dependency categories (in-process, local-substitutable, ports & adapters, mock), seam discipline, replace-don't-layer testing
- [references/html-report.md](references/html-report.md) — HTML scaffold, Tailwind/Mermaid via CDN, diagram patterns (mass, cross-section, call-graph collapse), tone and glossary usage
- [references/interface-design.md](references/interface-design.md) — interface design criteria: what an interface includes, depth, testability rules, comparing alternatives
- [references/design-it-twice.md](references/design-it-twice.md) — parallel sub-agent pattern for exploring alternative interfaces (Ousterhout's "Design It Twice")
