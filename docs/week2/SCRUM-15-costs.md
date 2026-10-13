# Week 2 architecture cost estimate

**Task:** [SCRUM-15](https://joshescobarx.atlassian.net/browse/SCRUM-15) / [SCRUM-38](https://joshescobarx.atlassian.net/browse/SCRUM-38)

**Owner:** Josh Escobar | **Date:** October 13, 2026 | **Status:** Draft for review

**Workload region:** US East (Ohio), us-east-2 | **Currency:** USD | **Taxes:** excluded

The proposed lab configuration costs **$0.98/month before account credits**, assuming 20 running hours and available standard CloudFront/transfer allowances. Continuous operation at 730 hours costs **$11.91/month**, exceeding the $5 budget. Keep the static website independent of EC2 so the tools instance can be stopped after testing. [ADR-001](../adr/ADR-001.md) records this decision.

## Planned inputs

These are planning values, not deployed settings. Read-only checks on October 13 found no EC2 instances, EBS volumes, Elastic IPs or NAT gateways in Ohio, and no S3 buckets. CloudFront returned no distribution details. The existing foundation stack remains CREATE_COMPLETE.

| Input | Proposed monthly quantity or setting |
| --- | --- |
| Compute | One Amazon Linux t3.micro, Linux On-Demand, shared tenancy, Standard CPU credits; 20 running hours |
| Continuous comparison | Same design and traffic, 730 compute and IPv4 hours |
| EBS | 8 GiB gp3 retained all month, 3,000 IOPS and 125 MiB/s; no additional provisioned performance |
| Public IPv4 | One auto-assigned address only while running; no Elastic IP retained |
| S3 bucket name | `s3-site-team07-a7f391`, selected from the approved naming standard; planned, availability pending creation |
| S3 storage | 1 GB-month total across current objects, noncurrent versions and any template staging; one month retention modeled |
| S3 requests | 1,000 PUT/COPY/POST/LIST and 10,000 GET/other requests, including deployment and staging requests |
| CloudFront | Pay-as-you-go; 1 GB to North American viewers; 10,000 HTTPS requests; 10 invalidation paths; no WAF |
| EC2 internet transfer | 0.1 GB outbound; inbound package downloads free; no cross-AZ/inter-region transfer modeled |
| Monitoring | Basic service metrics only; no paid logs, custom metrics, detailed monitoring or extra alarms |

Twenty hours is a proposed allowance for setup, coordinated SSH tests and retries. It is not a measured workload or approved deployment setting. Review the 8 GiB disk against the selected AMI. Do not apply these assumptions to an instance with a different disk, credit mode, runtime or pricing model.

## Monthly component costs

Rates retrieved October 13, 2026. Ohio compute, gp3 and S3 prices were verified with AWS Price List GetProducts; selected SKUs and effective dates are preserved in [pricing evidence](evidence/SCRUM-15/pricing.json). The table applies the shared recurring allowances described below, but **no account credits**. Values retain extra decimals to avoid hiding small charges.

| Component | Rate and calculation | Lab 20 h | Continuous 730 h |
| --- | --- | ---: | ---: |
| EC2 compute | $0.0104 per running hour | $0.2080 | $7.5920 |
| EBS gp3 | 8 x $0.08 per GB-month, retained even when stopped | $0.6400 | $0.6400 |
| Public IPv4 | $0.005 per address-hour | $0.1000 | $3.6500 |
| S3 Standard storage | 1 x $0.023 per GB-month, all versions included | $0.0230 | $0.0230 |
| S3 PUT/COPY/POST/LIST | 1,000 x $0.000005 | $0.0050 | $0.0050 |
| S3 GET/other | 10,000 x $0.0000004 | $0.0040 | $0.0040 |
| CloudFront delivery and HTTPS requests | 1 GB and 10,000 requests within shared allowances | $0.0000 | $0.0000 |
| CloudFront invalidations | 10 paths within first 1,000 paths/month | $0.0000 | $0.0000 |
| EC2 internet egress | 0.1 GB within shared 100 GB/month allowance | $0.0000 | $0.0000 |
| S3 to CloudFront transfer | No AWS origin-to-CloudFront transfer charge | $0.0000 | $0.0000 |
| VPC, subnet, route table, IGW, security group | No hourly charge for these base constructs; traffic accounted above | $0.0000 | $0.0000 |
| OAC, default CloudFront TLS, basic monitoring | No separate charge in this configuration | $0.0000 | $0.0000 |
| CloudFormation, IAM/key-pair configuration, budget monitoring | Native AWS resource types; no paid budget reports or custom handlers | $0.0000 | $0.0000 |
| **Total before account credits** | **Sum unrounded rows, round total to cents** | **$0.98** | **$11.91** |

NAT Gateway, load balancers, Route 53/custom domains, paid certificates, snapshots, customer-managed KMS keys, paid logging, paid support and CPU surplus credits have zero modeled usage. WAF is excluded by SCRUM-17. Lambda, API Gateway and DynamoDB belong to later weeks. Re-estimate if any are added. Standard CPU mode avoids Unlimited surplus charges but can reduce performance after credits run out.

## Free Tier and credit treatment

CloudFront pay-as-you-go publishes 1 TB of delivery and 10 million HTTP/HTTPS requests per month, plus the first 1,000 invalidation paths. EC2 internet egress uses the shared 100 GB monthly allowance. These limits are shared with other account usage; zero-dollar rows assume sufficient remaining allowance. They are separate from promotional credits. S3 origin requests still incur charges even when CloudFront viewer delivery is covered. [CloudFront pricing](https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/), [EC2 transfer pricing](https://aws.amazon.com/ec2/pricing/on-demand/).

The live account check confirmed an active FREE plan and a positive remaining credit balance. Plan expiration returned by AWS is March 30, 2027 at 23:01:33 UTC. Exact credit balance is retained in the private handoff, not the public repository. The API returned no Free Tier usage rows; that does not establish zero usage or eligibility for every offer. Individual credit expiration and service restrictions still need review in Billing. Do not assume the historical 750-hour EC2, EBS or S3 signup offers apply. AWS now distinguishes signup experiences, so the live account record governs. [AWS Free Tier guidance](https://aws.amazon.com/free/free-tier-faqs/).

For eligible charges while sufficient credits remain, the modeled payable amount can be $0.00. This is conditional, not a guaranteed bill. Credits are a finite balance, not a recurring monthly discount. The public budget comparison intentionally uses the pre-credit totals because the actual budget excludes credits and refunds.

If the listed shared CloudFront delivery/request/invalidation and EC2 egress allowances are already exhausted, the same usage adds $0.154/month: $0.085 delivery + $0.01 HTTPS requests + $0.05 invalidations + $0.009 EC2 egress. Totals become $1.134 lab / $12.068 continuous, before credits and tax. This is an allowance-exhaustion sensitivity at the listed first paid tiers, not an uncapped-traffic worst case.

## Live budget and October projection

Read-only budget checks at **2026-10-13 22:45 UTC** confirmed:

| Budget field | Observed value |
| --- | --- |
| Name / period / limit | budget-monthly-team07 / MONTHLY / $5 USD |
| Scope | Primary billing view; no region or Project tag restriction returned |
| Metric / exclusions | UnblendedCost; Credit and Refund record types excluded |
| Actual spend | $0.00; budget data last updated 2026-10-13 15:13:42 UTC |
| Notifications | ACTUAL greater than 80%, ACTUAL greater than 100%, FORECASTED greater than 100%; all reported OK |
| Forecast amount | Not returned; no AWS-generated forecast asserted |
| Tax treatment | No explicit tax exclusion returned; estimate is pre-tax |

The 80% threshold is $4; the returned comparison is strictly GREATER_THAN. Notifications do not constitute an automatic spending cap. Subscriber delivery was not tested. See [redacted observations](evidence/SCRUM-15/account-check.redacted.json).

The recurring lab model leaves $4.02 below the $5 limit and $3.02 below the $4 threshold, before other costs/tax. Continuous operation exceeds the budget by $6.914 before rounding. This is an incremental Week 2 model; account-wide future spend is not proven by the Ohio inventory.

**Conditional October scenario:** if resources begin October 14 at 00:00 UTC, remain through November 1 at 00:00 UTC, consume all 20 lab hours and the full modeled request traffic, and there are no additional in-scope costs:

`$0.00 reported MTD + 20 x ($0.0104 + $0.005) + (8 x $0.08 + 1 x $0.023) x 18/31 + $0.005 + $0.004 = $0.701967742`

The pre-tax projection is **$0.70**, with **$4.30** budget headroom and **$3.30** alert headroom. Billing lag, tax, unreported charges and other resources must be added before treating this as the account forecast. The 18/31 fraction uses October's actual length; 730 hours is used only for the recurring continuous comparison. Starting sooner or retaining more versions changes this scenario.

## Cost controls and verification

- Stop EC2 after validation. EBS remains billable; an Elastic IP would remain billable while stopped. One retained address for 730 hours alone costs $3.65. Each extra 10 running hours adds $0.154 for compute and IPv4.
- Use private S3 plus CloudFront pay-as-you-go with WAF disabled. Do not substitute a flat-rate bundle without revising the model.
- Retained S3 versions are full objects. Stack deletion with Retain policies does not stop their storage charges. Review storage after uploads and rollback tests; no deletion is authorized by this estimate.
- Compare the actual template and deployed disk, CPU mode, address allocation, pricing model, traffic and logs against these assumptions under SCRUM-16/17. Check budget and allowances after billing updates.
- Recompute with `python scripts/calculate_week2_costs.py`. Inputs are in [cost-model.json](cost-model.json); unrounded outputs are in [cost-results.json](cost-results.json). This is a reproducible price-list calculation, not an AWS Pricing Calculator export.

## Sources and remaining evidence

Primary project sources: [SCRUM-15](https://joshescobarx.atlassian.net/browse/SCRUM-15), [EC2 requirements](https://joshescobarx.atlassian.net/browse/SCRUM-16), [website requirements](https://joshescobarx.atlassian.net/browse/SCRUM-17), [SSH requirements](https://joshescobarx.atlassian.net/browse/SCRUM-18), the SCRUM-15 How-To version 2.0 attachment, and [Week 1 standard](../week1/Design_Standards_Cloud_Architect/01_Cloud_Foundation_and_Naming_Standard.md).

Additional pricing references checked October 13: [T3](https://aws.amazon.com/ec2/instance-types/t3/), [gp3](https://aws.amazon.com/ebs/pricing/), [IPv4](https://aws.amazon.com/vpc/pricing/), [S3](https://aws.amazon.com/s3/pricing/), [CloudFormation](https://aws.amazon.com/cloudformation/pricing/), [Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/pricing/), [basic monitoring](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-metrics-basic-detailed.html), [EC2 stop/start](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/how-ec2-instance-stop-start-works.html).

Saved Pricing Calculator links/exports, course-named screenshots, individual credit expiry details, official form mapping and review acceptance remain open. API observations support the draft but do not replace a required course screenshot. See [handoff](SCRUM-15-handoff.md).
