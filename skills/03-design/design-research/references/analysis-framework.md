# Analysis Framework

How to analyze each retrieved reference and synthesize the reference board. Two layers: the
**extraction axes** (what to pull from each reference, feeding downstream skills) and the
**analysis lenses** (deeper pattern reading). Then three **output frameworks** for the final board.

Adapted from established UX-research synthesis practice (the 8-lens structure originates in the
`ddruids/mobbin-skill` framework, MIT). The lenses analyze the design itself and are source-agnostic;
the extraction axes are tuned to what `imagegen` and `frontend-design` consume.

## Contents

- [Extraction axes (per reference)](#extraction-axes-per-reference)
- [The 8 analysis lenses](#the-8-analysis-lenses)
- [Three output frameworks](#three-output-frameworks)
- [Synthesis rules](#synthesis-rules)

## Extraction axes (per reference)

For each reference, extract these six axes — as **text description**, not pixel measurement
(WebFetch returns markdown, not the screenshot). These map directly to what `imagegen` Step 4 and
`frontend-design` Step 2 need:

| Axis | What to describe | Feeds |
|---|---|---|
| **Layout rhythm** | Section order, density pacing, where the page breathes vs compresses | imagegen section-count + composition anchors |
| **Grid** | Column structure, alignment logic, symmetry vs asymmetry, off-grid elements | frontend-design layout; imagegen visual-direction §3 |
| **Spacing** | Generous vs tight; breathing room around key elements; section gaps | frontend-design design-tokens scale |
| **Type scale** | Display vs body contrast; weight hierarchy; how many type sizes; serif/sans pairing | frontend-design font-pairings; imagegen hero minimalism |
| **Visual density** | Minimal vs rich; layering depth; how much fits per screen | imagegen hero-scale (giant/mid/mini) |
| **Accent-color logic** | Where the single accent lands (CTA? one word? icon?); how it recurs; palette restraint | frontend-design palettes (60/30/10); imagegen anti-slop |

Write 2-4 sentences per axis per reference. Concrete and specific — "single coral accent on the
CTA and one stat number, nowhere else" beats "good use of color".

## The 8 analysis lenses

Deeper reading of each reference, beyond the surface axes. Use 3-5 lenses per reference (not all 8
every time — pick the ones the reference rewards):

1. **Screen Moment** — What is the user doing/deciding at this moment? What does the screen optimize for (clarity? trust? speed? delight)?
2. **User Job** — What job is the user hiring this screen/flow to do? What friction does it remove?
3. **Information Hierarchy** — What leads? What's secondary? What's hidden until needed? How does the eye travel?
4. **Trust Mechanism** — Where does the design build trust (testimonials? logos? security badges? social proof? calm restraint)? fintech/health lean heavily here.
5. **Action Model** — What's the primary action? How unmistakable is it? Are secondary actions deferring or competing?
6. **Progressive Disclosure** — What's shown first vs revealed later? How does the design avoid front-loading complexity?
7. **Recovery** — How does it handle the empty/error/loading state? Does it guide the user back to a good state?
8. **Reusable Pattern** — What specific pattern here is worth lifting (a component shape, a layout move, a trust signal placement)? Name it concretely.

## Three output frameworks

Choose by intent (stated in Step 1 of the skill). Default to A.

### A. Reference Board (default — feeds imagegen/frontend-design)

Use when the intent is grounding downstream design work. The standard `docs/design/references.md`
shape:

```markdown
# Design Reference Board — <brief>

## Brief
<domain, surface, intent, target count>

## Sources queried
- Lapa Ninja /category/finance/ (12 candidates fetched)
- Pageflows onboarding-flow (8 candidates)
- ...

## References (curated 6)

### 1. <App/Site name> — <source URL>
![preview](<image URL>)
- **Layout rhythm:** ...
- **Grid:** ...
- **Spacing:** ...
- **Type scale:** ...
- **Visual density:** ...
- **Accent-color logic:** ...
- **Lenses:** Trust Mechanism, Action Model, Reusable Pattern
- **Feeds:** imagegen (art direction) / frontend-design (style) / image-to-code (sections)
- **Reusable pattern:** <concrete named pattern>

### 2. ...

## Pattern clusters
- **Cluster: <pattern name>** — <apps/sites exhibiting it> — <what they share>
- ...

## Load instruction
Load this file in `imagegen` Step 4 / `frontend-design` Step 2 / `image-to-code` Step 1.
```

### B. Competitive Comparison

Use when the intent is "how do different apps handle the same screen/flow":

```markdown
# Competitive Comparison — <screen/flow>

## Comparison table
| App | Pattern | Strength | Weakness | Reusable idea |
|---|---|---|---|---|
| Revolut | ... | ... | ... | ... |
| Wise | ... | ... | ... | ... |

## Winner analysis
<which handles it best, why>

## Recommendation
<what to take from each>
```

### C. Decision Log

Use when the intent is formalizing a design decision from the research:

```markdown
# Design Decision — <topic>

## Context / Problem
## Options considered (with references)
## Decision
## Rationale (which references support it)
## Consequences / tradeoffs
## Success metrics
```

## Synthesis rules

- **Every reference has a real source URL.** No URL, no entry — drop it.
- **Pattern clusters need ≥2 references.** A "pattern" from one example is an observation, not a pattern.
- **Name reusable patterns concretely.** "Trust-led hero with stat row" not "good hero design".
- **Tag the downstream skill.** Each reference states whether it feeds imagegen (art direction), frontend-design (style/tokens), or image-to-code (section plan) — so the consumer knows what to extract.
- **State the capability boundary when it bit.** If iOS per-screen depth or pixel precision was needed and unavailable, note it in the board's footer so the consumer calibrates expectations.
