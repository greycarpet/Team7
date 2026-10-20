# SCRUM-21: DynamoDB visitor counter how-to

Prepared 2026-10-20 UTC (2026-10-19 US Central). Status: preparation only; AWS deployment and seeding have not run.

Jira: https://joshescobarx.atlassian.net/browse/SCRUM-21

## 1. Goal and approved contract

Create the data store for the Week 3 visitor counter before Lambda/API integration.
Proposed implementer: Alyssa; proposed reviewer: Josh. Assignments are not changed by this guide.

| Setting | Value |
|---|---|
| Region | us-east-2 (Ohio) |
| Table | ddb-visitor-team07 |
| CloudFormation stack | cfn-visitor-data-team07 - proposed, requires approval |
| Logical resource | VisitorCounterTable |
| Partition key | id, String (S); no sort key |
| Seed item | {"id":"site","count":0}; count is a Number, not a key |
| Capacity / class | PAY_PER_REQUEST / STANDARD |
| Encryption | AWS-owned key; SSEEnabled: false selects this encryption mode |
| Data protection | Deletion protection + Retain on deletion and replacement |
| Recovery | PITR disabled for this reproducible lab counter; no backup in this scope |

AWS discovery at 2026-10-20 00:16 UTC found zero DynamoDB tables and zero Lambda functions in the verified Team7 account in us-east-2. The existing foundation, security, site and tools stacks were complete. This is a timestamped observation, not a guarantee about later changes.

Files: `infrastructure/cloudformation/week3/visitor-data.yaml`, `scripts/seed_visitor_counter.py`, `scripts/validation/scrum-21.guard`, and `docs/week3/SCRUM-21-deployment-plan.md`.

## 2. Prepare and review (safe to do now)

Use the Team7 repository root. Fetch and check out `feature/SCRUM-21-dynamodb-visitor-counter`. Review the PR diff and `AGENTS.md` first. Install cfn-lint 1.57.2 from `requirements-dev.txt`, boto3 1.43.115 in a virtual environment, and official CloudFormation Guard 3.2.1. These are the versions used for this preparation. No AWS access keys belong in files or screenshots.

Run these local checks from the repository root:

```bash
cfn-lint infrastructure/cloudformation/week3/visitor-data.yaml
cfn-guard validate --data infrastructure/cloudformation/week3/visitor-data.yaml --rules scripts/validation/scrum-21.guard --show-summary all
python -m unittest discover -s scripts/validation -p test_seed_visitor_counter.py -v
git diff --check
```

Authenticate using the existing `aws-Team7` profile. Independently verify the account ID against the Team7 account in your AWS console; do not just trust whichever account the CLI returns. Then check the CLI account and region:

```bash
aws sts get-caller-identity --profile aws-Team7 --region us-east-2
aws dynamodb list-tables --profile aws-Team7 --region us-east-2
aws cloudformation validate-template --template-body file://infrastructure/cloudformation/week3/visitor-data.yaml --profile aws-Team7 --region us-east-2
```

STOP before creating a stack, change set, or item. The repository requires the user to say `DEPLOYMENT AUTHORIZED` after reviewing the proposed stack name, one-table resource change, security settings and cost. No approval has been given yet.

## 3. Deploy through CloudFormation (only after authorization)

These are future operator instructions, not completed work. Use the reviewed PR commit. Recheck that the proposed stack and table do not already exist. If either exists, inspect ownership and state; do not delete it or switch to an unreviewed update/import.

Create a CREATE change set with an unused name. The example below uses `scrum21-create-v1`; change the suffix if needed. Run each fenced command as one line, or copy from the repository Markdown.

```bash
aws cloudformation create-change-set --stack-name cfn-visitor-data-team07 --change-set-name scrum21-create-v1 --change-set-type CREATE --template-body file://infrastructure/cloudformation/week3/visitor-data.yaml --profile aws-Team7 --region us-east-2
aws cloudformation wait change-set-create-complete --stack-name cfn-visitor-data-team07 --change-set-name scrum21-create-v1 --profile aws-Team7 --region us-east-2
aws cloudformation describe-change-set --stack-name cfn-visitor-data-team07 --change-set-name scrum21-create-v1 --profile aws-Team7 --region us-east-2
```

Review CloudFormation > Stacks > cfn-visitor-data-team07 > Change sets. Expected action: Add VisitorCounterTable, type AWS::DynamoDB::Table. No updates, replacements, removals, IAM resources or nested stacks. Review the change set's validation/events details as well; syntax validation alone does not verify deploy-time permissions, quotas or name availability. If the actual actions differ, stop for a revised review and authorization. Do not execute a failed change set.

If it matches the authorized plan, execute and wait for completion:

```bash
aws cloudformation execute-change-set --stack-name cfn-visitor-data-team07 --change-set-name scrum21-create-v1 --profile aws-Team7 --region us-east-2
aws cloudformation wait stack-create-complete --stack-name cfn-visitor-data-team07 --profile aws-Team7 --region us-east-2
aws cloudformation describe-stacks --stack-name cfn-visitor-data-team07 --profile aws-Team7 --region us-east-2
```

Use normal rollback behavior. On failure, inspect CloudFormation events and DynamoDB ownership before retrying. Retention and deletion protection can leave a table behind; do not disable protection, delete the table, or reset data without separate authorization.

## 4. Seed once, verify, and preserve the evidence

Run before Lambda/API testing. Replace `TEAM7_ACCOUNT_ID` below with the independently verified 12-digit account ID. The script requires the proposed stack name; if the reviewer approves another name, update and review the script first.

First inspect without writing. This fails safely if the table has not been deployed, the account is wrong, the table is not managed by the expected stack, or its schema/capacity is wrong.

