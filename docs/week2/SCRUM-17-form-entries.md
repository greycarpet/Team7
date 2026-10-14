# SCRUM-17: entries for the official Solution Architecture form

These are verified App/DevOps inputs for SCRUM-19. Copy them into the official
form; this file does not claim that the live form has been submitted. Leave
Infrastructure VM facts and Security/Ops SSH results for SCRUM-16/18.

## Website · App / DevOps

**Website URL (HTTPS):** https://d3jg1ev4a532iw.cloudfront.net/

**How you redeployed a change:** Edited index.html to show “Team7 Week 2 - Release 2”
and updated the release notes. Reviewed and committed the change, uploaded it
to the same private S3 key using AWS CLI, then invalidated /* in CloudFront.
After invalidation completed, refreshed the HTTPS site and verified the new
release and matching file hashes.

## Evidence · everyone

**Deployment screenshot:** 20261014_Team7_aws_w2-site-release2.jpg

[Open the screenshot](evidence/SCRUM-17/20261014_Team7_aws_w2-site-release2.jpg).
Captured on October 14 UTC, which was October 13 in Central time.

**What each component does:**

- s3-site-team07-a7f391 stores the website files privately with encryption and versioning.
- cf-site-team07 (E1PBX75YJOS2B9) serves the website through its HTTPS CloudFront address and redirects HTTP requests to HTTPS.
- oac-site-team07 signs CloudFront's requests to the private S3 origin.
- The site bucket policy permits this CloudFront distribution to read website objects and denies insecure transport.

## Supporting verification

Both Release 1 and Release 2 returned HTTPS 200 for the page and stylesheet,
redirected HTTP to the corresponding HTTPS paths, and denied unsigned access
to the known existing S3 index.html object. Authenticated S3 and public CloudFront
downloads matched source SHA-256 hashes. WAF remains unassociated.

The final architecture/cost review should retain the limitation that an
organization policy prevented independent billing-plan verification. No
pricing-plan subscription was created by this deployment.
