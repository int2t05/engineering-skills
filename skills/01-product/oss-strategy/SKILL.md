---
name: oss-strategy
description: Use when deciding open source strategy — business model, COSS, open core, commercialization, or growth. Triggers on "open source strategy", "open source to paid", "open source business model", "OSS 策略", "DevHunt", "开源策略", "开源商业模式".
---

# Open Source Strategy

Guide open source as a commercialization path: build community and trust first, monetize
later. Many products use open source for early growth (Supabase, Plausible, Cal.com, Llama, Qwen,
Dify) and later commercialize via managed services or open core.

**Core insight:** Brand is the moat when code is commoditized. Developers won't pay directly;
they become your marketing force through word-of-mouth, content, and recommendations.

## When to use

- User wants open source strategy, OSS commercialization, or open core / COSS business model.
- Deciding between open core, managed service, or support-first monetization.
- Planning open source growth: community building, stars strategy, DevHunt launch.
- User says "open source strategy", "open source to paid", "open source business model", "OSS 策略", "DevHunt", "开源策略", or "开源商业模式".

**Not for:** GitHub README/topics/About beautification — that's `oss-polish`.

## Steps

1. **Choose the business model.** Match the model to the product and audience:

   | Model | Description | Examples |
   |-------|-------------|----------|
   | **Open Core** | Core free; enterprise features (SSO, audit, multi-tenancy) paid | GitLab, Elastic, Grafana |
   | **Managed Services (SaaS)** | Self-host free; cloud/hosted paid | MongoDB Atlas, Confluent, Dify |
   | **Support-First** | Free software; enterprise support subscriptions | Red Hat |
   | **Free + Paid Convenience** | 70–80% revenue from cloud; self-host free | Most COSS companies |

   Enterprise users buy risk mitigation — SLAs, indemnification, security patches, support —
   not just code.
   For general pricing models, value-based pricing, GTM motions, and the indie-developer
   revenue ladder beyond OSS — load `references/commercialization-models.md`.

2. **Pick the license.** This determines who can fork and whether cloud giants can exploit
   your work without contributing:

   | License | Use | Trade-off |
   |---------|-----|-----------|
   | **MIT, Apache 2.0** | Permissive; max adoption | Cloud giants can fork without contributing |
   | **AGPL** | Prevent cloud fork without contribution | May reduce adoption |
   | **BSL/SSPL** | Source-available; commercial restrictions | Elastic, HashiCorp, Redis Labs shifted to this |

3. **Plan community and trust.** Open source distribution runs on trust, not ad spend:
   - **Build in public** — share progress, metrics, failures; attracts early adopters.
   - **CONTRIBUTING.md** — clear contribution path; lowers friction for outside PRs.
   - **Transparency** — published roadmap and changelog; community involvement in planning.
   - **Preserve goodwill** — communicate commercialization early; keep investing in the OSS core.

   Community benefits: organic word-of-mouth, user-generated content (SEO), free QA via bug
   reports, contribution activity signals project health.

4. **Plan the growth launch.** Stars without strategy are vanity metrics. Coordinate a
   multi-channel launch (HN, Reddit, Dev.to); Tuesday–Wednesday US Pacific morning often
   outperforms. A quality README and clear value proposition matter more than channel volume.
   For DevHunt (developer tools directory): prepare product info (name, tagline, description,
   category, GitHub URL); it's naturally aligned with open source projects.

**Output:** `docs/research/strategy.md` — the commercialization decision: business model, license,
community plan, and growth-launch channel plan. A PRD input when commercialization shapes product scope.

## Verify

- A business model is chosen and justified against the product and audience.
- A license is selected with its trade-offs acknowledged.
- A community plan exists (contributing guide, transparency, build-in-public cadence).
- The growth launch has a concrete channel plan, not just "post on GitHub."

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline shared by every skill.
- [${CLAUDE_PLUGIN_ROOT}/references/product-principles.md](${CLAUDE_PLUGIN_ROOT}/references/product-principles.md) — product discipline (opportunity = demand × giant blind spot ÷ difficulty, the real competitor is the current workaround).
- [references/commercialization-models.md](references/commercialization-models.md) — general pricing (subscription/freemium/usage/per-seat), value-based pricing, AI-product pricing trap, GTM motions (PLG/sales-led/product-led sales), indie-developer revenue ladder.
- GitHub README/Topics/About beautification: `08-ship/oss-polish`.
