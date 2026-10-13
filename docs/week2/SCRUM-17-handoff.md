# SCRUM-17 website handoff

**Status:** Prepared, not deployed. **Owner:** Josh Escobar.
**Recipients:** SCRUM-19/shared-document owner and Week 3 API owner.

## Values

| Field | Planned or observed value |
| --- | --- |
| Proposed stack | cfn-site-team07 |
| Planned S3 bucket | s3-site-team07-a7f391 |
| Planned distribution label | cf-site-team07 |
| Planned OAC name | oac-site-team07 |
| Region | us-east-2 for stack/S3; CloudFront global |
| HTTPS website URL | Pending deployment |
| Distribution and OAC IDs | Pending deployment |
| Reviewed template/site commit | Record exact approved commit before execution |
| Release 1 and Release 2 SHA-256 / object Version IDs | Release 1 source hashes in manifest; deployed versions and Release 2 pending |
| Deployment screenshot | Pending genuine deployed evidence |

## Repeatable publishing method

Source is `site/`; no build command. Upload `index.html` to the bucket root and
`assets/styles.css` to `assets/styles.css` using S3 Console. Use the Content-Type
and Cache-Control values in the [deployment plan](SCRUM-17-deployment-plan.md).
For a change, review/commit/hash the changed source, upload under the same keys,
record the new object versions, invalidate `/*` on the actual distribution, wait
for Completed, then verify the release marker and compare deployed bytes/hashes.
This is the planned procedure; record the actually performed method after testing.

## Acceptance checks (all pending)

- [ ] Stack CREATE_COMPLETE; CloudFront Deployed; actual names/IDs recorded.
- [ ] Four S3 public-access blocks true; BucketOwnerEnforced; SSE-S3; versioning enabled; website hosting disabled.
- [ ] Complete bucket policy inspected: only scoped CloudFront read Allow, plus insecure-transport Deny.
- [ ] Regional REST origin and OAC attached; S3/always/sigv4; no OAI or website endpoint.
- [ ] HTTPS root and `/index.html` return 200 with Release 1 and working CSS.
- [ ] HTTP redirects to the corresponding HTTPS URL.
- [ ] Authenticated S3 proves the exact object exists; unsigned direct-S3 access to that key is denied.
- [ ] Required tags, root object, cache/headers policies, pay-as-you-go and absence of WAF verified.
- [ ] Release 2 source change committed, uploaded and observed after completed invalidation.
- [ ] Authenticated deployed content SHA-256 matches each reviewed source file; both releases traceable.
- [ ] Official form URL, actual redeployment method, screenshot and component descriptions populated.
- [ ] Handoff to SCRUM-19 and Week 3 completed; website remains available.

## Evidence

Use the actual UTC capture date in `YYYYMMDD_Team7_aws_...png`. The guide suggests
these supporting views: `w2-site-stack`, `w2-site-s3-private`,
`w2-site-bucket-policy`, `w2-site-s3-properties`, `w2-site-objects`,
`w2-site-origin`, `w2-site-oac`, `w2-site-https-behavior`, `w2-site-settings`,
`w2-site-release1`, `w2-site-release2`, `w2-site-invalidation`, and
`w2-site-http-tests`. Reconcile evidence with the official course form/rubric;
the form itself does not specify this many screenshots. Keep originals private
and publish only reviewed redactions. Local previews are not deployment evidence.

## Draft component descriptions for the form

Use after deployment confirms the names and configuration:

- `s3-site-team07-a7f391` stores website files privately with encryption and versioning.
- `cf-site-team07` serves the website over HTTPS through its generated CloudFront hostname.
- `oac-site-team07` signs CloudFront's requests to the private S3 origin.
- The site bucket policy permits the selected CloudFront distribution to read objects and denies insecure transport.

For Week 3, hand over the exact HTTPS origin (scheme + hostname, without a trailing
path) for API CORS planning. The present site has no visitor-counter/API behavior.
