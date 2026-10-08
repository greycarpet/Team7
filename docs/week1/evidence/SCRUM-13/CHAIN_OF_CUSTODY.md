# Chain of Custody Log

Evidence stays on your machine and is handled like a real case. Fill one row per
artifact, hash it, and record every hand-off.
- Team: 7
- Cohort: 2026-09
- Started: 2026-10-07

## Handling rules

- Preserve the original — work on copies; never edit or rename the original artifact after collection.
- Name every artifact `YYYYMMDD_TeamXX_Tool_Action.ext` so it is dated, attributed and self-describing.
- Hash on collection: `sha256sum <file> >> Evidence_Hashes.txt`. Verify on receipt/before reporting: `sha256sum -c Evidence_Hashes.txt`.
- Log every artifact in this file the moment it is collected — and log every hand-off (who → who, when).
- Keep every artifact for a week in `~/team-artifacts/week-N/`; the team package gathers them into `04_Testing_and_Findings/Evidence/`. Keep originals read-only and backed up.
- One custodian holds the evidence at a time; record each transfer so the chain is unbroken.

## Log

| Evidence ID | Description | Collected by | Date/Time | Location (path) | SHA-256 | Transferred to | Transferred (date/time) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E-01 | 20261007_Team7_aws_w1-public-route-routes.png | Team 7 | 2026-10-07 | Evidence/20261007_Team7_aws_w1-public-route-routes.png | b3a4f3181a613e540c473807f722a6e41e63fd94a6252f28d9cbb9c6301a877d |   |   | 125.5 KB |
| E-02 | 20261007_Team7_aws_w1-igw.png | Team 7 | 2026-10-07 | Evidence/20261007_Team7_aws_w1-igw.png | 168cb450b7f0a335c74c0cd83975a84456f5431da7edcf0f9a2beebe71e82a99 |   |   | 99.7 KB |
| E-03 | 20261007_Team7_aws_w1-no-nat.png | Team 7 | 2026-10-07 | Evidence/20261007_Team7_aws_w1-no-nat.png | a005edda0207942aa206e24fb5698a27943b7d74dd8649b13088f89f1cd3350a |   |   | 60.8 KB |
| E-04 | 20261007_Team7_aws_w1-public-route.png | Team 7 | 2026-10-07 | Evidence/20261007_Team7_aws_w1-public-route.png | 45dceeb9ce8a9c1a5048cd2530d3d941e782f9f6138444f1c3a2471980e4da3a |   |   | 121.2 KB |
| E-05 | 20261007_Team7_aws_w1-public-subnet.png | Team 7 | 2026-10-07 | Evidence/20261007_Team7_aws_w1-public-subnet.png | acca4ef951913c552595bfdc845b80661f29953da0e7b3473f3c15a184d195e8 |   |   | 198.3 KB |
| E-06 | 20261007_Team7_aws_w1-route-association.png | Team 7 | 2026-10-07 | Evidence/20261007_Team7_aws_w1-route-association.png | 7801c99ca3013d679553983a3344450076c8ff113bfe535e2fa0698c6469c6b8 |   |   | 158.9 KB |
| E-07 | 20261007_Team7_aws_w1-stack.png | Team 7 | 2026-10-07 | Evidence/20261007_Team7_aws_w1-stack.png | af5bded58159da0a32d2d998193beeaf07673d356130a2865e3a687251c59fbd |   |   | 131.7 KB |
| E-08 | 20261007_Team7_aws_w1-vpc.png | Team 7 | 2026-10-07 | Evidence/20261007_Team7_aws_w1-vpc.png | 4aaaa471c7157ff32c040d17540f6b2bfb7445fb94111648921e14505f185bfd |   |   | 145.5 KB |
|   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |

_Aligned with NIST SP 800-61 (incident handling) and ISO/IEC 27037 (digital evidence)._


## SCRUM-13 collection and handling addition

