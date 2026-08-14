# Load Profiles

Depth reference for the `load-testing` skill. Traffic-mix modeling, the test-pattern catalog,
breaking-point characterization, and autoscaling validation.

## Contents

- [1. Traffic-mix modeling](#1-traffic-mix-modeling)
- [2. Test-pattern catalog](#2-test-pattern-catalog)
- [3. Breaking-point characterization](#3-breaking-point-characterization)
- [4. Autoscaling validation](#4-autoscaling-validation)

## 1. Traffic-mix modeling

Load is only meaningful if it resembles real usage. Model the traffic mix from production
analytics (for an existing system) or expected user journeys (for a new one).

### The traffic-mix document

Before any test, write down the mix:

| Endpoint / journey | % of traffic | Method | Read/Write | Payload profile | Auth? |
|---|---|---|---|---|---|
| `GET /api/products` (browse) | 60% | GET | Read | 95th-pctile size | No |
| `GET /api/cart` (view cart) | 20% | GET | Read | Small | Yes |
| `POST /api/cart/items` (add to cart) | 15% | POST | Write | Medium, idempotency key | Yes |
| `POST /checkout` (checkout) | 5% | POST | Write | Large, 3-party calls | Yes |

Rules:
- **Read/write ratio matches real usage** — not 100% reads (hides write bottlenecks) and not
  uniform (hides hot endpoints)
- **Payload variety** — include the 95th-percentile payload size, not just the trivial case; a
  `GET /products` returning 3 items is a different test from one returning 300
- **Pacing / think time** — humans don't hammer at max RPS. Add 1-5s think time between actions
  in a journey to model real session behavior (affects concurrent-user count, not just RPS)
- **Auth cost included** — login/token-refresh is real load; don't test only authenticated
  requests and skip the auth path

### Journey-based vs. endpoint-based

- **Endpoint-based:** fire N requests at `/api/products`. Simple; good for saturating one path.
- **Journey-based:** simulate a user: browse → view product → add to cart → checkout. Models
  real session state, cache warming, and sequential dependencies. Closer to production load.

Use journey-based for capacity validation; endpoint-based for isolating a single path's ceiling.

## 2. Test-pattern catalog

Run each pattern separately — mixing them produces unattributable results.

### Ramp (gradual increase)

Gradually increase load from 0 to peak over minutes. Observe where latency starts to degrade
and where errors begin.

```
Stage 1: 0 → target RPS over 2 min (ramp)
Stage 2: hold target RPS for 5 min (steady)
Stage 3: target → 2× target over 3 min (push)
```

**What it tells you:** the latency-vs-load curve — the inflection point where marginal load
causes disproportionate latency. This is your early-warning ceiling.

### Steady / soak (sustained)

Hold target load for hours (not minutes). Short tests miss the failures that need time to
surface:

- **Memory leaks** — slow growth over hours, invisible in a 10-min test
- **Connection pool exhaustion** — connections leak slowly until the pool starves
- **GC pressure** — periodic full-GC pauses that only appear after enough allocation
- **Cache warm-up effects** — cold-cache p99 vs. warm-cache p99 can differ 10×
- **Log/disk growth** — a log path that fills disk over hours

**What it tells you:** whether the system is stable at target load, or merely survives it
briefly. A system that passes a ramp test but fails a soak test has a resource leak.

### Spike (sudden burst)

Instantaneous jump to 10× steady load, hold briefly, drop back.

```
Stage 1: steady at 1000 RPS
Stage 2: instant jump to 10000 RPS, hold 30s
Stage 3: drop back to 1000 RPS
```

**What it tells you:** how the system handles sudden traffic (a viral moment, a restart after
downtime). Validates backpressure (does it queue or crash?), queueing (how deep?), and recovery
(does it return to normal latency, or stay degraded?).

### Stress (past the break)

Push deliberately past the breaking point. Confirm graceful degradation and recovery.

```
Increase load until error rate > 5% or p99 > SLO threshold.
Record the RPS at which the system failed.
Continue past failure; observe degradation mode.
Drop load; measure time-to-recover.
```

**What it tells you:** the failure mode — does the system return controlled errors (503 with
backpressure), or crash/hang (cascading failure)? And whether it recovers on its own when load
drops, or requires manual intervention.

## 3. Breaking-point characterization

The "breaking point" is not a single number. Characterize it precisely:

```
At X RPS (sustained for Y minutes):
  - p50 latency: A ms
  - p99 latency: B ms  (SLO threshold: C ms — exceeded)
  - error rate: D%     (SLO threshold: E% — exceeded)
  - limiting resource: [CPU / DB pool / memory / network / downstream]
  - saturation mode: [graceful 503s / queue growth / cascading timeout / crash]
  - recovery: [auto-recovered in F min after load dropped / required restart]
```

### Identifying the limiting resource

The RPS number is useless without knowing what saturated first. Watch these during the test:

| Resource | Metric to watch | Saturation signal |
|---|---|---|
| CPU | host CPU% | sustained > 80%; latency rises with load |
| DB connection pool | active connections / pool max | hits max; requests queue for a connection |
| DB CPU / IOPS | DB metrics | queries slow; p99 driven by DB latency, not app |
| Memory | RSS / available | growth under load (leak) or OOM kills |
| Network | bandwidth / packet loss | saturates link; retransmits rise |
| Downstream dependency | dependency p99 / error rate | the dependency saturates first; your system waits |

The first resource to saturate is the bottleneck. Optimizing anything else is waste until that
resource is addressed.

## 4. Autoscaling validation

Autoscaling rules are untested until a load test exercises them. Validate:

- **Trigger condition** — does the scaling rule fire at the right threshold? (e.g. CPU > 60% for
  3 min triggers scale-up). Confirm it fired during the ramp/spike test.
- **Scale speed** — how long from trigger to new capacity serving traffic? If it takes 5 minutes
  to add a replica and the spike lasts 30 seconds, autoscaling didn't help during the spike.
- **Right dimension** — did it scale the right thing? Scaling app instances when the DB is the
  bottleneck adds capacity that can't be used.
- **Scale-down** — does it scale back down after load drops? Aggressive scale-down can cause
  flapping; too slow wastes cost.
- **Limits** — what happens at the max-scale limit? If max is 10 instances and you need 15, the
  system degrades. Know the ceiling.

### The autoscaling test protocol

1. Run a ramp test past the scale-up threshold
2. Confirm: scale-up fired, new capacity joined, latency recovered
3. Measure: time from threshold-crossed to new-capacity-serving (the "scale gap")
4. Drop load; confirm scale-down fired without flapping
5. Push to max-scale; observe behavior at the limit (degradation mode)

If the scale gap exceeds the spike duration, autoscaling is insufficient for bursty load — add
headroom (higher min instances) or a faster scaling rule.
