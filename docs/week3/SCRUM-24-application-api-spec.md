# SCRUM-24: Application and API design specification

**Status:** Working draft for review. Data, API and website deployment are verified in the October 19 records. The foreign-origin browser check passed in Josh’s supplied October 20 screenshot. Remaining end-of-week screenshots, final course-form review and PDF are pending.

**Owner:** Alyssa. **Architect / application / security reviewer:** Josh Escobar.

**Ticket:** [SCRUM-24](https://joshescobarx.atlassian.net/browse/SCRUM-24). **Updated:** October 20, 2026.

This revision builds on Alyssa's draft at commit `a8b2ee66d35c216301afcf6312011379b1bf7f6c`. It replaces preparation-only status with the recorded deployment results in PRs [#8](https://github.com/greycarpet/Team7/pull/8) and [#9](https://github.com/greycarpet/Team7/pull/9). Jira was checked directly through the plugin on October 20. This draft does not claim a fresh AWS test, official form edit, final PDF export, reviewer approval or course submission.

## Purpose and status

The Team7 website displays a page-view counter. Each accepted POST causes one atomic increment of a fixed DynamoDB item and returns the new numeric count. Reloads and test traffic are included; this is not a unique-visitor measure.

| Work item | Verified progress | Remaining acceptance |
| --- | --- | --- |
| SCRUM-21 / 47 / 48 | DynamoDB deployed; initial zero conditionally seeded and verified; subtasks Done | Parent In Review for course evidence and datastore review |
| SCRUM-22 / 49 / 50 | Lambda, API and website deployed; live counter tests passed; subtasks Done | Parent In Review for course evidence and specification review |
| SCRUM-23 / 51 | Exact-origin CORS, allowed-origin browser, HTTP negative tests and foreign-origin browser rejection verified | SCRUM-51 Done; parent In Review for final evidence/specification review |
| SCRUM-52 | Browser code and deployed role/environment checks complete; Done | Include recorded result in final evidence |
| SCRUM-20 / 46 | Architect-owned flow populated below and detailed handoff prepared | Josh's review and final course evidence |
| SCRUM-24 | Shared working draft assembled; Jira In Progress under Alyssa | Official form completeness, screenshots, review, PDF and separate submission record |

## Deployed components

| Component | Actual configuration and responsibility |
| --- | --- |
| Website | https://d3jg1ev4a532iw.cloudfront.net/; HTTPS static page with external counter script |
| CloudFront / S3 | cf-site-team07, distribution E1PBX75YJOS2B9; private S3 REST origin s3-site-team07-a7f391 with OAC; static delivery |
| HTTP API | api-visitor-team07, ID 24prug4iuj; POST /visits; $default stage with auto-deploy; Lambda integration |
| Lambda | lambda-visitor-team07; Python 3.13, arm64, 256 MB, 5-second timeout |
| Execution role | role-lambda-team07, inline policy policy-visitor-ddb-team07; exact-table UpdateItem restricted to site and own log writes; no attached managed policies |
| DynamoDB | ddb-visitor-team07; id String partition key, no sort key/indexes; item id=site with numeric count |
| CloudFormation | cfn-visitor-data-team07 owns the table; cfn-visitor-api-team07 references that existing table |
| Workload region | us-east-2 |

The API stack reached CREATE_COMPLETE at **October 19, 2026, 20:04:51.881 CDT**. Deployed code: `e7e283dd5ba6494588254ef8853239d10e8072df`. Evidence commit: `14e6c7104e15001b975de4a5cef7543fa82dbc5c`. PRs #8 and #9 remain draft/unmerged at this review; deployment and Git merge are separate states.

## Architect-owned request flow

The visitor loads `https://d3jg1ev4a532iw.cloudfront.net/`. CloudFront delivers HTML, CSS and JavaScript from cache or the private S3 origin `s3-site-team07-a7f391` using OAC. The browser calls `POST https://24prug4iuj.execute-api.us-east-2.amazonaws.com/visits` directly with Content-Type application/json, body `{}` and credentials omitted. API Gateway handles browser preflight and allows the exact CloudFront origin. Its $default stage routes POST /visits through a Lambda proxy integration with payload 2.0 to `lambda-visitor-team07`. Lambda validates the request and uses `role-lambda-team07` for one conditional atomic UpdateItem on `ddb-visitor-team07`, key id=site, adding 1 to count and requesting UPDATED_NEW. The function returns HTTP 200 and `{"count":N}` through API Gateway. The website validates and displays the integer using textContent.

CloudFront delivers static files; the browser connects directly to the API. The release builder fills the source HTML's blank endpoint and allows the exact API host in CSP. The deployed files and browser result were verified. See [SCRUM-20 request flow](SCRUM-20-request-flow.md) for the diagram, failure paths, resource mapping and evidence.

## Infrastructure-owned datastore fields

| Field | Recorded deployed value |
| --- | --- |
| Table / stack | ddb-visitor-team07 / cfn-visitor-data-team07 |
| Partition key | id, String (S) |
| Sort key / indexes | None |
| Capacity / class | PAY_PER_REQUEST / STANDARD |
| Item | id=site (String); count (Number) |
| Initial seed | count=0; strong GetItem on October 19, 2026 at 19:32:26 CDT, before API tests |
| Subsequent observation | count=5 after four HTTP tests and one browser load; historical value, not the current count |
| Encryption | AWS-owned key; SSEEnabled=false selects this mode and does not mean unencrypted |
| Protection | Deletion protection; CloudFormation Retain on deletion/replacement; PITR disabled |
| Table ARN | arn:aws:dynamodb:us-east-2:ACCOUNT_ID:table/ddb-visitor-team07; use the actual full ARN recorded privately in Jira or stack output VisitorTableArn for the course form |

Initial seeding required an absent item. Lambda never seeds or resets the counter. Preserve the original zero evidence and the true current value for end-of-week screenshots.

## Application-owned endpoint specification

| Field | Contract |
| --- | --- |
| API base URL | https://24prug4iuj.execute-api.us-east-2.amazonaws.com |
| Method / path / stage | POST /visits; $default; no URL stage prefix |
| Full endpoint | https://24prug4iuj.execute-api.us-east-2.amazonaws.com/visits |
| Request | Content-Type application/json; empty JSON object {}; exact website Origin; no caller-supplied key/count/table |
| Success | HTTP 200; JSON {"count":N}, positive safe integer; Content-Type application/json; Cache-Control no-store |
| Invalid request | HTTP 400 / invalid_request for invalid content/body |
| Origin rejection | HTTP 403 / origin_not_allowed for missing/foreign Origin; browser CORS may hide the body |
| Counter failure | HTTP 503 / counter_unavailable for failed condition, datastore/access error or invalid returned count |
| Other route/method | Public unmatched route returns API Gateway 404; defensive direct-Lambda method guard returns 405 |
| Preflight | API Gateway handles OPTIONS without a counter write |
| Throttling / platform errors | 2 requests/sec, burst 5; best effort; 429 or gateway-dependent 5xx may occur |
| Retry / display | No automatic browser/SDK retry; 8-second browser timeout; failure displays Temporarily unavailable |

The update condition requires an existing item with a numeric, nonnegative count below JavaScript's maximum safe integer. The returned integer is checked. Atomic increments prevent lost updates, but a response may be lost after a successful write; exactly-once delivery is not guaranteed. Throttling and the $5 budget alert are not hard spending caps.

## Security-owned CORS and credential validation

| Control | Recorded result |
| --- | --- |
| Allowed origin | Exactly https://d3jg1ev4a532iw.cloudfront.net; POST/OPTIONS; content-type; credentials false; max age 300 seconds |
| Allowed browser | Live CloudFront page displayed count 5 with correct endpoint/CSP and no site CSP/CORS errors |
| HTTP negative checks | Foreign OPTIONS: 204 without matching allow-origin; foreign/missing-Origin POST: 403 without incrementing |
| Foreign-origin browser | **Passed October 20.** Josh’s screenshot shows origin https://example.org and Chrome explicitly rejecting the actual API preflight for missing Access-Control-Allow-Origin; Console time 23:53:22.051Z / 18:53:22.051 CDT |
| Browser credentials | Delivered HTML/JS matched reviewed files; inspection and credential-pattern checks passed |
| Lambda credentials | Execution-role temporary credentials; environment contains only TABLE_NAME and ALLOWED_ORIGIN |
| Invocation / data access | API-to-Lambda permission scoped to API/account/stage/route; Lambda UpdateItem scoped to exact table and site key |
| Logs | API request ID, route, status, integration status and response length; Lambda error categories/request ID; both log groups retain seven days |

This is a public demo API with AuthorizationType NONE. CORS and Origin checking are not authentication; external clients can spoof Origin. Pattern scanning is supporting evidence, not a universal guarantee. The separate API Gateway service-linked role and resource-scoped CloudWatch delivery policy are documented in the deployment evidence.

## Recorded verification and evidence

| Evidence | Result and boundary |
| --- | --- |
| [Datastore handoff](https://github.com/greycarpet/Team7/blob/54825ef4c11b5dc8133f71feff33a001e8b8de7c/docs/week3/SCRUM-21-deployment-handoff.md) | Table ACTIVE; schema/settings and initial-zero strong read |
| [API deployment handoff](https://github.com/greycarpet/Team7/blob/14e6c7104e15001b975de4a5cef7543fa82dbc5c/docs/week3/SCRUM-22-deployment-handoff.md) | Nine resources completed; deployed template/configuration matched; website release and manual CORS procedure |
| [HTTP test record](https://github.com/greycarpet/Team7/blob/14e6c7104e15001b975de4a5cef7543fa82dbc5c/docs/week3/evidence/SCRUM-22/20261019_Team7_aws_w3-api-tests.json) | One sequential and three concurrent increments returned distinct counts 1–4; strong read confirmed total; negative requests did not increment |
| [Browser record](https://github.com/greycarpet/Team7/blob/14e6c7104e15001b975de4a5cef7543fa82dbc5c/docs/week3/evidence/SCRUM-22/20261019_Team7_browser_w3-counter-verification.json) | October 19 historical record: allowed-origin count; foreign-origin check pending at that time |
| [Website verification](https://github.com/greycarpet/Team7/blob/14e6c7104e15001b975de4a5cef7543fa82dbc5c/docs/week3/evidence/SCRUM-22/20261019_Team7_aws_w3-site-verification.json) | HTML/JS hashes matched; private S3 index returned 403; credential-pattern check passed |

The October 19 records are deployment/test records rather than screenshots. The [October 20 browser review](https://github.com/greycarpet/Team7/blob/02f1d19b635871d01389b81387753e1979dbdff8/docs/week3/evidence/SCRUM-22/20261020_Team7_browser_w3-cors-negative-review.json) documents Josh’s genuine supplied screenshot, including its SHA-256. Its explicit CORS diagnostic closes the browser-test gap. The original remains private and unchanged. The screenshot does not show Network-panel OPTIONS status/raw headers or a fresh DynamoDB count; the printed time is the client Console clock. The prior draft used preparation commit e7e283d; the later evidence commit supplies the actual endpoint and live results. Do not repeat deployment or seeding because the earlier draft marked them pending.

## Remaining work and final review

- [x] Josh: foreign-origin browser check completed. The supplied screenshot shows the exact foreign origin and endpoint, and Chrome explicitly identifies preflight CORS rejection rather than a generic CSP/network failure. See the October 20 review record; raw Network-panel headers/status are not claimed.
- [ ] Josh and Alyssa: collect genuine console/browser screenshots at the end of Week 3, using the course filename convention and actual capture date. Preserve the counter's true current value.
- [ ] Alyssa: map these sections to every official Application & API Design Specification field, including the full table ARN from private Jira/stack output. This repository draft does not establish official form completion.
- [ ] Josh: review the flow, contract, evidence and security result. Alyssa: review datastore values and final assembly.
- [ ] Check Completeness, Correctness, Authenticity and Consistency; include required evidence and component descriptions.
- [ ] Generate and review the final course PDF after the remaining inputs are complete. Record submission separately from PDF readiness.

All AWS changes remain subject to AGENTS.md. This documentation revision changes no AWS resource, website object, counter value or deployment approval scope.
