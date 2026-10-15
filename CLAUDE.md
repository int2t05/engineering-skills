# Maintainer Instructions

This is a cross-platform engineering skill pack. Read [AGENTS.md](AGENTS.md) for routing and [references/engineering-principles.md](references/engineering-principles.md) for shared discipline.

## Maintain

- Source skills use `skills/<phase>/<name>/SKILL.md`; follow [skill-anatomy.md](references/skill-anatomy.md).
- Keep workflow descriptions concise and references task-specific. Shared links are relative to the source file, not a host environment variable.
- Confirm document paths and apply [human-audit.md](references/human-audit.md); suggested output paths do not authorize creation.
- The Claude hook injects shared principles; standalone installation bundles dependencies for Codex and other hosts.
- Update manifests and routing catalogs when names change; update the output matrix when artifact contracts change.

## Verify

```bash
python scripts/gen-agents-yaml.py
bash scripts/validate-skills.sh
python -m unittest discover -s test -v
```

Model evaluation is separate and on demand; do not claim behavioral quality from static checks. Do not publish without user authorization.
