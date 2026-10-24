# SCRUM-24: Application API specification

**Status:** Working draft for review. Deployment and functional results are documented in October 19 handoffs; Josh's foreign-origin browser check is documented in an October 20 screenshot review. End-of-week screenshots, official course-form review, and final PDF remain outstanding.
**Branch:** `feature/SCRUM-24-application-api-spec`
**Ticket:** [SCRUM-24](https://joshescobarx.atlassian.net/browse/SCRUM-24).
**Last updated:** October 24, 2026.

## Status summary

The deployment/configuration and test results below are reported in Josh's PR #10 draft and its linked October 19–20 handoffs. No fresh AWS test was run for this document update. Course-form completion, remaining end-of-week screenshots, final review, PDF, and submission are not claimed complete.

| Work item | Current status | Evidence boundary |
| --- | --- | --- |
| SCRUM-21 / 47 / 48 datastore | Table deployed; initial zero was verified before API tests; subtasks reported Done. | Parent remains In Review for course evidence/datastore review (PR #10's October 20 status snapshot). |
| SCRUM-22 / 49 / 50 API | Lambda, API, and website deployed; live counter tests passed; subtasks reported Done. | Parent remains In Review for course evidence/specification review (October 20 snapshot). |
| SCRUM-23 / 51 CORS | Exact-origin CORS, HTTP negative tests, and foreign-origin browser rejection documented; SCRUM-51 reported Done. | Parent remains In Review for final evidence/specification review (October 20 snapshot). |
| SCRUM-52 browser/security | Browser code and deployed role/environment checks reported complete; ticket Done. | Include the result in the course evidence. |
| SCRUM-20 / 46 request flow | Architect-owned flow is in PR #10 and its request-flow document. | Josh's review and final course evidence remain. |
| SCRUM-24 specification | Shared working draft; Jira reported In Progress under Alyssa. | Official form completeness, screenshots, review, PDF, and separate submission record remain (October 20 snapshot). |

## Purpose and scope

This document records the application/API design and the deployment and functional test results reported by the SCRUM-24 Jira handoff. Deployment details and test results are distinguished from screenshots and other course artifacts that still need to be collected and reviewed.

The API endpoint is `https://24prug4iuj.execute-api.us-east-2.amazonaws.com/visits`; the operation is `POST /visits`.

## Verified architecture today

The current website is static content in a private S3 bucket, delivered to visitors over HTTPS by CloudFront. The deployed website and its recorded verification are documented in [the SCRUM-17 handoff](../week2/SCRUM-17-handoff.md) and [its evidence index](../week2/evidence/SCRUM-17/README.md).

| Component | Verified information | What it means for this API |
| --- | --- | --- |
| CloudFront | The deployed distribution is `cf-site-team07` (`E1PBX75YJOS2B9`); the HTTPS site is `https://d3jg1ev4a532iw.cloudfront.net/`. CloudFront serves the static site from a private S3 REST origin using OAC. | The website origin is known. It is not evidence that an API origin or CloudFront API behavior exists. |
| API Gateway | `api-visitor-team07` (ID `24prug4iuj`); HTTP API; `POST /visits`; `$default` stage with auto-deploy. Endpoint: `https://24prug4iuj.execute-api.us-east-2.amazonaws.com/visits`. | Browser calls the endpoint directly. Deployment values are documented in the October 19 API handoff; no fresh AWS query was made for this update. |
| Lambda | `lambda-visitor-team07`; Python 3.13, arm64, 256 MB, five-second timeout. | Invoked through API Gateway's Lambda proxy integration (payload format 2.0); uses an IAM execution role. Configuration is from the deployment handoff, not a fresh AWS inspection. |
| Execution role | `role-lambda-team07`; inline policy `policy-visitor-ddb-team07`; no attached managed policies. | Deployment handoff records exact-table `UpdateItem`, restricted to leading key `site`, plus writes to its own log streams; no `GetItem`, `PutItem`, or `DeleteItem` grant is described. |
| DynamoDB | `ddb-visitor-team07`, `us-east-2`, `ACTIVE`, `PAY_PER_REQUEST`, `STANDARD`; partition key `id` (String), no sort key/indexes; item `id=site` with numeric `count`. | API stack `cfn-visitor-api-team07` references the existing table owned by `cfn-visitor-data-team07`. Its live count is not assumed here. |

The component settings above reflect the October 19 deployment handoff/evidence, while the HTTP and browser outcomes below reflect their linked test records. Template/source settings describe intended configuration by themselves; they are not deployment proof. No AWS inspection was run for this document update.

## API contract and reported functional tests

The endpoint/configuration is documented in Josh's PR #10 draft and the October 19 deployment handoff. Test outcomes below are recorded in linked October 19 HTTP/browser evidence; the October 20 foreign-origin browser result is documented by a screenshot review record. This update did not run fresh tests.

| Contract item | Decision |
| --- | --- |
| API type and route | API Gateway HTTP API; `POST /visits`. |
| Endpoint | `https://24prug4iuj.execute-api.us-east-2.amazonaws.com/visits` |
| Request | `Content-Type: application/json`; body must be exactly `{}`. Caller-supplied key, count, or table values are not accepted. |
| Successful response | HTTP 200; JSON `{"count":N}` with a positive safe integer; `Content-Type: application/json`; `Cache-Control: no-store`. |
| Invalid request | HTTP 400 / `invalid_request` for invalid content or body, before a write. |
| Origin rejection | HTTP 403 / `origin_not_allowed` for missing or foreign Origin, before a write. The browser may hide the response body under CORS. |
| CORS/preflight | Exact origin `https://d3jg1ev4a532iw.cloudfront.net`; methods POST/OPTIONS; header `content-type`; credentials disabled; max age 300 seconds. API Gateway handles OPTIONS without invoking the counter Lambda or writing to DynamoDB. |
| Foreign-origin tests | HTTP evidence records foreign OPTIONS as 204 without a matching allow-origin header and foreign/missing-Origin POST as 403 without increment. The October 20 browser screenshot review records Chrome rejecting the foreign-origin preflight. |
| Unmatched route/method | Unmatched public route returns API Gateway HTTP 404; a defensive direct-Lambda wrong-method guard returns 405. |
| Counter failure | HTTP 503 / `counter_unavailable` for failed condition, datastore/access error, or invalid returned count. No reset or automatic retry. |
| Authentication | Public demo API (`AuthorizationType: NONE`). CORS and Origin checks are not authentication; non-browser clients can spoof Origin. |
| Atomic update | One conditional `UpdateItem` on `{ "id": "site" }`: `SET #count = #count + :one`, with `:one=1`, `ReturnValues=UPDATED_NEW`. Requires an existing item with numeric, nonnegative count below JavaScript's maximum safe integer. Lambda never seeds or resets it. |
| Historical observations | Initial `count=0` was read before API tests; tests returned counts 1–4, and a later browser load displayed 5. These are historical observations, not the current count. |
| Throttling/platform errors | `$default` stage limit 2 requests/second, burst 5; best effort, not a hard spending cap. Gateway/platform behavior may return 429 or 5xx. |
| Retry and display | Browser/SDK does not automatically retry; browser request timeout is eight seconds. Failure displays “Temporarily unavailable.” A response may be lost after a successful write, so retries/reloads can count again; exactly-once delivery is not guaranteed. Reloads and test traffic count; this is not a unique-visitor metric. |
| Logging | API access logs record request ID, route, status, integration status, and response length; Lambda logs error category and request ID. Both log groups retain logs for seven days. API access logs omit bodies, headers, and client IPs. |
| DynamoDB table/item | `ddb-visitor-team07`; `id` String partition key; counter item `id=site`; numeric `count`. The current value is not specified. |

## Application request flow — deployment and testing reported

The following end-to-end flow is documented in Josh's PR #10 handoff and the SCRUM-24 Jira handoff:

```mermaid
flowchart LR
  Browser[Visitor browser] -->|HTTPS site request| CF[CloudFront]
  CF -->|OAC origin request| S3[Private S3 website]
  S3 -->|site content| CF
  CF -->|HTML, CSS, and JavaScript| Browser
  Browser -->|POST /visits, JSON body {}| API[API Gateway HTTP API]
  API -->|Lambda proxy payload 2.0| Lambda[lambda-visitor-team07]
  Lambda -->|conditional atomic UpdateItem| DDB[DynamoDB ddb-visitor-team07]
  DDB -->|UPDATED_NEW numeric count| Lambda
  Lambda -->|HTTP 200 JSON count| API
  API -->|CORS-approved response| Browser
  Browser -->|display count| Visitor[Visitor]
```

The website is `https://d3jg1ev4a532iw.cloudfront.net/`. CloudFront serves cached content or retrieves it from the private S3 origin through OAC. The browser calls the API directly; CloudFront does not proxy API requests. The browser sends `{}` with credentials omitted, validates the integer response, and displays it using `textContent`.

## Security and deployment notes

- Keep the static S3 origin private and continue using CloudFront OAC, as verified for SCRUM-17.
- Do not place secrets in browser code, site files, Lambda environment variables committed to Git, or this specification.
- The Jira handoff reports that the Lambda uses an IAM execution role rather than embedded AWS access keys. Do not add credentials to browser code, site files, environment values committed to Git, or this specification.
- The allowed CORS origin is exactly `https://d3jg1ev4a532iw.cloudfront.net`; foreign-origin browser access was blocked in reported testing. CORS and Origin checks do not authenticate callers.
- The API Gateway invoke permission is scoped to the API/account/stage/method/route. The Lambda role is scoped to `UpdateItem` on the visitor table and partition key `site`, plus writes to its own log streams; no `GetItem`, `PutItem`, or `DeleteItem` grant or attached managed policy is described. The function environment contains `TABLE_NAME` and `ALLOWED_ORIGIN` only.
- The deployment handoff says API access logs omit request bodies, headers, and client IPs. The source HTML's blank API URL is a build input; the deployed release builder inserts the endpoint and the exact API host in CSP.
- The counter uses the existing DynamoDB table. This document authorizes no deployment or AWS resource change.
- All AWS changes remain subject to the repository's read-only-by-default policy. This document authorizes no deployment or resource change.

## Course evidence and finalization still outstanding

- [ ] Locate the official course specification form and map the completed specification into its required fields.
- [ ] Josh and Alyssa: collect genuine console/browser screenshots at the end of Week 3 using the course filename convention and actual capture date; preserve the counter's true current value.
- [ ] Alyssa: map every section to the official Application & API Design Specification fields, including the full DynamoDB table ARN from private Jira/stack output. The full ARN is intentionally not copied here.
- [ ] Josh: review request flow, API contract, evidence, and security results. Alyssa: review datastore values and final assembly.
- [ ] Check completeness, correctness, authenticity, and consistency; include the required evidence and component descriptions.
- [ ] Generate and review the final course PDF when the remaining inputs are complete; record submission separately. No course-form review, final PDF, approval, or submission is claimed complete.

## Evidence and source references

- [PR #10](https://github.com/greycarpet/Team7/pull/10): Josh's open draft targeting this SCRUM-24 branch. Its head is `feature/SCRUM-20-verified-request-flow` at `02f1d19`; it has no comments or reviews in the GitHub CLI result. Its specification and flow details were compared for this review; the PR was not merged.
- [PR #10 proposed specification](https://github.com/greycarpet/Team7/blob/02f1d19/docs/week3/SCRUM-24-application-api-spec.md) and [request-flow handoff](https://github.com/greycarpet/Team7/blob/02f1d19/docs/week3/SCRUM-20-request-flow.md): deployed configuration, contract, trust boundaries, retry/throttling/logging details, and remaining course work.
- [Datastore deployment handoff](https://github.com/greycarpet/Team7/blob/54825ef4c11b5dc8133f71feff33a001e8b8de7c/docs/week3/SCRUM-21-deployment-handoff.md) and [API deployment handoff](https://github.com/greycarpet/Team7/blob/14e6c7104e15001b975de4a5cef7543fa82dbc5c/docs/week3/SCRUM-22-deployment-handoff.md): recorded deployed resources/configuration and deployment boundary.
- [API deployment evidence](https://github.com/greycarpet/Team7/blob/14e6c7104e15001b975de4a5cef7543fa82dbc5c/docs/week3/evidence/SCRUM-22/20261019_Team7_aws_w3-api-deployment.json), [HTTP test evidence](https://github.com/greycarpet/Team7/blob/14e6c7104e15001b975de4a5cef7543fa82dbc5c/docs/week3/evidence/SCRUM-22/20261019_Team7_aws_w3-api-tests.json), and [website verification](https://github.com/greycarpet/Team7/blob/14e6c7104e15001b975de4a5cef7543fa82dbc5c/docs/week3/evidence/SCRUM-22/20261019_Team7_aws_w3-site-verification.json): October 19 deployment and functional records, not screenshots or fresh tests from this update.
- [October 20 CORS screenshot review record](https://github.com/greycarpet/Team7/blob/02f1d19b635871d01389b81387753e1979dbdff8/docs/week3/evidence/SCRUM-22/20261020_Team7_browser_w3-cors-negative-review.json): records Josh's supplied, unchanged screenshot and its provenance; the original remains private. This check is complete, but the record does not show Network-panel OPTIONS status/raw headers or a fresh DynamoDB read.
- [Jira SCRUM-24](https://joshescobarx.atlassian.net/browse/SCRUM-24): ticket reference. PR #10 says Jira was checked October 20; status values above are that dated snapshot, not a fresh Jira query in this turn.
- [Week 2 SCRUM-17 handoff](../week2/SCRUM-17-handoff.md) and [evidence index](../week2/evidence/SCRUM-17/README.md): earlier CloudFront/private S3 verification.
- No Week 3 screenshot originals, official course form, final PDF, review approval, or submission are included or claimed complete in this working branch.

