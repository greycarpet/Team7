# SCRUM-22 deployment review

Status: implementation prepared and validated; **not deployed**. Owner: Josh Escobar. Related tasks: SCRUM-49, SCRUM-50; security acceptance: SCRUM-23/51/52. Screenshots are scheduled for the end of Week 3.

## Approval scope

Target: verified Team7 account, **us-east-2**. Proposed stack name: **cfn-visitor-api-team07**. This name and the two log-group names below require approval with this plan. The Lambda, role, inline policy and API names follow the existing naming standard. The October 19 DynamoDB authorization covered SCRUM-21 only.

| Action | Logical resource / name | Impact |
|---|---|---|
| Create stack | cfn-visitor-api-team07 | Nine CloudFormation resources listed below |
| Add | LambdaLogGroup / /aws/lambda/lambda-visitor-team07 | Seven-day retention; Retain on stack deletion/replacement |
| Add | ApiAccessLogGroup / /aws/apigateway/api-visitor-team07 | Seven-day retention; Retain on stack deletion/replacement |
| Add | LambdaExecutionRole / role-lambda-team07 | Lambda trust; inline policy policy-visitor-ddb-team07 |
| Add | VisitorFunction / lambda-visitor-team07 | Python 3.13, arm64, 256 MB, five-second timeout |
| Add | VisitorApi / api-visitor-team07 | Public HTTP API, exact website CORS origin |
| Add | VisitorIntegration | Lambda proxy payload version 2.0 |
| Add | VisitorRoute | POST /visits; no authentication |
| Add | VisitorStage / $default | Auto-deploy; rate 2 requests/sec, burst 5; access logs |
| Add | ApiInvokePermission | Only this API's $default POST /visits may invoke Lambda |
| Automatic service side effect | AWSServiceRoleForAPIGateway | Absent in preflight; API Gateway creates its AWS-managed service-linked role when creating the first API |
| Automatic service side effect | CloudWatch log delivery/resource permission | API Gateway may configure service-managed delivery permissions for access logs; inspect the resulting policy scope |
| Upload new object | s3://s3-site-team07-a7f391/assets/visitor-counter-v1.js | External browser script; no credentials |
| Upload new version | s3://s3-site-team07-a7f391/index.html | Counter display, real endpoint, exact API CSP origin |
| Invalidate cached paths | E1PBX75YJOS2B9: / and /index.html | Publish the updated HTML; styles.css stays unchanged |
| Increment existing data | ddb-visitor-team07, id=site | Up to 20 deliberate successful smoke-test requests; subsequent public page views also increment |
| Infrastructure update/replacement/deletion | None planned | Existing stacks and DynamoDB table configuration are not modified |

The new API references the deployed table by its constrained name parameter. This PR branches from main and is independent of unmerged data PR #8; it does not copy or re-create that table. Preflight found no Lambda functions, HTTP APIs, matching role/log groups or proposed stack. The strong read returned numeric count=0. Recheck immediately before an authorized change set.

## Security and cost

The execution role permits only `dynamodb:UpdateItem` on the exact table ARN, restricted to partition key `site`, and `logs:CreateLogStream`/`logs:PutLogEvents` in its own log group. It cannot GetItem, PutItem, DeleteItem or access another table through this policy. The handler requires an existing numeric counter and never seeds or resets it. IAM alone does not enforce increment-only semantics: the trusted handler supplies that operation. No managed broad-access policy, static credentials, VPC attachment, NAT, paid provisioned concurrency, SnapStart or customer-managed KMS key is added.

The Lambda trust uses AWS's documented `lambda.amazonaws.com` execution-role policy. Confused-deputy restrictions on the API-to-Lambda permission use the exact SourceArn and SourceAccount. Deployment requires `CAPABILITY_NAMED_IAM`, permission to pass this role to Lambda, and first-API service-linked-role/log-delivery setup permissions. The AWS-managed API Gateway service-linked role includes broader service permissions and is distinct from the tightly scoped application role; see the official source below. No attempt will be made to bypass an SCP denial.

CORS allows only `https://d3jg1ev4a532iw.cloudfront.net`, POST/OPTIONS, content-type, and no credentials. The handler also rejects missing/foreign Origin headers before any write. This is a public demo API: scripts outside a browser can spoof Origin. CORS is not authentication or bot protection. Throttling is best effort, not a spending cap. There is no unique-visitor detection or exactly-once guarantee. Neither the browser nor SDK automatically retries a counter update; a lost response can still conceal a successful write.

Access logs contain request ID, route, status, integration status and response length, without request bodies, headers, cookies, IPs or query values. Application errors log a category and Lambda request ID, not raw events or exception details. Seven-day log retention limits storage; retained log groups can outlive a failed/deleted stack.

