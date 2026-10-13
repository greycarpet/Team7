# SCRUM-17: Private S3 and CloudFront website

**Status:** Prepared for review; AWS deployment is not authorized or completed.
**Owner:** Josh Escobar. **Prepared:** October 13, 2026.
**Tickets:** [SCRUM-17](https://joshescobarx.atlassian.net/browse/SCRUM-17), SCRUM-42, SCRUM-43.

The website runs independently of the tools EC2 instance. This change prepares
the website source, infrastructure, and verification procedure. Actual HTTPS,
private-origin, and redeployment results must be collected after deployment.

## Reviewed scope

| Action | Resource | Name / purpose |
| --- | --- | --- |
| Create | S3 bucket | `s3-site-team07-a7f391`, private website origin in Ohio |
| Create | S3 bucket policy | CloudFront object reads scoped to this distribution/account; deny non-TLS access |
| Create | CloudFront OAC | `oac-site-team07`, always sign S3 requests with SigV4 |
| Create | CloudFront distribution | Name tag/comment `cf-site-team07`, default HTTPS hostname |

Proposed stack: **`cfn-site-team07`**, following `cfn-{workload}-{team}`.
Target: the existing Team7 account, stack/S3 region **us-east-2**. CloudFront is
global; its API endpoint uses us-east-1. The four resources are managed by
[site.yaml](../../infrastructure/cloudformation/week2/site.yaml).

No existing resources are updated, replaced, or deleted by this new-stack plan.
There are no IAM roles, access keys, WAF resources, EC2 resources, network changes,
custom domains, certificates, edge functions, or pricing-plan resources. The
bucket policy is security-sensitive and is included in the deployment review.

The bucket name was selected with Josh from the approved naming standard. Its
global availability remains unproven until AWS checks creation. Do not silently
change the suffix or create a second stack to work around a collision.

Required tags are on the bucket and distribution. OAC and bucket policy do not
support the same resource tags; use their approved name/description and stack
ownership. Apply the standard Project, Team, Environment, Workload, Component,
ManagedBy, Repository, and JiraProject tags to the stack as supported.

## Access, caching, and retained data

- All four S3 public-access blocks remain enabled. BucketOwnerEnforced disables
  ACLs; SSE-S3 encrypts stored objects. S3 website hosting remains disabled.
- CloudFront uses the bucket's regional REST hostname, GET/HEAD only, root
  `index.html`, HTTP-to-HTTPS redirection, and the default CloudFront certificate.
- The policy grants only `s3:GetObject` to `cloudfront.amazonaws.com`, restricted
  by the exact distribution ARN and source account. A separate explicit Deny
  protects bucket/object requests over insecure transport. Authorized account
  deployment roles can still upload with appropriate existing permissions.
- Resolve managed policies by name before deployment. The checked IDs and full
  configurations are recorded in [preflight evidence](evidence/SCRUM-17/preflight.redacted.json)
  and supplied through [parameters](../../infrastructure/cloudformation/week2/site.parameters.json).
- `Managed-CachingOptimized` excludes cookies/query strings from the cache key
  and supports compression. Its one-second minimum TTL is intentional for public
  static content; it can override `no-cache`, `no-store`, or `private` for that
  second. Use `Cache-Control: public,max-age=60` for both current files and
  invalidate `/*` after a release. Query-string cache busting is insufficient.
- `Managed-SecurityHeadersPolicy` supplies HSTS, content-type protection,
  SAMEORIGIN framing, and referrer/XSS headers. It supplies **no CSP header**.
  The static HTML adds a restrictive CSP meta tag, with same-origin CSS/images
  and no scripts/forms. Review CSP when adding the Week 3 API/JavaScript; do not
  claim that the managed policy supplies CSP or CORS.
- Versioning preserves earlier uploads. Bucket and policy use Retain for stack
  deletion/replacement, so storage and the retained policy require explicit
  ownership/cleanup review later. No lifecycle deletion is configured.

The course excludes WAF. The proposal follows SCRUM-15's basic-metrics-only cost
scope: no paid access logs, CloudTrail data events, custom metrics, or Shield
Advanced subscription. This limits request-level investigation and is not a
production monitoring design. Revisit those controls with their cost impact if
the scope changes. Existing audit configuration has not been asserted as verified.

## Cost impact

Use **pay-as-you-go**, not a flat-rate subscription. `PriceClass_100` is an edge
location selection, not a billing-plan selector. Confirm pricing and absence of
a WAF association in the deployed console/API before accepting the result.

The [SCRUM-15 draft estimate](https://github.com/greycarpet/Team7/pull/4) models
1 GB-month across all current/noncurrent/staging objects, 1,000 S3 write/list
requests, 10,000 S3 reads, 1 GB CloudFront delivery to North American viewers,
10,000 HTTPS requests and 10 invalidation paths. S3 is **$0.032/month**, rounded
to **$0.03**, before promotional credits/tax. CloudFront is modeled at $0 only
while the shared recurring allowances remain available. With those CloudFront
allowances exhausted, modeled website cost is approximately **$0.18/month**.
These are estimates, not caps or measured bills. The complete Week 2 lab estimate
remains $0.98/month including the separate tools VM; this website is already
included in that total. Retained versions and unexpected traffic can add cost.

Pricing references: [S3](https://aws.amazon.com/s3/pricing/),
[CloudFront pay-as-you-go](https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/).

## Files to publish

| Local source | S3 key | Content-Type | Cache-Control |
| --- | --- | --- | --- |
| `site/index.html` | `index.html` | `text/html; charset=utf-8` | `public,max-age=60` |
| `site/assets/styles.css` | `assets/styles.css` | `text/css; charset=utf-8` | `public,max-age=60` |

No build is needed. Publish only these two files; keep evidence, templates,
repository metadata and billing information out of the site bucket. The release
manifest records their SHA-256 hashes. Preview with a local HTTP server before
upload. This initial page is a proposed course landing page, pending Josh's review.

## Deployment sequence after explicit approval

1. Record the reviewed commit, stack name, parameters, costs, and content. Confirm
   Team7 account and Ohio. Re-resolve the managed policy names and check resource
   inventory/collisions. Read-only inventory so far returned no S3 buckets;
   CloudFront distribution/OAC calls returned empty objects, which are insufficient
   to assert a complete zero-resource inventory.
2. In CloudFormation, prepare a new-stack change set for `cfn-site-team07` using
   this exact template and parameters. Keep rollback enabled. Review its service
   validation and changes: exactly the four additions above, no unexpected writes.
   If the console stages the template in S3, identify that staging destination and
   its access/cost separately before allowing it; do not create an unreviewed bucket.
3. Execute only under the repository's `DEPLOYMENT AUTHORIZED` approval, covering
   the exact resource/content plan. Wait for CREATE_COMPLETE and CloudFront Deployed.
4. Inspect stack outputs and all controls in the handoff checklist. After initial
   versioning enablement, allow AWS's recommended 15 minutes before object writes.
5. Upload the two Release 1 files through S3 Console, preserving keys and metadata.
   Confirm Release 1 at HTTPS `/` and `/index.html`, CSS load, HTTP redirect,
   known-object existence, and unsigned direct-S3 denial.
6. Change the visible marker to `Team7 Week 2 - Release 2` and release heading/copy,
   review/commit/hash that content, then upload under the same keys. Record new
   object Version IDs. Invalidate `/*`, wait for Completed, and test again using
   a fresh browser request. Do not prepare the second upload before Release 1
   has actually been observed.
7. Compare authenticated downloads to source SHA-256 values; ETags are not a
   substitute. Capture genuine deployment evidence and complete the handoff.
   Leave the HTTPS website available with the bucket private and WAF disabled.

CloudFormation does not upload website content. CloudFront propagation, bucket
name availability, account permissions, service quotas, and successful live
delivery remain deployment-time checks; local validation does not prove them.

## Recovery

For content recovery, review the previous source/object version, upload those
bytes as a new current version, invalidate the changed paths, and retest.
Do not delete versions or weaken bucket access to fix a 403. For infrastructure
failure, inspect events and the actual retained resources before proposing a
reviewed update; do not delete/recreate the stack automatically.

## Validation and references

See [validation record](evidence/SCRUM-17/validation.md) and
[handoff checklist](SCRUM-17-handoff.md). No deployment check is marked passed.
The official shared form requires the actual HTTPS URL, redeployment method,
deployment screenshot, and one-line component descriptions; the ticket also
requires private S3/OAC and a verified changed release. Additional console views
in the guide corroborate those outcomes; they are not an extra screenshot count
imposed by the form itself.

Sources: Jira SCRUM-17; attached SCRUM-17 How-To v2.0; official
`02_Solution_Architecture_Document.md`; [approved naming standard](../week1/Design_Standards_Cloud_Architect/01_Cloud_Foundation_and_Naming_Standard.md);
[AWS OAC guidance](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html);
[managed response headers](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-response-headers-policies.html);
[S3 versioning guidance](https://docs.aws.amazon.com/AmazonS3/latest/userguide/manage-versioning-examples.html).
