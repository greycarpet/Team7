# SCRUM-21 deployment and datastore handoff

Deployed on October 19, 2026 (America/Chicago), after the user explicitly authorized deployment at 19:27 CDT. This record supersedes the preparation-only status in the original how-to PDF. The table now exists: do not repeat the CREATE workflow.

## Result

CloudFormation stack `cfn-visitor-data-team07` reached `CREATE_COMPLETE` at 2026-10-20 00:30:07 UTC (October 19, 19:30:07 CDT). The table is `ACTIVE`. A conditional PutItem created the missing seed; a strongly consistent GetItem confirmed the exact item below at 2026-10-20 00:32:26 UTC (October 19, 19:32:26 CDT).

```json
{"id":"site","count":0}
```

The API response represents `id` as String (`S`) and `count` as Number (`N`). No counter increment or reset was performed. Table-level ItemCount/TableSizeBytes are asynchronous metadata; the strongly consistent GetItem is the evidence of the actual seed item.

## Fields for SCRUM-20, SCRUM-22 and SCRUM-24

| Field | Deployed value |
|---|---|
| AWS region | us-east-2 |
| CloudFormation stack | cfn-visitor-data-team07 |
| Logical resource | VisitorCounterTable |
| Table | ddb-visitor-team07 |
| Partition key | id, String (S) |
| Sort key / secondary indexes | None |
| Item key | id=site |
| Counter attribute | count, Number (N), initially 0 |
| Capacity / class | PAY_PER_REQUEST / STANDARD |
| Table status | ACTIVE |
| Encryption configuration | AWS-owned key; deployed SSEEnabled=false selects this mode |
| Deletion protection | Enabled |
| CloudFormation policies | DeletionPolicy=Retain; UpdateReplacePolicy=Retain |
| Point-in-time recovery | DISABLED |
| Table ARN | arn:aws:dynamodb:us-east-2:ACCOUNT_ID:table/ddb-visitor-team07 |

The account portion of the ARN is masked in this public repository. The full ARN is recorded in the Jira handoff and in stack Output `VisitorTableArn`. Retrieve it with:

```bash
aws cloudformation describe-stacks --stack-name cfn-visitor-data-team07 --query "Stacks[0].Outputs" --profile aws-Team7 --region us-east-2
```

All ten table tags were verified: Name=ddb-visitor-team07, Project=Team7, Team=Team7, Environment=Dev, Workload=VisitorCounter, Component=Storage, Owner=Team7, ManagedBy=Team7, Repository=Team7, JiraProject=SCRUM. The stack itself has no user-defined tags; these are table tags.

## Deployment trace and validation

- Deployed template source: commit `25e3a8e44baf547e7bb79e07862253e889777b22`, template blob `754976bd5b98454509cfdcd21ad1286dc73f0b7f`.
- Change set: `scrum21-create-20261020-0028`, type CREATE. Actual plan contained one Add: VisitorCounterTable / AWS::DynamoDB::Table. No updates, replacements, deletions, IAM resources or nested stacks.
- Change-set status was CREATE_COMPLETE / AVAILABLE; DescribeEvents returned no VALIDATION_ERROR events. Execution used STANDARD mode with rollback enabled.
- Post-deployment GetTemplate matched the reviewed template exactly. DescribeTable, ListTagsOfResource, DescribeContinuousBackups and DescribeStackResource verified settings and ownership. ListStackResources confirmed the one-table scope.
- The live seed used the AWS connector API with the reviewed script's account, stack ownership, schema and conditional-write safeguards. The local CLI script was tested offline; it was not executed against live AWS. GetItem found the item absent, PutItem used attribute_not_exists(id), and a separate strongly consistent GetItem verified count=0.
- No IAM changes were made. DynamoDB usage-based charges and retained storage remain subject to the approved cost assumptions in the deployment plan. No live billing total is claimed.

Machine-readable evidence: [20261019_Team7_aws_w3-ddb-deployment.json](evidence/20261019_Team7_aws_w3-ddb-deployment.json). It contains the AWS response data, API-call outcomes, timestamps, requested seed and explicit account-ID redaction. It is API evidence, not a console screenshot.

## Remaining review and course evidence

SCRUM-47 and SCRUM-48's technical work is complete. SCRUM-21 remains In Review while the course evidence and datastore section of the final shared specification are reviewed. PR #8 remains draft and unmerged.

Capture the genuine console views listed in the [how-to guide](SCRUM-21-how-to.md#5-screenshot-checklist-and-handoff). Use the actual capture date in filenames. Capture the zero seed before SCRUM-22 starts increment tests; if testing has already advanced it, preserve the working counter and use this timestamped API evidence for the original zero value. Never reset the counter to recreate evidence.

SCRUM-24 must incorporate these datastore fields and the required screenshots into the course's Application & API Design Specification; this handoff does not claim the final form or PDF is complete. SCRUM-22 can now implement Lambda, its table-scoped IAM policy, HTTP API and website integration under a separately reviewed deployment plan. Obtain the actual ARN from the stack outputs, use atomic updates, and coordinate the website CSP/CORS changes with SCRUM-23.
