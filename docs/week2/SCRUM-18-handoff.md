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
- Authorized Windows login, in-guest VM facts, CloudShell blocked test, repeat positive control, screenshots and final stop are still pending.
- VM IS RUNNING for testing. Stop after testing or if the session is delayed. Refresh current public IPv4 after every restart.
- Client key fingerprint is not the server fingerprint. Never bypass host checking or upload the private key.
