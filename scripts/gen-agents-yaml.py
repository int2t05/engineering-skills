#!/usr/bin/env python3
"""Generate agents/openai.yaml (Codex adapter) for every skill.

Reads each skills/<phase>/<name>/SKILL.md frontmatter and emits:
  interface:
    display_name: <Title Case / acronym>
    short_description: <first clause of description>
  policy:                       # only for user-invoked skills
    allow_implicit_invocation: false

Idempotent: re-running overwrites in place. Delete the file with `rm` to remove.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

ACRONYMS = {"tdd", "api", "e2e", "ci", "cd", "oss", "ai", "ui", "pr", "adr", "css", "html", "sql", "cli", "sdk", "rest", "grpc"}


def display_name(slug: str) -> str:
    if slug == "ci-cd":
        return "CI/CD"
    parts = []
    for tok in slug.split("-"):
        if tok in ACRONYMS:
            parts.append(tok.upper())
        else:
            parts.append(tok.capitalize())
    return " ".join(parts)


def short_description(desc: str) -> str:
    """First clause of the description, trimmed for the Codex skill picker."""
    d = desc.strip()
    # Strip a leading "Use when/before/after [the user (wants to|asks for)]?"
    d = re.sub(r"^Use (?:when|before|after) (?:the user (?:wants to |asks for )?)?", "", d, flags=re.I)
    # Cut at the first sentence boundary or trigger clause
    d = re.split(r"\. |\bTriggers on\b|\bUse when\b|\bMentions\b", d, maxsplit=1)[0]
    d = d.strip().rstrip(".")
    # Capitalize the first letter (verb phrase for the picker)
    if d:
        d = d[0].upper() + d[1:]
    # Trim to ~90 chars on a word boundary
    if len(d) > 90:
        d = d[:90].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return d


def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    fm = m.group(1)
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    dmi = re.search(r"^disable-model-invocation:\s*(true|false)", fm, re.M)
    if not name or not desc:
        return None
    return {
        "name": name.group(1).strip(),
        "description": desc.group(1).strip(),
        "user_invoked": bool(dmi and dmi.group(1) == "true"),
    }


def yaml_double_quoted(s: str) -> str:
    """Wrap s as a YAML double-quoted scalar, escaping \\ and "."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_yaml(meta: dict) -> str:
    lines = [
        "interface:",
        f"  display_name: {yaml_double_quoted(display_name(meta['name']))}",
        f"  short_description: {yaml_double_quoted(short_description(meta['description']))}",
    ]
    if meta["user_invoked"]:
        lines.append("policy:")
        lines.append("  allow_implicit_invocation: false")
    return "\n".join(lines) + "\n"


def main():
    count = 0
    errors = []
    for skill_md in sorted(SKILLS_DIR.glob("*/*/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        if not meta:
            errors.append(f"  {skill_md}: could not parse frontmatter")
            continue
        agents_dir = skill_md.parent / "agents"
        agents_dir.mkdir(exist_ok=True)
        out = agents_dir / "openai.yaml"
        out.write_text(render_yaml(meta), encoding="utf-8", newline="\n")
        count += 1
    print(f"Generated {count} agents/openai.yaml files")
    if errors:
        print("Errors:", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
