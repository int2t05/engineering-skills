# Brief Inference and Design Dials

Read the brief before touching code. Most LLM design output is bad because the model
jumps to a default aesthetic instead of reading the room. This reference defines the
inference protocol and the three dials that gate every layout, motion, and density
decision.

## When to load this

Load when the brief is ambiguous or could go multiple aesthetic directions — to infer
the right design language before generating. Skip when the user has already pinned the
exact aesthetic and stack.

## The design read

Before any code, state in one line:

> "Reading this as: \<page kind> for \<audience>, with a \<vibe> language, leaning toward
> \<design system or aesthetic family>."

### Signals to read first

1. **Page kind** — landing (SaaS / consumer / agency / event), portfolio (dev / designer /
   studio), redesign (preserve vs overhaul), editorial / blog.
2. **Vibe words** the user used — "minimalist", "calm", "Linear-style", "Awwwards",
   "brutalist", "premium", "Apple-y", "playful", "serious B2B", "editorial", "glassy".
3. **Reference signals** — URLs linked, screenshots pasted, products named, competitors.
4. **Audience** — B2B procurement vs. design-conscious consumer vs. recruiter scanning a
   portfolio. The audience picks the aesthetic, not your taste.
5. **Brand assets that already exist** — logo, color, type, photography. For redesigns,
   these are starting material, not optional input.
6. **Quiet constraints** — accessibility-first audiences, public-sector, regulated
   industries, trust-first commerce, kids' products. These OVERRIDE aesthetic preference.

### If the brief is ambiguous

Ask **one** clarifying question — never a multi-question dump — and only when the design
read genuinely diverges. Example: *"Should this feel closer to Linear-clean or
Awwwards-experimental?"* If you can confidently infer from context, do not ask. Declare
the design read and proceed.

## The three dials

After the design read, set three dials. Every layout, motion, and density decision is
gated by these.

| Dial | Range | Baseline | Meaning |
|---|---|---|---|
| `DESIGN_VARIANCE` | 1–10 | 8 | 1 = perfect symmetry, 10 = artsy chaos |
| `MOTION_INTENSITY` | 1–10 | 6 | 1 = static, 10 = cinematic / physics |
| `VISUAL_DENSITY` | 1–10 | 4 | 1 = art gallery / airy, 10 = cockpit / packed |

Use the baseline unless the design read overrides. Overrides happen conversationally —
do not ask the user to edit configuration files.

### Dial inference (design read → dial values)

| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial / Linear-style" | 5–6 | 3–4 | 2–3 |
| "premium consumer / Apple-y / luxury / brand" | 7–8 | 5–7 | 3–4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9–10 | 8–10 | 3–4 |
| "landing page / portfolio / marketing site (default)" | 7–9 | 6–8 | 3–5 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3–4 | 2–3 | 4–5 |
| "redesign — preserve" | match existing | +1 | match existing |
| "redesign — overhaul" | +2 | +2 | match existing |

### Use-case presets

| Use case | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Landing (Premium consumer) | 7 | 6 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |
| Redesign — preserve | match | match+1 | match |
| Redesign — overhaul | +2 | +2 | match |

## Anti-default discipline

Do not default to: AI-purple gradients, centered hero over dark mesh, three equal feature
cards, generic glassmorphism on everything, infinite-loop micro-animations everywhere,
Inter + slate-900. These are the LLM defaults. Reach past them deliberately based on the
design read.

## Design system selection

Once you have the design read and dials, pick the right foundation. Do not invent CSS
for things that have an official package. Do not pretend an aesthetic trend is an official
system.

| Brief reads as… | Reach for | Why |
|---|---|---|
| Microsoft / enterprise SaaS / dashboards | Fluent UI | Official, Microsoft tokens, accessibility done |
| Google-ish UI, Material-flavored | Material Web + Material 3 tokens | Official, theme-able |
| IBM-style B2B / enterprise analytics | Carbon | Mature data-density patterns |
| Shopify app surfaces | Polaris | Required for Shopify admin UI |
| Atlassian / Jira-style product | Atlaskit + Atlassian tokens | Official |
| GitHub-style devtool | Primer CSS / Primer React Brand | Official; Brand for marketing |
| Public-sector UK service | GOV.UK Frontend | Legally expected |
| US public-sector / trust-first | USWDS | Same |
| Fast local-business / agency MVP | Bootstrap 5.3 | Boring, fast, works |
| Modern accessible React foundation | Radix Themes | Primitives + polished theme |
| Modern SaaS where you own the components | shadcn/ui | You own the code; never ship default state |
| Tailwind-based modern SaaS / AI marketing | Tailwind v4 utilities | Default for indie + small team |

**Honesty rule:** if the brief reads as one of these systems, install and use the official
package. Do not recreate its CSS by hand. Do not import a system's tokens but then override
90% of them.

**One system per project.** Do not mix Fluent with Carbon in the same tree. Do not import
shadcn/ui components into a Material 3 app.

When the brief is an aesthetic (not a system) — editorial, brutalist, glassmorphism,
organic — there is no official package. Build with native CSS + Tailwind + a maintained
component library. Be honest in code comments about what is borrowed inspiration vs.
official material.

## Verify

- A one-line "Design Read" is declared before any code.
- Dial values are explicit and reasoned from the brief — not silently using baseline.
- The design system (or aesthetic) is chosen and labeled honestly.
- Anti-default discipline applied — no LLM-default aesthetic shipped.
