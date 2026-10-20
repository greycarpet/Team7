"""Bounded live HTTP tests: four valid POSTs increment the real counter. No retries."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.request

ORIGIN = "https://d3jg1ev4a532iw.cloudfront.net"


def request(url, method, origin=None, body=None, preflight=False):
    headers = {"Accept": "application/json"}
    if origin is not None:
        headers["Origin"] = origin
    if body is not None:
        headers["Content-Type"] = "application/json"
    if preflight:
        headers.update({"Access-Control-Request-Method": "POST",
                        "Access-Control-Request-Headers": "content-type"})
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        response = urllib.request.urlopen(req, timeout=12)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        return {"method": method, "origin": origin, "status": response.status,
                "headers": {k.lower(): v for k, v in response.headers.items()},
                "body": response.read(2048).decode()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--authorized-live-test", action="store_true", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"https://[a-z0-9]+\.execute-api\.us-east-2\.amazonaws\.com/visits", args.endpoint):
        parser.error("Expected a us-east-2 VisitEndpoint output")
    if args.output.exists():
        parser.error("Evidence file already exists; choose a new name")
    checks = {}
    cases = [
        ("allowed_preflight", "OPTIONS", ORIGIN, None, True),
        ("foreign_preflight", "OPTIONS", "https://example.org", None, True),
        ("foreign_post", "POST", "https://example.org", b"{}", False),
        ("missing_origin", "POST", None, b"{}", False),
        ("malformed_json", "POST", ORIGIN, b"{", False),
        ("wrong_method", "GET", ORIGIN, None, False),
        ("success", "POST", ORIGIN, b"{}", False),
    ]
    for name, method, origin, body, preflight in cases:
        checks[name] = request(args.endpoint, method, origin, body, preflight)
        time.sleep(0.7)  # Respect the approved two-request/sec route setting.
    time.sleep(2)  # Refill the burst bucket before three parallel requests.
    with ThreadPoolExecutor(max_workers=3) as pool:
        parallel = list(pool.map(lambda _: request(args.endpoint, "POST", ORIGIN, b"{}"), range(3)))
    result = {"captured_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "endpoint": args.endpoint, "checks": checks, "parallel": parallel,
              "deliberate_valid_posts": 4, "retries": 0}
    failures = []
    for name, expected in {"foreign_post": 403, "missing_origin": 403,
                           "malformed_json": 400, "wrong_method": 404, "success": 200}.items():
        if checks[name]["status"] != expected:
            failures.append(f"{name}: expected {expected}, got {checks[name]['status']}")
    pre = checks["allowed_preflight"]
    if pre["status"] not in (200, 204) or pre["headers"].get("access-control-allow-origin") != ORIGIN:
        failures.append("allowed preflight failed")
    if checks["foreign_preflight"]["headers"].get("access-control-allow-origin") == "https://example.org":
        failures.append("foreign preflight was allowed")
    if checks["success"]["headers"].get("access-control-allow-origin") != ORIGIN:
        failures.append("success response missing allowed CORS origin")
    counts = []
    for response in [checks["success"], *parallel]:
        try:
            count = json.loads(response["body"])["count"]
            if response["status"] != 200 or type(count) is not int or count < 1:
                raise ValueError()
            counts.append(count)
        except (ValueError, KeyError, TypeError):
            failures.append("valid POST did not return a positive integer count")
    if len(counts) == 4 and sorted(counts) != list(range(min(counts), min(counts) + 4)):
        failures.append("counts were not distinct and consecutive; inspect concurrent traffic")
    result.update({"counts": counts, "failures": failures})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