Capture timestamps are embedded in API evidence: account review 00:54:31Z and policy review 00:55:23Z, preparation refresh 01:05:06Z, deployment/change-set 01:17:58Z–01:18:50Z, live validation 01:19:09Z, all 2026-10-08 UTC. The table timestamp records local hashing/package preparation, not screenshot capture. No screenshot or external custody transfer is claimed. Originals and historical entries remain unchanged. Public redactions are separate artifacts. Publication destination is the SCRUM-13 branch/draft PR, subject to final push verification.

| Evidence ID | Description | Collected by | Date/Time | Location (path) | SHA-256 | Transferred to | Transferred (date/time) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCRUM13-E-01 | 20261008_Team7_aws_w1-account-review-original.json | Josh Escobar's Codex session | 2026-10-08T01:21:30.412369+00:00 | .tools/scrum13/20261008_Team7_aws_w1-account-review-original.json | 8240df77f0b8ea15537a45be3366e9d7f9dcbe48c8911d337e5a5af08d831ffc |  |  | Private original account-review API responses; not transferred |
| SCRUM13-E-02 | 20261008_Team7_aws_w1-security-discovery-original.json | Josh Escobar's Codex session | 2026-10-08T01:21:30.412369+00:00 | .tools/scrum13/20261008_Team7_aws_w1-security-discovery-original.json | 78177bc428f8863054fb1332be853f785179605072fd1c93908e6da4fe1a3c6e |  |  | Private original preparation inventory; not transferred |
| SCRUM13-E-03 | 20261008_Team7_aws_w1-account-review.redacted.json | Josh Escobar's Codex session | 2026-10-08T01:21:30.412369+00:00 | docs/week1/evidence/SCRUM-13/20261008_Team7_aws_w1-account-review.redacted.json | 99d9d415dce274b4e9e96ce23ff8f700038734244b9ce38f5d8318825e754023 |  |  | Public derived redaction of account review; publication through draft PR only |
| SCRUM13-E-04 | 20261008_Team7_aws_w1-security-deployment-original.json | Josh Escobar's Codex session | 2026-10-08T01:21:30.412369+00:00 | .tools/scrum13/20261008_Team7_aws_w1-security-deployment-original.json | ab4e1f92ff5397e97a24f1c5a8bdede7180d39f2282d60115ed8c20388bdaabe |  |  | Private original approved deployment/change-set/verification API responses; not transferred |
| SCRUM13-E-05 | 20261008_Team7_aws_w1-security-deployment.redacted.json | Josh Escobar's Codex session | 2026-10-08T01:21:30.412369+00:00 | docs/week1/evidence/SCRUM-13/20261008_Team7_aws_w1-security-deployment.redacted.json | d9ff270c0b471b917ae8768bb4c2ff9c6a80707efb5ca43abf9553e8268a902b |  |  | Public derived redaction; account IDs/session identifiers masked; publication through draft PR only |

## Supplied screenshot package verification — 2026-10-08

Josh supplied the private archive in this conversation. These append-only records
describe verification of the review copy, not a new capture or transfer of
custodianship. Capture/upload timestamps are unknown; filenames are retained as
supplied. No image was edited or publicly republished. Historical entries above
are unchanged. See [SCREENSHOT_REVIEW.md](SCREENSHOT_REVIEW.md) for findings.

