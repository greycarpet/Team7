# SCRUM-13 preparation evidence manifest

This is **read-only preparation evidence**, not proof that the tools security
group has been deployed. No screenshot, change set, security stack, or tools
group was created during preparation.

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

After approved deployment, append real stack/group responses, original screenshot
hashes, separately named public redactions, UTC capture times, and actual transfer
details. Retain existing entries and the reviewed Week 1 package's original logs.
See [the deployment and screenshot plan](../../SCRUM-13-security-controls.md).
