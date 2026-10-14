# Week 2 architect handoff

**From:** Josh Escobar | **Intended recipient:** Alyssa Esteves / [SCRUM-19](https://joshescobarx.atlassian.net/browse/SCRUM-19)

**Prepared:** October 13, 2026 | **Reconciled:** October 14 UTC / October 13 America/Chicago | **Status:** In Review; ADR acceptance pending

The architect's draft is available in [the cost report](SCRUM-15-costs.md) and [ADR-001](../adr/ADR-001.md), under [PR #4](https://github.com/greycarpet/Team7/pull/4). The proposed lab configuration is $0.98/month before account credits; 730-hour operation is $11.91. Both now have saved calculator links, original CSV exports and genuine screenshots. Preserve their assumptions when assembling the shared Solution Architecture Document.

## Prepared architect fields

Josh explicitly confirmed **"Already entered those sections"** in response to whether document control, component costs, and redundancy/storage tiers were entered. The downloaded official course template was inspected for exact field names; the saved live form has not been independently read back. This is owner confirmation of transcription, not ADR acceptance or a teammate's approval. The mapping below documents the supplied inputs rather than claiming an independent transcript of saved values.

| Architect field | Prepared content |
| --- | --- |
| Document owner and scope | Josh Escobar; Team7 Week 2 architecture and cost inputs; draft dated October 13, 2026 |
| Architecture | Private S3 REST origin served through CloudFront OAC and HTTPS; separate Amazon Linux t3.micro tools VM in existing Ohio public subnet |
| Deployed S3 bucket name | `s3-site-team07-a7f391`; follows `s3-{workload}-{team}-{suffix}` and adopts the approved standard's example. Created and verified under SCRUM-17. |
| Region | us-east-2; tools subnet in us-east-2a; CloudFront global with US viewer assumption (North America) |
| Cost model | 20 compute/IPv4 hours, 8 GiB gp3 all month, 1 GB total S3 current/noncurrent/staging storage, 1,000 PUT/LIST and 10,000 GET, 1 GB CloudFront delivery, 10,000 HTTPS requests, 10 invalidation paths |
| Monthly estimate | $0.98 before account credits with shared allowances; $11.91 at 730 hours; tax excluded |
| Budget | $5/month UnblendedCost, primary billing view, credits/refunds excluded; actual alert above $4; other observed alerts at actual/forecast above $5 |
| Current-month scenario | Historical illustrative October result $0.70 and $4.30 headroom; not a current account forecast. The website began before the assumed start and EC2 timing is unknown. Current account-wide projection UNVERIFIED. |
| Free Tier | Active FREE plan verified; account credits tracked privately. No legacy signup allowances assumed. Shared delivery/request allowances are conditional on remaining capacity. |
| Decision and rejected option | Private S3 + CloudFront chosen; hosting on the tools EC2 rejected because stopping it would take down the website and continuous operation exceeds the modeled budget |
| Consequences | Cache management, retained versions and EBS charges, CPU Standard-mode limits, ongoing budget monitoring, separate VM and website operations |
| Decision status | ADR-001 Proposed; requested reviewer Alyssa; actual review date and acceptance pending. PR #5 approval does not approve this ADR or PR #4. |

### Exact official form mapping

| Official section | Supplied content |
| --- | --- |
| Document control · Architect | Document ID, Version, Owner, Approved by, Date, Status. Prepared values were Team7-SAD-001, 0.1, Josh Escobar, reviewer approval pending, October 13, 2026, Draft. Record actual reviewer/date only when review occurs. |
| Components and cost · Architect | Service, Resource name, Purpose, Monthly cost. See component rows below; preserve precision or note rounding. |
| Redundancy and tiers · Architect | Asset, Option chosen, Alternative and why not, Monthly cost. See tier rows below; these costs are already counted in the components table. |

| Service / resource | Purpose | Lab USD/month |
| --- | --- | ---: |
| EC2 / ec2-tools-team07 (planned) | Amazon Linux t3.micro tools VM; Standard CPU credits, 20 running hours | 0.2080 |
| EBS / ebs-tools-team07 (planned) | 8 GiB gp3 disk retained all month, including stopped hours | 0.6400 |
| Public IPv4 / auto-assigned address for ec2-tools-team07 (planned) | Internet/SSH reachability while running; no retained Elastic IP | 0.1000 |
| S3 / s3-site-team07-a7f391 (deployed) | Private website files and retained versions; 1 GB-month, 1,000 writes/list and 10,000 GETs | 0.0320 |
| CloudFront / cf-site-team07 (deployed) | HTTPS delivery; 1 GB US viewers, 10,000 HTTPS requests, 10 invalidation paths within assumed remaining shared allowances | 0.0000 |
| CloudFront OAC / oac-site-team07 (deployed) | Signed access to the private S3 REST origin | 0.0000 |
| Existing VPC / subnet / route table / IGW / sg-tools-team07 | Network foundation and instance access controls; no NAT gateway | 0.0000 |
| **Total before account credits and tax** | **Proposed recurring lab usage, no paid extras** | **0.9800** |

Do not double-count EBS or IPv4 inside the EC2 row. The CloudFront zero-dollar figure assumes pay-as-you-go and sufficient remaining shared allowances, not a guaranteed bill.

| Asset | Option chosen | Alternative, and why not | Lab USD/month |
| --- | --- | --- | ---: |
| s3-site-team07-a7f391 | S3 Standard, redundant across at least three Availability Zones within the region; versioning enabled | S3 Standard-IA targets infrequent access and adds retrieval charges; the small, actively updated site does not justify that tradeoff. No cross-region replication is configured. | 0.0320 including modeled requests; storage alone 0.0230 |
| ebs-tools-team07 (planned) | gp3 in the VM's Availability Zone; 8 GiB, 3,000 IOPS, 125 MiB/s | Provisioned-IOPS SSD is unnecessary for the planned lab workload. A single disk/VM is not multi-AZ high availability. | 0.6400 |

The tier rows are not extra charges. [AWS S3 storage classes](https://aws.amazon.com/s3/storage-classes/) supports the S3 access-pattern and redundancy comparison.

## Responsibility boundaries

| Input | Owner and status |
| --- | --- |
| Cost table and ADR | SCRUM-38/39: review drafts, saved calculator estimates and exports prepared; ADR acceptance pending |
| Architect form sections | Josh confirms entered; no independent saved-form readback |
| Actual instance/volume settings and VM facts | SCRUM-16, Alyssa: not supplied by this architecture task |
| HTTPS URL, OAC/privacy checks, redeployment evidence | SCRUM-17, Josh: Done; PR #5 merged and App/DevOps form completion confirmed |
| Authorized/unauthorized SSH results, CloudShell test | SCRUM-18, Josh: pending deployed instance and coordinated testing |
| Official form, course checks and final PDF | SCRUM-19, Alyssa: pending all contributor inputs |

## Evidence and review remaining

- Review PR #4 and ADR-001; confirm proposed monthly usage, record the actual reviewer/date/decision, and confirm the evidence format. SCRUM-15/38/39 remain In Review until review is complete. A posted handoff is not proof of recipient acceptance.
- Website settings have been reconciled with SCRUM-17 evidence. Reconcile planned VM/disk/CPU/address settings when SCRUM-16 supplies them; this does not prevent preparing the cost/ADR package.
- Per-credit expiry/service restrictions, the current account-wide projection, and independent CloudFront pricing-plan confirmation remain UNVERIFIED. Organization policy denied the pricing-plan lookup; no permissions were changed or bypass attempted. The model subtracts no account credits.
- The official form's deployment screenshot is supplied by SCRUM-17. The execution guide also suggests private budget/Free Tier/credit console screenshots; these are not included here. If the instructor requires that exact format, obtain genuine private captures before course submission. The guide's suggested list is not an independently verified course rubric.
- Josh confirms the Architect fields are entered. VM facts and SSH results remain implementation-owned inputs to SCRUM-19; do not replace them with guesses.

## Reproducible evidence

[Model inputs](cost-model.json), [calculated results](cost-results.json), [AWS regional price records](evidence/SCRUM-15/pricing.json), and [redacted account check](evidence/SCRUM-15/account-check.redacted.json). Run `python scripts/calculate_week2_costs.py` from the repository root to regenerate results. Account checks are dated October 13, 2026 and predate the website deployment; they are not an all-region inventory.

- [Lab calculator estimate](https://calculator.aws/#/estimate?id=cd51e782cfb2e064fcefe2cc0bd67ae62706da26) / [original CSV](evidence/SCRUM-15/20261014_Team7_aws_w2-cost-lab.csv).
- [Continuous calculator estimate](https://calculator.aws/#/estimate?id=340bd531f85e38382e84d5701c939d8e6cd4d4d4) / [original CSV](evidence/SCRUM-15/20261014_Team7_aws_w2-cost-continuous.csv).
- [Calculator screenshots and provenance](evidence/SCRUM-15/README.md), captured October 14 UTC, with the native JPEG format preserved.
- [Website deployment evidence](evidence/SCRUM-17/README.md), [merged PR #5](https://github.com/greycarpet/Team7/pull/5), and https://d3jg1ev4a532iw.cloudfront.net/.

This documentation task makes no AWS changes. Original private billing evidence remains outside the public repository.
