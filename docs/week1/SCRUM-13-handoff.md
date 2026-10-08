# SCRUM-13 review handoff

Prepared for Josh Escobar and the Cloud Architect on **2026-10-08 UTC**.
Deployment checks passed; Josh accepted the documented exceptions and remaining
review limitations. The findings handoff was posted on SCRUM-14. See
[completion acceptance](SCRUM-13-completion-acceptance.md).
Draft [PR #3](https://github.com/greycarpet/Team7/pull/3) targets `main` from
`feature/SCRUM-13-security-controls`. The deployed template is exactly approved
commit `d0be5dce16b2ad7b7915bf882ccc8f6755e7b913`; later commits contain evidence
and documentation only. No merge, Jira comment, or Done transition was performed
during deployment. Subsequent root-MFA exception documentation was explicitly
authorized by Josh on 2026-10-08.

## Deployment and verification

Account `123109186025`, region `us-east-2`, stack `cfn-security-team07`:
**CREATE_COMPLETE** at `2026-10-08T01:18:50.251Z`, standard mode, rollback enabled.
The inspected change set contained exactly one Add and no Modify/Remove or
replacement. All post-deployment reads succeeded at `01:19:09.227Z`.

| Item | Actual value |
| --- | --- |
| SecurityGroupId | `sg-0d4b70aeec5581403` |
| Name tag | `sg-tools-team07` |
| Physical GroupName | `cfn-security-team07-Team7ToolsSecurityGroup-zyMccvqygh0Z` |
| VPC / VpcId output | `vpc-05ac92d29e000c0ce`, Name `vpc-capstone-team07`, `10.7.0.0/16` |
| Inbound | Zero rules |
| Outbound | One rule `sgr-0c5218ce1138a563f`, all protocols/ports, IPv4 `0.0.0.0/0`; no IPv6/group/prefix-list destination |
| Attachments / resources | Zero ENIs attached; exactly one CloudFormation-managed security group |
| Description | `Team7 tools security group - Week 1` |
| Tags | Exact ten approved user tags and three reserved ownership tags |

See [full procedure and findings](SCRUM-13-security-controls.md),
[actual API evidence, hashes, and handling records](evidence/SCRUM-13/README.md),
and [updated shared standard](Design_Standards_Cloud_Architect/01_Cloud_Foundation_and_Naming_Standard.md).
The original reviewed ZIP is preserved; the completed landing-zone section is
unchanged, and all eight earlier screenshot hashes still match both supplied
custody logs. A private local package is prepared under
`.tools/scrum13/handoff/Capstone_Team7_Week1`; the private package itself has not
been sent. The findings/shared-document handoff was delivered through
[SCRUM-14 comment 10017](https://joshescobarx.atlassian.net/browse/SCRUM-14?focusedCommentId=10017).

## Accepted owner decisions and review limitations

- **Accepted root-MFA exception:** Josh explicitly accepted the finding on
  2026-10-08 at 18:34:18 America/Chicago (23:34:18Z) and elected not to remediate
  it for this task. `AccountMFAEnabled=0` still differs from baseline 1; root
  keys/password/signing certificates are all 0. Centralized root management
  remains **unconfirmed** because `iam:ListOrganizationsFeatures` was SCP-denied.
  This is an accepted exception, not a passing MFA control or instructor approval.
  See the [decision record](SCRUM-13-root-MFA-exception.md).
- IAM users/groups/roles are `0/0/12`. Josh's observed assumed role has attached
  `AdministratorAccess`, constrained by SCPs. A complete named team-access roster,
  intended scopes, and individual MFA evidence remain unverified. Root MFA does
  not establish individual MFA. Identity-provider reads were denied, credential
  report absent, and the regional Identity Center list was empty.
- Josh subsequently supplied the reviewed 19-image `Week01(1).zip`. Security
  screenshots are complete and their hashes are integrated in
  [the screenshot review](evidence/SCRUM-13/SCREENSHOT_REVIEW.md). Original pixels
  remain private. The findings and document links were handed off via SCRUM-14;
  no private original-image custody transfer is claimed.
- Josh explicitly accepted the separate unverified team roster/access-scope and
  individual-MFA limitations at 2026-10-08T23:47:17Z. These remain unverified,
  accepted limitations; no passing access/MFA control or instructor approval is implied.

This handoff does not authorize changing root credentials/MFA, permissions,
access assignments, or group rules. Owner remediation, cleanup, or later
infrastructure changes require a separately reviewed scope and approval.

## Console screenshot capture

Sign in through your normal supported account flow, select account
`123109186025` and **US East (Ohio) / us-east-2**. Use the real UTC capture date
for `YYYYMMDD` below. Show the account/region where safe and enough rows to prove
the result. Do not open or capture credentials, tokens, or root sign-in screens.

| View / exact filter | Filename |
| --- | --- |
| CloudFormation > Stacks > `cfn-security-team07` > Resources; include CREATE_COMPLETE status and sole resource | `YYYYMMDD_Team7_aws_w1-security-stack.png` |
| Same stack > Outputs; include both values | `YYYYMMDD_Team7_aws_w1-security-outputs.png` |
| VPC or EC2 > Security groups > filter group ID `sg-0d4b70aeec5581403` > Details; show ID, generated name, description, VPC | `YYYYMMDD_Team7_aws_w1-sg-details.png` |
| Selected group > Inbound rules; show empty list | `YYYYMMDD_Team7_aws_w1-sg-inbound.png` |
| Selected group > Outbound rules; show all traffic / all / `0.0.0.0/0`, sole rule | `YYYYMMDD_Team7_aws_w1-sg-outbound.png` |
| Selected group > Tags; show all ten user tags, using additional genuine captures if scrolling is required | `YYYYMMDD_Team7_aws_w1-sg-tags.png` |
| Permitted account review view or sanitized read-only output; record limitations, without implying individual MFA passed | `YYYYMMDD_Team7_aws_w1-account-review.png` |

Keep original screenshots privately under `.tools/scrum13/screenshots-original/`.
Compute `Get-FileHash -Algorithm SHA256 -LiteralPath '<exact original path>'`
for each capture. Record actual capture/hash time, custodian, location and any
transfer in both working custody logs. Create separately named `.redacted.png`
copies for public use, record redaction/time and their own hashes, then publish
only reviewed redactions to `docs/week1/evidence/SCRUM-13/`. Original images,
previous logs, and original API responses remain preserved. The budget screenshot is now present in the later supplied archive; its view
does not establish the 80% alert configuration or recipients.

## Completion evidence and acceptance checklist

**SCRUM-36:** Deployed `cfn-security-team07` through the reviewed CloudFormation
template at approved commit d0be5dc. Stack CREATE_COMPLETE; sole resource
`sg-0d4b70aeec5581403` in foundation VPC `vpc-05ac92d29e000c0ce`, Name tag
sg-tools-team07, generated physical name recorded. Zero inbound rules; actual
default outbound is one all-traffic IPv4 rule to 0.0.0.0/0, no IPv6 rule; group
unattached. Ten user tags, ownership, and outputs verified. API evidence/hashes
are in draft PR #3; supplied console screenshots have been reviewed and hashed.

- [x] Required VPC parameter has no default; exactly one group; no GroupName or custom egress.
- [x] Approved change set inspected, executed with rollback, stack result verified.
- [x] Actual ID, VPC, description, rules, tags, outputs, ownership and zero attachments verified.
- [x] Original API evidence preserved and separately redacted public evidence hashed.
- [x] Supplied genuine console screenshots reviewed and hashed; private originals preserved and review records committed. No public redacted images claimed.
- [x] Josh authorizes ticket completion when its requirements are satisfied (2026-10-08T23:40:41Z).

**SCRUM-37:** Completed the permitted read-only IAM/root review. Account summary:
MFA 0 (expected 1; exception accepted by Josh on 2026-10-08; not remediated),
root keys 0 (passed), root password/signing certificates
0/0, IAM users/groups/roles 0/0/12. Caller is an assumed AccountFullAccessRole
with AdministratorAccess and SCP restrictions. Centralized-root configuration,
named team assignments and individual MFA remain unverified; denied/unavailable
checks are explicitly documented. No root sign-in or credential/IAM changes.
The root-MFA owner decision is recorded in [the accepted exception](SCRUM-13-root-MFA-exception.md).
Josh accepted the separate unverified team-access/individual-MFA limitations
at 2026-10-08T23:47:17Z; the review may close with those explicit limitations.

- [x] Caller/sign-in method, account summary, inventory and permitted policy scope recorded.
- [x] Root and individual MFA findings distinguished; AccessDenied is a limitation.
- [x] Shared Security & Ops table populated with observed Josh session and honest limitations.
- [x] Josh accepts the root-MFA exception with the existing evidence and unverified centralized-root status; baseline remains unmet. See the dated decision record.
- [x] Josh accepts the unverified named team access/scopes/individual-MFA limitations; see the dated completion-acceptance record.
- [x] Josh authorizes ticket completion when its requirements are satisfied (2026-10-08T23:40:41Z).

**SCRUM-13:** Implemented and deployed the reviewed one-group Week 1 controls;
completed read-only account review, validators, API evidence, custody hashes,
updated shared naming/access document, and draft PR #3. Landing-zone material
is preserved. Security group technical checks pass; the root-MFA finding has an
accepted exception. Screenshot review and hash integration are complete. Josh accepted the remaining
access-review limitations, and the findings handoff was posted to SCRUM-14.
The parent task is accepted for completion with documented exceptions; actual
merge and Jira transition results are recorded in PR #3 and the Jira issues.

- [x] Setup/connections and real reads verified in this Codex environment.
- [x] SCRUM-13 feature branch, template, validators, deployment and API evidence prepared.
- [x] Shared document and reviewed-package history preserved; handoff prepared locally.
- [x] SCRUM-36 evidence complete; SCRUM-37 findings and limitations accepted.
- [x] Findings/shared-document handoff posted to SCRUM-14 as comment 10017; private originals were not transferred.
- [x] Josh authorizes PR merge and Jira closure; remaining owner decisions accepted at 2026-10-08T23:47:17Z and required findings handoff delivered.

## Recovery and resume

No rollback was needed. Do not rerun the CREATE change set or create another
group. If later validation finds a difference, capture actual stack events and
resource state and review the cause before any change. Cleanup is a separate
CloudFormation plan and approval; inspect attachments/references first and never
delete the foundation or default group as SCRUM-13 recovery.

To resume: open `X:\Team7` in VS Code, select
`feature/SCRUM-13-security-controls`, keep the selected model and High or higher
reasoning, read this handoff and `.tools/scrum13/SCRUM-13-checkpoint.json`, and
recheck current provider sessions. The Week 1 owner decisions and findings handoff are complete; consult PR #3 and Jira for the merge/closure results. The approved deployment is complete; no further AWS changes are approved.
