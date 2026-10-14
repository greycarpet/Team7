"""Read-only release evidence: authenticated object bytes and unsigned HTTP checks."""
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess
import urllib.error
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(url):
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": "Team7-SCRUM17-Verification", "Accept-Encoding": "identity"})
    try:
        response = opener.open(req, timeout=30)
    except urllib.error.HTTPError as response:
        body = response.read()
        return response.code, dict(response.headers), body
    with response:
        return response.status, dict(response.headers), response.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", required=True, choices=["1", "2"])
    parser.add_argument("--repo", required=True, type=pathlib.Path)
    parser.add_argument("--out", required=True, type=pathlib.Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    host = "d3jg1ev4a532iw.cloudfront.net"
    bucket = "s3-site-team07-a7f391"
    region = "us-east-2"
    marker = f"Team7 Week 2 - Release {args.release}"
    evidence = {"observed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "release": marker, "https_origin": f"https://{host}", "authenticated_objects": [], "http_checks": [], "checks": {}}
    sources = {}
    for key in ["index.html", "assets/styles.css"]:
        source = (args.repo / "site" / key).read_bytes()
        sources[key] = hashlib.sha256(source).hexdigest()
        download = args.out / (key.replace("/", "-") + ".authenticated")
        command = ["aws", "s3api", "get-object", "--profile", "aws-Team7", "--region", region, "--bucket", bucket, "--key", key, str(download), "--output", "json", "--no-cli-pager"]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        metadata = json.loads(result.stdout)
        actual = hashlib.sha256(download.read_bytes()).hexdigest()
        evidence["authenticated_objects"].append({"key": key, "version_id": metadata["VersionId"], "bytes": len(download.read_bytes()), "content_type": metadata.get("ContentType"), "cache_control": metadata.get("CacheControl"), "encryption": metadata.get("ServerSideEncryption"), "sha256": actual, "source_sha256": sources[key]})
        evidence["checks"][f"authenticated_hash:{key}"] = actual == sources[key]
    for path, key in [("/", "index.html"), ("/index.html", "index.html"), ("/assets/styles.css", "assets/styles.css")]:
        status, headers, body = request(f"https://{host}{path}")
        headers = {k.lower(): v for k, v in headers.items()}
        actual = hashlib.sha256(body).hexdigest()
        evidence["http_checks"].append({"url": f"https://{host}{path}", "status": status, "headers": headers, "bytes": len(body), "sha256": actual})
        evidence["checks"][f"https_200:{path}"] = status == 200
        evidence["checks"][f"https_hash:{path}"] = actual == sources[key]
        evidence["checks"][f"security_headers:{path}"] = (headers.get("x-content-type-options") == "nosniff" and headers.get("x-frame-options") == "SAMEORIGIN" and "max-age=31536000" in headers.get("strict-transport-security", ""))
        if key == "index.html":
            evidence["checks"][f"release_marker:{path}"] = marker.encode() in body
        redirect_status, redirect_headers, _ = request(f"http://{host}{path}")
        redirect_headers = {k.lower(): v for k, v in redirect_headers.items()}
        evidence["http_checks"].append({"url": f"http://{host}{path}", "status": redirect_status, "location": redirect_headers.get("location")})
        evidence["checks"][f"http_redirect:{path}"] = redirect_status == 301 and redirect_headers.get("location") == f"https://{host}{path}"
    direct = f"https://{bucket}.s3.{region}.amazonaws.com/index.html"
    status, headers, body = request(direct)
    evidence["http_checks"].append({"url": direct, "status": status, "access_denied": b"<Code>AccessDenied</Code>" in body})
    evidence["checks"]["unsigned_known_s3_object_denied"] = status == 403 and b"<Code>AccessDenied</Code>" in body
    evidence["passed"] = all(evidence["checks"].values())
    evidence["completed_at_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (args.out / "live-verification.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))
    return 0 if evidence["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
