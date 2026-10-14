# SCRUM-17 website handoff

**Status:** Deployed and technically verified; shared-form transcription and final
review remain. **Owner:** Josh Escobar. **Review:** [PR #5](https://github.com/greycarpet/Team7/pull/5).

## Confirmed values

| Field | Observed value |
| --- | --- |
| Stack | cfn-site-team07 — CREATE_COMPLETE |
| S3 bucket | s3-site-team07-a7f391 — private, us-east-2 |
| Distribution | cf-site-team07 / E1PBX75YJOS2B9 — Deployed |
| OAC | oac-site-team07 / E2X7EYYCOARJ7I — s3, always, sigv4 |
| HTTPS website | https://d3jg1ev4a532iw.cloudfront.net/ |
| Week 3 exact origin | https://d3jg1ev4a532iw.cloudfront.net |
| Approved infrastructure and Release 1 commit | 081da4c5c8cab8b9c76e5186664ea16316d415fa |
| Release 2 source commit | e5472eb706cc02e44c9284f3fd60a5abdb2ffe6d |
| Release 1 HTML S3 version | FoR5j2mkqHvscZXRw0kqTV546fCa3NyG |
| Release 2 HTML S3 version | gU6a2x9eXr.nDxPOxb0MgTmPiGw_pAoQ |
| Shared CSS S3 version | bNUUntS0gwSvuOg83pnfuBtTjN0s9xU_ |
| Invalidation | ICN1KYXRYPHLQQJBFAPBLB5CWP, /*, Completed |

Josh explicitly authorized this deployment. CloudFormation created exactly the
four reviewed resources with rollback enabled. The deployed original template
matched the reviewed source. Initial object writes began after the planned
15-minute wait following bucket/versioning creation.

## Actual publishing and redeployment method

Used AWS CLI with the existing Team7 profile to upload only `site/index.html`
and `site/assets/styles.css` under `index.html` and `assets/styles.css`.
Metadata: respectively `text/html; charset=utf-8` and
`text/css; charset=utf-8`, both `Cache-Control: public,max-age=60`, SSE-S3 and
SHA-256 upload checksums. This used CLI uploads rather than the console steps
in the prepared guide; keys, content and security settings were unchanged.

Release 1 was uploaded and observed before editing Release 2. The second release
changed the release heading to “One change, published.”, changed its explanatory
text and changed the marker to “Team7 Week 2 - Release 2”. That change was
reviewed locally, committed and pushed, then uploaded as a new `index.html`
version. The unchanged CSS was not uploaded again. After invalidating `/*`
and observing Completed, fresh HTTP requests and a browser reload confirmed
Release 2. Both releases matched the reviewed source SHA-256 values through
authenticated S3 downloads and public CloudFront responses.

For another release: review and commit the source, hash it, upload only the
changed website keys with the same metadata, record the new versions, invalidate
the affected paths, wait for completion, then compare downloaded hashes and
capture the visible release. Never upload repository files or private evidence.

## Acceptance results

- [x] Stack CREATE_COMPLETE and CloudFront Deployed; actual identifiers recorded.
- [x] Four public-access blocks true; BucketOwnerEnforced; SSE-S3; versioning enabled; no S3 website configuration.
- [x] Complete bucket policy inspected: exact distribution/account-scoped CloudFront read Allow and insecure-transport Deny; AWS reports IsPublic=false.
- [x] Regional REST origin with OAC s3/always/sigv4; no OAI or website endpoint.
- [x] HTTPS root, index.html and CSS return 200 for both releases; all body hashes match source.
- [x] HTTP returns 301 to the corresponding HTTPS URL for all three tested paths.
- [x] Authenticated exact-object downloads and HeadObject establish existence; unsigned direct-S3 index.html returns AccessDenied/403.
- [x] Tags, root object, managed policies and no WAF association verified.
- [x] Release 2 committed, uploaded, invalidated and observed; previous HTML version retained.
- [x] Genuine screenshots, timestamps, hashes and component descriptions recorded.
- [ ] Independently confirm the distribution billing plan: organization policy denies PricingPlanManager ListSubscriptions.
- [ ] Copy the supplied App/DevOps fields into the shared official form and complete final PR/course review.

[Form entries](SCRUM-17-form-entries.md) contain the precise Website and Evidence
fields owned by App/DevOps. No live course form was available to edit here;
its submission has not been claimed. VM facts and SSH test results belong to
SCRUM-16/18 and remain separate inputs to SCRUM-19.

## Evidence and limitations

[Evidence index](evidence/SCRUM-17/README.md), [Release 1 checks](evidence/SCRUM-17/release1-verification.json),
[Release 2 checks](evidence/SCRUM-17/release2-verification.json), and
[screenshot provenance](evidence/SCRUM-17/screenshots.json).

The screenshot date is October 14 in UTC (October 13 in America/Chicago).
JPEG is the browser's native screenshot format; originals were copied unchanged.
The images show public content, with their source URL recorded in the manifest.

No pricing-plan subscription was created. Pay-as-you-go is the intended model,
but the independent lookup is denied by the organization's policy; neither
PriceClass_100 nor the stack's literal PricingModel output proves billing state.
No permissions or policies were changed to bypass that restriction.

CloudTrail event history includes the actual change-set writes. No configured
trail was returned, so durable retention is not established. WAF and paid request
logging remain absent under the approved course scope. Bucket and policy are
retained on stack deletion; future cleanup needs explicit review.

## Week 3 handoff

Use the exact HTTPS origin above for CORS planning. No visitor counter, API or
JavaScript integration is implemented in this static site. The current HTML CSP
does not allow scripts or API connections, so review it when implementing those
features. Keep the S3 origin private and continue publishing through CloudFront.
