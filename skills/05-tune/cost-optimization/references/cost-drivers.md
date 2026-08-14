# Cost Drivers — Symptom → Cause Map

Load when identifying which lever moves a cloud bill. The top 1–2 services by spend
share are where the money goes; this map turns a symptom ("compute is expensive")
into a cause and a lever.

## The driver categories

Almost all cloud spend falls into one of six categories. Rank yours by share of the
bill; the biggest is the lever.

| Category | What it is | Typical share |
|---|---|---|
| Compute | VMs, containers, serverless invocations | 30–60% |
| Storage | Volumes, object storage, snapshots, backups | 10–25% |
| Network/egress | Data transfer out, cross-AZ, cross-region | 5–20% |
| Managed services | DBs, queues, caches, CDNs (PaaS markup) | 10–30% |
| Idle/waste | Resources running but unused | 5–15% |
| Commitment gap | Paying on-demand for steady-state load | 10–30% |

## Symptom → cause → lever

| Symptom (you see…) | Likely cause | Lever |
|---|---|---|
| Compute spend high, CPU p95 < 30% | Over-provisioned instance class | Right-size down one class; re-measure p95 |
| Compute spend high, CPU p95 > 70% | Genuinely loaded — not a cost problem | Don't cut; look elsewhere or commit to reserved |
| Dev/staging running 24/7, used 8h/day | Idle outside business hours | Schedule stop (auto-start/stop); ~60% cut |
| Unattached EBS/GCP disks | Volumes left after instance deletion | Snapshot + delete; alert on unattached age |
| Snapshot count growing, old snapshots | No lifecycle policy | Set retention; expire > N days |
| Egress is a top-3 cost | Cross-region/AZ data transfer | Co-locate services; use a CDN; move read replicas |
| S3/GCS storage grows monotonically | No lifecycle/tiering | Transition to Infrequent Access/Archive after N days |
| On-demand spend dominant, load is steady | No reserved/committed-use | Reserved instances / savings plans (30–60% off) |
| Batch jobs on on-demand, interruptible | Wrong pricing model | Spot/preemptible (70–90% off) with checkpointing |
| Managed DB much costlier than self-hosted equiv | PaaS markup for features you don't use | Audit: do you need HA/auto-failover, or can a smaller tier work? |
| Cost spikes at month-end | Batch/backfill job | Reschedule to off-peak; throttle concurrency |

## Pricing model decision

```
Is the load steady-state (runs 24/7, predictable)?
  YES → reserved instance / savings plan / committed-use discount (30–60% off on-demand)
  NO  → is it interruptible (batch, CI, background)?
          YES → spot / preemptible (70–90% off, with checkpointing + fallback)
          NO  → on-demand (the default; only correct for spiky/unpredictable load)
```

The commitment gap (paying on-demand for steady-state) is the single most common
waste — and the highest-payoff fix, often 30–50% off the compute line with zero
architecture change. But it commits you to a spend level, so only commit what you've
verified is steady for 30+ days.

## Per-platform quick checks

**AWS:** Cost Explorer → group by service, then by tag (owner/env). Look for:
`aws ec2 describe-instances` with State=stopped (paying for EBS only); unattached EBS
(`describe-volumes --filter Status=available`); old snapshots; Compute Optimizer
recommendations.

**GCP:** Billing → Reports → group by label. `gcloud compute instances list` filtering
`STATUS:TERMINATED`; idle recommendations in the Recommender API; committed-use
discounts for steady-state.

**Azure:** Cost Management → Cost analysis → group by resource. `az vm list --show-details`
for stopped VMs (still paying disk); Azure Advisor cost recommendations; reserved VM
instances for steady-state.

**Kubernetes / containers:** FinOps on k8s is about attribution — who owns which workload's
spend. `kubectl costs` (kubecost/OpenCost) gives per-namespace and per-label cost allocation;
without it, shared-cluster spend is invisible. Check: unrequested-pod overprovisioning (requests
>> actual usage — the #1 k8s waste), idle LoadBalancers pointing at nothing, PersistentVolumes
not reclaimed after PVC deletion, and orphaned snapshots. Right-size via vertical autoscaler
recommendations; spot/preemptible for batch workloads; shared clusters over per-team clusters
(attribution via labels, not isolation). For managed k8s control-plane fees (EKS/GKE/AKS charge
per cluster-hour), consolidate clusters — a $70/mo control plane × 10 teams = $8.4k/yr of pure waste.

**General:** the fastest single win is usually committing steady-state compute that's
currently on on-demand — verify 30 days of steady load, then commit 1 year. Second is
cutting idle dev/staging. Architecture changes (cache, co-locate) pay off most but take
longest; do them last, after the quick wins bank the savings.
