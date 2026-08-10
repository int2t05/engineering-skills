---
name: shipping
description: Use when deploying or launching to production. Faster is safer — checklist-driven launch with rollback readiness and launch-day verification.
---

# Shipping and Launch

Ship with confidence: deploy safely, with monitoring in place, a rollback plan ready, and a clear definition of success. Every launch should be reversible, observable, and incremental. Faster is safer — smaller batches and more frequent releases reduce risk, not increase it.

## When to use

- Deploying a feature or significant change to production for the first time.
- Migrating data or infrastructure.
- Opening a beta or early access program.
- Any deployment that carries risk (all of them).

## Steps

### 1. Complete the pre-launch checklist

Before deploying, every section must be green.

**Code quality**
- [ ] All tests pass (unit, integration, e2e)
- [ ] Build succeeds; lint and type checking pass
- [ ] Code reviewed and approved
- [ ] No `console.log` / debug statements; no pre-launch TODOs left
- [ ] Error handling covers expected failure modes

**Security**
- [ ] No secrets in code or version control
- [ ] Dependency audit (`npm audit`, `pip-audit`, `cargo audit`, ...) shows no critical/high vulnerabilities
- [ ] Input validation on all user-facing endpoints
- [ ] Authn/authz in place; rate limiting on auth endpoints
- [ ] Security headers (CSP, HSTS); CORS scoped to specific origins, not wildcard

**Performance & accessibility**
- [ ] Core Web Vitals in "Good" thresholds; bundle within budget
- [ ] No N+1 queries on critical paths; indexes and caching in place
- [ ] Keyboard navigation, screen reader, WCAG 2.1 AA contrast
- [ ] No axe-core / Lighthouse accessibility warnings

**Infrastructure & docs**
- [ ] Environment variables set in production; DB migrations applied or ready
- [ ] DNS, SSL, CDN configured; health check endpoint responds
- [ ] Logging and error reporting configured
- [ ] README, API docs, ADRs, changelog, user-facing docs updated

### 2. Ship behind a feature flag

Decouple deployment from release so code can land in production inert.

```typescript
const flags = await getFeatureFlags(userId);
if (flags.taskSharing) return <TaskSharingPanel task={task} />;
return null; // existing behavior
```

Flag lifecycle: `DEPLOY (flag OFF) → ENABLE for team/beta → GRADUAL ROLLOUT (5% → 25% → 50% → 100%) → MONITOR at each stage → CLEAN UP`.

Rules: every flag has an owner and an expiration date; clean up within 2 weeks of full rollout; don't nest flags (exponential combinations); test both states in CI.

### 3. Follow the staged rollout sequence

```
1. DEPLOY to staging          → full test suite + manual smoke of critical flows
2. DEPLOY to production (OFF) → verify health check; check error monitoring
3. ENABLE for team            → 24-hour monitoring window
4. CANARY 5%                  → 24-48h; compare metrics vs. baseline
5. GRADUAL 25% → 50% → 100%  → monitor each step; roll back to previous % at any point
6. FULL rollout               → monitor for 1 week; clean up flag
```

Decision thresholds at each stage:

| Metric | Advance | Hold / investigate | Roll back |
|--------|---------|---------------------|-----------|
| Error rate | within 10% of baseline | 10–100% above | >2x baseline |
| P95 latency | within 20% of baseline | 20–50% above | >50% above |
| Client JS errors | no new types | new errors <0.1% sessions | >0.1% sessions |
| Business metrics | neutral or positive | decline <5% | decline >5% |

### 4. Document the rollback plan before launch

Every deployment needs a rollback plan written **before** it happens:

- **Trigger conditions** — error rate > 2x baseline; P95 > [X]ms; user reports of [specific issue]; data integrity issues; security vulnerability discovered.
- **Rollback steps** — disable feature flag (if applicable) OR `git revert <commit> && git push`; verify rollback via health check and error monitoring; notify team.
- **Database considerations** — migration `[X]` has a rollback (`npx prisma migrate rollback`); data inserted by the new feature is preserved or cleaned up.
- **Time to rollback** — feature flag < 1 min; redeploy previous version < 5 min; database rollback < 15 min.

### 5. Verify in the first hour after launch

1. Health endpoint returns 200.
2. Error monitoring dashboard shows no new error types.
3. Latency dashboard shows no regression.
4. Test the critical user flow manually.
5. Logs are flowing and readable.
6. Rollback mechanism confirmed working (dry run if possible).

## Verify

Before deploying:
- [ ] Pre-launch checklist completed (all sections green)
- [ ] Feature flag configured (if applicable)
- [ ] Rollback plan documented
- [ ] Monitoring dashboards set up
- [ ] Team notified of deployment

After deploying:
- [ ] Health check returns 200
- [ ] Error rate is normal
- [ ] Latency is normal
- [ ] Critical user flow works
- [ ] Logs are flowing
- [ ] Rollback tested or verified ready

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, surgical scope, simplicity)