```bash
python scripts/seed_visitor_counter.py --expected-account TEAM7_ACCOUNT_ID
```

After authorization explicitly covers the one-time data seed, run:

```bash
python scripts/seed_visitor_counter.py --expected-account TEAM7_ACCOUNT_ID --apply --authorization "DEPLOYMENT AUTHORIZED"
```

The flag is an operator acknowledgement, not an IAM security boundary. AWS IAM remains authoritative. The script uses conditional PutItem with attribute_not_exists(id), then a strongly consistent GetItem. It never resets an existing counter. It preserves a concurrent creator's item as well.

Expected first seed result: `status: seeded`, `count: 0`, `zero_observed: true`. Save this real output before API tests. On a repeat, `already_exists_preserved` is normal. A later nonzero counter is valid usage; do not reset it to manufacture a zero screenshot. If the item has an invalid count, investigate instead of overwriting it.

Verify in DynamoDB > Tables > ddb-visitor-team07 > Explore table items (or the Explore items navigation). Query partition key `id = site`; use a strongly consistent read where available. Confirm `count` is a Number. Reading the item should not increment it. Re-run the script without `--apply` to verify the preserved value.

## 5. Screenshot checklist and handoff

Capture the real console after deployment. These are required evidence instructions, not screenshots already captured. Keep the region, table name and relevant values visible. Exclude credentials, tokens and unrelated account details. Use the actual capture date as YYYYMMDD; tab labels can vary slightly by console version.

| Filename | Console view / evidence |
|---|---|
| YYYYMMDD_Team7_aws_w3-ddb-stack.png | CloudFormation stack status CREATE_COMPLETE and Resources tab with VisitorCounterTable |
| YYYYMMDD_Team7_aws_w3-ddb-outputs.png | Stack Outputs: table name, ARN, key and item ID |
| YYYYMMDD_Team7_aws_w3-ddb-overview.png | DynamoDB table Overview: ACTIVE and id (String), no sort key |
| YYYYMMDD_Team7_aws_w3-ddb-capacity.png | Table capacity section: On-demand, Standard class |
| YYYYMMDD_Team7_aws_w3-ddb-protection.png | Additional settings / protection sections: AWS-owned encryption and deletion protection |
| YYYYMMDD_Team7_aws_w3-ddb-tags.png | Table Tags: all Team7 naming-standard tags |
| YYYYMMDD_Team7_aws_w3-ddb-seed.png | Explore items: id=site and count=0 as Number, before API tests |

Attach screenshots and seed output to SCRUM-21 / SCRUM-47 / SCRUM-48 as appropriate, and reference them in SCRUM-24's final design specification. Record the capture timestamp, approved commit, stack status, table ARN and actual seed result. Only then can the relevant acceptance criteria be marked complete.

Handoff to SCRUM-20/22/23/24: region us-east-2; table ddb-visitor-team07; key id (String); item id=site; count (Number). Obtain the ARN from stack Outputs for the later least-privilege Lambda IAM policy. Use atomic counter updates in SCRUM-22. This PR does not implement Lambda, API Gateway, CORS or the website.

The actual website source is `site/`. Its current CSP allows neither JavaScript nor API connections, so the later API integration must add narrow script/connect allowances. The exact CORS origin is `https://d3jg1ev4a532iw.cloudfront.net` without a trailing slash.

## 6. Cost, recovery and assistance prompt

The AWS Pricing API lookup on 2026-10-20 for DynamoDB Standard in us-east-2 returned $0.625 per million write request units, $0.125 per million read request units and $0.25 per GB-month of paid storage. The saved response also lists a first-25-GB storage tier at $0; this estimate does not assume credits or free-tier availability.

Illustrative monthly usage: 1,000 WRUs + 1,000 RRUs + 1 MiB stored. Gross model: 1000 x 0.000000625 + 1000 x 0.000000125 + (1/1024) x 0.25 = $0.000994140625, approximately $0.001/month. This is a small assumed workload, not a bill prediction or spending cap. Larger items, transactions, retries and traffic change request-unit consumption. Lambda, API Gateway, logs, CloudFront and existing resources are excluded. On-demand usage and retained storage can still incur charges; the project-wide $5 budget is not a hard limit.

PITR and on-demand backups are not configured here. Retain prevents CloudFormation from deleting the table; it does not recover overwritten or deleted items. Deleting the stack can leave billable storage and a name collision for later stack creation. Cleanup needs an explicit reviewed plan.

Copy this prompt to the implementing teammate's assistant:

> Work on Team7 SCRUM-21 using the Jira plugin and greycarpet/Team7. Read AGENTS.md and the SCRUM-21 how-to/deployment plan on feature/SCRUM-21-dynamodb-visitor-counter. Start read-only; verify the AWS Team7 account and us-east-2. Review the proposed cfn-visitor-data-team07 stack, ddb-visitor-team07 table, id String key and seed {id:site,count:0}. Show the change list, security and cost before asking for DEPLOYMENT AUTHORIZED. Do not deploy, create a change set or seed until authorization is explicit. Use CloudFormation and the conditional seed script. Capture real evidence, preserve any existing count, and hand the result to SCRUM-22 and SCRUM-24.

Sources: repository AGENTS.md and naming standard; Jira SCRUM-21/47/48; saved AWS preflight and pricing responses in `docs/week3/evidence/`.

Official references:
- https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-dynamodb-table.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-dynamodb-table-ssespecification.html
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html
- https://aws.amazon.com/dynamodb/pricing/
- https://github.com/aws-cloudformation/cloudformation-guard/releases/tag/3.2.1
