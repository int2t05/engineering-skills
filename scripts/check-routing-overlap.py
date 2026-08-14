#!/usr/bin/env python3
"""Routing-overlap metric for the engineering-skills pack.

Complements the validator's literal trigger-phrase collision check with a
semantic-level overlap score: for every pair of skills, compute the Jaccard
similarity of their frontmatter `description` word sets. High overlap means
two descriptions are confusable — the model may route to the wrong one.

Pure Python (no embedding API, no external deps, deterministic, CI-safe).
Pairs above the threshold are flagged WARN (non-blocking) — the validator's
exact-phrase collision check remains the hard gate; this surfaces semantic
near-misses it can't catch.

Usage: python scripts/check-routing-overlap.py [--threshold 0.6]
Exit code: 0 always (WARN-only); prints a table of overlapping pairs.
"""

import argparse
import glob
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Stopwords removed before comparison — they inflate overlap without carrying
# routing signal. Domain terms (review, test, deploy, etc.) are KEPT.
STOPWORDS = frozenset("""
use when for the a an of and or to in on at by with from into vs is are be
this that these those it its their your you we they not no do does did
will can should would could may might must shall
when where why how what who which whom whose
more most less least very just also only even still already yet now then
than then so such as well about above below over under again further once
here there all any both each few many other some such no nor not only own same
s
""".split())


def tokenize(description):
    """Lowercase, split on non-word, drop stopwords and short tokens."""
    words = re.findall(r"[a-z0-9]+", description.lower())
    return frozenset(w for w in words if len(w) > 2 and w not in STOPWORDS)


def jaccard(a, b):
    """Jaccard similarity of two sets: |A∩B| / |A∪B|."""
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def load_descriptions():
    """Return list of (skill_name, description, token_set) for every skill."""
    skills = []
    for skill_md in sorted(glob.glob(str(REPO_ROOT / "skills" / "*" / "*" / "SKILL.md"))):
        skill_md = Path(skill_md)
        text = skill_md.read_text(encoding="utf-8")
        # Extract frontmatter
        m = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not m:
            continue
        fm = m.group(1)
        desc_match = re.search(r"^description:\s*(.+)$", fm, re.M | re.S)
        if not desc_match:
            continue
        desc = desc_match.group(1).strip()
        name = skill_md.parent.name
        skills.append((name, desc, tokenize(desc)))
    return skills


def main():
    parser = argparse.ArgumentParser(description="Routing-overlap metric (Jaccard on description word sets)")
    parser.add_argument("--threshold", type=float, default=0.6,
                        help="Flag pairs with Jaccard >= this (default 0.6)")
    parser.add_argument("--top", type=int, default=20,
                        help="Show top N pairs even if below threshold (default 20)")
    args = parser.parse_args()

    skills = load_descriptions()
    n = len(skills)
    if n < 2:
        print("Need at least 2 skills to compare.")
        return

    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            score = jaccard(skills[i][2], skills[j][2])
            pairs.append((score, skills[i][0], skills[j][0], skills[i][1], skills[j][1]))

    # Sort by score descending
    pairs.sort(key=lambda p: p[0], reverse=True)

    flagged = [p for p in pairs if p[0] >= args.threshold]

    print(f"Routing Overlap Report")
    print(f"=======================")
    print(f"Skills compared: {n} | pairs: {len(pairs)} | threshold: {args.threshold}")
    print()

    if flagged:
        print(f"FLAGGED ({len(flagged)} pair(s) >= {args.threshold} — consider sharpening descriptions):")
        for score, a, b, _, _ in flagged:
            print(f"  {score:.2f}  {a}  ↔  {b}")
        print()

    print(f"Top {min(args.top, len(pairs))} pairs by overlap (context):")
    for score, a, b, desc_a, desc_b in pairs[:args.top]:
        marker = " ⚠" if score >= args.threshold else ""
        print(f"  {score:.2f}  {a} ↔ {b}{marker}")

    if not flagged:
        print(f"\nNo pairs above threshold {args.threshold}.")
    else:
        print(f"\n{len(flagged)} pair(s) flagged. Review whether the overlap reflects genuine routing ambiguity.")
    # WARN-only: always exit 0 so CI stays green.
    sys.exit(0)


if __name__ == "__main__":
    main()
