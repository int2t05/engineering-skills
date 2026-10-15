## Summary

What this changes and why.

## Related issue

Closes #

## Affected skills

List any `skills/<phase>/<skill>/` touched, or "none" if docs/CI only.

## Checklist

- [ ] `bash scripts/validate-skills.sh` passes (0 errors)
- [ ] `python scripts/gen-agents-yaml.py` run if frontmatter changed (adapters in sync)
- [ ] `python -m unittest discover -s test -v` passes if installation or resources changed
- [ ] Applicable model checks and unrun behavioral evaluations are identified
- [ ] Release metadata is updated when preparing a release
- [ ] Purity principle honored — root-cause fix, self-documenting, no residual artifacts
