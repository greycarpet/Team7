# SCRUM-17 deployment evidence

The approved infrastructure and Release 1 source are commit
`081da4c5c8cab8b9c76e5186664ea16316d415fa` in
[PR #5](https://github.com/greycarpet/Team7/pull/5).
Josh explicitly authorized deployment with `DEPLOYMENT AUTHORIZED`.

## Infrastructure

- [Local validation](validation.md) records cfn-lint, CloudFormation Guard and
  the negative checks performed before deployment.
- [Deployment record](deployment.redacted.json) records the reviewed four-addition
  change set, successful stack, actual identifiers, configuration checks and
  known verification limits.
- The deployed original template matched the reviewed file byte-for-byte.
- CloudFormation `DescribeEvents` returned a successful change-set operation
  with no validation-error events. It did not return individual validator results.
- CloudTrail event history contains `CreateChangeSet` and `ExecuteChangeSet`.
  No configured trail was returned, so durable retention is not established.

The original AWS responses are preserved outside the Git repository in the
private evidence directory. This repository record removes account identifiers,
assumed-role details and organization-policy identifiers. There are no credentials
or signed URLs in the published evidence.

## Release verification

- [Release 1 verification](release1-verification.json): all 17 checks passed at 2026-10-14 00:00 UTC.
- [Release 2 verification](release2-verification.json): all 17 checks passed at 2026-10-14 00:04 UTC.
- [Completed invalidation](invalidation.json) records the one-path /* invalidation.
- [Release 1 screenshot](20261014_Team7_aws_w2-site-release1.jpg) and
  [Release 2 screenshot](20261014_Team7_aws_w2-site-release2.jpg) are genuine live captures.
- [Screenshot manifest](screenshots.json) records capture times, source URL and SHA-256.
- [Form entries](../../SCRUM-17-form-entries.md) and [handoff](../../SCRUM-17-handoff.md) provide the role's required fields.

Screenshots were captured after midnight UTC on October 14 (October 13 Central).
Both show reviewed public website content and were copied without edits. The
browser's native JPEG format is preserved. Browser warning/error logs were empty.

The repeatable read-only verification script is
[scripts/validation/verify_scrum17_live.py](../../../../scripts/validation/verify_scrum17_live.py).
It accepts --release, --repo and --out; keep authenticated downloads in a private
output directory outside Git. It requires the existing AWS CLI Team7 profile
and network access; it makes no AWS changes.

For each release, verification downloads the authenticated current S3 object and
the public CloudFront response, computes SHA-256 for both, and compares them with
the reviewed source. It checks HTTPS `/`, `/index.html`, and `/assets/styles.css`,
HTTP-to-HTTPS redirects for those paths, and unsigned access denial for the known
existing S3 `index.html` object. These content checks supplement the separately
inspected bucket policy and access controls; a 403 alone is not proof of privacy.

## Limits

PricingPlanManager `ListSubscriptions` was denied by an organization service
control policy. This deployment created no pricing-plan subscription. The intended
model is pay-as-you-go, but the independent subscription check remains unverified.
The stack's `PricingModel` output and `PriceClass_100` do not independently prove
the billing plan. No permissions or organization policies were changed.

The course deployment intentionally has no WAF or paid request logging. Tests
represent the recorded times and locations, not a continuous availability or
production-security guarantee.
