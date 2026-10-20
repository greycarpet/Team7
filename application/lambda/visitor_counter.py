"""SCRUM-22: one atomic increment per accepted HTTP API request."""
import json
import logging
import os

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
MAX_COUNT = 9007199254740991  # Largest integer a browser can represent exactly.
ALLOWED_ORIGIN = os.environ["ALLOWED_ORIGIN"]
TABLE = boto3.resource(
    "dynamodb",
    config=Config(
        connect_timeout=1,
        read_timeout=2,
        retries={"mode": "standard", "total_max_attempts": 1},
    ),
).Table(os.environ["TABLE_NAME"])


def response(status, payload):
    # HTTP API owns CORS; do not add a second CORS implementation here.
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json", "cache-control": "no-store"},
        "isBase64Encoded": False,
        "body": json.dumps(payload, separators=(",", ":")),
    }


def handler(event, context):
    if event.get("requestContext", {}).get("http", {}).get("method") != "POST":
        return response(405, {"error": "method_not_allowed"})
    if event.get("rawPath") != "/visits":
        return response(404, {"error": "not_found"})
    headers = {key.lower(): value for key, value in (event.get("headers") or {}).items()}
    # Reject foreign simple requests too. Origin is spoofable outside browsers;
    # this is defense in depth, not authentication or an anti-bot guarantee.
    if headers.get("origin") != ALLOWED_ORIGIN:
        return response(403, {"error": "origin_not_allowed"})
    body = event.get("body") or ""
    if (headers.get("content-type", "").split(";", 1)[0].strip().lower()
            != "application/json" or event.get("isBase64Encoded")
            or not isinstance(body, str) or len(body) > 64):
        return response(400, {"error": "invalid_request"})
    try:
        payload = json.loads(body)
    except (ValueError, TypeError):
        return response(400, {"error": "invalid_request"})
    if payload != {}:
        return response(400, {"error": "invalid_request"})

    try:
        updated = TABLE.update_item(
            Key={"id": "site"},
            UpdateExpression="SET #count = #count + :one",
            ExpressionAttributeNames={"#count": "count"},
            ExpressionAttributeValues={":one": 1},
            ConditionExpression=(Attr("id").exists() & Attr("count").attribute_type("N")
                                 & Attr("count").gte(0) & Attr("count").lt(MAX_COUNT)),
            ReturnValues="UPDATED_NEW",
        )
        count = updated["Attributes"]["count"]
        if count != int(count) or not 1 <= count <= MAX_COUNT:
            raise ValueError("invalid stored count")
        return response(200, {"count": int(count)})
    except TABLE.meta.client.exceptions.ConditionalCheckFailedException:
        LOGGER.error("counter_condition_failed request_id=%s", context.aws_request_id)
    except (ClientError, BotoCoreError, ValueError, KeyError, TypeError) as error:
        LOGGER.error("counter_unavailable kind=%s request_id=%s",
                     type(error).__name__, context.aws_request_id)
    # Never seed/reset here. A timed-out update may have succeeded; do not retry.
    return response(503, {"error": "counter_unavailable"})
