# SCRUM-13: Week 1 initial security controls

Prepared by Josh Escobar on `feature/SCRUM-13-security-controls` for a draft PR
to `main`. Discovery and validation were performed on **2026-10-08 UTC**.
The approved template was deployed successfully on **2026-10-08 UTC**. Josh accepted
the [root-MFA exception](SCRUM-13-root-MFA-exception.md) at 23:34:18Z on that date;
the observed flag remains 0 and the baseline is not passed. Supplied screenshots
have now been reviewed and hashed. Team-access owner review and the Cloud
Architect handoff remain open. Josh has authorized merge/closure once complete. No AWS changes
were performed during the earlier preparation stage.

## Sources and precedence

- Live Jira: [SCRUM-13](https://joshescobarx.atlassian.net/browse/SCRUM-13),
  [SCRUM-36](https://joshescobarx.atlassian.net/browse/SCRUM-36),
  [SCRUM-37](https://joshescobarx.atlassian.net/browse/SCRUM-37), and
  [SCRUM-11](https://joshescobarx.atlassian.net/browse/SCRUM-11). Josh is assigned
  to SCRUM-13/36/37; SCRUM-11 and its subtasks are Done.
- Root `AGENTS.md` was read; no nested instruction files were found. Its global
  AWS approval policy remains in force. The user explicitly authorized this
  separate SCRUM-13 security template; the SCRUM-11 resource list describes the
  completed landing-zone task.
- Remote SCRUM-13 branch and `main` both started at
  `5dae7e4a45aa27333fbf8eeddf21d88c4bb995be`, verified by fetch and remote reads.
- Current local course guide: `W1_Establish_Initial_Security_Controls_SCRUM-13.pdf`,
  instruction v1.0 dated 2026-10-07; SHA256
  `818ab0c9758f7420984f788903234b9be63cf7201ca302bf74545735c857bfd7`.
- Jira attachment 10009: `Team7_W1_Establish_Initial_Security_Controls_How_To.pdf`,
  dated 2026-09-30; SHA256
  `51529c89dd9addcf9cf71194f795aa23826866a839027f500f3132a025b780ee`.
  Both guides were extracted and relevant rendered pages reviewed. The older
  manual instruction to use an `sg-` physical name is superseded by the current
  guide, the explicit task instructions, and AWS's naming restriction.
- Reviewed shared-document source:
  `Capstone_Team7_Week1_Reviewed.zip`, member
  `Capstone_Team7_Week1/Design_Standards_Cloud_Architect/01_Cloud_Foundation_and_Naming_Standard.md`,
  SHA256 `6b2f495a23fd9c142d493db9e5daea030a41d11bf2acedeaad217fe9476c081e`.
  This version contains the completed landing-zone section and eight evidence
  references. The loose Downloads Markdown copy has blank landing-zone fields
  and is not the handoff baseline. Preserve the reviewed version and its
  completed Infrastructure section when updating it after approved deployment.

## Development environment and connection checks

The actual execution environment is Windows (`10.0.26300`), native Windows
PowerShell 5.1, workspace `X:\Team7`; no WSL environment was detected. The current
Codex session records source `vscode`, CLI 0.161.0, model `gpt-6.1-sol`, and
effective effort `high`. The selected model and approval controls were preserved.
VS Code 1.140.0, Git 2.56.0.windows.2, AWS CLI 2.37.7, uv 0.12.21, project Python
3.13.15, cfn-lint 1.57.2, and Guard 3.2.1 were reused. PyMuPDF 1.28.2 was installed
only into the project virtual environment to read/render the supplied PDFs.

| Connection | Actual read-only test | Result |
| --- | --- | --- |
| GitHub | Authenticated profile and `greycarpet/Team7` metadata | `greycarpet`, linked account ID 250448628; repository push permission reported |
| Git transport | Fetch and remote branch-head reads; Git Credential Manager account listing | Existing `manager` helper and `greycarpet` credential entry reused |
| Atlassian/Rovo | Personal Projects reads of SCRUM-13/36/37/11, plus authenticated PDF download | Correct site `joshescobarx.atlassian.net`; ticket and attachment reads passed |
| AWS MCP | STS identity, CloudFormation, EC2, and IAM reads | Expected account `123*****6025`; regional calls explicitly `us-east-2` |
| AWS CLI | STS identity using `--profile aws-Team7 --region us-east-2` | Same expected account and assumed role |

Git author name is set locally to **Josh Escobar**. His existing linked GitHub
noreply address `250448628+greycarpet@users.noreply.github.com` was retained.
GitHub CLI was not required because the working official connector and existing
Git Credential Manager cover PR creation and Git authentication. Normal branch
push and draft PR #3 were verified. No credentials were printed or
copied into source, no long-lived keys were created, and no permissions widened.
The prior SCRUM-11 setup stash was not applied to this branch.

For a fresh clone, install only missing tools using their official installers.
For this existing checkout, use `.venv\Scripts\python.exe`; the system `python`
alias points to the Microsoft Store. The local validator is pinned in
`requirements-dev.txt` and can be installed into a suitable isolated environment:

```powershell
.\.venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements-dev.txt
.\scripts\Validate-Scrum13.ps1
```

The validation helper expects the reused local Guard binary under
`.tools/cfn-guard/cfn-guard-v3-x86_64-windows-latest/`; use the
[official Guard installation guidance](https://docs.aws.amazon.com/cfn-guard/latest/ug/setting-up.html)
if it is missing. Its 3.2.1 release archive was previously verified with SHA256
`52af28c02081f1067c6710c08619d359899734ec59d51f17f68e1b4b396a1203`.
`.tools/` and `.venv/` are excluded by repository ignore rules; credentials remain in provider-managed
stores. No restart was needed. If a later restart is required, save a sanitized
checkpoint, reopen `X:\Team7`, select this branch, retain the model and High or
higher effort, and recheck connections. Do not assume another session's access.

## AWS discovery and account review

| Check | Observed state | Assessment |
| --- | --- | --- |
| Account / region | `123109186025` / `us-east-2` | Matches required target |
| Caller | Assumed `AccountFullAccessRole`, not root | Console-based temporary CLI/MCP access; trust principal is `account-access.amazonaws.com` |
| Foundation | `cfn-foundation-team07`, `CREATE_COMPLETE` | Existing dependency |
| Resolved VPC | `vpc-05ac92d29e000c0ce`, Name `vpc-capstone-team07`, `10.7.0.0/16`, available, non-default | Matches the comparison ID and approved design |
| Security stack before creation | DescribeStacks returned explicit does-not-exist ValidationError | No existing `cfn-security-team07` found before the approved deployment |
| Tools group before creation | Regional Name-tag lookup returned zero; target VPC inventory contained only its default group | No tools-group ownership conflict found before creation |
| Existing default group | `sg-06e08b526126cc50c`; default self-reference ingress and IPv4 allow-all egress | Observed only; must remain unchanged |
| AccountMFAEnabled | **0**, expected baseline **1** | **Accepted exception by Josh, 2026-10-08; not remediated; baseline not passed** |
| AccountAccessKeysPresent | **0**, expected **0** | Root no-access-key baseline passed |
| AccountPasswordPresent / signing certificates | **0 / 0** | Consistent with credential-free root; does not prove centralized root management is enabled |
| IAM users / groups / roles | **0 / 0 / 12**; user/group lists empty | Zero IAM users can be valid for federated access |
| Caller role policy | `AdministratorAccess` v1: Allow `Action=*`, `Resource=*`; no inline policies | Broad attached policy; actual access is limited by explicit SCP denies |
| Other managed roles | Account management and advanced-features roles have their corresponding AWS-managed policies | Service-managed access; not evidence of individual team assignments |
| Individual MFA | Not independently verified | Root flag does not establish Josh's or other team members' MFA |

Discovery timestamps: initial inventory `2026-10-08T00:51:04.677412Z`; detailed
account/VPC review `2026-10-08T00:54:31.453239Z`; role-policy inspection
`2026-10-08T00:55:23.865206Z`. A final inventory at
`2026-10-08T01:05:06.093952Z` again verified the foundation/VPC, absent security
stack, and zero matching tools groups. The account is an active AWS Organizations member
with all features and SCPs enabled. Centralized root management may explain the
credential-free root observations, but `iam:ListOrganizationsFeatures` was
explicitly denied by an SCP. It is **not confirmed** and does not turn MFA=0 into
a passing result. Josh accepted this unresolved root-MFA finding for the Week 1
task on 2026-10-08; see the [decision record](SCRUM-13-root-MFA-exception.md).
Centralized-root verification remains unavailable; no instructor approval is
claimed. Do not sign in as root or create/enroll credentials.
[AWS centralized-root documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-enable-root-access.html)
explains that managed member accounts can have root credentials removed.

Other limitations: `iam:ListSAMLProviders` and `iam:ListOpenIDConnectProviders`
were explicitly denied by an SCP; `iam:GetCredentialReport` returned
`ReportNotPresent`, and no report was generated. Identity Center `ListInstances`
in `us-east-2` returned empty, which does not establish other home regions or
external identity inventories. Named team access assignments and individual MFA
remain unverified. None of these unavailable checks is recorded as a pass.
The root-MFA owner decision is recorded as an accepted exception, not a passing
control. The separate team-assignment and individual-MFA review remains open.
No review or exception authorizes an agent to remediate root or broaden policies.

## Template design and concrete change scope

`infrastructure/cloudformation/week1/security.yaml` defines exactly one
`AWS::EC2::SecurityGroup`, logical ID `Team7ToolsSecurityGroup`, in the separately
supplied existing `VpcId`. The required `AWS::EC2::VPC::Id` parameter has **no
default**. It is supplied from the current foundation output at deployment time.
No foundation export, foundation edit, attachment, IAM resource, or other AWS
resource is introduced.

| Planned action | Resource | Result |
| --- | --- | --- |
| Create | One new security group in `cfn-security-team07` | Description `Team7 tools security group - Week 1`, zero ingress |
| Change | None | Existing VPC/default group and IAM remain unchanged |
| Replace | None | Stop if the later change set proposes any replacement |
| Delete | None | Stop if the later change set proposes any deletion |

Name tag is **`sg-tools-team07`**. Physical `GroupName` is omitted: AWS prohibits
physical names starting with `sg-`, and CloudFormation generates the name.
`SecurityGroupId` is the generated `sg-...` identifier, output with `VpcId`.
Record actual generated GroupName from EC2 discovery after creation.

`SecurityGroupIngress: []` grants no inbound rule, including SSH or self-reference.
`SecurityGroupEgress` is omitted for this **new** group to retain default outbound
behavior. This is allow-all default egress, not deny-all. CloudFormation describes
default IPv4/IPv6 allow-all egress when none is supplied; record every actual
IPv4/IPv6 rule returned after deployment rather than assuming its exact list.
See the [CloudFormation resource contract](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-securitygroup.html).
The group is unattached, so this stack does not change any workload's rules.

Exact user tags (CloudFormation may add its reserved `aws:` ownership tags):
`Name=sg-tools-team07`, `Project=Team7`, `Team=Team7`, `Environment=Dev`,
`Owner=Team7`, `Workload=Tools`, `Component=Security`, `ManagedBy=Team7`,
`Repository=Team7`, `JiraProject=SCRUM`.

## Validation and review

- cfn-lint 1.57.2: **0 errors, 0 warnings, 0 informational findings**.
- Guard 3.2.1: all seven task-specific scope, required VPC, empty ingress,
  default egress, generated-name, exact-tag, and output rules passed.
- AWS `ValidateTemplate` in `us-east-2` passed at
  `2026-10-08T00:58:43.284295Z`, returning the single required `VpcId` parameter.
- Template is 2,365 bytes, below the 51,200-byte inline limit.
- Six negative contract copies were rejected as expected: SSH ingress, explicit
  egress, physical GroupName, VPC default, wrong tag, and an extra EC2 resource.
  The real template was left unchanged by these checks.
- Full diff, credential scan, foundation preservation, and `git diff --check`
  are required before the preparation commit; their final results are recorded
  in the draft PR.

These preparation checks did not prove deployment permissions, SCP allowance,
quotas, or live behavior. The subsequently approved change set and actual
deployment checks are recorded below; neither was performed during preparation.

## Approval and deployment procedure

The final plan must name the actual template commit and draft PR, expected
account, `us-east-2`, `cfn-security-team07`, and the re-resolved VPC ID. Require the
user's separate **DEPLOYMENT AUTHORIZED** response approving that concrete plan.
The phrase in a prompt or this document is not authorization.

Only after that approval, recheck the immutable template version, branch,
caller/account, foundation/VPC Name/CIDR/state, and absence/ownership of any
matching stack/group. Stop if material state or scope changed. Example approved
preparation in PowerShell, with the VPC fetched rather than hardcoded:

```powershell
$taskProfile = 'aws-Team7'
$taskRegion = 'us-east-2'
$taskAccount = aws sts get-caller-identity --profile $taskProfile --region $taskRegion --query Account --output text --no-cli-pager
if ($LASTEXITCODE -ne 0 -or $taskAccount.Trim() -ne '123109186025') { throw 'Unexpected identity or failed identity check' }
$taskVpcId = aws cloudformation describe-stacks --stack-name cfn-foundation-team07 --profile $taskProfile --region $taskRegion --query "Stacks[0].Outputs[?OutputKey=='VpcId'].OutputValue | [0]" --output text --no-cli-pager
if ($LASTEXITCODE -ne 0 -or $taskVpcId -notmatch '^vpc-[0-9a-f]+$') { throw 'Foundation VPC output unavailable' }
# Re-describe this VPC and verify the reviewed Name/CIDR/state before proceeding.
# Run only after deployment approval; this creates a change set without executing it.
aws cloudformation deploy --template-file infrastructure/cloudformation/week1/security.yaml --stack-name cfn-security-team07 --parameter-overrides "VpcId=$taskVpcId" --profile $taskProfile --region $taskRegion --no-execute-changeset
```

Inspect the resulting change set: exactly one Add, no Modify/Remove/replacement,
correct VPC, required tags, empty ingress, and no explicit egress. Stop for any
material difference and present a revised plan. Execute only the inspected change
set under the separate approved plan, with normal rollback enabled and no IAM
capabilities. Wait for the actual terminal stack result. Do not report success
from command submission alone.

Required permissions include CloudFormation change-set creation/read/execution,
stack/resource/event reads, and EC2 CreateSecurityGroup/CreateTags/DescribeVpcs/
DescribeSecurityGroups. DeleteSecurityGroup is needed for normal rollback of
the newly created group. No role creation or `iam:PassRole` is required by this
template because no execution role is supplied. Applicable SCPs and resource
handler permissions can still deny an operation. Never attach broader policies
to get past a denial.

Incremental cost for this one unattached security group is expected to be **$0**:
[AWS security groups have no additional charge](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html),
and [CloudFormation adds no charge for AWS::* providers](https://aws.amazon.com/cloudformation/pricing/).
Official pages were checked on 2026-10-08 UTC. No compute, public IP, NAT,
monitoring, or other billable service is created. Existing workload costs remain
separate. The course budget is $5/month with an 80%/$4 alert; it is not a spend cap.

## Post-deployment validation, evidence, and handoff

After approved deployment, read the actual stack Resources/Outputs and the group
identified by `SecurityGroupId`. Verify VpcId, generated GroupName, Name tag,
exact description, zero IpPermissions, every IpPermissionsEgress entry (protocol,
ports, IPv4/IPv6 destinations, group/prefix-list targets), ten user tags, and
CloudFormation ownership. Record UTC timestamps and actual command/API results.

Capture genuine screenshots in these exact console views, setting region to
US East (Ohio), account to Team7, and filtering by the deployed group ID:

| Console view | Filename suffix after `YYYYMMDD_Team7_aws_w1-` |
| --- | --- |
| CloudFormation > cfn-security-team07 > Resources, stack status | `security-stack.png` |
| CloudFormation > cfn-security-team07 > Outputs | `security-outputs.png` |
| EC2/VPC > Security groups > group Details | `sg-details.png` |
| Selected group > Inbound rules, empty list | `sg-inbound.png` |
| Selected group > Outbound rules, all entries | `sg-outbound.png` |
| Selected group > Tags, all required values | `sg-tags.png` |
| Permitted IAM view or sanitized actual CLI output | `account-review.png` or `account-review.json` |

Browser inspection is not currently available in this VS Code session. If that
remains true, Josh must capture these views; an API result is not a screenshot.
Preserve originals privately and compute SHA256; make separately named redacted
copies for the public repository. Add truthful capture/redaction/transfer details
to the existing evidence log. The current preparation API evidence is explicitly
identified in [the evidence manifest](evidence/SCRUM-13/README.md), with a private
original and a separate redacted JSON; it is not deployment evidence.

The reviewed shared document's **Team access - Security & Ops** and new **Access
and Security Group summary** are now populated with verified values in
[01_Cloud_Foundation_and_Naming_Standard.md](Design_Standards_Cloud_Architect/01_Cloud_Foundation_and_Naming_Standard.md).
Its completed landing-zone section is preserved verbatim. The original reviewed
package remains unchanged; the older loose Markdown was not substituted. Only
Josh's observed session is documented, with individual MFA and the broader team
roster explicitly unverified. Josh subsequently supplied the reviewed 19-image
`Week01(1).zip`; [screenshot review and hashes](evidence/SCRUM-13/SCREENSHOT_REVIEW.md)
are now recorded. Security-group screenshots are complete; originals stay private.

## Authorized deployment result

Josh explicitly approved commit `d0be5dce16b2ad7b7915bf882ccc8f6755e7b913`,
account `123109186025`, `us-east-2`, `cfn-security-team07`, and
`vpc-05ac92d29e000c0ce`. The approved template SHA256 is
`7c6b00d2e66f1b73237787ce21cb5f9993a79d95c7420b34bdb3a70f7e55317e`.
The local branch/commit/hash, STS account, foundation output, VPC Name/CIDR/state,
and absent stack/group were rechecked before creation.

Change set `cfn-security-team07-scrum13-20261008-reviewed-d0be5dc` was created at
`2026-10-08T01:17:58.324Z`. It reached `CREATE_COMPLETE`/`AVAILABLE`, proposed
exactly one **Add AWS::EC2::SecurityGroup**, and contained no modifications,
replacements, removals, IAM capabilities, nested stacks, or execution role.
Resolved properties matched the approved VPC, description, empty ingress,
omitted GroupName/egress, and ten tags. Retrieved original template matched the
approved text (CloudFormation omits the terminal newline). `DescribeEvents`
reported the change-set operation `SUCCEEDED`, with no validation errors.

Execution was submitted at `2026-10-08T01:18:39.773Z` with
`DisableRollback=false`, standard mode. The stack reached **CREATE_COMPLETE**
at `2026-10-08T01:18:50.251Z`; the operation reported `SUCCEEDED`.
Read-only verification at `2026-10-08T01:19:09.227Z` confirmed:

| Check | Actual result |
| --- | --- |
| Managed resource | Only `Team7ToolsSecurityGroup`, `AWS::EC2::SecurityGroup`, `CREATE_COMPLETE` |
| Group ID / SecurityGroupId output | `sg-0d4b70aeec5581403` |
| Generated physical GroupName | `cfn-security-team07-Team7ToolsSecurityGroup-zyMccvqygh0Z` |
| Name tag | `sg-tools-team07` |
| Description | `Team7 tools security group - Week 1` |
| VPC / VpcId output | `vpc-05ac92d29e000c0ce`; `vpc-capstone-team07`; `10.7.0.0/16` |
| Ingress | Zero permission entries and zero inbound rule records; no SSH or self-reference |
| Egress | Exactly one rule, `sgr-0c5218ce1138a563f`: protocol `-1` (all), all ports, IPv4 `0.0.0.0/0`; API FromPort/ToPort `-1/-1` |
| Other outbound destinations | No IPv6 rule, group reference, or prefix-list destination present |
| Attachments | `DescribeNetworkInterfaces` filtered by group ID returned zero |
| Tags / ownership | Exact ten user tags plus three reserved CloudFormation ownership tags; logical ID and stack match |
| Duplicate check | Regional Name-tag lookup returned exactly this one group |
| Deployed template | Retrieved Original text matches the approved template |
| Foundation/default group | Foundation remains `CREATE_COMPLETE` with unchanged last-update time/outputs; default group rules match earlier reads |
| Root account review refresh | MFA `0`, root keys `0`, password `0`, signing certificates `0`, users/groups/roles `0/0/12`; findings remain open |

Actual default egress is IPv4 allow-all only. No IPv6 rule was observed, so none
is claimed or added. No other AWS resources were created, changed, replaced, or
deleted. No rollback was needed. Post-deployment checks passed; stack/resource
drift status is `NOT_CHECKED`, and no drift-detection operation is claimed.
See [deployment API evidence and hashes](evidence/SCRUM-13/README.md) and
[review handoff](SCRUM-13-handoff.md).

## Failure, rollback, and recovery

Use normal CloudFormation rollback. If creation fails, inspect the actual stack
status, stack resource events, and change-set validation events; preserve both
the cause and resulting state. Rollback may remove the newly created group.
Do not widen ingress, IAM access, or SCPs, disable rollback, modify the default
group, or delete/recreate stacks automatically. Template fixes require review
and a new plan if material. Cleanup requires a separately approved CloudFormation
plan; first inspect group network-interface attachments and references from
other rules. Never delete the foundation as part of SCRUM-13.

## Acceptance and completion review

| Work item | Verified state | Remaining completion requirements |
| --- | --- | --- |
| SCRUM-36 | Approved one-group deployment and actual group/VPC/rules/tags/outputs verified; genuine screenshots reviewed and hashed | Technical and screenshot requirements satisfied |
| SCRUM-37 | Root/IAM review recorded; root-MFA exception accepted by Josh on 2026-10-08 | Separate team-assignment and individual-MFA review/evidence or explicit acceptance of those limitations; final acceptance |
| SCRUM-13 | Design, deployment, API evidence/hashes, shared deliverable, and draft PR ready for review | Remaining SCRUM-37 owner review; actual handoff to Cloud Architect |

Completion text and checklists are prepared in the handoff document. Evidence
and documentation are published to the same branch and draft PR. Josh authorized
merge and Jira closure on 2026-10-08T23:40:41Z if the task is complete. The remaining
owner review and actual handoff must be resolved before claiming completion.
