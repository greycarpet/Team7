# SCRUM-17 preparation validation

October 13, 2026. This record covers source preparation only; no AWS resources
have been created or changed, and no live deployment tests have passed yet.

| Check | Result / coverage |
| --- | --- |
| cfn-lint 1.57.2, us-east-2 | PASS: 0 errors, 0 warnings, 0 informational findings |
| cfn-guard 3.2.1 | PASS: all six project rules in `scripts/validation/scrum-17.guard` |
| Security negative cases | PASS: public-access weakening, anonymous read Allow, wildcard distribution scope, unsigned origin, HTTP allowed, and WAF addition were each rejected by the expected rule |
| Local browser preview | Page and stylesheet rendered; Release notes navigation reached the visible Release 1 marker; no captured browser warning/error entries |
| Template size / scope | 7,808 bytes, four resources; below inline template limit |
| AWS identity / managed policies | Read-only identity matched Team7; current managed policy IDs/configurations saved in `preflight.redacted.json` |
| CloudFormation service pre-deployment validation | NOT RUN: requires the approved change-set workflow |
| Deployment, public HTTPS, anonymous S3 denial, Release 2 | NOT RUN: pending deployment approval and actual publishing |

Machine-readable findings, checker versions, template/rule hashes and the six
negative cases are in [validation.json](validation.json). The rules cover the
project's explicit security/scope contract, not the entire AWS compliance rules
registry. Manual review additionally covered approved names, required tags,
intrinsic references, scoped object permissions, retained data, policy selection,
cost scope, no secrets in deployable files, and no changes to Week 1 resources.
Scoped `.gitattributes` rules preserve LF bytes for the hashed template, Guard
rules and website files so Windows checkout conversion does not invalidate hashes.

Reproduce from the repository root in an environment with cfn-lint and cfn-guard:

```sh
python scripts/validation/check_scrum17.py --output docs/week2/evidence/SCRUM-17/validation.json
```

Use `--lint` and `--guard` for installed executable paths when not on PATH.
The runner requires cfn-lint's Python package in the selected Python environment.
The existing project installation was reused; no new packages were installed.

The local browser preview is not course deployment evidence. Browser review
covered the current app viewport, not a full cross-browser/device test matrix.
S3 global name availability, effective deployment permissions, quotas, account
pricing-plan state, and live content delivery still need verification.
