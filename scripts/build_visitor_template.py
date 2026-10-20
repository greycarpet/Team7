"""Synchronize the reviewed Python source into CloudFormation's inline ZipFile."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "infrastructure/cloudformation/week3/visitor-api.yaml"
START = "        # BEGIN GENERATED HANDLER\n"
END = "        # END GENERATED HANDLER\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    original = TEMPLATE.read_text()
    before, remainder = original.split(START)
    _, after = remainder.split(END)
    source = (ROOT / "application/lambda/visitor_counter.py").read_text()
    block = "        ZipFile: |\n" + "".join(("          " + line if line else "") + "\n" for line in source.splitlines())
    rendered = before + START + block + END + after
    if args.check:
        if rendered != original:
            print("Handler differs from template; run scripts/build_visitor_template.py", file=sys.stderr)
            return 1
        print("Inline handler matches source.")
    else:
        TEMPLATE.write_text(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
