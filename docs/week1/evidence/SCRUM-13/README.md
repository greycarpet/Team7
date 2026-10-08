# SCRUM-13 evidence manifest

The first account-review artifacts below are **read-only preparation evidence**.
The subsequent deployment record contains genuine change-set, execution, stack,
group, rule, tag, output, and attachment responses from the approved deployment.
No console screenshot was captured in this session.

The account-review original contains the actual detailed AWS MCP discovery/policy
responses and their executed `api_calls` records. It is preserved privately under
`.tools/scrum13/20261008_Team7_aws_w1-account-review-original.json`, outside Git.
The public file is a separately identified derived redaction, retaining factual
flags/counts/rules and check limitations while masking account IDs and omitting
  personal/organization/session details. The final stack/group/VPC refresh is
  preserved separately in the private security-discovery original below.

Evidence JSON is marked `-text` in this directory's `.gitattributes`, preventing
Git's Windows/Linux line-ending conversion from changing its recorded byte hash.

| Artifact | SHA256 |
| --- | --- |
| Private `20261008_Team7_aws_w1-account-review-original.json` | `8240df77f0b8ea15537a45be3366e9d7f9dcbe48c8911d337e5a5af08d831ffc` |
| Private `.tools/scrum13/20261008_Team7_aws_w1-security-discovery-original.json` | `78177bc428f8863054fb1332be853f785179605072fd1c93908e6da4fe1a3c6e` |
| Public [20261008_Team7_aws_w1-account-review.redacted.json](20261008_Team7_aws_w1-account-review.redacted.json) | `99d9d415dce274b4e9e96ce23ff8f700038734244b9ce38f5d8318825e754023` |

## Collection and handling record

- AWS discovery was captured at `2026-10-08T00:54:31.453239Z`; policy review at
  `2026-10-08T00:55:23.865206Z`, by executed read-only API calls in account
  `123*****6025`, with regional operations in `us-east-2`.
- Final security-stack absence, zero matching-name groups, and foundation/VPC
  verification were captured at `2026-10-08T01:05:06.093952Z` and saved separately
  at `2026-10-08T01:05:06.4316635Z`. Their explicit results are labeled in the
  public snapshot. Absence is not inferred from AccessDenied.
- Private original saved locally at `2026-10-08T00:57:56.8409539Z`.
- Public redaction last updated at `2026-10-08T01:05:07.1591902Z`; account-ID
  replacement was applied throughout the derived JSON. The original was not
  overwritten. Hashes were computed after redaction.
- Collector: Josh Escobar's Codex session, using the authenticated Team7 AWS
  connection. No AWS credentials were collected in these artifacts.
- Preparation publication is through the requested SCRUM-13 draft PR. No Jira
  comments, ticket transitions, or external handoff messages were posted.

Root MFA flag **0** remains an owner-review finding. Root access keys flag **0**
passes that baseline. IAM user/group counts **0/0** and role count **12** do not
establish individual MFA or a team roster. SCP-denied reads and unavailable
credential-report data remain explicit limitations.

## Approved deployment evidence

Approved template commit: `d0be5dce16b2ad7b7915bf882ccc8f6755e7b913`.
Template SHA256: `7c6b00d2e66f1b73237787ce21cb5f9993a79d95c7420b34bdb3a70f7e55317e`.
Account target was verified as `123*****6025`, with every regional API in
`us-east-2`. Change-set creation was captured at `2026-10-08T01:17:58.475Z`,
inspection at `01:18:08.572Z`, validation/template retrieval at `01:18:17.193Z`,
execution at `01:18:39.773Z`, and final read-only checks at `01:19:09.227Z`.
Stack `cfn-security-team07` reached `CREATE_COMPLETE` at `01:18:50.251Z`.

| Artifact | SHA256 |
| --- | --- |
| Private `.tools/scrum13/20261008_Team7_aws_w1-security-deployment-original.json` | `ab4e1f92ff5397e97a24f1c5a8bdede7180d39f2282d60115ed8c20388bdaabe` |
| Public [20261008_Team7_aws_w1-security-deployment.redacted.json](20261008_Team7_aws_w1-security-deployment.redacted.json) | `d9ff270c0b471b917ae8768bb4c2ff9c6a80707efb5ca43abf9553e8268a902b` |

The complete original was saved before redaction. The public copy masks account
IDs throughout and removes STS user/session identifiers. It retains executed
`api_calls`, resolved change-set properties, CloudFormation events, and actual
EC2 records; it is **API evidence, not screenshots**. Hashes were computed after
the original/redaction writes. Local handling/package preparation was recorded at
`2026-10-08T01:21:30.412Z`. Prior evidence hashes remain unchanged.

Verified result: one unattached group `sg-0d4b70aeec5581403`; Name tag
`sg-tools-team07`; generated GroupName
`cfn-security-team07-Team7ToolsSecurityGroup-zyMccvqygh0Z`; zero ingress; one
IPv4 allow-all egress rule `sgr-0c5218ce1138a563f` to `0.0.0.0/0`; no IPv6 rule.
All ten user tags and three reserved ownership tags match. Both outputs match.
Normal rollback was enabled. Root/account flags refreshed and remain unchanged.

[CHAIN_OF_CUSTODY.md](CHAIN_OF_CUSTODY.md) and
[CHAIN_OF_CUSTODY.csv](CHAIN_OF_CUSTODY.csv) preserve all historical reviewed
package entries and append the genuine SCRUM-13 collection/hashing records.
Earlier screenshot locations are historical paths within the reviewed package.
The original ZIP and its logs are unchanged. All eight prior screenshot hashes
were verified. Publication uses the requested branch/draft PR; no external
handoff message, Jira comment, transition, or merge is claimed.

The private working handoff package in `.tools/scrum13/handoff/` retains the eight
previous screenshot originals, updated shared document, appended logs, and new
original/redacted API evidence. It must be reviewed before sharing because it
contains private originals. Repository copies link earlier screenshots as
historical package references, without republishing those images.

Console evidence remains pending. Use [the exact screenshot checklist and
acceptance handoff](../../SCRUM-13-handoff.md). Capture filenames using the actual
UTC date; preserve originals, hash them, and create separately identified
redacted copies for public publication. Do not invent capture or transfer times.
