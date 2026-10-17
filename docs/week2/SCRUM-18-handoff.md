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
- FINAL STATE: Stopped, verified by DescribeInstances at 2026-10-17T20:36:18.805918Z after testing. Root EBS remains retained/billable; there is no current public IPv4.

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

## Acceptance gaps and correction

The conversation initially summarized the restricted SSH test as passed. More precisely, the configuration, positive SSH login and negative TCP probe support expected restriction. The How-To requires an SSH-client probe from standard CloudShell followed by a new authorized SSH login. Neither that SSH-client negative probe nor the post-negative positive control has been captured. SCRUM-45 remains In Progress; no complete guide-level pass is claimed.

The initial server host key was accepted by Josh on first use (TOFU). Independent console-fingerprint comparison was unavailable. Later collection enforced the known_hosts entry. Record this deviation; do not label host identity independently verified.

SCRUM-44's configuration objective is complete. SCRUM-18 stays open until remaining test evidence, genuine screenshots and course-form fields are complete. Obtain a coordinated authorized start/test/stop window before rerunning: refresh target IP, verify healthy running VM and authorized source, use the guide's keyless CloudShell SSH probe, repeat fresh authorized login, save genuine evidence, then stop and verify. Do not broaden ingress or upload keys.

PR #7 remains unmerged. cfn-lint, AWS template validation and the dedicated Python security checks passed during preparation; no cfn-guard execution is claimed. Week 1 empty-ingress evidence remains historical.
