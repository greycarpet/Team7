# SCRUM-22 deployment handoff

Deployed after Josh's **DEPLOYMENT AUTHORIZED** at **October 19, 2026, 20:02:02 CDT**. Approved code commit: `e7e283dd5ba6494588254ef8853239d10e8072df`, [PR #9](https://github.com/greycarpet/Team7/pull/9). Region: **us-east-2**. No PR was merged.

The stack reached **CREATE_COMPLETE at 20:04:51.881 CDT** (2026-10-20T01:04:51.881Z), with all nine planned resources complete. The change set contained only the nine reviewed Add actions and no validation errors. The deployed template exactly matched the approved template.

| Handoff field | Verified value |
|---|---|
| Stack | cfn-visitor-api-team07 |
| Website | https://d3jg1ev4a532iw.cloudfront.net/ |
| Endpoint | **POST https://24prug4iuj.execute-api.us-east-2.amazonaws.com/visits** |
| API / stage | api-visitor-team07 / 24prug4iuj / $default |
| Integration / route | ack7qg8 / ho9l4vg / POST /visits |
| Function | lambda-visitor-team07; Active; Python 3.13; arm64; 256 MB; timeout 5 s |
| Execution role / inline policy | role-lambda-team07 / policy-visitor-ddb-team07; no attached managed policies |
| Datastore | Existing ddb-visitor-team07; id String partition key; item id=site; numeric count |
| CORS origin | https://d3jg1ev4a532iw.cloudfront.net; POST/OPTIONS; content-type; credentials disabled |
| Throttle | 2 requests/sec, burst 5; best effort, not a billing cap |
| Log groups | /aws/lambda/lambda-visitor-team07 and /aws/apigateway/api-visitor-team07; retention 7 days |
| Latest observed count | 5: four API tests and one browser page view; normal subsequent traffic will change it |

Request: Origin matching the website, Content-Type application/json, body `{}`. Successful response is HTTP 200 with `{"count":N}` and Cache-Control no-store. Actual tested errors: malformed JSON 400, missing/foreign Origin 403, unmatched GET 404. Gateway/platform throttling and failures can return 429/5xx. The [full endpoint specification](SCRUM-22-how-to.md) describes the remaining cases.

## Verified behavior

- Strong read before tests: count=0. One valid POST returned 1; three concurrent requests returned 4, 2 and 3. The subsequent strong read was 4. No reset or direct UpdateItem was used; all increments passed through the HTTP API.
- Allowed-origin OPTIONS returned 204 with the exact allow-origin, methods and content-type headers. Foreign-origin OPTIONS returned 204 without allow-origin. Foreign/missing-origin POST returned 403; malformed JSON returned 400. Negative tests did not add to the four successful increments.
- Actual Lambda role, exact-table/site-key permissions, log permissions, source-scoped API invocation permission, API integration, CORS, stage and throttling matched the template. Function environment contains only TABLE_NAME and ALLOWED_ORIGIN, with no stored AWS credentials.
- API Gateway created its service-linked role and a resource-scoped CloudWatch delivery policy. The latter allows delivery.logs.amazonaws.com to write only this API log group's streams, with the current account and regional source ARN conditions. It is not returned by an account-scoped DescribeResourcePolicies call; the resource-scoped read is in the evidence.
- Both Lambda execution logs and HTTP API access logs contain real test events. No raw bodies, request headers, credentials or client IPs are in the selected log format.
- The website's HTML and JavaScript served through CloudFront match the release hashes. A real cloud Chrome page displayed **Page views: 5** and the Week 3 release marker. Its exact endpoint and CSP matched the release; no site CSP/CORS errors were observed. A separate browser-extension metadata error was recorded accurately and is unrelated to the site request.
- Anonymous access to the private S3 index.html returned 403. Browser-delivered HTML/JavaScript were inspected and matched the reviewed credential-free code; the automated key/private-key pattern scan also passed. A pattern scan alone is not a universal secret-detection guarantee.