| Evidence ID | Description | Collected by | Date/Time | Location (path) | SHA-256 | Transferred to | Transferred (date/time) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCRUM13-ZIP-01 | Week01(1).zip | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private user-supplied archive | 23c43c447422cf37d67c96f0cf14e434afd63f392971cb86b27fe2db7ca8fc81 |  |  | Verification of review copy only; capture/upload time unknown; no Architect transfer |
| SCRUM13-S-01 | 20260930_Team7_aws_w1-budget.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20260930_Team7_aws_w1-budget.png | 7e06536bdfae0cad854a3b369d88b2620ca8515919e6d30d14b781ad775f3b22 |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-02 | 20261007_Team7_aws_w1-igw.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261007_Team7_aws_w1-igw.png | 168cb450b7f0a335c74c0cd83975a84456f5431da7edcf0f9a2beebe71e82a99 |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-03 | 20261007_Team7_aws_w1-no-nat.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261007_Team7_aws_w1-no-nat.png | a005edda0207942aa206e24fb5698a27943b7d74dd8649b13088f89f1cd3350a |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-04 | 20261007_Team7_aws_w1-public-route-routes.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261007_Team7_aws_w1-public-route-routes.png | b3a4f3181a613e540c473807f722a6e41e63fd94a6252f28d9cbb9c6301a877d |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-05 | 20261007_Team7_aws_w1-public-route.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261007_Team7_aws_w1-public-route.png | 45dceeb9ce8a9c1a5048cd2530d3d941e782f9f6138444f1c3a2471980e4da3a |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-06 | 20261007_Team7_aws_w1-public-subnet.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261007_Team7_aws_w1-public-subnet.png | acca4ef951913c552595bfdc845b80661f29953da0e7b3473f3c15a184d195e8 |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-07 | 20261007_Team7_aws_w1-route-association.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261007_Team7_aws_w1-route-association.png | 7801c99ca3013d679553983a3344450076c8ff113bfe535e2fa0698c6469c6b8 |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-08 | 20261007_Team7_aws_w1-stack.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261007_Team7_aws_w1-stack.png | af5bded58159da0a32d2d998193beeaf07673d356130a2865e3a687251c59fbd |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-09 | 20261007_Team7_aws_w1-vpc.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261007_Team7_aws_w1-vpc.png | 4aaaa471c7157ff32c040d17540f6b2bfb7445fb94111648921e14505f185bfd |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-10 | 20261008_Team7_aws_w1-account-review.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261008_Team7_aws_w1-account-review.png | e1f0d57c5a3a65c22490fe11fb0c0e2273b1bad40a7cc4731b9e2b1340001e53 |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-11 | 20261008_Team7_aws_w1-iam-roles.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261008_Team7_aws_w1-iam-roles.png | 06e93da55b93b631852029e5fdc53c6eecb2d184cd9f385ed32d26add33d1d3f |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-12 | 20261008_Team7_aws_w1-iam-users.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261008_Team7_aws_w1-iam-users.png | fd59e2dae4e4aa0a60c7976256401fb3224a5bf8cc8fb091f58a57a14aa26b23 |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-13 | 20261008_Team7_aws_w1-security-outputs.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261008_Team7_aws_w1-security-outputs.png | e7bbbcba2a8bf4808a6f5dd5062fddb6b1db8aff67081ada536c8e0a3c44226e |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-14 | 20261008_Team7_aws_w1-security-stack-info.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261008_Team7_aws_w1-security-stack-info.png | 0097fb1623ce0b401a6023e61f82121327eed4955204790f6dbad9e3386c9a18 |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-15 | 20261008_Team7_aws_w1-security-stack.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261008_Team7_aws_w1-security-stack.png | e7a90701c90997731999973d4256778e764b89f01a51d70425cfb4a54a6e9f31 |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-16 | 20261008_Team7_aws_w1-sg-details.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261008_Team7_aws_w1-sg-details.png | b1f4825ba7dfb76e9f51de09451fecdc9896be14a357bcbc36b9c8a68295112c |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-17 | 20261008_Team7_aws_w1-sg-inbound.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261008_Team7_aws_w1-sg-inbound.png | ca1423c764995206f055e320c518e693ca095aba58b6245d4d4e2bfd76c5edc5 |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-18 | 20261008_Team7_aws_w1-sg-outbound.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261008_Team7_aws_w1-sg-outbound.png | eff65a08d037624390d8279fd3925c51fa8adc0efdc1e80ecdda457261863d33 |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
| SCRUM13-S-19 | 20261008_Team7_aws_w1-sg-tags.png | Josh Escobar (supplied) | 2026-10-08T23:44:14.332044+00:00 | Private Week01(1).zip::Week01/20261008_Team7_aws_w1-sg-tags.png | ef4863d4a6a3e955290c6ce8477ca14abded80ba78f40b3b517171365b134294 |  |  | Verification of unchanged supplied original; timestamp is verification not capture; no Architect transfer |
