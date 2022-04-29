from unittest import TestCase

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.hashes import SHA256, Hash

from owner import Owner
from toycoin import ToyCoin
from transaction import Transaction

SEED = b'seed'

CURVE = ec.SECP256K1()
HASH_ALGORITHM = SHA256()
SIGNATURE_ALGORITHM = ECDSA(HASH_ALGORITHM)


def defraud(source_transaction: Transaction, swindler: Owner, schnook: Owner) -> Transaction:
    data_to_hash = source_transaction.transaction_hash + schnook.default_public_bytes()

    signed_data = swindler.private_key.sign(data_to_hash, SIGNATURE_ALGORITHM)
    hasher = Hash(HASH_ALGORITHM)
    hasher.update(signed_data)
    hashed_data = hasher.finalize()

    fraudulent_transaction = Transaction(signed_data, hashed_data, swindler, schnook)

    return fraudulent_transaction


class TestDoubleSpend(TestCase):
    def setUp(self) -> None:
        self.duplicitous_owner = Owner(ec.generate_private_key(CURVE))
        self.recipient1 = Owner(ec.generate_private_key(CURVE))
        self.recipient2 = Owner(ec.generate_private_key(CURVE))

        self.coin = ToyCoin(SEED, self.duplicitous_owner, SIGNATURE_ALGORITHM)

    def test_keys(self):
        self.assertNotEqual(self.duplicitous_owner.public_key(), self.recipient1.public_key())
        self.assertNotEqual(self.duplicitous_owner.public_key(), self.recipient2.public_key())
        self.assertNotEqual(self.recipient1.public_key(), self.recipient2.public_key())

    def test_double_spend(self):
        t0 = self.coin.chain[0]
        t1 = defraud(t0, self.duplicitous_owner, self.recipient1)
        t2 = defraud(t0, self.duplicitous_owner, self.recipient2)

        try:
            self.coin.verify_link(t0, t1)
        except InvalidSignature:
            self.fail("Double spend is not handled and therefore this should not throw")

        try:
            self.coin.verify_link(t0, t2)
        except InvalidSignature:
            self.fail("Double spend is not handled and therefore this should not throw")
