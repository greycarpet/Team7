# SCRUM-22 implementation and endpoint handoff

Owner: Josh Escobar. Status: prepared; deployment authorization and live acceptance pending. Read [the deployment plan](SCRUM-22-deployment-plan.md) before any AWS mutation. Screenshots are due at the end of Week 3; preserve textual API evidence now and never reset the counter to recreate a zero screenshot.

## Request flow

The existing CloudFront site serves index.html and an external script from private S3. The browser sends one POST to the HTTP API, which invokes Lambda. Lambda uses its execution role to atomically increment `count` on DynamoDB item `id=site`, then returns the new value. The script displays that value using textContent. Reloads and test calls count as page views; this is not a unique-visitor metric.

## Endpoint contract

The actual endpoint is not yet assigned. After deployment, read the stack output **VisitEndpoint**; do not invent an API ID.

| Field | Contract |
|---|---|
| Method/path | POST /visits, $default stage |
| Origin | https://d3jg1ev4a532iw.cloudfront.net, exact match |
| Content-Type/body | application/json; an empty JSON object `{}` |
| Success | HTTP 200, `{"count":1}` with the actual positive numeric count |
| Invalid content/body | HTTP 400, `{"error":"invalid_request"}` |
| Missing/foreign Origin | HTTP 403, `{"error":"origin_not_allowed"}`; browser CORS may hide the body |
| Missing/invalid seed, access or datastore failure | HTTP 503, `{"error":"counter_unavailable"}` |
| Unmatched public route or method | API Gateway 404 (Lambda's defensive method guard returns 405 if directly invoked) |
| Throttling/platform failure | API Gateway/Lambda can return 429 or 5xx; bodies are gateway-dependent |
| Preflight | API Gateway handles OPTIONS; no Lambda invocation or increment |
| Cache/retry | Application responses use no-store; browser and SDK do not automatically retry |
| Authentication | Public demo endpoint; no keys in frontend or Lambda configuration |

The application pins the item key and increment, accepts no caller-supplied count/table/key, rejects missing/non-numeric/out-of-range stored values, and returns a JSON integer. An ambiguous failed response can follow a successful write. A later page reload is another visit, not a retry with exactly-once semantics.

## Files and local checks

- `application/lambda/visitor_counter.py`: maintain the handler here.
- `scripts/build_visitor_template.py`: copies that source into the YAML ZipFile block. CloudFormation names the inline Python module index, so Handler is index.handler.
- `infrastructure/cloudformation/week3/visitor-api.yaml`: the deployable plain CloudFormation template; no SAM packaging bucket is needed. Python uses the runtime-included SDK, which AWS may update; rerun acceptance tests after runtime updates.
- `site/index.html`, `site/assets/visitor-counter-v1.js`: website integration. The source endpoint is deliberately empty and connect-src is none until the release builder binds the deployed URL.
- `scripts/build_visitor_site.py`: prepares the exact release files and SHA-256 manifest locally, with no AWS calls.

From the repository root, use a Python environment with boto3 and cfn-lint, Node.js, and the official cfn-guard binary:

```bash
python scripts/build_visitor_template.py
python scripts/build_visitor_template.py --check
python -m unittest discover -s scripts/validation -p test_visitor_counter.py -v
node --test scripts/validation/test_visitor_site.cjs
cfn-lint infrastructure/cloudformation/week3/visitor-api.yaml
cfn-guard validate -d infrastructure/cloudformation/week3/visitor-api.yaml -r scripts/validation/scrum-22.guard
git diff --check
```

After an authorized backend deployment, set `VISIT_ENDPOINT` to the exact VisitEndpoint output and choose a new output directory:

```bash
python scripts/build_visitor_site.py --endpoint "$VISIT_ENDPOINT" --output /tmp/team7-week3-release
```

This rejects foreign-region URLs, queries, fragments and HTML injection. It binds the endpoint and CSP to the same exact HTTPS host. Do not upload the unrendered source HTML, test endpoint or release-manifest.json. Upload only the reviewed files described in the deployment plan; the manifest is evidence, not website content.

## Live acceptance and handoff

SCRUM-49 requires the deployed function/role, verified atomic increment, no seed/reset behavior and actual logging. SCRUM-50 requires the deployed route, documented actual endpoint, API tests and a website displaying the returned count. Offline tests alone do not complete either ticket.

SCRUM-23/51/52 require actual allowed/foreign-origin browser behavior, a credential scan of browser-delivered code, and deployed role/environment inspection. The Lambda role obtains temporary service credentials automatically; the public API endpoint is configuration, not a secret. No browser test has been represented as complete during preparation.

Hand off the actual endpoint, method/path, response/status contract, table schema, identity permissions, CORS origin and test evidence to SCRUM-20 (request flow) and SCRUM-24 (Alyssa's final Application & API Design Specification). Capture console/browser screenshots at the end of Week 3 showing the true current state, including nonzero counts. The initial zero is already recorded in SCRUM-21's timestamped evidence in [PR #8](https://github.com/greycarpet/Team7/pull/8).
