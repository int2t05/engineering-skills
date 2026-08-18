# Web tool fallback

Reference for the `research` skill. When the default web fetch is unavailable or a search tool's
quota is exhausted, switch **tools** by quota dependency. This is orthogonal to Step 3's page-level
retries (retry the same page: add wait, switch format, switch canonical URL, sitemap, site search) —
use it when the *tool itself* is blocked, rate-limited, or out of quota.

## Tiers by quota dependency

| Tier | Role (example tools) | Quota source | Best for |
| --- | --- | --- | --- |
| 0 | GitHub source fetch — `get_file_contents`, `search_code`, `list_commits`, `search_repositories` | Your GitHub token (effectively unlimited) | Anything whose source lives in a repo: specs, schemas, READMEs, SDK source, release notes, LICENSE. Ground truth for "is X released / open-sourced / alive" (latest commit/release date). |
| 1 | Indexed docs lookup — Context7 `resolve-library-id` + `query-docs` | Independent service quota (separate pool from scrape) | "How do I use library X" — API syntax, config, version migration, CLI usage. Returns code snippets by concept. Not for company/market/non-doc facts. |
| 2 | Full-page scrape — Exa `web_fetch_exa`, Firecrawl `firecrawl_scrape` | Third-party scrape quota (finite, **per-provider**) | Official-doc full text not on GitHub. Batch multi-URL fetches here. |
| Discovery | Semantic/developer search — Firecrawl `firecrawl_developer_search`, Exa `web_search_exa`, built-in `WebSearch` | Independent quota from scrape | Finding the URL first; surfacing GitHub mirrors or community copies when the canonical domain is unreachable. |

Tiers 0 and 1 do not share quota with Tier 2 — one scrape tool exhausting does **not** mean search
or indexed-docs are down. But each Tier 2 provider exhausts under load: treat scrape quota as
finite, watch for quota/timeout errors, and fall through.

## Decision flow

1. **Source lives in a GitHub repo?** → Tier 0. Zero quota, most authoritative. Prefer this for
   any spec, schema, SDK, or release note whose canonical home is a repo.
2. **Library/framework/SDK docs?** → Tier 1. Independent quota, concept-indexed.
3. **Official-doc page not on GitHub?** → Tier 2 (Exa or Firecrawl scrape). On a quota/timeout
   error, do not retry the same dead tool — switch provider, then drop to the discovery layer to
   find a GitHub mirror, then back to Tier 0.
4. **All fail?** → Mark the access limit in the source appendix (tool, tier, limit hit, fallback
   tried). Do not present the result as researched — see SKILL.md Step 6.

## Discipline

- **Per-provider quota, not global.** "One scrape tool is out" ≠ "search is down". Try another
  pool before declaring a source unreachable. But design as if each Tier 2 provider is finite: batch
  fetches, prefer Tier 0/1 for repeated lookups, don't fan out many parallel scrapes.
- **Tool choice does not relax Step 4.** Negative claims ("X 未发布 / 不存在 / 未开源") still
  require GitHub falsification regardless of which tool surfaced them — record search term, org,
  result. A scrape tool returning empty is not evidence of absence.
- **GitHub mirrors are common.** Many official docs sites are mirrored in community repos. When the
  canonical domain is unreachable, search GitHub for a mirror before giving up, then fetch via
  Tier 0.
- **Record the toolchain in the source appendix:** tool, tier, any limit hit, fallback taken.
  Access limits are evidence, not an embarrassment to hide.