## Website release and recovery details

The new script was uploaded and retrieved through CloudFront before index.html was published. Uploads preserved AES256 encryption and versioning; an IfNoneMatch condition protected the new script and IfMatch protected the old HTML against a concurrent overwrite. Cache-Control is public,max-age=60. No bucket/distribution configuration changed, and styles.css was not uploaded.

| Object / action | Recorded identifier |
|---|---|
| Previous index.html version, available for approved content rollback | gU6a2x9eXr.nDxPOxb0MgTmPiGw_pAoQ |
| New index.html version | y_Qz.QfW.cnlzOce7hZOlsYHzJsMsCQi |
| New assets/visitor-counter-v1.js version | di15_4GyxszN9lgR.Mh7rT.Urjc680h_ |
| Invalidation | I53B07ZQ3S9OCO811JA64U3Z0O; Completed; / and /index.html only |
| HTML SHA-256 | 613764435327339eeea4a7d266d495be5f04958e48c25a54e38c713b681099df |
| Script SHA-256 | 8b87821065a8c72cf6fdf82896937245721ea32d1a906a8dbcce95bfe80aebce |

The repository HTML retains the empty endpoint as a source template. Reproduce the deployed bytes using `scripts/build_visitor_site.py` with the actual VisitEndpoint above; do not upload the unrendered source HTML. The manifest records the built release. No further deployment is needed simply to replace that source placeholder.

## Remaining Week 3 acceptance

SCRUM-49 and SCRUM-50 technical implementation is verified. SCRUM-22 remains In Review for the end-of-week course evidence and shared specification review.

**SCRUM-23/51's foreign-origin browser test remains pending.** HTTP-level negative tests passed, but the cloud browser rejected the separate local data: test page before navigation because its URL policy allows only http: and https:. No alternate execution or workaround was attempted. This is a tooling limitation, not a passed browser negative test. SCRUM-52's deployed role and browser credential-handling checks are complete.

For the remaining browser check, Josh can use an unrelated HTTPS test page in his own browser and run the following in its developer console. The page's CSP must permit this API connection, or the result proves only CSP blocking. This is a negative request and is expected to fail without incrementing the counter:

```javascript
fetch('https://24prug4iuj.execute-api.us-east-2.amazonaws.com/visits', {
  method: 'POST',
  mode: 'cors',
  credentials: 'omit',
  headers: {'Content-Type': 'application/json'},
  body: '{}'
}).then(response => console.log('Unexpected readable response', response.status))
  .catch(error => console.log('Blocked cross-origin request', error.name));
```

Record the foreign page's actual origin and inspect Network/Console: the preflight must lack a matching Access-Control-Allow-Origin and the browser must report a CORS failure, not merely a CSP/network error. Do not use browser extensions that disable CORS. Capture screenshots at the end of Week 3, as Josh directed. Preserve the original zero evidence and the current nonzero counter; never reset it for a screenshot.

SCRUM-20 and SCRUM-24 can now use the actual endpoint, request/response contract, permissions and verified flow above. Alyssa retains ownership of the final specification; Josh reviews it.

## Evidence

All files below are in [evidence/SCRUM-22](evidence/SCRUM-22). Public deployment evidence replaces the AWS account ID with ACCOUNT_ID and redacts the caller session identity.

- `20261019_Team7_aws_w3-api-deployment.json`: authorization, change set, stack/resources, deployed configuration, logs, object versions, invalidation and final strong read.
- `20261019_Team7_aws_w3-api-tests.json`: exact HTTP requests/statuses/headers/count results.
- `20261019_Team7_aws_w3-site-verification.json`: live hashes, credential-pattern check and private-origin denial.
- `20261019_Team7_browser_w3-counter-verification.json`: observed browser result and explicitly pending foreign-origin check.
- `20261019_Team7_site_w3-release-manifest.json`: actual endpoint and built website hashes.

Earlier preflight/local-validation files remain historical preparation evidence. No screenshots were captured during this deployment.
