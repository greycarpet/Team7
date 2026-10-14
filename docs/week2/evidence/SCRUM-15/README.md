# SCRUM-15 estimate evidence

Prepared October 13, 2026 for the Week 2 cost/ADR package, accepted through Josh Escobar's PR #4 approval on October 13, 2026 (America/Chicago). These records contain no credentials, private keys or full account identifiers.

| Record | Provenance and use |
| --- | --- |
| pricing.json | AWS Price List GetProducts, us-east-1 endpoint, Ohio product filters. Five calls succeeded. Selected ordinary S3 request products; annotation-request products were deliberately excluded. Rates use OnDemand terms and the first paid storage tier. |
| egress-pricing.json | AWSDataTransfer GetProducts, fromLocation=US East (Ohio), toLocation=External. Selected USE2-DataTransfer-Out-Bytes; accelerated transfer and peering products excluded. |
| account-check.redacted.json | Read-only account plan, Free Tier usage, budget, notifications and inventory checks. Account identifiers, owner IDs, ARNs, resource IDs and exact credit balance removed from this public extract. |

The original structured account responses are kept privately outside the repository. The redacted file is a selected summary, not an unmodified API export. Price List records are public pricing data. Retrieval timestamps and effective dates are separate fields.

Remaining rates and allowances were checked on [IPv4 pricing](https://aws.amazon.com/vpc/pricing/), [CloudFront pay-as-you-go pricing](https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/) and [EC2 transfer pricing](https://aws.amazon.com/ec2/pricing/on-demand/). The CloudFront pricing page has inconsistent request counts in some worked examples; this estimate uses its explicit 10-million-request offer/table, not the 20-million figure in example prose.

## Calculator evidence added October 14 UTC

The public calculator now has two saved estimates with original, unedited CSV exports:

- [Lab 20 hours: $0.98/month](https://calculator.aws/#/estimate?id=cd51e782cfb2e064fcefe2cc0bd67ae62706da26) / [CSV](20261014_Team7_aws_w2-cost-lab.csv).
- [Continuous 730 hours: $11.91/month](https://calculator.aws/#/estimate?id=340bd531f85e38382e84d5701c939d8e6cd4d4d4) / [CSV](20261014_Team7_aws_w2-cost-continuous.csv).

Screenshots use the actual UTC date and Team7 course naming pattern. The browser returned JPEG, so files retain `.jpg`; no PNG extension was applied to JPEG bytes. These are genuine calculator captures, not reconstructed images. Input captures show the calculation area; CSVs preserve full configuration details.

| Screenshot | View |
| --- | --- |
| [Lab summary](20261014_Team7_aws_w2-cost-estimate-lab.jpg) | Named lab estimate and $0.98 monthly total |
| [Continuous summary](20261014_Team7_aws_w2-cost-estimate-continuous.jpg) | Named 730-hour estimate and $11.91 monthly total |
| [EC2 inputs](20261014_Team7_aws_w2-cost-ec2-inputs.jpg) | On-Demand runtime calculation |
| [EBS inputs](20261014_Team7_aws_w2-cost-ebs-inputs.jpg) | Separate retained gp3 calculation |
| [S3 inputs](20261014_Team7_aws_w2-cost-s3-inputs.jpg) | Storage and request calculation |
| [CloudFront inputs](20261014_Team7_aws_w2-cost-cloudfront-inputs.jpg) | Pay-as-you-go billable usage after manual allowance adjustment |
| [IPv4 inputs](20261014_Team7_aws_w2-cost-ipv4-inputs.jpg) | One address for 20 hours expressed as 20/730 address-months |

[Provenance and integrity hashes](calculator-evidence.json) records original file hashes, capture/write times and CSV reconciliation. Public estimate inputs contain no account identifiers, private billing balances or credentials. The calculator's rounded S3 row differs from the price-list model's unrounded $0.032; final monthly totals agree to cents. No live account credits are built into either estimate.

Website tests and screenshots are in the [SCRUM-17 package](../SCRUM-17/README.md). The October 13 account inventory predates that deployment and is not an all-region audit. This package has no private billing-console screenshot or instructor approval. User confirmation of Architect fields, project-owner acceptance of ADR-001 through PR #4, and the distinction between the official form and the guide's suggested screenshots are recorded in [the handoff](../../SCRUM-15-handoff.md).
