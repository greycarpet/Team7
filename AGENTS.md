# Team7 Codex Instructions

## AWS Project Context

- Project: Team7
- Jira project: SCRUM
- GitHub repository: Team7
- AWS workload region: us-east-2
- Infrastructure as Code: AWS CloudFormation YAML

## AWS Safety Policy

Default AWS behavior is READ ONLY.

Do not create, update, deploy, modify, replace, or delete AWS resources unless the user explicitly states:

DEPLOYMENT AUTHORIZED

Before any authorized AWS deployment:

1. Identify the Jira ticket being implemented.
2. Review the relevant CloudFormation template.
3. Show all resources that will be created, changed, replaced, or deleted.
4. Confirm the target AWS region is us-east-2.
5. Identify IAM/security implications.
6. Identify estimated cost implications.
7. Stop and request explicit approval before execution.

Never create or expose:
- AWS access keys
- secret access keys
- session tokens
- private keys
- passwords
- credentials in source code

Do not commit credentials or secrets to Git.

## Team7 Naming Standard

Use the approved Team7 naming standard.

Examples:

- VPC: vpc-capstone-team07
- Public subnet: snet-public-team07
- Internet Gateway: igw-capstone-team07
- Route table: rt-public-team07
- Security group: sg-tools-team07
- CloudFormation foundation stack: cfn-foundation-team07
- CloudFormation security stack: cfn-security-team07

Do not invent alternate resource names without approval.

## Infrastructure Workflow

For AWS infrastructure changes:

Jira requirement
→ feature branch
→ CloudFormation
→ validation
→ git diff review
→ commit
→ draft pull request
→ deployment plan
→ explicit approval
→ AWS deployment
→ read-only validation
→ evidence
→ Jira completion

Do not bypass CloudFormation by creating resources manually unless explicitly instructed.

## SCRUM-11 Scope

For W1 - Build AWS Landing Zone, allowed resources are:

- VPC
- public subnet
- Internet Gateway
- Internet Gateway attachment
- public route table
- route table association
- 0.0.0.0/0 route through the IGW
- required Team7 tags

Do not create:

- NAT Gateway
- private subnet
- EC2 instance
- Elastic IP
- Lambda
- DynamoDB
- S3 bucket
- CloudFront
- API Gateway