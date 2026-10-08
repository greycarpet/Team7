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
