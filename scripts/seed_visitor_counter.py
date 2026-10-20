#!/usr/bin/env python3
"""SCRUM-21: inspect by default; conditionally seed without resetting a counter."""
import argparse
import json
import re
import sys
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import BotoCoreError, ClientError

REGION = 'us-east-2'
TABLE = 'ddb-visitor-team07'
STACK = 'cfn-visitor-data-team07'  # Proposed name; approval required before deployment.


def validate_request(expected_account, apply, authorization):
    if not re.fullmatch(r'[0-9]{12}', expected_account):
        raise ValueError('expected-account must be the independently verified 12-digit Team7 account ID')
    if apply and authorization != 'DEPLOYMENT AUTHORIZED':
        raise ValueError('--apply requires --authorization "DEPLOYMENT AUTHORIZED"')


def checked_count(item):
    count = item.get('count')
    if (item.get('id') != 'site' or isinstance(count, bool)
            or not isinstance(count, (int, Decimal))
            or (isinstance(count, Decimal) and not count.is_finite())
            or count < 0 or count != int(count)):
        raise ValueError('Existing item has an invalid counter; no write performed')
    return int(count)


def run(session, expected_account, apply=False, authorization=None):
    validate_request(expected_account, apply, authorization)
    identity = session.client('sts', region_name=REGION).get_caller_identity()
    if identity['Account'] != expected_account:
        raise ValueError('AWS account mismatch; no write performed')
    cf = session.client('cloudformation', region_name=REGION)
    resource = cf.describe_stack_resource(
        StackName=STACK, LogicalResourceId='VisitorCounterTable')['StackResourceDetail']
    if (resource['PhysicalResourceId'] != TABLE
            or resource['ResourceType'] != 'AWS::DynamoDB::Table'
            or resource['ResourceStatus'] not in ('CREATE_COMPLETE', 'UPDATE_COMPLETE', 'IMPORT_COMPLETE')):
        raise ValueError('Expected completed CloudFormation table resource not found')
    dynamodb = session.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(TABLE)
    metadata = table.meta.client.describe_table(TableName=TABLE)['Table']
    if (metadata.get('TableStatus') != 'ACTIVE'
            or metadata.get('KeySchema') != [{'AttributeName': 'id', 'KeyType': 'HASH'}]
            or metadata.get('AttributeDefinitions') != [{'AttributeName': 'id', 'AttributeType': 'S'}]
            or metadata.get('BillingModeSummary', {}).get('BillingMode') != 'PAY_PER_REQUEST'):
        raise ValueError('Table must be ACTIVE, on-demand, with only an id String partition key')

    def read():
        return table.get_item(Key={'id': 'site'}, ConsistentRead=True).get('Item')

    result = {'region': REGION, 'table': TABLE, 'account_matches': True}
    item = read()
    if item is not None:
        return dict(result, status='already_exists_preserved', count=checked_count(item))
    if not apply:
        return dict(result, status='seed_planned_no_write', proposed_item={'id': 'site', 'count': 0})
    try:
        table.put_item(Item={'id': 'site', 'count': 0}, ConditionExpression=Attr('id').not_exists())
        status = 'seeded'
    except table.meta.client.exceptions.ConditionalCheckFailedException:
        # Another process created it after our read: preserve that process's value.
        status = 'concurrent_creation_preserved'
    item = read()
    if item is None:
        raise ValueError('Item absent during verification; inspect concurrent deletion, do not reset')
    count = checked_count(item)
    return dict(result, status=status, count=count, zero_observed=(count == 0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', default='aws-Team7')
    parser.add_argument('--expected-account', required=True)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--authorization')
    args = parser.parse_args()
    try:
        # Reject an unauthorized request before even resolving AWS credentials.
        validate_request(args.expected_account, args.apply, args.authorization)
        result = run(boto3.Session(profile_name=args.profile), args.expected_account,
                     args.apply, args.authorization)
        print(json.dumps(result, indent=2))
    except (ValueError, BotoCoreError, ClientError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
