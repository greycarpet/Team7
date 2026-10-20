# SCRUM-22 implementation and endpoint handoff

> **Acceptance update — October 20, 2026:** Josh supplied a browser Console screenshot from https://example.org. It explicitly reports that the POST /visits preflight was blocked by CORS because Access-Control-Allow-Origin was absent. SCRUM-51’s foreign-origin browser acceptance now passes; SCRUM-23 is ready for review. This supersedes pending-browser notes below, which describe the October 19 tooling limitation. See the [review record](evidence/SCRUM-22/20261020_Team7_browser_w3-cors-negative-review.json). The screenshot’s Console clock reads 2026-10-20T23:53:22.051Z (18:53:22.051 CDT); Network headers/status and a new counter read are not shown. The original remains private and unchanged. Remaining course screenshots and final specification review are still outstanding.

Owner: Josh Escobar. Status: deployed and technically verified on October 19, 2026. See [the deployment handoff](SCRUM-22-deployment-handoff.md) for evidence, actual values and the pending foreign-origin browser test under SCRUM-23. Read [the deployment plan](SCRUM-22-deployment-plan.md) before any further AWS mutation. Screenshots are due at the end of Week 3; preserve textual API evidence and never reset the counter to recreate a zero screenshot.

## Request flow

The existing CloudFront site serves index.html and an external script from private S3. The browser sends one POST to the HTTP API, which invokes Lambda. Lambda uses its execution role to atomically increment `count` on DynamoDB item `id=site`, then returns the new value. The script displays that value using textContent. Reloads and test calls count as page views; this is not a unique-visitor metric.

## Endpoint contract

The deployed **VisitEndpoint** is `https://24prug4iuj.execute-api.us-east-2.amazonaws.com/visits`. It accepts POST; opening it as a browser GET returns 404 by design.

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

SCRUM-49's deployed function/role, atomic increment and actual logging are verified. SCRUM-50's route, actual endpoint, API tests and live website count are verified. The deployment handoff records four successful HTTP increments and the fifth page view in a real browser.

SCRUM-23/51 still require the foreign-origin browser test. Allowed-origin browser behavior and HTTP-level negative tests passed. SCRUM-52's browser-delivered code scan and deployed role/environment inspection passed. The Lambda role obtains temporary service credentials automatically; the public API endpoint is configuration, not a secret. The blocked foreign-origin browser check is explicitly pending in the deployment handoff.

Hand off the actual endpoint, method/path, response/status contract, table schema, identity permissions, CORS origin and test evidence to SCRUM-20 (request flow) and SCRUM-24 (Alyssa's final Application & API Design Specification). Capture console/browser screenshots at the end of Week 3 showing the true current state, including nonzero counts. The initial zero is already recorded in SCRUM-21's timestamped evidence in [PR #8](https://github.com/greycarpet/Team7/pull/8).
