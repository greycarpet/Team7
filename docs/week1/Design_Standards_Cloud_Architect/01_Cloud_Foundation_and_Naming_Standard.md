---
title: Cloud Foundation & Naming Standard
file: 01_Cloud_Foundation_and_Naming_Standard.md
standard: AWS tagging best practices — naming and tagging
team: 7
cohort: 2026-09
date: 2026-10-07
---

# Cloud Foundation & Naming Standard

> The rules every later resource obeys: where it lives in AWS, what it is called, how it is tagged, who does what, and the spending limit that stops a mistake costing money.
>
> _Standard: AWS tagging best practices — naming and tagging_

## Document control · Architect

**Document ID:** Team7-STD-001

**Version:** 1.0

**Owner:** Joshua Escobar

**Approved by:** Alyssa Esteves

**Date:** 2026-09-30

**Status:** Draft

## Account and guardrails · Architect

**Account name:** 123109186025

**Primary region:** us-east-2

**Monthly budget:** 5

**Budget alert goes to:** joshescobarx@gmail.com, estevesalyssa01@gmail.com

**Region and availability zone, and why:** us-east-2, us-east-2a - This is where the free services are

## Service model and shared responsibility · Architect

| Component | Model | We manage | The provider manages |
| --- | --- | --- | --- |
|   |   |   |   |

## Naming standard · Architect

| Resource type | Pattern | Example (your team) |
| --- | --- | --- |
| VPC | vpc-{workload}-{team} | vpc-capstone-team07 |
| Subnet | snet-{public\|private}-{team} | snet-public-team07 |
| Internet Gateway | igw-{workload}-{team} | igw-capstone-team07 |
| Route Table | rt-{public\|private}-{team} | rt-public-team07 |
| Security Group | sg-{workload}-{team} | sg-tools-team07 |
| EC2 Instance | ec2-{workload}-{team} | ec2-tools-team07 |
| EBS Volume | ebs-{workload}-{team} | ebs-tools-team07 |
| EC2 Key Pair | key-{workload}-{team} | key-tools-team07 |
| S3 Bucket | s3-{workload}-{team}-{suffix} | s3-site-team07-a7f391 |
| CloudFront Distribution | cf-{workload}-{team} | cf-site-team07 |
| CloudFront OAC | oac-{workload}-{team} | oac-site-team07 |
| DynamoDB Table | ddb-{workload}-{team} | ddb-visitor-team07 |
| Lambda Function | lambda-{workload}-{team} | lambda-visitor-team07 |
| IAM Role | role-{workload}-{team} | role-lambda-team07 |
| IAM Policy | policy-{workload}-{team} | policy-visitor-ddb-team07 |
| API Gateway | api-{workload}-{team} | api-visitor-team07 |
| CloudWatch Alarm | alarm-{workload}-{team} | alarm-lambda-errors-team07 |
| SNS Topic | sns-{workload}-{team} | sns-ops-alerts-team07 |
| CloudWatch Dashboard | dashboard-{workload}-{team} | dashboard-ops-team07 |
| AWS Budget | budget-{workload}-{team} | budget-monthly-team07 |
| CloudFormation Stack | cfn-{workload}-{team} | cfn-foundation-team07 |

## Required tags · Architect

| Tag key | Example value | Why we need it |
| --- | --- | --- |
| Project | Team7 | Identifies resources that belong to the Team7 capstone project. |
| Team | Team7 | Identifies the team responsible for the resource. |
| Environment | Dev | Identifies whether the resource belongs to development, test, or production. |
| Workload | VisitorCounter | Identifies the application or workload the resource supports. |
| Component | API | Identifies the architectural function of the resource. |
| ManagedBy | Team7 | Identifies who is responsible for maintaining the resource. |
| Repository | Team7 | Links the resource to the Team7 GitHub repository. |
| JiraProject | SCRUM | Links the resource to the Jira project where the work is tracked. |

## Landing zone · Infrastructure

**Stack:** `cfn-foundation-team07` — `us-east-2`; seven managed resources recorded as `CREATE_COMPLETE`.

**VPC:** `vpc-capstone-team07` — `vpc-05ac92d29e000c0ce` (Available; not the default VPC).

**VPC address space:** `10.7.0.0/16`.

**First subnet:** `snet-public-team07` — `subnet-015dee27e366615f0`; `10.7.1.0/24`; `us-east-2a`; automatic public IPv4 assignment disabled.


**Infrastructure handoff:**

