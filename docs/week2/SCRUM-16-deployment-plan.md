> EXECUTED 2026-10-17: Josh authorized deployment. See [actual deployment handoff](SCRUM-16-handoff.md) for the completed deployment, naming correction, verified stopped state and pending SSH/course evidence. The proposal below is preserved as the pre-deployment record.

# SCRUM-16: reviewed deployment proposal

Prepared 2026-10-17. Status: PREPARED, NOT DEPLOYED. Josh is taking over implementation because Alyssa is unavailable, per the project conversation. Existing Jira assignments have not been changed.

## Scope and prerequisites
Repository: greycarpet/Team7. Branch: feature/SCRUM-16-ec2-tools.
Proposed stack: cfn-tools-team07 (matches cfn-{workload}-{team}; requires owner approval).
Region: us-east-2. Expected account: 123109186025.
Template: infrastructure/cloudformation/week2/tools.yaml.
Source requirements: SCRUM-16/40/41 and Team7_Week2_SCRUM-16_How-To.pdf v2.0.
Operator: Josh, with his private key retained on his workstation.

## Exact proposed resources
1. Team7ToolsKeyPair, AWS::EC2::KeyPair: import Josh's RSA public key as key-tools-team07. PublicKeyMaterial is mandatory; no AWS-generated private key or SSM secret.
2. Team7ToolsLaunchTemplate, AWS::EC2::LaunchTemplate: generated physical name; configure the settings below.
3. Team7ToolsInstance, AWS::EC2::Instance: use the explicit latest launch-template version at deployment. Name ec2-tools-team07.
Launching also creates the primary ENI, ephemeral public IPv4 and encrypted root EBS volume; these are not separate change-set rows.

No existing resource is replaced or deleted. Existing subnet, routes and security group are reused. No IAM profile, IAM resources, SSH ingress, Elastic IP, NAT gateway, user data or website change.

## Parameters and reviewed settings
- SubnetId: subnet-015dee27e366615f0, us-east-2a, VPC vpc-05ac92d29e000c0ce.
- SecurityGroupId: sg-0d4b70aeec5581403 (sg-tools-team07), presently zero ingress.
- ImageId: ami-0d31a22b09ceec4db, Amazon Linux 2023.12.20261016.0 x86_64, /dev/xvda; Amazon-owned, available, minimum root size 8 GiB.
- PublicKeyMaterial: REQUIRED FROM JOSH, not yet supplied. Validate with ssh-keygen and record fingerprint before any deployment.
- t3.micro On-Demand; Standard CPU credits; detailed monitoring off.
- IMDS endpoint enabled, tokens required, hop limit 1, instance tags unavailable through metadata.
- Primary interface explicitly requests public IPv4; subnet-wide auto-assignment remains disabled.
- Root disk: 8 GiB gp3, 3000 IOPS, 125 MiB/s, encrypted with alias/aws/ebs.
- Distinct instance and volume tags: ec2-tools-team07/Compute and ebs-tools-team07/Storage, plus all required Team7 tags.
- Stop preserves the disk. DeleteOnTermination=true deletes root data on termination/stack deletion. This disposable lab VM must not hold the sole copy of evidence. No termination/deletion is authorized by this proposal.

## Read-only preflight
On 2026-10-17, AWS confirmed:
- Foundation, security and website stacks CREATE_COMPLETE.
- No EC2 instances, key pairs or launch templates in us-east-2.
- Existing subnet is available with public-IP auto-assignment false.
- Explicit public route is active through igw-08399ea7488b80534.
- Subnet NACL allows IPv4 traffic; tools group has zero ingress.
- t3.micro offered in us-east-2a (capacity at launch is not guaranteed).
- EBS default key is alias/aws/ebs.
Effective launch/KMS authorization is not proven by read-only discovery; inspect change-set validation and deployment errors rather than changing permissions.

## Validation
cfn-lint 1.57.2: zero errors/warnings, JSON output [].
AWS CloudFormation ValidateTemplate: succeeded, four expected parameters, no IAM capabilities.
Manual security/scope review: only the three approved resource types; public-key import required; no credentials; IMDSv2 required; encrypted disk; single existing group; no ingress mutation; Standard credits; no paid extras.
cfn-guard executable is unavailable and no SCRUM-16 rules exist in main. No Guard pass is claimed. The task guide permits disclosing this gap with manual security review.
Pre-deployment change-set validation has NOT run: creating the change set is an AWS write requiring authorization under AGENTS.md.

## Cost and lifecycle
Use the accepted SCRUM-15 model, not a new price quote: EC2 $0.0104/running hour plus public IPv4 $0.005/hour; root gp3 $0.64/month for 8 GiB. Twenty running hours gives $0.948/month for the VM/disk/address, or $0.98/month including the modeled website. Continuous 730-hour total is $11.91/month. Before credits/tax, with documented shared-allowance assumptions.
The $5 budget is an alert, not a cap. EBS remains billable when stopped. Stop promptly after testing; if SSH testing cannot proceed, stop immediately after deployment verification. Starting later requires an agreed test window and fresh public IP.

## Execution gate
Obtain Josh's public key and explicit DEPLOYMENT AUTHORIZED approval for this proposal before creating or executing a change set.
Recheck account, region, resource collisions and template hash. Create a CREATE change set with normal rollback, required tags and no IAM capability/execution role. Inspect DescribeChangeSet and DescribeEvents validation results: exactly three Adds and no existing-resource modification, replacement or deletion. Stop for an unexpected scope or failed validation. Execute only the reviewed change set.

## Remaining acceptance
After creation: record actual instance/ENI/volume IDs, IPs, AMI, metadata settings, Standard credits, tags, status checks and encryption; compare with template.
SCRUM-18 separately updates the existing security stack to allow one verified public IPv4 /32. It requires its own reviewed template/plan, authorization, successful authorized SSH and blocked-source/CloudShell tests. Do not infer these passes from a successful launch.
Verify SSH host-key fingerprints against the EC2 console system log before accepting the host. Never display or upload the private key or passphrase.
Collect hostnamectl, /etc/os-release, uname -r, lscpu, free -h, lsblk, ip -brief address and ip route through the authorized SSH client. Preserve genuine evidence; stop and verify Stopped.
SCRUM-19 remains pending actual VM facts, SSH tests and final course-form/PDF assembly. Do not mark completion or recipient/instructor approval prematurely.
