# SCRUM-13 / SCRUM-37: accepted root-MFA exception

**Status:** Accepted exception; not remediated; root-MFA baseline not passed.

| Field | Record |
| --- | --- |
| Decision owner | Josh Escobar, assigned owner of SCRUM-13 and SCRUM-37 |
| Accepted at | 2026-10-08 18:34:18 America/Chicago (2026-10-08T23:34:18Z) |
| Scope | Week 1 root-MFA finding for AWS account `123109186025`, SCRUM-13 / SCRUM-37 |
| Desired baseline | `AccountMFAEnabled=1` |
| Observed result | `AccountMFAEnabled=0`; root access keys, password, and signing certificates all `0` |
| Evidence timestamp | Last recorded API verification: 2026-10-08T01:19:09.227Z; no new AWS inspection is claimed by this decision record |
| Decision | Complete the review with a documented exception; Josh elects not to enable or remediate root MFA for this task |
| Expiration | No expiration or remediation date was specified |

## Explicit acceptance

After being told that the review could be documented while the root-MFA
baseline remained unmet, Josh stated:

> I accept that exception. And document it

This records Josh's acceptance of the root-MFA finding and its unresolved
verification limitations for this task. It does not represent instructor
approval, confirmation that MFA is enabled, or a passing root-MFA control.

## Findings retained

- The no-root-access-key check passed: `AccountAccessKeysPresent=0`.
- Root password/signing-certificate flags are `0/0`. These observations are
  consistent with absent root credentials but do not confirm centralized root
  management. `iam:ListOrganizationsFeatures` was denied by an SCP.
- The supplied Root access management screenshot shows a privileged-action
  menu. It does not establish root MFA or centralized-root configuration.
- Root authentication protection cannot be fully established from the available
  evidence. The uncertainty is retained in this accepted exception, not reported
  as a verified compensating control.

## Scope boundaries and completion

This exception does not accept or verify the separate named team-access roster,
intended access scopes, or individual MFA. Those remain unverified and subject
to their own review. It authorizes no AWS, IAM, credential, permission, or
security-group changes.

The root-MFA owner-decision item is satisfied by this recorded exception.
Remaining evidence integration, team-access review, handoff, and final ticket/PR
acceptance are separate. This record does not merge PR #3 or mark tickets Done.

Original API evidence, its historical assessments, and recorded hashes are
preserved. See [account/deployment evidence](evidence/SCRUM-13/README.md),
[security findings](SCRUM-13-security-controls.md), and
[handoff checklist](SCRUM-13-handoff.md).

Related tickets: [SCRUM-13](https://joshescobarx.atlassian.net/browse/SCRUM-13)
and [SCRUM-37](https://joshescobarx.atlassian.net/browse/SCRUM-37).

## Subsequent completion decision

At 2026-10-08T23:47:17Z, Josh separately accepted the unverified team-access /
access-scope and individual-MFA limitations and authorized the SCRUM-14 handoff.
That handoff was posted as comment 10017. See
[completion acceptance](SCRUM-13-completion-acceptance.md).
This later decision resolves the separate owner-review item without changing
the original root exception, measured evidence, or any control's verified state.
