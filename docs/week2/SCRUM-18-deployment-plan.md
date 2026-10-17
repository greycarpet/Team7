# SCRUM-18 restricted SSH deployment plan

Prepared 2026-10-17. NOT DEPLOYED. Josh is the operator on Windows.
Existing stack: cfn-security-team07; region us-east-2.
Existing group: sg-0d4b70aeec5581403; logical ID Team7ToolsSecurityGroup.
Existing VPC: vpc-05ac92d29e000c0ce.
Instance: i-0dd31fddcfc283ea7, ec2-tools-team07; currently stopped.

## Change
Evolve infrastructure/cloudformation/week1/security.yaml in place. Add required AuthorizedSshCidr (valid IPv4 /32, no default), then one inline TCP/22 rule referencing it. Use Josh's public IPv4 supplied in the project chat on October 17 at 15:15 Central, plus /32; keep the actual home address out of this public repository.
Preserve VpcId, resource GroupDescription, physical group, tags, outputs and existing outbound behavior. No new groups, IAM resources, IPv6 rules, routes, or instance changes. Historical Week 1 evidence and validator stay unchanged; that old validator is intentionally not the Week 2 contract.

## Validation
- cfn-lint 1.57.2: [] (zero findings).
- AWS ValidateTemplate: succeeded.
- check_scrum18.py: approved source passed; five unsafe variants rejected (two broad networks, invalid IPv4, extra SSH rule, all-protocol rule).
- Semantic comparison: every non-ingress resource property and output equals main.
- cfn-guard unavailable; the dedicated Python policy validator is used instead, with no Guard pass claimed.
- Initial generated draft had a YAML syntax error, caught locally and by ValidateTemplate; corrected before commit. No AWS write used that draft.
- Change-set validation and replacement check remain pending authorization.

## Execution and cost
Authorization must cover: update the existing security stack with exactly one IPv4 /32 rule; start the existing VM for coordinated SSH tests; stop after testing or if delayed. Expected change set: only Modify Team7ToolsSecurityGroup ingress, Replacement=False. Stop if preview includes replacement, deletion or unrelated changes.
Use original VpcId, normal rollback, unchanged stack tags and no new execution role/capability. Inspect DescribeChangeSet and DescribeEvents before execution. Verify exact rule and every group attached to the VM afterward.
Security-group rule has no separate fee. Accepted SCRUM-15 model: compute plus public IPv4 $0.0154/hour while running; EBS $0.64/month remains billable while stopped. These are recorded model rates, not a new price quote.

## Coordinated test
Recheck source public IPv4 without changing VPN/network. Start only the existing instance under this approval; re-read current public IP and wait for health checks.
Verify server SSH fingerprints independently from EC2 system log before accepting the Windows SSH prompt. Use retained private key on Windows, username ec2-user, no proxy/multiplexed session, no host-check bypass.
Capture successful authenticated login and SSH_CONNECTION matching the authorized source. Collect read-only host OS/kernel/CPU/memory/disk/network facts.
Use standard Ohio CloudShell (not a VPC environment), confirm internet access and a different public egress IP. Probe the same current instance without uploading keys. A host-key/authentication error means SSH was reached, not blocked. A timeout needs the paired successful control and reviewed rules.
Repeat fresh authorized login after the negative probe, close sessions, stop VM, and verify Stopped.
Save genuine screenshots with the established date/Team7 naming convention and hash private originals. No test result, course completion, merge or ticket closure is claimed by this plan.

## Recovery
The previous security template is on main at 3ee063f5c01ed3fc657de048e2431589215446f3. If deployment fails, inspect errors read-only and preserve rollback. A reviewed rollback to zero ingress can restore the prior boundary; do not broaden access or remove the group.
