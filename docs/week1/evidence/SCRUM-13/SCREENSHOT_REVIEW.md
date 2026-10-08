# SCRUM-13 supplied screenshot review

Josh supplied `Week01(1).zip` in the task conversation. The archive contains
19 genuine console PNGs: the prior 17 unchanged images plus the IAM roles and
security stack-info views. Visual review was completed in this conversation;
the existing review manifest, every ZIP member, and each extracted original
were checked for byte equality at **2026-10-08T23:44:14.332044+00:00**.

Archive SHA256: `23c43c447422cf37d67c96f0cf14e434afd63f392971cb86b27fe2db7ca8fc81`.

This timestamp records verification, not capture or an external handoff.
Exact capture times and the original upload time were not independently
established. Dates below are retained from the supplied filenames. Original
names and bytes are unchanged. The originals remain in Josh's supplied private
archive and the conversation's review copy; no screenshot pixels are published
in this public repository. This file publishes review results and hashes only.
The prior API evidence and all historical custody entries remain unchanged.

## Review results

| Original filename | Review |
| --- | --- |
| `20260930_Team7_aws_w1-budget.png` | Budget list shows budget-monthly-team07, $5 limit, and $0 used; 80% alert configuration and recipients are not shown. |
| `20261007_Team7_aws_w1-igw.png` | Internet gateway attached to the Team7 VPC; unchanged prior landing-zone evidence. |
| `20261007_Team7_aws_w1-no-nat.png` | No NAT gateways listed; region is not visible in this image. |
| `20261007_Team7_aws_w1-public-route-routes.png` | Both local and internet-gateway routes are Active. |
| `20261007_Team7_aws_w1-public-route.png` | Public route-table details and subnet association. |
| `20261007_Team7_aws_w1-public-subnet.png` | Correct subnet, VPC, CIDR, availability zone, and public IPv4 assignment setting. |
| `20261007_Team7_aws_w1-route-association.png` | Explicit public-subnet association. |
| `20261007_Team7_aws_w1-stack.png` | Foundation resources show CREATE_COMPLETE. |
| `20261007_Team7_aws_w1-vpc.png` | Correct non-default VPC, Available state, and CIDR. |
| `20261008_Team7_aws_w1-account-review.png` | Root-access privileged-action menu only; does not prove MFA, centralized-root configuration, or an AccessDenied result. |
| `20261008_Team7_aws_w1-iam-roles.png` | All 12 IAM roles are visible; this is not a named human-access roster. |
| `20261008_Team7_aws_w1-iam-users.png` | IAM users count is zero; this does not establish absence of federated users or individual MFA. |
| `20261008_Team7_aws_w1-security-outputs.png` | SecurityGroupId and VpcId match the approved deployment. |
| `20261008_Team7_aws_w1-security-stack-info.png` | Overall security stack CREATE_COMPLETE; account/region and stack identity match. |
| `20261008_Team7_aws_w1-security-stack.png` | Exactly one security-group resource, CREATE_COMPLETE. |
| `20261008_Team7_aws_w1-sg-details.png` | Security-group ID, generated name, description, and VPC match. |
| `20261008_Team7_aws_w1-sg-inbound.png` | Zero inbound rules. |
| `20261008_Team7_aws_w1-sg-outbound.png` | One all-traffic IPv4 rule to 0.0.0.0/0; no IPv6 rule shown. |
| `20261008_Team7_aws_w1-sg-tags.png` | All ten required user tags are visible; reserved ownership tags corroborated by API evidence. |

The security-group screenshot collection is complete and corroborates the
recorded deployment. No retakes are required for these views. Account-summary
API evidence remains the source for root MFA and root access-key flags.
The [accepted root-MFA exception](../../SCRUM-13-root-MFA-exception.md) does
not resolve the separate unverified team assignments or individual MFA.
The budget screenshot is now supplied, but it does not prove alert settings.

## Original SHA256 hashes

