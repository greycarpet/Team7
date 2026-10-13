"""Validate the website template and prove dangerous policy changes are rejected.

Uses already installed cfn-lint and cfn-guard. Makes no AWS calls or deployments.
Run from the repository root; pass executable paths if they are not on PATH.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime, timezone

from cfnlint.decode import decode


def run_json(command):
    completed = subprocess.run(command, capture_output=True, text=True)
    return completed.returncode, json.loads(completed.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lint", default="cfn-lint")
    parser.add_argument("--guard", default="cfn-guard")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    template = Path("infrastructure/cloudformation/week2/site.yaml")
    rules = Path("scripts/validation/scrum-17.guard")
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "aws_writes": False}
    report["template_sha256"] = hashlib.sha256(template.read_bytes()).hexdigest()
    report["rules_sha256"] = hashlib.sha256(rules.read_bytes()).hexdigest()
    for name, executable in (("cfn_lint_version", args.lint), ("cfn_guard_version", args.guard)):
        report[name] = subprocess.check_output([executable, "--version"], text=True).strip()
    code, findings = run_json([args.lint, "--format", "json", "--regions", "us-east-2", "--", str(template)])
    assert code == 0 and findings == [], findings
    report["lint"] = {"exit_code": code, "findings": findings}
    guard_command = [args.guard, "validate", "--rules", str(rules), "--output-format", "json", "--show-summary", "none", "--data"]
    code, baseline = run_json(guard_command + [str(template)])
    assert code == 0 and baseline["status"] == "PASS", baseline
    report["guard"] = {"status": baseline["status"], "rules_passed": sorted(baseline["compliant"])}
    data, parsing_errors = decode(str(template))
    assert not parsing_errors, parsing_errors
    cases = [
        ("public_bucket", ["SiteBucket", "Properties", "PublicAccessBlockConfiguration", "BlockPublicPolicy"], False, "scrum17_private_encrypted_bucket"),
        ("anonymous_read_allow", ["SiteBucketPolicy", "Properties", "PolicyDocument", "Statement", 0, "Principal"], "*", "scrum17_scoped_policy"),
        ("broad_distribution_scope", ["SiteBucketPolicy", "Properties", "PolicyDocument", "Statement", 0, "Condition", "StringEquals", "AWS:SourceArn"], "*", "scrum17_scoped_policy"),
        ("unsigned_origin", ["SiteOriginAccessControl", "Properties", "OriginAccessControlConfig", "SigningBehavior"], "never", "scrum17_signed_origin"),
        ("http_allowed", ["SiteDistribution", "Properties", "DistributionConfig", "DefaultCacheBehavior", "ViewerProtocolPolicy"], "allow-all", "scrum17_https_static_delivery"),
        ("waf_added", ["SiteDistribution", "Properties", "DistributionConfig", "WebACLId"], "unexpected-web-acl", "scrum17_https_static_delivery"),
    ]
    report["negative_checks"] = []
    with tempfile.TemporaryDirectory(prefix="team7-scrum17-") as temporary:
        for name, path, value, expected_rule in cases:
            changed = copy.deepcopy(data)
            parent = changed["Resources"]
            for part in path[:-1]:
                parent = parent[part]
            parent[path[-1]] = value
            candidate = Path(temporary) / (name + ".json")
            candidate.write_text(json.dumps(changed), encoding="utf-8")
            code, observed = run_json(guard_command + [str(candidate)])
            failed = [entry["Rule"]["name"] for entry in observed.get("not_compliant", [])]
            assert code != 0 and observed["status"] == "FAIL" and expected_rule in failed, observed
            report["negative_checks"].append({"case": name, "result": "rejected", "expected_rule": expected_rule})
    report["service_predeployment_validation"] = "Not run; change-set creation awaits approval."
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
