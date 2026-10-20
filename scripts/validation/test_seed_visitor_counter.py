"""Offline safety tests: no AWS credentials or network calls."""
import importlib.util
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock

spec = importlib.util.spec_from_file_location('seed', Path(__file__).parents[1] / 'seed_visitor_counter.py')
seed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seed)


class ConditionalFailure(Exception):
    pass


class SeedSafetyTests(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.sts, self.cf = MagicMock(), MagicMock()
        self.session.client.side_effect = lambda name, **kw: {'sts': self.sts, 'cloudformation': self.cf}[name]
        self.sts.get_caller_identity.return_value = {'Account': '111111111111'}
        self.cf.describe_stack_resource.return_value = {'StackResourceDetail': {
            'PhysicalResourceId': seed.TABLE, 'ResourceType': 'AWS::DynamoDB::Table',
            'ResourceStatus': 'CREATE_COMPLETE'}}
        self.table = self.session.resource.return_value.Table.return_value
        self.table.meta.client.exceptions = SimpleNamespace(ConditionalCheckFailedException=ConditionalFailure)
        self.metadata = {'TableStatus': 'ACTIVE', 'KeySchema': [{'AttributeName': 'id', 'KeyType': 'HASH'}],
                         'AttributeDefinitions': [{'AttributeName': 'id', 'AttributeType': 'S'}],
                         'BillingModeSummary': {'BillingMode': 'PAY_PER_REQUEST'}}
        self.table.meta.client.describe_table.return_value = {'Table': self.metadata}
        self.table.get_item.return_value = {}

    def run_seed(self, **kwargs):
        return seed.run(self.session, '111111111111', **kwargs)

    def test_default_is_read_only(self):
        self.assertEqual(self.run_seed()['status'], 'seed_planned_no_write')
        self.table.put_item.assert_not_called()

    def test_apply_requires_exact_authorization_before_clients(self):
        with self.assertRaises(ValueError): self.run_seed(apply=True)
        self.session.client.assert_not_called()

    def test_wrong_account_cannot_write(self):
        self.sts.get_caller_identity.return_value = {'Account': '222222222222'}
        with self.assertRaises(ValueError): self.run_seed()
        self.session.resource.assert_not_called()

    def test_unmanaged_table_cannot_write(self):
        self.cf.describe_stack_resource.return_value['StackResourceDetail']['PhysicalResourceId'] = 'other'
        with self.assertRaises(ValueError): self.run_seed()
        self.session.resource.assert_not_called()

    def test_bad_schema_cannot_write(self):
        self.metadata['KeySchema'] = [{'AttributeName': 'other', 'KeyType': 'HASH'}]
        with self.assertRaises(ValueError): self.run_seed(apply=True, authorization='DEPLOYMENT AUTHORIZED')
        self.table.put_item.assert_not_called()

    def test_existing_counter_is_never_reset(self):
        self.table.get_item.return_value = {'Item': {'id': 'site', 'count': Decimal(42)}}
        self.assertEqual(self.run_seed(apply=True, authorization='DEPLOYMENT AUTHORIZED')['count'], 42)
        self.table.put_item.assert_not_called()

    def test_invalid_existing_counter_is_not_repaired(self):
        self.table.get_item.return_value = {'Item': {'id': 'site', 'count': '42'}}
        with self.assertRaises(ValueError): self.run_seed(apply=True, authorization='DEPLOYMENT AUTHORIZED')
        self.table.put_item.assert_not_called()

    def test_seed_is_conditional_and_verified_with_strong_read(self):
        self.table.get_item.side_effect = [{}, {'Item': {'id': 'site', 'count': Decimal(0)}}]
        result = self.run_seed(apply=True, authorization='DEPLOYMENT AUTHORIZED')
        self.assertEqual(result['status'], 'seeded')
        self.assertTrue(result['zero_observed'])
        expression = self.table.put_item.call_args.kwargs['ConditionExpression'].get_expression()
        self.assertEqual(expression['operator'], 'attribute_not_exists')
        self.assertEqual(expression['values'][0].name, 'id')
        self.assertTrue(all(c.kwargs['ConsistentRead'] for c in self.table.get_item.call_args_list))

    def test_concurrent_creation_preserves_new_count(self):
        self.table.get_item.side_effect = [{}, {'Item': {'id': 'site', 'count': Decimal(7)}}]
        self.table.put_item.side_effect = ConditionalFailure()
        result = self.run_seed(apply=True, authorization='DEPLOYMENT AUTHORIZED')
        self.assertEqual(result['status'], 'concurrent_creation_preserved')
        self.assertEqual(result['count'], 7)


if __name__ == '__main__':
    unittest.main()