Captured Ohio gross prices, before free tier/credits: HTTP API $1/million requests; Lambda $0.20/million invocations and $0.0000133334/GB-second on arm64; DynamoDB $0.625/million WRUs; standard logs $0.50/GB ingested and $0.03/GB-month stored. Example: **10,000 visits, up to one preflight each, 200 ms billed Lambda duration at 256 MB, one <=1 KB update each, 0.01 GB logs ingested and 0.01 GB-month stored = about $0.04**. Actual cold-start duration, traffic and log size change this estimate. It excludes existing EC2/EBS/S3/CloudFront costs, transfer, DynamoDB storage and extra diagnostics. The $5 project budget is an alert, not an enforced cap. Sustained abusive traffic can exceed it even with throttling. See evidence/SCRUM-22/pricing.json.

## Validation already completed

- cfn-lint and project CloudFormation Guard rules passed; generated inline handler matches its source.
- Nine offline Python tests and three JavaScript tests passed, covering the atomic update request, failed/missing datastore, origin/input rejection, endpoint/CSP binding and browser fallback without retries.
- AWS ValidateTemplate succeeded and identified CAPABILITY_NAMED_IAM.
- IAM Access Analyzer found no findings in the identity or trust policy. IAM policy simulation allowed UpdateItem for site and denied GetItem/PutItem/DeleteItem, a foreign key, and missing key context.
- No change set, role, function, API, website upload, invalidation or live increment was performed during preparation.

The IAM Policy Autopilot version check succeeded, but policy generation was blocked by automatic approval review for attempted contact with an unverified endpoint while processing source. It was not retried or counted as validation. The safer fallback used the official AWS service authorization reference, Access Analyzer and policy simulation. These checks do not prove deployed integration behavior or effective access through SCPs.

## Authorized execution sequence

1. Recheck branch commit, table ACTIVE/schema/seed, account, region, conflicts and current S3 versions. Preserve the old index.html object version for rollback. Do not reset the counter.
2. Create a **CREATE** CloudFormation change set for `infrastructure/cloudformation/week3/visitor-api.yaml`, using the reviewed defaults and CAPABILITY_NAMED_IAM. Include the standard project tags. This is an AWS write and occurs only after approval.
3. Inspect DescribeChangeSet and DescribeEvents. Require the nine planned Add actions, no update/replacement/delete, and no validation error. Stop on any unexpected effect or permission denial; do not broaden IAM automatically.
4. Execute with normal rollback enabled. Wait for CREATE_COMPLETE. Verify deployed template, function configuration, role policies, API route/integration/stage/CORS/throttling, permission SourceArn and log retention/delivery.
5. Read the actual VisitEndpoint output. Record an initial strong GetItem, a successful POST and returned count, and a small bounded concurrency test. Compare successful requests to the final strong read in a quiet test interval. Record other traffic or ambiguity rather than claiming exact isolation. Never reset data.
6. Test allowed and foreign preflights, foreign/missing Origin POST, malformed JSON and an unknown route. Foreign/invalid requests must not increment. Verify expected CORS headers and capture textual test evidence. A real browser must also confirm CORS/CSP behavior; curl alone is insufficient.
7. Run the local site builder with the actual output. Review the generated endpoint, CSP and manifest. Upload the new script first, verify it can be retrieved, then upload index.html. Both use `Cache-Control: public,max-age=60`; MIME types are text/javascript and text/html respectively. Preserve existing object encryption/versioning and use no ACL. Do not sync with --delete.
8. Invalidate only / and /index.html. Verify the live HTML and JS hashes and the browser's displayed count with no CSP/CORS errors. Confirm the private S3 origin remains inaccessible anonymously.
9. Save redacted deployment/test evidence and actual endpoint to GitHub and Jira; hand off to SCRUM-20/23/24. Leave final course screenshot/specification acceptance open until completed at the end of Week 3.

Approval includes the described content uploads and bounded counter smoke tests. It does not authorize merging PRs, resetting/deleting the table, changing existing infrastructure or adding unlisted resources.

## Recovery

Keep CloudFormation rollback enabled. A failed creation may leave retained log groups or the service-linked role; inspect ownership before retrying, without silently renaming resources. If the frontend fails, restore the saved pre-release HTML version as a new object version and invalidate the same two paths; the new script can remain unused. This content rollback is included in the deployment scope. A successful backend stack is not deleted automatically. Propose and approve any subsequent infrastructure cleanup separately. The data stack remains independent, and no recovery step resets the counter.

## Sources

- [AWS Lambda runtimes and inline SDK guidance](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html)
- [Lambda execution-role trust](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html)
- [DynamoDB atomic counters and retry limitations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html)
- [DynamoDB fine-grained IAM conditions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/specifying-conditions.html)
- [HTTP API CORS](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html)
- [API Gateway service-linked role and automatic creation](https://docs.aws.amazon.com/apigateway/latest/developerguide/using-service-linked-roles.html)
