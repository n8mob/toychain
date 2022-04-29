from unittest import TestCase

from cryptography.hazmat.primitives.asymmetric import ec
from owner import Owner
from toycoin import ToyCoin

CURVE = ec.SECP256K1()


# noinspection DuplicatedCode
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

    def test_verify_initial_transaction(self):
        initial_transaction = self.unit_under_test.chain[0]

        self.owner0.public_key().verify(
            initial_transaction.signature,
            self.unit_under_test.data,
            self.unit_under_test.signature_algorithm,
        )

    def test_verify_signature_after_transfer(self):
        self.unit_under_test.transfer(self.owner1)
        expected_data = self.unit_under_test.chain[0].transaction_hash + self.owner1.default_public_bytes()

        transaction = self.unit_under_test.last_transaction()

        self.owner0.public_key().verify(
            transaction.signature,
            expected_data,
            self.unit_under_test.signature_algorithm
        )

    def test_verify_with_previous_owner_from_transaction(self):
        self.unit_under_test.transfer(self.owner1)

        expected_data = self.unit_under_test.chain[0].transaction_hash + self.owner1.default_public_bytes()

        transaction = self.unit_under_test.chain[1]

        transaction.previous_owner.public_key().verify(
            transaction.signature,
            expected_data,
            self.unit_under_test.signature_algorithm
        )

    def test_verify_link(self):
        self.unit_under_test.transfer(self.owner1)

        t0 = self.unit_under_test.chain[0]
        t1 = self.unit_under_test.chain[1]

        self.unit_under_test.verify_link(t0, t1)
