---
name: oss-polish
description: Use when polishing an open source project's GitHub presence — README, topics/About description, commit-history narrative story, and trending-repo positioning. Triggers on "polish my repo", "开源项目美化", "优化项目展示".
---

# Open Source Project Polish

One-pass workflow to turn a bare repo into a professional, discoverable open source
project. Four phases: README → topics/About → commit-history narrative → trending-repo
positioning.

## When to use

- Preparing a project for public release or first launch
- Repo has working code but a bare README, missing topics, or no About description
- Want a commit-history narrative (`REPOSITORY_SUMMARY.md` + `THE_STORY_OF_THIS_REPO.md`)
- Researching trending repos in a domain for positioning benchmarking
- Triggers: "polish my repo", "beautify open source project", "开源项目美化", "优化项目展示"

## Steps

### Step 1: Analyze project

1. Read entry files (`package.json`, `go.mod`, `Cargo.toml`, `requirements.txt`, `mkdocs.yml`).
2. Scan source dirs for architecture and key features; note tech stack, target users, unique value.
3. Check existing `README.md` and repo metadata.
4. If `README.md` exists, ask: update in place or back up to `README-backup.md` first?

Output: a one-paragraph summary of what the project does, who it's for, and what's special.

### Step 2: Generate README

Produce a professional `README.md` with sections in this order:

1. **Title (H1)** — repository name.
2. **Badges** — shields.io format. Order: build status → tech stack → hosting → license.
   Pick templates from `references/badges.md`. Limit 5–10 for readability. Do NOT add a
   self-link "GitHub repo" badge — readers are already on GitHub.
3. **Live site link** — if deployed (GitHub Pages, Netlify, Vercel).
4. **Overview** — 1–3 paragraphs answering what / who / why / unique. Hook a visitor in <15s.
5. **Site metrics** — run `python references/scripts/collect-site-metrics.py <repo-path>`;
   emit a `| Metric | Count |` table (markdown files, words, chapters, MicroSims, glossary…).
6. **Getting Started** — prerequisites, clone, install, build/serve, deploy.
7. **Repository Structure** — concise ASCII tree (10–20 lines), representative not exhaustive.
8. **Reporting Issues** — link to GitHub Issues + bug-report template.
9. **License** — match `LICENSE` file / `mkdocs.yml` copyright; default CC BY-NC-SA 4.0 for
   educational content, MIT or Apache-2.0 for code.
10. **Acknowledgements** — key dependencies only.
11. **Contact** — maintainer info.
12. **Optional** — Contributing, Citation (BibTeX), Changelog.

Formatting: ATX headers, blank line before lists, code fences with a language tag, lines <120 chars.

### Step 3: Topics & About description

1. Research trending repos in the same domain — what topics do they use? Run
   `python references/scripts/github_fetcher.py` with `TOPIC=<domain>` env var to list repos
   by stars; inspect each repo's `topics` field.
2. Identify 8–15 highly relevant topics; rank by discoverability × relevance × search volume.
3. Select the final list (max 20 — GitHub limit).
4. Write the **About description** (GitHub allows ≤350 chars): one compelling sentence
   covering what + who + why.

Present the final list + rationale to the user before applying. Apply via GitHub API
(`PUT /repos/:owner/:repo/topics`) and repo settings (description).

### Step 4: Commit-history narrative story

Generate two files in the repo root using git data as evidence — write the files directly,
do NOT paste markdown to chat.

- **`REPOSITORY_SUMMARY.md`** — overview, architecture, key components, technologies, data
  flow, team/ownership.
- **`THE_STORY_OF_THIS_REPO.md`** — chronicles (year in numbers), cast of characters
  (contributors + specialties), seasonal patterns, great themes (feat/fix/refactor),
  plot twists/turning points, current chapter.

Git commands to run systematically (POSIX forms for Git Bash):

- `git rev-list --all --count` — total commits
- `git shortlog -sn --since="1 year ago" | head -20` — top contributors
- `git log --since="1 year ago" --format="%ai" | cut -c1-7 | sort | uniq -c | sort -rn | head -12` — monthly activity
- `git log --since="1 year ago" --oneline --grep="feat\|fix\|update\|add\|remove" | head -50` — change themes
- `git log --since="1 year ago" --name-only --oneline` — hotspot files
- `git log --since="1 year ago" --merges --oneline | head -20` — collaboration patterns

Be specific: actual file names, commit messages, contributor names. Evidence-based — explain
why patterns exist (holidays, releases, incidents).

### Step 5: Trending-repo positioning

1. Run `python references/scripts/github_fetcher.py` with `TOPIC=<your-domain>` to fetch top
   repos by stars.
2. Run `python references/scripts/readme_fetcher.py` (or the batch helper) to pull competitor
   README summaries.
3. Benchmark: how does this project compare on stars, README quality, topic coverage, positioning?
4. Produce: a 5–10 word **tagline**, recommended **launch channels** (HN / Reddit / Dev.to /
   DevHunt by domain), and a short positioning paragraph noting differentiators.

`GH_TOKEN` env var is optional but recommended (5000 req/hr authenticated vs 60 unauthenticated).

### Step 6: Consolidated report

Output a single report:

```
# [Project Name] Open Source Polish
## Analysis Summary    — what / stack / audience
## README              — full content or diff
## Topics & About      — About (≤350 chars), topics list, rationale
## Narrative           — links to the two generated .md files
## Positioning         — tagline, launch plan, differentiators
## Next Steps          — apply checklist (README, topics, About, LICENSE)
```

After user approval, apply changes via GitHub MCP tools (`create_or_update_file` for
README/LICENSE; GitHub API `PUT /repos/:owner/:repo/topics` for topics; repo settings for
the About description).

## Verify

- [ ] README conforms to best practices — run
      `python references/scripts/validate-readme.py README.md`; score ≥75/100 and no missing
      required sections (overview, getting started, license, contact).
- [ ] Topics set on the repo (1–20 topics, all relevant to the project's domain).
- [ ] About description set (≤350 chars, covers what + who + why).
- [ ] Both narrative files (`REPOSITORY_SUMMARY.md`, `THE_STORY_OF_THIS_REPO.md`) exist in repo
      root with complete content (not chat output).
- [ ] Badge URLs resolve; no self-link GitHub-repo badge; all README links work.
- [ ] Positioning report includes tagline, launch channels, and ≥1 differentiator vs trending repos.

## References

- [engineering-principles](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline every skill shares.
- [Badge reference](references/badges.md) — shields.io templates by category (languages, hosting, license, status, custom).
- [Scripts](references/scripts/) — `collect-site-metrics.py` (README metrics), `validate-readme.py` (README linter, scores 0–100), `github_fetcher.py` + `readme_fetcher.py` + `config.py` (trending-repo research via GitHub API).
