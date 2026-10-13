# SCRUM-15 estimate evidence

Prepared October 13, 2026 for the Week 2 cost/ADR draft. These records contain no credentials, private keys or full account identifiers.

| Record | Provenance and use |
| --- | --- |
| pricing.json | AWS Price List GetProducts, us-east-1 endpoint, Ohio product filters. Five calls succeeded. Selected ordinary S3 request products; annotation-request products were deliberately excluded. Rates use OnDemand terms and the first paid storage tier. |
| egress-pricing.json | AWSDataTransfer GetProducts, fromLocation=US East (Ohio), toLocation=External. Selected USE2-DataTransfer-Out-Bytes; accelerated transfer and peering products excluded. |
| account-check.redacted.json | Read-only account plan, Free Tier usage, budget, notifications and inventory checks. Account identifiers, owner IDs, ARNs, resource IDs and exact credit balance removed from this public extract. |

The original structured account responses are kept privately outside the repository. The redacted file is a selected summary, not an unmodified API export. Price List records are public pricing data. Retrieval timestamps and effective dates are separate fields.

Remaining rates and allowances were checked on [IPv4 pricing](https://aws.amazon.com/vpc/pricing/), [CloudFront pay-as-you-go pricing](https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/) and [EC2 transfer pricing](https://aws.amazon.com/ec2/pricing/on-demand/). The CloudFront pricing page has inconsistent request counts in some worked examples; this estimate uses its explicit 10-million-request offer/table, not the 20-million figure in example prose.

This package has no saved AWS Pricing Calculator export, billing screenshot, deployment-test evidence or instructor approval. Required course evidence remains tracked in [the handoff](../../SCRUM-15-handoff.md). The inventory was limited to relevant Ohio/global services and is not an all-region audit.
