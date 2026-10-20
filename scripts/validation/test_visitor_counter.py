"""Offline failure-path and request-contract tests. No AWS calls are made."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import boto3
from botocore.config import Config
from botocore.stub import ANY, Stubber

ROOT = Path(__file__).resolve().parents[2]
ORIGIN = "https://d3jg1ev4a532iw.cloudfront.net"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CounterTests(unittest.TestCase):
    def setUp(self):
        # Intentionally invalid test-only credentials and loopback fallback.
        self.table = boto3.resource(
            "dynamodb", region_name="us-east-2", endpoint_url="http://127.0.0.1:9",
            aws_access_key_id="TEST_ONLY", aws_secret_access_key="TEST_ONLY",
            config=Config(retries={"total_max_attempts": 1}),
        ).Table("ddb-visitor-team07")
        resource = SimpleNamespace(Table=lambda _: self.table)
        with patch.dict(os.environ, {"ALLOWED_ORIGIN": ORIGIN, "TABLE_NAME": self.table.name}), \
                patch("boto3.resource", return_value=resource) as create:
            self.module = load("visitor_counter", ROOT / "application/lambda/visitor_counter.py")
        self.assertEqual(create.call_args.kwargs["config"].retries["total_max_attempts"], 1)
        self.stub = Stubber(self.table.meta.client)
        self.stub.activate()
        self.addCleanup(self.stub.deactivate)
        self.event = {"requestContext": {"http": {"method": "POST"}}, "rawPath": "/visits",
                      "headers": {"origin": ORIGIN, "content-type": "application/json"},
                      "body": "{}", "isBase64Encoded": False}

    def call(self):
        return self.module.handler(self.event, SimpleNamespace(aws_request_id="offline-test"))

    def test_atomic_update_returns_numeric_count_without_separate_read(self):
        self.stub.add_response("update_item", {"Attributes": {"count": {"N": "42"}}}, {
            "TableName": "ddb-visitor-team07", "Key": {"id": "site"},
            "UpdateExpression": "SET #count = #count + :one",
            "ExpressionAttributeNames": {"#count": "count"},
            "ExpressionAttributeValues": {":one": 1},
            "ConditionExpression": ANY, "ReturnValues": "UPDATED_NEW",
        })
        result = self.call()
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(json.loads(result["body"]), {"count": 42})
        self.assertEqual(result["headers"]["cache-control"], "no-store")
        self.stub.assert_no_pending_responses()

    def test_missing_or_invalid_seed_is_not_recreated(self):
        self.stub.add_client_error("update_item", "ConditionalCheckFailedException")
        self.assertEqual(self.call()["statusCode"], 503)
        self.stub.assert_no_pending_responses()

    def test_database_failure_does_not_leak_details_or_retry(self):
        self.stub.add_client_error("update_item", "AccessDeniedException", "PRIVATE_ERROR_DETAIL")
        result = self.call()
        self.assertEqual(result["statusCode"], 503)
        self.assertEqual(json.loads(result["body"]), {"error": "counter_unavailable"})
        self.stub.assert_no_pending_responses()

    def test_foreign_and_missing_origins_do_not_write(self):
        for origin in ("https://example.org", "", ORIGIN + ".evil.example"):
            with self.subTest(origin=origin):
                self.event["headers"]["origin"] = origin
                self.assertEqual(self.call()["statusCode"], 403)

    def test_wrong_method_and_path_do_not_write(self):
        self.event["requestContext"]["http"]["method"] = "GET"
        self.assertEqual(self.call()["statusCode"], 405)
        self.event["requestContext"]["http"]["method"] = "POST"
        self.event["rawPath"] = "/other"
        self.assertEqual(self.call()["statusCode"], 404)

    def test_untrusted_body_does_not_select_item_or_increment(self):
        for body in ('{"id":"other"}', '{"count":100}', '[]', 'null', 'false', '', '{', 'x' * 65):
            with self.subTest(body=body):
                self.event["body"] = body
                self.assertEqual(self.call()["statusCode"], 400)

    def test_form_and_base64_requests_do_not_write(self):
        self.event["headers"]["content-type"] = "text/plain"
        self.assertEqual(self.call()["statusCode"], 400)
        self.event["headers"]["content-type"] = "application/json"
        self.event["isBase64Encoded"] = True
        self.assertEqual(self.call()["statusCode"], 400)


class SiteBuildTests(unittest.TestCase):
    def setUp(self):
        self.builder = load("build_visitor_site", ROOT / "scripts/build_visitor_site.py")

    def test_endpoint_and_csp_bind_to_same_exact_host(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "release"
            endpoint = "https://test123.execute-api.us-east-2.amazonaws.com/visits"
            manifest = self.builder.build(endpoint, target)
            html = (target / "index.html").read_text()
            self.assertIn(f'content="{endpoint}"', html)
            self.assertIn("connect-src " + endpoint.removesuffix("/visits") + ";", html)
            self.assertNotIn("unsafe-inline", html)
            self.assertEqual(len(manifest["files"]), 3)
            with self.assertRaises(ValueError):
                self.builder.build(endpoint, target)

    def test_foreign_url_or_injection_is_rejected_before_writing(self):
        for endpoint in ("https://example.org/visits", "http://test.execute-api.us-east-2.amazonaws.com/visits",
                         "https://test.execute-api.us-east-1.amazonaws.com/visits",
                         'https://test.execute-api.us-east-2.amazonaws.com/visits\" onload=\"bad',
                         "https://test.execute-api.us-east-2.amazonaws.com/visits?key=anything"):
            with self.subTest(endpoint=endpoint), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "release"
                with self.assertRaises(ValueError):
                    self.builder.build(endpoint, target)
                self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
