# SCRUM-21 deployment review

Status: DEPLOYED after explicit authorization on October 19, 2026 at 19:27 CDT. See [deployment handoff and evidence](SCRUM-21-deployment-handoff.md). The reviewed plan below covered SCRUM-21, SCRUM-47 and SCRUM-48 only and is retained as the approval record.

## Proposed operation

Target: verified Team7 AWS account, us-east-2. Stack name approved with deployment authorization: `cfn-visitor-data-team07`. Approved table name: `ddb-visitor-team07`.

| Action | Resource / data | Expected impact |
|---|---|---|
| Create | CloudFormation stack cfn-visitor-data-team07 | Owns one table; no nested stacks |
| Add | VisitorCounterTable / AWS::DynamoDB::Table | id String partition key, on-demand, Standard |
| Conditional insert | ddb-visitor-team07 item id=site, count=0 | Only if absent; an existing counter is preserved |
| Update / replace / delete | None | Existing infrastructure unchanged by this template |

Security: no new IAM resources or permissions. Table data is encrypted with an AWS-owned key; template SSEEnabled=false does not disable encryption. No customer-managed KMS key, public endpoint policy, stream or index is added. Deletion protection and Retain are enabled. PITR is disabled; retention is not a backup. AWS service authorization still controls all table access. A later PR must scope the Lambda role to this table's ARN.

Cost: pay-per-request and storage. Captured Ohio prices: $0.625/million WRUs, $0.125/million RRUs, $0.25/GB-month paid storage. An illustrative 1,000 WRUs + 1,000 RRUs + 1 MiB-month costs $0.000994140625 gross without credits/free tier, excluding all other services. There is no spending cap, and retained storage may continue billing.

## Validation and approval boundary

See evidence/validation-20261020.json for the original preparation checks. Local lint, project Guard policy and offline safety tests passed, as did AWS ValidateTemplate. Subsequently, the authorized CREATE change set passed pre-deployment validation, the stack reached CREATE_COMPLETE, and the seed was verified. The deployment handoff records these later results.

Approval covered the stack name, one-table creation and conditional seed. The user's `DEPLOYMENT AUTHORIZED` satisfied AGENTS.md before change-set creation. The actual change set matched this plan and was executed. Future changes require their own scope review and authorization.

Rollback: retain normal CloudFormation rollback behavior. A failed deployment or stack deletion may leave the protected table. Inspect events and ownership before retrying. Do not disable deletion protection, delete the table or reset the counter as an automatic recovery action. Cleanup, import, replacement and data resets require their own approved plan.

Completion: stack CREATE_COMPLETE, table ACTIVE with required settings/tags, actual zero seed evidence before API tests, then handoff table ARN/key/item schema and attach real evidence to Jira. Keep SCRUM-21/47/48 unfinished until their corresponding live acceptance criteria pass.
