"""SCRUM-18 policy check; run with template and optional CIDR. Requires cfn-lint."""
import copy
import ipaddress
import re
import sys
from cfnlint.decode import decode

def validate(t, cidr):
    p = t["Parameters"]["AuthorizedSshCidr"]
    assert "Default" not in p
    assert re.fullmatch(p["AllowedPattern"], cidr)
    net = ipaddress.ip_network(cidr, strict=True)
    assert net.version == 4 and net.prefixlen == 32 and net.network_address.is_global
    assert set(t["Resources"]) == {"Team7ToolsSecurityGroup"}
    r = t["Resources"]["Team7ToolsSecurityGroup"]
    assert r["Type"] == "AWS::EC2::SecurityGroup"
    v = r["Properties"]
    assert v["GroupDescription"] == "Team7 tools security group - Week 1"
    assert v["VpcId"] == {"Ref": "VpcId"}
    assert "GroupName" not in v and "SecurityGroupEgress" not in v
    rules = v["SecurityGroupIngress"]
    assert len(rules) == 1
    rule = rules[0]
    assert rule["IpProtocol"] == "tcp" and rule["FromPort"] == rule["ToPort"] == 22
    assert rule["CidrIp"] == {"Ref": "AuthorizedSshCidr"}
    assert set(rule) == {"IpProtocol", "FromPort", "ToPort", "CidrIp", "Description"}

def main():
    template, errors = decode(sys.argv[1])
    assert not errors, errors
    cidr = sys.argv[2] if len(sys.argv) > 2 else "8.8.8.8/32"
    validate(template, cidr)
    cases = []
    for value in ["0.0.0.0/0", "8.8.8.0/24", "999.1.1.1/32"]:
        cases.append((template, value))
    extra = copy.deepcopy(template)
    extra["Resources"]["Team7ToolsSecurityGroup"]["Properties"]["SecurityGroupIngress"] *= 2
    cases.append((extra, cidr))
    all_protocols = copy.deepcopy(template)
    all_protocols["Resources"]["Team7ToolsSecurityGroup"]["Properties"]["SecurityGroupIngress"][0]["IpProtocol"] = "-1"
    cases.append((all_protocols, cidr))
    for bad, source in cases:
        try:
            validate(bad, source)
        except (AssertionError, ValueError):
            continue
        raise AssertionError("Unsafe negative case accepted")
    print("PASS: approved policy; 5 unsafe cases rejected")
if __name__ == "__main__":
    main()
