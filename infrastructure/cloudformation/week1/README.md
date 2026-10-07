# SCRUM-11 Week 1 landing zone

`foundation.yaml` defines the approved Team7 VPC, one public subnet in
`us-east-2a`, an attached Internet Gateway, and a subnet-associated route table
with an IPv4 default route through that gateway. It does not enable automatic
public IPv4 assignment and does not create private networking, compute, or a
NAT Gateway. AWS-created default VPC resources are separate and are not managed
by this template.

## Deploy

Deployment is subject to the Team7 AWS approval gate. Before deployment, verify
the active identity is account `123109186025`, region `us-east-2`, and confirm
that no matching resources or stack appeared since the last read-only inventory.
Review the proposed CloudFormation change set for the exact resources and effects
before execution. The configured `aws-Team7` CLI profile was unavailable at the
time this change was prepared; use only a profile whose caller identity has
already been verified for the expected account.

After explicit deployment approval, the intended CLI operation is:

```sh
aws cloudformation deploy \
  --template-file infrastructure/cloudformation/week1/foundation.yaml \
  --stack-name cfn-foundation-team07 \
  --region us-east-2 \
  --profile <verified-profile>
```

Do not run this command before approval. Review the generated change set before
execution; do not use deployment options that skip change review or
CloudFormation.

## Validation

Local validation, where tools are installed:

```sh
cfn-lint -r us-east-2 infrastructure/cloudformation/week1/foundation.yaml
aws cloudformation validate-template \
  --template-body file://infrastructure/cloudformation/week1/foundation.yaml \
  --region us-east-2
```

After an approved deployment, validate read-only with CloudFormation stack
outputs and resource inventory, plus EC2 descriptions of the VPC, subnet,
Internet Gateway, route table, association, and routes. Confirm the local route
remains present, the subnet is associated with `rt-public-team07`, the active
`0.0.0.0/0` route targets the Team7 Internet Gateway, all required tags are
present, and there is no Team7 NAT Gateway. Record the command outputs and
stack events as evidence; do not report an unrun check as passed.

## Evidence and handoff

Capture genuine AWS console screenshots only after approved deployment. Suggested
files are `W1_team07_vpc.png`, `W1_team07_public-subnet.png`,
`W1_team07_igw.png`, `W1_team07_public-route.png`,
`W1_team07_route-association.png`, and `W1_team07_no-nat.png`. Mask the account
ID in shared screenshots and keep credentials out of the evidence.

Record the stack name and status, resource IDs, VPC/subnet CIDRs, subnet AZ,
IGW attachment, route table association, active default route, required tags,
validation results, and any deviations. Infrastructure-owned Week 1 values are:
VPC `vpc-capstone-team07` / `10.7.0.0/16`; public subnet
`snet-public-team07` / `10.7.1.0/24` / `us-east-2a`; IGW
`igw-capstone-team07`; route table `rt-public-team07`; default route
`0.0.0.0/0` via that IGW. Provide these values and the recorded evidence to the
Architect and Security & Ops handoff.

## Recovery and cleanup

If stack creation fails, inspect the actual stack status and CloudFormation
events before deciding on recovery. Do not delete or recreate resources
automatically. Resolve the reported cause and use a reviewed CloudFormation
update or a separately approved cleanup plan. Stack deletion removes the
network resources owned by this stack; first confirm ownership, dependencies,
and whether any workloads have since attached to or depend on them. Never delete
or alter the pre-existing default VPC or its default components as part of this
task.
