from unittest import TestCase

from cryptography.hazmat.primitives.asymmetric import ec
from owner import Owner
from toycoin import ToyCoin

CURVE = ec.SECP256K1()


class TestToyCoin(TestCase):
    def setUp(self) -> None:
        self.owner0 = Owner(ec.generate_private_key(CURVE))
        self.owner1 = Owner(ec.generate_private_key(CURVE))
        self.unit_under_test = ToyCoin(b'test data', self.owner0)

    def test_transfer_new_coin(self):
        self.assertTrue(self.unit_under_test.chain)  # non-empty is truth-y

        self.unit_under_test.transfer(self.owner0)

        self.assertTrue(self.unit_under_test.last_transaction())
        self.assertTrue(self.unit_under_test.chain)

    def test_transfer_second_coin(self):
        self.assertEqual(1, len(self.unit_under_test.chain))
        self.assertEqual(self.owner0, self.unit_under_test.last_owner())

        self.unit_under_test.transfer(self.owner1)

        self.assertEqual(2, len(self.unit_under_test.chain))
        self.assertEqual(self.owner1, self.unit_under_test.last_owner())
