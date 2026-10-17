# SCRUM-16 deployment handoff

> Current checkpoint, 2026-10-17: deployment, VM facts, SSH positive/negative/positive tests, final stop, and requested screenshot follow-ups are recorded. Remaining: PR review and the official Solution Architecture form/PDF (last). Initial SSH host identity was accepted on first use; independent verification is not claimed. Earlier observations below are historical where superseded.

Josh authorized deployment on October 17, 2026 at 15:03 America/Chicago. Initial template commit: 25cf463. The CREATE change set contained exactly three Adds, no IAM capabilities, normal rollback and no validation-error events. Stack creation succeeded.

## Verified infrastructure

- Stack cfn-tools-team07, us-east-2: UPDATE_COMPLETE.
- Instance i-0dd31fddcfc283ea7, Name ec2-tools-team07, Amazon Linux 2023 AMI ami-0d31a22b09ceec4db, t3.micro, us-east-2a.
- Existing subnet subnet-015dee27e366615f0, VPC vpc-05ac92d29e000c0ce; private IPv4 10.7.1.86.
- Launch template lt-0c14241003db84e8b version 1; imported key key-tools-team07.
- IMDSv2 required, endpoint enabled, hop limit 1; Standard CPU credits; detailed monitoring disabled.
- Root vol-06c9656cbce745cdb: encrypted 8 GiB gp3, 3000 IOPS, 125 MiB/s, Name ebs-tools-team07. Retained on stop; deleted on termination.
- System, instance and attached EBS status checks all passed before stopping.
- FINAL STATE: Stopped, verified 2026-10-17T20:47:53.236206Z after the completed SSH retest window. Disk remains attached/billable. There is no current public IPv4; re-read it after next start. Creation-time CloudFormation outputs are not authoritative after restart.
- Only sg-0d4b70aeec5581403 attached. SCRUM-18 has since changed the Week 1 zero-ingress baseline to exactly TCP/22 from one authorized operator IPv4 /32; no IPv6 ingress. Authorized Windows SSH succeeded.
- Imported public-key bytes match Josh's supplied RSA public key. SHA256:PXjRehpG9x82mXhuq3lG0mH7Ys5aiNaTxkeTVL75rc4. This is the client key fingerprint, not the server host fingerprint. Private key remains on Josh's Windows laptop.

## Naming correction
CloudFormation propagated stack Name=cfn-tools-team07 over the launch template's instance Name. Corrected by explicitly defining instance resource tags at commit 48d77a53422b6e7c5bdd6c65e12fbd3a88d6827c. cfn-lint returned []. The reviewed UPDATE change set showed only Team7ToolsInstance Tags, Replacement=False, RequiresRecreation=Never, with no validation errors. Update succeeded; actual Name=ec2-tools-team07 verified. No instance replacement or ingress change.

## Host-level facts collected

Josh took over Alyssa's implementation because she was unavailable. At 2026-10-17T20:30:12Z (15:30:12 CDT), Josh ran Collect-Team7-VMFacts.ps1 from Windows. All ten diagnostic commands returned 0, collection reported zero failed checks, and SSH returned 0.

| Field | Observed value |
| --- | --- |
| VM name | ec2-tools-team07 |
| Login | ec2-user |
| OS | Amazon Linux 2023.12.20261016 |
| Kernel | 6.18.54-121.166.amzn2023.x86_64 |
| Type / CPU | t3.micro / 2 logical CPUs, x86_64 |
| Guest memory | 913 MiB total, 634 MiB available at collection |
| Disk / root filesystem | 8 GiB / XFS |
| Private IPv4 | 10.7.1.86/24, ens5 |
| Default gateway | 10.7.1.1 |

Server-observed SSH_CONNECTION source matched the approved /32. The original report remains private: Team7-VM-Facts-20261017T203004365Z.txt, SHA-256 5090a9a067e987aae4c38c44a39843b9d388552fe447a90e52a59fceaa964b1f. This public summary omits personal public IP, temporary destination public IP, machine/boot IDs and full raw output. Private key/passphrase remain on Josh's Windows laptop; they were not transferred.

## Host identity limitation

The server ED25519 key was accepted on first use by Josh. Available EC2 console logs did not contain a usable fingerprint for independent comparison. Later scripted SSH required the existing known_hosts entry. This is TOFU, not independently verified host identity. Preserve the deviation from the guide; do not claim that control passed.

## Handoff and remaining acceptance

SCRUM-40's deployment objective and SCRUM-41's facts/access/stop objectives are complete. Josh performed both infrastructure and Security & Ops work with his own retained key. Copy the values above into the actual course form; no live form edit is claimed.

SCRUM-16 remains open for final review and shared-form population. The requested storage screenshots have been received and reviewed below. SCRUM-18's SSH-specific negative probe and fresh positive controls are now complete: authorized logins at 20:43:02Z and 20:45:26Z bracket the CloudShell SSH timeout at 20:44:12Z on October 17. The same instance remained running throughout; it was stopped afterward. See PR #7's SCRUM-18 handoff. Josh requested the shared Solution Architecture form be completed last.

SCRUM-19 requires the current official form, final field mapping, evidence, review and official PDF export. No Alyssa/instructor approval or submission is claimed. PR #6 remains unmerged.

Earlier AWS deployment extract: [deployment.json](evidence/SCRUM-16/deployment.json). Its earlier zero-ingress/stopped observations are historical; this dated handoff records subsequent changes.

## Root storage screenshot received, October 17, 2026

Visually reviewed original 20261017_Team7_aws_w2-ec2-volume.png (SHA-256 424065a32cb7b9969b8416750e92918ce0f658ea4cc5298127ba3a54ce6f690c). It shows the exact stopped instance, root /dev/xvda, vol-06c9656cbce745cdb, 8 GiB, Attached/In-use, Encrypted Yes, and Delete on termination Yes. It is the instance Storage tab, not the volume Details view; gp3 is not visible in this image. The volume Details capture reviewed below establishes gp3 visually as well. Original retained privately in the project upload, not published here.

## Detail screenshot follow-up, October 17, 2026

Visually verified 20261017_Team7_aws_w2-ec2-volume-details.png: vol-06c9656cbce745cdb / ebs-tools-team07, 8 GiB gp3, 3000 IOPS, throughput 125, us-east-2a, attached to the correct tools instance as /dev/xvda, Encrypted with aws/ebs. Volume is In-use because it remains attached; this does not contradict the stopped instance. SHA-256 4b07aeb41bebab2cea3d5c3539136c50937bc058cf04883a7351674caf034d37. This closes the requested volume-type screenshot gap.

Original retained privately in the project upload, unchanged and not publicly published. This follow-up supersedes the corresponding pending screenshot note above. The Solution Architecture form remains deferred until last; PR merge and parent-ticket completion are not claimed.
