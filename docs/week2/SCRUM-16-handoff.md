# SCRUM-16 deployment handoff

Josh authorized deployment on October 17, 2026 at 15:03 America/Chicago. Initial template commit: 25cf463. The CREATE change set contained exactly three Adds, no IAM capabilities, normal rollback and no validation-error events. Stack creation succeeded.

## Verified infrastructure

- Stack cfn-tools-team07, us-east-2: UPDATE_COMPLETE.
- Instance i-0dd31fddcfc283ea7, Name ec2-tools-team07, Amazon Linux 2023 AMI ami-0d31a22b09ceec4db, t3.micro, us-east-2a.
- Existing subnet subnet-015dee27e366615f0, VPC vpc-05ac92d29e000c0ce; private IPv4 10.7.1.86.
- Launch template lt-0c14241003db84e8b version 1; imported key key-tools-team07.
- IMDSv2 required, endpoint enabled, hop limit 1; Standard CPU credits; detailed monitoring disabled.
- Root vol-06c9656cbce745cdb: encrypted 8 GiB gp3, 3000 IOPS, 125 MiB/s, Name ebs-tools-team07. Retained on stop; deleted on termination.
- System, instance and attached EBS status checks all passed before stopping.
- FINAL STATE: Stopped, verified 2026-10-17T20:09:59.751050Z. Disk remains attached/billable. Re-read public IPv4 after next start; creation-time CloudFormation output is not authoritative after restart.
- Only sg-0d4b70aeec5581403 attached; zero inbound rules. SSH tests have not been performed.
- Imported public-key bytes match Josh's supplied RSA public key. SHA256:PXjRehpG9x82mXhuq3lG0mH7Ys5aiNaTxkeTVL75rc4. This is the client key fingerprint, not the server host fingerprint. Private key remains on Josh's Windows laptop.

## Naming correction
CloudFormation propagated stack Name=cfn-tools-team07 over the launch template's instance Name. Corrected by explicitly defining instance resource tags at commit 48d77a53422b6e7c5bdd6c65e12fbd3a88d6827c. cfn-lint returned []. The reviewed UPDATE change set showed only Team7ToolsInstance Tags, Replacement=False, RequiresRecreation=Never, with no validation errors. Update succeeded; actual Name=ec2-tools-team07 verified. No instance replacement or ingress change.

## Acceptance still pending
SCRUM-40's technical deployment objective is verified. SCRUM-16/41 remain incomplete pending host-level VM facts, access/test evidence and course screenshots. SCRUM-18 needs Josh's current Windows-laptop public IPv4, one approved /32 ingress rule on the existing security stack, and a coordinated start/test/stop window. Verify server fingerprints before SSH acceptance; collect host facts on Windows using the retained private key. A CloudShell timeout is not proof without paired allowed-source success and reviewed network configuration.

SCRUM-19 still needs these actual VM/test fields in the official form and final PDF. Do not claim Alyssa or instructor approval. PR #6 stays draft; no merge or ticket closure is asserted.

Evidence: [compact AWS observations](evidence/SCRUM-16/deployment.json). This extract excludes full public-key material, account identifiers, temporary public IP and unrelated fields. No console screenshot or in-guest OS/kernel observation is claimed.
