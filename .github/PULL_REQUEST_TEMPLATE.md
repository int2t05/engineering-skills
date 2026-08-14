## Summary

What this changes and why.

## Related issue

Closes #

## Affected skills

List any `skills/<phase>/<skill>/` touched, or "none" if docs/CI only.

## Checklist

- [ ] `bash scripts/validate-skills.sh` passes (47 skills, 0 errors)
- [ ] `python scripts/gen-agents-yaml.py` run if frontmatter changed (adapters in sync)
- [ ] `.claude-plugin/plugin.json` version bumped (patch / minor / major per CLAUDE.md semver rule)
- [ ] Purity principle honored — root-cause fix, self-documenting, no residual artifacts
