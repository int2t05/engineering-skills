---
name: load-testing
description: Use when validating capacity under load — generate realistic and adversarial traffic, find breaking points, characterize saturation, validate autoscaling. Triggers on "load test", "stress test", "capacity", "k6", "Locust", "wrk", "压测", "压力测试", "容量测试".
---

# Load Testing

`performance` fixes measured slowness after it appears. Load testing finds the breaking point
before users do — generate realistic and adversarial traffic, characterize how the system
saturates, and validate that autoscaling and capacity claims hold. This is proactive capacity
validation, a distinct discipline from reactive optimization.

## When to use

- Before launch: validate the system handles expected and peak traffic
- After a major change: new endpoint, architecture shift, dependency swap, data growth
- Setting or validating SLOs (p99 latency, error rate under load)
- Validating autoscaling rules and capacity headroom
- Triggers on "load test", "stress test", "capacity", "k6", "Locust", "wrk", "压测", "压力测试", "容量测试"

**Not for:** fixing a known performance bottleneck (use `performance`); unit/integration/e2e
correctness tests (use `tdd` / `api-testing` / `e2e-testing`). Load testing answers "how much can
it handle," not "does it work" or "why is it slow."

## Steps

### 1. Define capacity goals

State the targets before generating load — without them, a load test produces numbers without
judgment. Extract from SLOs, business expectations, or historical peak:

- Expected steady-state load (RPS, concurrent users)
- Peak load (2–10× steady state, sustained for how long)
- Acceptable p99 latency and error rate under target load
- The "break" threshold: the point past which the system is considered failed

_Verify: goals are written as numbers with units, not "should handle traffic."_

### 2. Design realistic traffic profiles

Load is only meaningful if it resembles real usage. Model the traffic mix from production analytics
or expected user journeys:

- Read/write ratio matching real usage (not 100% reads)
- Geo distribution and connection patterns (keep-alive, new connections)
- Think time / pacing between requests (humans don't hammer at max RPS)
- Payload variety: don't test only the smallest payload — include the 95th-percentile size
- Authentication and session lifecycle (don't skip login cost)

_Verify: the profile document states the read/write ratio, pacing, and payload distribution._

### 3. Choose tooling and set up the harness

Use a dedicated load-generation tool (k6, Locust, wrk, Artillery, or equivalent), running from
infrastructure independent of the system under test — otherwise the load generator becomes the
bottleneck and the numbers lie.

- Separate load generator from the target (different host/region)
- Verify the generator can produce the target RPS before the test (calibrate against a trivial
  endpoint)
- Instrument the target: the load test must pair with `observability` telemetry (CPU, memory,
  connection pools, queue depth, DB latency) so saturation is visible, not just the RPS number
- Run against a production-like environment; staging with 1/10 the capacity of prod produces
  numbers that don't extrapolate

_Verify: the generator saturates the target before saturating itself; telemetry dashboards are
open and capturing during the test._

### 4. Run the test battery

Run each pattern separately — mixing them produces unattributable results:

- **Ramp:** gradually increase load to peak, observe where latency degrades and errors begin
- **Steady / soak:** hold target load for hours; surface memory leaks, connection exhaustion, GC
  pressure, and cache warm-up effects that short tests miss
- **Spike:** sudden traffic burst (10× steady); validate backpressure, queueing, and recovery
- **Stress:** push past the break point deliberately; confirm graceful degradation (errors, not
  crashes) and that the system recovers when load drops

_Verify: each test pattern has a recorded result — RPS achieved, p50/p99 latency, error rate,
and the saturation point observed._

### 5. Characterize the breaking point

Identify and document the system's ceiling — the load at which it stops meeting SLOs:

- What saturated first (CPU, DB connection pool, memory, network, downstream dependency)?
- What was the p99 latency and error rate at the break point?
- Did the system fail gracefully (controlled errors, backpressure) or catastrophically (crash,
  hang, cascading failure)?
- Did autoscaling trigger correctly and in time? Did it scale the right dimension?

_Verify: the breaking point is stated as "at X RPS, p99 hit Yms and errors reached Z%, limited by
[resource]," not "it broke around 5000 users."_

### 6. Document and act

Record the capacity ceiling, the bottleneck, and the validated autoscaling behavior. Create
action items for bottlenecks found (optimize, scale, or add backpressure). Set or adjust alert
thresholds based on the measured saturation point — alert before the break, not at it.

**Output:** load-test scripts under `test/` (committed, re-runnable) plus `docs/CAPACITY.md`
(optional) — the capacity ceiling, bottleneck, autoscaling validation, and action items. Pair
with `observability` for the alert thresholds.

## Verify

- [ ] Capacity goals stated as numbers (target RPS, p99, error rate, break threshold)
- [ ] Traffic profile matches real usage (read/write ratio, pacing, payload distribution)
- [ ] Load generator runs from separate infrastructure; calibrated to exceed target RPS
- [ ] Ramp + soak + spike + stress patterns each run and recorded
- [ ] Breaking point documented with the saturating resource, not just an RPS number
- [ ] Autoscaling validated (triggered correctly, scaled the right dimension, in time)
- [ ] Test scripts committed under `test/`; capacity report produced; alert thresholds set

**Red flags:** load generator and target on the same host; testing only the happy-path endpoint
with minimal payloads; no telemetry during the test (RPS without resource data is unactionable);
extrapolating from a staging environment with a fraction of prod capacity; "it handled 10k RPS"
with no p99 or error rate; running one giant mixed test instead of isolated patterns.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, goal-driven execution)
- [references/load-profiles.md](references/load-profiles.md) — traffic-mix modeling, test-pattern catalog (ramp/soak/spike/stress), breaking-point characterization, autoscaling validation checklist
