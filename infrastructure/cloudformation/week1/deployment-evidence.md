# SCRUM-11 deployment evidence

Deployment completed on 2026-10-07 in `us-east-2` using CloudFormation stack
`cfn-foundation-team07` in account `123*****6025`.

## Stack result

- Stack status: `CREATE_COMPLETE`
- CloudFormation change set: `cfn-foundation-team07-scrum11-20261007`
- Change set actions: seven additions; no replacements or deletions
- Final stack event: `CREATE_COMPLETE` at `2026-10-07T23:33:31.680Z`
- All seven stack resources report `CREATE_COMPLETE`

## Resource IDs and configuration

| Resource | ID or value | Validation |
| --- | --- | --- |
| VPC | `vpc-05ac92d29e000c0ce` | Available; `10.7.0.0/16`; not the default VPC |
| Public subnet | `subnet-015dee27e366615f0` | Available; `10.7.1.0/24`; `us-east-2a`; automatic public IPv4 assignment disabled |
| Internet Gateway | `igw-08399ea7488b80534` | Attached to the Team7 VPC; attachment state `available` |
| Public route table | `rtb-02b7d4064159c1d42` | In the Team7 VPC |
| Route table association | `rtbassoc-0700cfab29e7855cf` | Subnet association state `associated` |
| VPC local route | `10.7.0.0/16` → `local` | `active` |
| IPv4 default route | `0.0.0.0/0` → `igw-08399ea7488b80534` | `active` |
| NAT Gateway | None | `DescribeNatGateways` returned zero for the Team7 VPC |

Required Team7 tags were present on the VPC, subnet, Internet Gateway, and route
table. The CloudFormation stack lists only the seven approved SCRUM-11 resources.

## Validation

- CloudFormation stack outputs matched the deployed VPC, subnet, Availability
  Zone, Internet Gateway, and route table values above.
- Read-only EC2 descriptions confirmed the VPC, subnet, gateway attachment,
  route table, subnet association, local route, and active default route.
- `cfn-lint --format json --regions us-east-2 -- infrastructure/cloudformation/week1/foundation.yaml`
  reported no errors. It reported W3010 for the fixed `us-east-2a` Availability
  Zone, which is part of the approved SCRUM-11 design.

## Evidence source

Values above were captured from AWS CloudFormation `DescribeStacks`,
`DescribeStackResources`, and `DescribeStackEvents`, plus EC2 `DescribeVpcs`,
`DescribeSubnets`, `DescribeInternetGateways`, `DescribeRouteTables`, and
`DescribeNatGateways` read-only API responses after deployment.
