# Commercialization Models

Depth reference for the `oss-strategy` skill. Generalizes beyond OSS to the full commercialization
decision: pricing models, value-based pricing, the AI-product pricing trap, go-to-market motions, and
the indie-developer revenue ladder. OSS (the skill's primary focus) is one commercialization shape; this
reference covers the rest so the skill can advise non-OSS projects too.

## 1. Pricing models

| Model | Best for | Risk |
|---|---|---|
| **One-time purchase** | Tools with one-time value (desktop apps, plugins) | No recurring revenue; constant new-customer pressure |
| **Subscription (MRR)** | Continuously valuable products (SaaS, content) | Churn kills revenue; must earn renewal every month |
| **Freemium** | Products where most users need little, few need a lot | Free tier can balloon costs; conversion rate typically 2-5% |
| **Usage-based** | Cost scales with use (APIs, infra, AI) | Unpredictable for buyer; hard to forecast revenue |
| **Per-seat** | Team products (collaboration, admin tools) | Caps at org size; shared accounts reduce revenue |
| **Hybrid** | Platform + usage + seats combined | Complexity — pricing must stay explainable |

Rule: the pricing model should mirror how the user receives value. A product used daily wants
subscription; a product used once wants one-time; a product whose cost you incur per use wants
usage-based.

## 2. Value-based pricing

Price between the cost floor and the value ceiling, as close to the ceiling as the user will accept.

```
Cost floor (must cover)        Value ceiling (what it's worth to the user)
        │                              │
        │   ──── price here ────       │
        │                              │
```

- **Cost-plus** (floor + margin) leaves money on the table when value >> cost.
- **Value-based** charges for the outcome the user gets, not the effort you spent.
- Find the ceiling by asking: what does this user pay for the workaround today (time, money, tools)?
  Your price sits below that, above your cost.

**Three-tier pricing (Free / Pro / Enterprise):** the tiers exist for the **anchoring effect**, not
just segmentation. The Enterprise tier (expensive, rarely chosen) makes Pro look like a bargain. Without
the high anchor, Pro feels expensive; with it, Pro feels reasonable. Three tiers also capture different
buyer types (self-serve vs team vs enterprise procurement).

## 3. AI-product pricing trap

API cost per call is opaque — it hides behind usage volume, prompt length, and model tier. Before
pricing an AI feature:

1. **Calculate per-call cost** — input tokens × rate + output tokens × rate + any tool/RAG cost. This is
   your variable cost floor per use.
2. **Price above it with margin** — but expect variance: a power user's call can cost 100× a casual
   user's.
3. **Cap exposure** — usage limits, or usage-based pricing that passes cost through. A flat-fee AI
   product without caps is one power user away from a margin disaster.
4. **Model tiering** — route cheap requests to a small model, hard requests to the frontier model (see
   the `prompt-engineering` skill's cascaded architecture). This is the single biggest AI cost lever.

The principle: model is the engine, product decisions are the steering wheel. Price reflects the
steering-wheel value, but cost reflects the engine — make sure the gap is positive.

## 4. GTM (Go-to-Market) — 4 steps

| Step | Question | Output |
|---|---|---|
| **Audience** | Who exactly buys this? (name the segment) | A specific, reachable group |
| **Channel** | Where do they already spend attention? | The places you show up |
| **Message** | What one sentence makes them try it? | Positioning + hook |
| **Conversion path** | What's the first action they take? | The click → activation step |

## 5. Cold-start funnel

Acquisition only matters if the funnel holds end-to-end. Diagnose which step breaks:

```
Exposure → Click → Register → Activate → Retain
```

- Breaking at **Click** → wrong message or channel.
- Breaking at **Register** → friction in signup, or click was curiosity not intent.
- Breaking at **Activate** → the "aha" moment is too far or unclear.
- Breaking at **Retain** → product doesn't deliver repeat value (the hardest to fix).

Pouring acquisition into a broken funnel wastes money — fix the broken step before scaling the one
before it (same logic as AARRR in `metrics-frameworks.md`).

## 6. GTM motions by buyer

The motion depends on who buys and how:

| Motion | Buyer | How it works | Examples |
|---|---|---|---|
| **PLG (Product-Led Growth)** | End-user self-serves | Product itself drives adoption; free → paid | Figma, Notion, Calendly |
| **Sales-led** | Enterprise procurement | Sales team drives deal; high ACV | Salesforce, Palantir |
| **Product-Led Sales** | Bottom-up adoption + top-down deal | PLG entry, sales closes the enterprise expansion | Slack, Datadog, Zoom |

For developer tools specifically (B2D): PLG dominates — developers reject sales-led motions. The product
must be tryable in minutes, documented excellently, and free to start. Community (GitHub stars, Discord)
replaces the sales pipeline as the trust-builder. OSS is the extreme of B2D PLG — the code itself is the
trial.

## 7. Indie-developer revenue ladder

The solo/small-team path without VC — milestones, not a single exit:

| Rung | What it means | What changes |
|---|---|---|
| **First payment** | A stranger paid real money | Validates willingness to pay (not just "would use") |
| **Ramen profitable** | Covers living expenses | You can do this full-time |
| **$5k MRR** | Sustainable small business | Can reinvest / hire part-time |
| **Scale** | Beyond founder's direct effort | Hiring, process, the hard second phase |

Payment solutions for solo devs: Stripe (needs a foreign entity in many countries), Paddle (Merchant of
Record, handles tax/compliance, China-friendlier), Lemon Squeezy (acquired by Stripe). The MoR services
cost more but eliminate international tax/compliance work — worth it solo.

## 8. Community-first sequencing (OSS and beyond)

For OSS and PLG products: build the community before monetizing.

1. **Community first** — trust, contributors, usage. The moat when code is commoditized is brand and
   community, not the code itself.
2. **Monetize later** — once adoption is real, add the commercial layer (managed hosting, enterprise
   features, support). Premature monetization chills community growth.
3. **The open-core model** — core is OSS (free, adopted), premium is proprietary (paid, enterprise).
   GitLab, Elastic, Grafana.

This sequencing is the bridge between `oss-strategy`'s OSS-specific models and general commercialization:
community is the GTM for OSS the way sales is the GTM for enterprise. Choose the motion that fits your
buyer.
