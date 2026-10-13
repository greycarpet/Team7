# Week 2 architect handoff

**From:** Josh Escobar | **Intended recipient:** Alyssa Esteves / [SCRUM-19](https://joshescobarx.atlassian.net/browse/SCRUM-19)

**Prepared:** October 13, 2026 | **Status:** Draft ready for review; handoff receipt pending

The architect's draft is available in [the cost report](SCRUM-15-costs.md) and [ADR-001](../adr/ADR-001.md). The proposed lab configuration is $0.98/month before account credits; 730-hour operation is $11.91. Preserve their assumptions when assembling the shared Solution Architecture Document.

## Prepared architect fields

These entries are ready to transfer into the official form. The official Week 2 template was not present in the repository or the retrieved Jira task, so its exact fields have not yet been populated or checked.

| Architect field | Prepared content |
| --- | --- |
| Document owner and scope | Josh Escobar; Team7 Week 2 architecture and cost inputs; draft dated October 13, 2026 |
| Architecture | Private S3 REST origin served through CloudFront OAC and HTTPS; separate Amazon Linux t3.micro tools VM in existing Ohio public subnet |
| Planned S3 bucket name | `s3-site-team07-a7f391`; follows `s3-{workload}-{team}-{suffix}` and adopts the approved standard's example. Availability pending creation. |
| Region | us-east-2; tools subnet in us-east-2a; CloudFront global with North American viewer assumption |
| Cost model | 20 compute/IPv4 hours, 8 GiB gp3 all month, 1 GB total S3 current/noncurrent/staging storage, 1,000 PUT/LIST and 10,000 GET, 1 GB CloudFront delivery, 10,000 HTTPS requests, 10 invalidation paths |
| Monthly estimate | $0.98 before account credits with shared allowances; $11.91 at 730 hours; tax excluded |
| Budget | $5/month UnblendedCost, primary billing view, credits/refunds excluded; actual alert above $4; other observed alerts at actual/forecast above $5 |
| Current-month scenario | Conditional October projection $0.70 and $4.30 headroom, given October 14 start, 18 days retention, 20 runtime hours, available allowances and no additional costs; not an AWS forecast |
| Free Tier | Active FREE plan verified; account credits tracked privately. No legacy signup allowances assumed. Shared delivery/request allowances are conditional on remaining capacity. |
| Decision and rejected option | Private S3 + CloudFront chosen; hosting on the tools EC2 rejected because stopping it would take down the website and continuous operation exceeds the modeled budget |
| Consequences | Cache management, retained versions and EBS charges, CPU Standard-mode limits, ongoing budget monitoring, separate VM and website operations |
| Decision status | ADR-001 Proposed; requested reviewer Alyssa; review date and acceptance pending |

## Responsibility boundaries

| Input | Owner and status |
| --- | --- |
| Cost table and ADR | SCRUM-38/39: drafts prepared; review pending |
| Actual instance/volume settings and VM facts | SCRUM-16, Alyssa: not supplied by this architecture task |
| HTTPS URL, OAC/privacy checks, redeployment evidence | SCRUM-17, Josh: pending implementation |
| Authorized/unauthorized SSH results, CloudShell test | SCRUM-18, Josh: pending deployed instance and coordinated testing |
| Official form, course checks and final PDF | SCRUM-19, Alyssa: pending all contributor inputs |

## Evidence and review remaining

- Confirm the proposed 20-hour schedule, disk size, retained storage/traffic and monitoring settings; reconcile with final CloudFormation and deployed resources.
- Review per-credit expiration and service eligibility in Billing. The plan-expiration timestamp is not proof of each credit's expiry. Private billing records remain outside this public repository.
- Save AWS Pricing Calculator lab and continuous estimates and exports, or obtain reviewer/instructor acceptance of the price-list calculation as the evidence format. No calculator URL or screenshot has been fabricated.
- Capture course evidence using the approved convention. Suggested filenames from the guide are YYYYMMDD_Team7_aws_w2-cost-estimate.png, w2-cost-ec2-inputs.png, w2-cost-s3-inputs.png, w2-cost-cloudfront-inputs.png, w2-budget.png, w2-free-tier.png and w2-credits.png, each with the full date/Team7/aws prefix. Confirm suffixes against the rubric. Keep raw billing screenshots private; review redactions before sharing.
- Transfer these entries into the instructor's actual form and check completeness, correctness, authenticity and consistency. Do not replace implementation-owned pending values with guesses.
- Record ADR reviewer acceptance and receipt of the architect handoff. SCRUM-15 remains In Progress until its evidence, form and handoff criteria are satisfied.

## Reproducible evidence

[Model inputs](cost-model.json), [calculated results](cost-results.json), [AWS regional price records](evidence/SCRUM-15/pricing.json), and [redacted account check](evidence/SCRUM-15/account-check.redacted.json). Run `python scripts/calculate_week2_costs.py` from the repository root to regenerate results. Account checks are dated October 13, 2026; they are not a deployment validation or an all-region inventory.
