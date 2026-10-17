# SCRUM-18 deployment checkpoint

Updated 2026-10-17. Josh authorized PR #7 at 15:18 America/Chicago.
Template commit 562d839eaa65bcc8cbf285aae7059cbdbfb213eb.

- cfn-security-team07 reached UPDATE_COMPLETE.
- Reviewed change set: scrum18-ssh-562d839-20261017. One Modify of Team7ToolsSecurityGroup, Replacement=False. Runtime property change is ingress only; descriptive metadata also updated. No validation-error events.
- Group sg-0d4b70aeec5581403 retains original VPC, GroupDescription, tags and default IPv4 egress.
- Exactly one ingress rule: TCP/22, one approved operator public IPv4 /32. Actual source retained in private project conversation and AWS parameter; omitted here.
- Instance i-0dd31fddcfc283ea7 has only this security group attached.
- Instance started at 2026-10-17T20:20:07Z for the authorized coordinated test window.
- All three health checks passed after startup. Latest console output shows the restarted OS, AL2023.12.20261016 and kernel 6.18.54-121.166.amzn2023.x86_64, but no SSH host-key fingerprints. Standard console-output reads returned empty output. Independent host identity verification remains pending; no host identity pass is claimed.
- FINAL STATE: Stopped, verified by DescribeInstances at 2026-10-17T20:47:53.236206Z after the completed retest. Root EBS remains retained/billable; there is no current public IPv4.

## Actual validation record, October 17, 2026

| Observation | Evidence | Interpretation |
| --- | --- | --- |
| Authorized login | Windows report at 20:30:12Z; ec2-user; SSH_CONNECTION source matched authorized /32; SSH exit 0 | Authenticated positive test succeeded |
| CloudShell public connectivity | checkip endpoint returned a different public egress IPv4 at 20:34:39Z | Internet access and distinct observed source established; environment type not separately captured |
| CloudShell TCP/22 | timeout 10 bash -c TCP-connect probe against same temporary public target; exit 124 | Expected TCP timeout; this was not an SSH-client probe |
| Effective access | AWS read after tests: only intended group attached; exactly TCP/22 from one /32, no IPv6 ingress | Configuration supports source restriction |
| Target state | AWS read after negative test found instance running at the test target; normal StopInstances followed | Timeout was not manufactured by stopping the VM |
| Final state | DescribeInstances at 20:36:18.805918Z: stopped | Required cost-control stop verified |

Original positive report: Team7-VM-Facts-20261017T203004365Z.txt, SHA-256 5090a9a067e987aae4c38c44a39843b9d388552fe447a90e52a59fceaa964b1f, retained privately. CloudShell output was supplied by Josh in the project conversation; do not describe it as an uploaded file or screenshot. Personal source/destination public IPs are omitted from this public summary and recorded in private Jira. No private key was sent to CloudShell.

## Initial acceptance gaps (historical)

The conversation initially summarized the restricted SSH test as passed. More precisely, the configuration, positive SSH login and negative TCP probe support expected restriction. The How-To requires an SSH-client probe from standard CloudShell followed by a new authorized SSH login. Those two observations were missing at the first checkpoint; the completed retest below supersedes that gap.

The initial server host key was accepted by Josh on first use (TOFU). Independent console-fingerprint comparison was unavailable. Later collection enforced the known_hosts entry. Record this deviation; do not label host identity independently verified.

SCRUM-44's configuration objective is complete. SCRUM-18 stays open for remaining genuine screenshots and course-form fields. The form is deferred until last per Josh's instruction.

PR #7 remains unmerged. cfn-lint, AWS template validation and the dedicated Python security checks passed during preparation; no cfn-guard execution is claimed. Week 1 empty-ingress evidence remains historical.

## Completed SSH retest, October 17, 2026

Josh continued the authorized test workflow. The same instance was restarted; its temporary public IPv4 changed. Both positive logins and the negative probe targeted that same new address (exact public addresses retained privately in Jira).

| UTC time | Source / test | Actual result |
| --- | --- | --- |
| 20:43:02 | Josh's Windows laptop, fresh SSH | ec2-user, expected hostname, SSH_CONNECTION source matches authorized /32 |
| 20:44:12 | Ohio CloudShell, keyless OpenSSH probe | connect to host port 22: Connection timed out; SSH exit 255 |
| 20:45:26 | Josh's Windows laptop, fresh SSH after negative | ec2-user, expected hostname, same authorized source and private target |
| 20:47:53.236206 | AWS DescribeInstances after normal stop | stopped; no current public IPv4 |

The negative probe used -4, -F /dev/null, ConnectTimeout=10, ConnectionAttempts=1, BatchMode=yes, PubkeyAuthentication=no, PasswordAuthentication=no, KbdInteractiveAuthentication=no and StrictHostKeyChecking=yes. Public checkip succeeded and showed a different source. Windows used -F NUL, IdentitiesOnly=yes, StrictHostKeyChecking=yes, and HostKeyAlias referencing its previously saved server entry. No authentication bypass or ingress expansion was used.

Post-test AWS inspection confirmed running at the same target before stopping, only sg-0d4b70aeec5581403 attached, and exactly TCP/22 from the authorized /32 with no IPv6 ingress. Combined configuration and before/after SSH controls support the unauthorized-source network block. A timeout alone does not identify which network control dropped traffic.

Genuine screenshot visually reviewed: 20261017_Team7_aws_w2-ssh-cloudshell-blocked.png. It shows the Ohio CloudShell tab, source, complete SSH command, 20:44:12 UTC timestamp, timeout and exit 255. SHA-256: 723f3b5ff972c2f51bf1fc5a973d75274cfa96e8f5886de90291180d8f42edf8. Original retained privately in the project upload; not published to this public repository. It also includes the earlier TCP test, which remains separately identified as historical.

SCRUM-45's allowed/blocked validation objective is complete. Windows positive results are user-supplied terminal transcripts; their screenshot remains requested for the course package. Remaining parent deliverables: configuration/final-stopped screenshots, allowed-login screenshot, shared-form population (last), and review. TOFU limitation above remains; the retest proves host-key continuity, not independent initial identity verification.