| Original filename | SHA256 |
| --- | --- |
| `20260930_Team7_aws_w1-budget.png` | `7e06536bdfae0cad854a3b369d88b2620ca8515919e6d30d14b781ad775f3b22` |
| `20261007_Team7_aws_w1-igw.png` | `168cb450b7f0a335c74c0cd83975a84456f5431da7edcf0f9a2beebe71e82a99` |
| `20261007_Team7_aws_w1-no-nat.png` | `a005edda0207942aa206e24fb5698a27943b7d74dd8649b13088f89f1cd3350a` |
| `20261007_Team7_aws_w1-public-route-routes.png` | `b3a4f3181a613e540c473807f722a6e41e63fd94a6252f28d9cbb9c6301a877d` |
| `20261007_Team7_aws_w1-public-route.png` | `45dceeb9ce8a9c1a5048cd2530d3d941e782f9f6138444f1c3a2471980e4da3a` |
| `20261007_Team7_aws_w1-public-subnet.png` | `acca4ef951913c552595bfdc845b80661f29953da0e7b3473f3c15a184d195e8` |
| `20261007_Team7_aws_w1-route-association.png` | `7801c99ca3013d679553983a3344450076c8ff113bfe535e2fa0698c6469c6b8` |
| `20261007_Team7_aws_w1-stack.png` | `af5bded58159da0a32d2d998193beeaf07673d356130a2865e3a687251c59fbd` |
| `20261007_Team7_aws_w1-vpc.png` | `4aaaa471c7157ff32c040d17540f6b2bfb7445fb94111648921e14505f185bfd` |
| `20261008_Team7_aws_w1-account-review.png` | `e1f0d57c5a3a65c22490fe11fb0c0e2273b1bad40a7cc4731b9e2b1340001e53` |
| `20261008_Team7_aws_w1-iam-roles.png` | `06e93da55b93b631852029e5fdc53c6eecb2d184cd9f385ed32d26add33d1d3f` |
| `20261008_Team7_aws_w1-iam-users.png` | `fd59e2dae4e4aa0a60c7976256401fb3224a5bf8cc8fb091f58a57a14aa26b23` |
| `20261008_Team7_aws_w1-security-outputs.png` | `e7bbbcba2a8bf4808a6f5dd5062fddb6b1db8aff67081ada536c8e0a3c44226e` |
| `20261008_Team7_aws_w1-security-stack-info.png` | `0097fb1623ce0b401a6023e61f82121327eed4955204790f6dbad9e3386c9a18` |
| `20261008_Team7_aws_w1-security-stack.png` | `e7a90701c90997731999973d4256778e764b89f01a51d70425cfb4a54a6e9f31` |
| `20261008_Team7_aws_w1-sg-details.png` | `b1f4825ba7dfb76e9f51de09451fecdc9896be14a357bcbc36b9c8a68295112c` |
| `20261008_Team7_aws_w1-sg-inbound.png` | `ca1423c764995206f055e320c518e693ca095aba58b6245d4d4e2bfd76c5edc5` |
| `20261008_Team7_aws_w1-sg-outbound.png` | `eff65a08d037624390d8279fd3925c51fa8adc0efdc1e80ecdda457261863d33` |
| `20261008_Team7_aws_w1-sg-tags.png` | `ef4863d4a6a3e955290c6ce8477ca14abded80ba78f40b3b517171365b134294` |

## Completion acceptance

Screenshot review and hash integration are complete. Josh explicitly accepted
the separate named team-access / individual-MFA limitations at
2026-10-08T23:47:17Z. The prepared findings were delivered to SCRUM-14 in
[comment 10017](https://joshescobarx.atlassian.net/browse/SCRUM-14?focusedCommentId=10017).
See [completion acceptance](../../SCRUM-13-completion-acceptance.md).
Underlying unverified findings and the root-MFA exception remain explicit;
no private original-image custody transfer is claimed.