- Internet Gateway: `igw-capstone-team07` — `igw-08399ea7488b80534`, attached to the Team7 VPC.
- Public route table: `rt-public-team07` — `rtb-02b7d4064159c1d42`.
- Explicit association: `snet-public-team07` to the public route table; association ID `rtbassoc-0700cfab29e7855cf`.
- Routes recorded in the merged deployment evidence: `10.7.0.0/16` to `local` and `0.0.0.0/0` to `igw-08399ea7488b80534`, both active.
- No Team7 NAT Gateway was found in the earlier live AWS verification.
- Implementation, instructions, and deployment evidence are on [GitHub main](https://github.com/greycarpet/Team7/tree/main/infrastructure/cloudformation/week1), including [deployment-evidence.md](https://github.com/greycarpet/Team7/blob/main/infrastructure/cloudformation/week1/deployment-evidence.md).

Values were reconciled against the supplied screenshots and the previously reviewed deployment evidence on 2026-10-07. The additional public-route-routes screenshot confirms both route destinations, targets, and Active states. The Infrastructure-owned landing-zone fields and handoff are complete for SCRUM-11.

## Team tooling · App / DevOps

**Team repository:** https://github.com/greycarpet/Team7.git

**Task board:** https://joshescobarx.atlassian.net/?continue=https%3A%2F%2Fjoshescobarx.atlassian.net%2Fwelcome%2Fsoftware%3FprojectId%3D10000&atlOrigin=eyJpIjoiZTIxNmY3NDYwNzJmNDQwMmI1YjYzZGMwMWQyNmU3ZTYiLCJwIjoiamlyYS1zb2Z0d2FyZSJ9

## Team access · Security & Ops

| Person | Sign-in | Group, role and scope | MFA |
| --- | --- | --- | --- |
| Josh Escobar (observed task session; full assignment roster unverified) | Console-based temporary CLI/MCP session; assumed AccountFullAccessRole; managed trust principal account-access.amazonaws.com | AdministratorAccess v1 permits Action=* / Resource=*; no inline policy; effective access restricted by SCP denies. No team group/assignment mapping independently verified. | Individual MFA unverified; root AccountMFAEnabled=0 does not establish individual MFA. Owner review open. |

## Access and Security Group summary · Security & Ops

SCRUM-13 deployment approved by Josh for commit `d0be5dce16b2ad7b7915bf882ccc8f6755e7b913`.
CloudFormation completed at `2026-10-08T01:18:50.251Z`; read-only checks at `2026-10-08T01:19:09.227Z`.

| Field | Verified value |
| --- | --- |
| Account / region | `123109186025` / `us-east-2` |
| Stack / resource | `cfn-security-team07`, `CREATE_COMPLETE`; exactly one `Team7ToolsSecurityGroup` |
| Group ID | `sg-0d4b70aeec5581403` |
| Physical GroupName | `cfn-security-team07-Team7ToolsSecurityGroup-zyMccvqygh0Z`, generated by CloudFormation |
| Approved Name tag | `sg-tools-team07`; distinct from generated physical name and group ID |
| Description | `Team7 tools security group - Week 1` |
| VPC | Foundation output `vpc-05ac92d29e000c0ce`; Name `vpc-capstone-team07`; `10.7.0.0/16` |
| Inbound | Zero rules, including no SSH or self-reference |
| Actual outbound | One rule `sgr-0c5218ce1138a563f`: all protocols/ports (`-1`), IPv4 `0.0.0.0/0`; no IPv6, group, or prefix-list destination |
| Attachments | Zero network interfaces attached; this task creates no workload |
| Outputs | `SecurityGroupId=sg-0d4b70aeec5581403`; `VpcId=vpc-05ac92d29e000c0ce` |
| Tags | `Name=sg-tools-team07`, `Project=Team7`, `Team=Team7`, `Environment=Dev`, `Owner=Team7`, `Workload=Tools`, `Component=Security`, `ManagedBy=Team7`, `Repository=Team7`, `JiraProject=SCRUM`; plus reserved CloudFormation ownership tags |
| Root baseline | `AccountMFAEnabled=0` (expected 1; exception accepted by Josh on 2026-10-08; not remediated and not passed); `AccountAccessKeysPresent=0` (baseline passed); password/signing certificates `0/0` |
| IAM inventory | Users/groups/roles `0/0/12`; zero users may be valid for federation |
| Limitations | Centralized-root features and SAML/OIDC provider reads denied by SCP; credential report absent. Centralized root not confirmed. Individual MFA and named team assignments unverified. No denied check counted as passed. |

Week 1 supplies an unattached group with zero ingress. The later tools-instance/SSH description in the original component notes is future context; no SSH was added here. The root-MFA finding is an accepted exception; separate team-access and individual-MFA findings remain open. No credentials, policies, or assignments were altered.

**Root-MFA exception:** Josh explicitly accepted the exception at 2026-10-08T23:34:18Z and elected not to remediate root MFA for this Week 1 task. The observed MFA flag remains 0; centralized-root management remains unverified. This does not establish individual MFA, accept team-access limitations, or assert instructor approval. See [the decision record](../SCRUM-13-root-MFA-exception.md).

Deployment API evidence is supplemented by Josh's 19-image `Week01(1).zip`, reviewed and hashed in [the screenshot review](../evidence/SCRUM-13/SCREENSHOT_REVIEW.md). Security-group screenshots are complete. Original images remain private; team-access/individual-MFA owner review and the Cloud Architect handoff remain open.
Repository review: [draft PR #3](https://github.com/greycarpet/Team7/pull/3), [security evidence manifest](../evidence/SCRUM-13/README.md), and [handoff/checklists](../SCRUM-13-handoff.md).
In the private handoff package, new evidence is under `../Evidence/SCRUM-13/`; previous landing-zone links still resolve there. This repository copy preserves the earlier screenshot references as historical package references; those private originals are not republished here.

This working copy comes from the reviewed Week 1 ZIP, source document SHA256 `6b2f495a23fd9c142d493db9e5daea030a41d11bf2acedeaad217fe9476c081e`. The original package and completed landing-zone section are preserved unchanged. No new Architect approval or document-status change is asserted.

## RACI · Architect

| Activity | Responsible | Accountable |
| --- | --- | --- |
| Create AWS Budget & 80% Alert | Architect | Architect |
| Define Naming, Tagging & RACI | Architect | Architect |
| Build VPC, Public Subnet & Internet Gateway | Infrastructure | Infrastructure |
| Configure Public Route & Validate Landing Zone | Infrastructure | Infrastructure |
| Create Repository & README | App / DevOps | App / DevOps |
| Create Four-Week Project Board | App / DevOps | App / DevOps |
| Create Tools Security Group | Security & Ops | Security & Ops |
| Review IAM & Root Account Security | Security & Ops | Security & Ops |

## Evidence · everyone


**Landing-zone evidence received and reviewed (2026-10-07):**

| Screenshot | What it shows | Review |
| --- | --- | --- |
| [20261007_Team7_aws_w1-stack.png](../Evidence/20261007_Team7_aws_w1-stack.png) | Stack name and all seven resources with CREATE_COMPLETE | Confirmed |
| [20261007_Team7_aws_w1-vpc.png](../Evidence/20261007_Team7_aws_w1-vpc.png) | VPC name, ID, Available state, and 10.7.0.0/16 | Confirmed |
| [20261007_Team7_aws_w1-public-subnet.png](../Evidence/20261007_Team7_aws_w1-public-subnet.png) | Subnet name/ID, VPC, CIDR, us-east-2a, and public IPv4 auto-assignment disabled | Confirmed |
| [20261007_Team7_aws_w1-igw.png](../Evidence/20261007_Team7_aws_w1-igw.png) | Internet Gateway attached to the Team7 VPC | Confirmed |
| [20261007_Team7_aws_w1-public-route.png](../Evidence/20261007_Team7_aws_w1-public-route.png) | Route table Details tab and explicit subnet association | Details view retained; routes are confirmed by the additional Routes-tab screenshot below |
| [20261007_Team7_aws_w1-public-route-routes.png](../Evidence/20261007_Team7_aws_w1-public-route-routes.png) | Active 10.7.0.0/16 to local and active 0.0.0.0/0 to igw-08399ea7488b80534 in rt-public-team07 | Confirmed |
| [20261007_Team7_aws_w1-route-association.png](../Evidence/20261007_Team7_aws_w1-route-association.png) | Explicit subnet association for snet-public-team07 | Confirmed |
| [20261007_Team7_aws_w1-no-nat.png](../Evidence/20261007_Team7_aws_w1-no-nat.png) | No NAT gateways found | Corroborates the earlier live check; region is not visible in this image |

All eight screenshot SHA-256 hashes match both supplied chain-of-custody logs. Original screenshots and logs have been preserved byte-for-byte. Resource tags are not visible in these screenshots; their validation is recorded in the previously reviewed AWS deployment evidence. The budget image was absent from the original reviewed ZIP and is now supplied in `Week01(1).zip`. It shows the budget list, not the 80% alert configuration or recipients.

**Deployment screenshot:** 20260930_Team7_aws_w1-budget.png

**What each component does:** budget-monthly-team07 — Tracks Team7 AWS spending and provides an alert when monthly costs reach 80% of the defined budget.

vpc-capstone-team07 — Provides the isolated virtual network that contains the Team7 AWS infrastructure.

snet-public-team07 — Provides the public network segment for resources that require internet connectivity, including the Week 2 EC2 tools instance.

igw-capstone-team07 — Connects the Team7 VPC to the public internet.

rt-public-team07 — Routes public-subnet traffic to the Internet Gateway and defines the public network path.

sg-tools-team07 — Defines the network security rules for the tools EC2 instance, including restricting SSH access to an authorized source.
