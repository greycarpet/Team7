"""Build a local website release using the deployed VisitEndpoint output. No AWS writes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = re.compile(r"https://[a-z0-9]+\.execute-api\.us-east-2\.amazonaws\.com/visits")


def build(endpoint, output):
    if not ENDPOINT.fullmatch(endpoint):
        raise ValueError("Expected the exact us-east-2 HTTPS VisitEndpoint output; no query or fragment")
    output = Path(output).resolve()
    # A new directory prevents stale files or accidental overwrites.
    if output.exists():
        raise ValueError("Output directory must not already exist")
    html = (ROOT / "site/index.html").read_text()
    meta = '<meta name="visitor-api" content="">'
    csp = "connect-src 'none'"
    if html.count(meta) != 1 or html.count(csp) != 1:
        raise ValueError("Expected exactly one endpoint and CSP placeholder")
    origin = endpoint.removesuffix("/visits")
    html = html.replace(meta, f'<meta name="visitor-api" content="{endpoint}">')
    html = html.replace(csp, f"connect-src {origin}")
    output.mkdir(parents=True)
    (output / "assets").mkdir()
    (output / "index.html").write_text(html)
    for name in ("styles.css", "visitor-counter-v1.js"):
        shutil.copyfile(ROOT / "site/assets" / name, output / "assets" / name)
    manifest = {
        "endpoint": endpoint,
        "files": {str(path.relative_to(output)): hashlib.sha256(path.read_bytes()).hexdigest()
                  for path in sorted(output.rglob("*")) if path.is_file()},
    }
    (output / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.endpoint, args.output), indent=2))
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    sys.exit(main())
