from typing import List

from cryptography.hazmat.primitives.asymmetric.ec import ECDSA, EllipticCurveSignatureAlgorithm
from cryptography.hazmat.primitives.hashes import SHA256, HashAlgorithm, Hash

from owner import Owner
from transaction import Transaction

DEFAULT_HASH_ALGORITHM = SHA256()
DEFAULT_SIGNATURE_ALGORITHM = ECDSA


class ToyCoin:
    signature_algorithm: EllipticCurveSignatureAlgorithm
    hash_algorithm: HashAlgorithm
    data: bytes

    def __init__(
            self,
            data: bytes,
            initial_owner: Owner,
            signature_algorithm=None,
            hash_algorithm=DEFAULT_HASH_ALGORITHM
    ):
        self.data = data
        self.hash_algorithm = hash_algorithm
        self.signature_algorithm = signature_algorithm or DEFAULT_SIGNATURE_ALGORITHM(hash_algorithm)

        signed_seed = initial_owner.private_key.sign(self.data, self.signature_algorithm)
        hasher = Hash(self.hash_algorithm)
        hasher.update(signed_seed)

        hashed_signature = hasher.finalize()

        self.chain: List[Transaction] = [Transaction(signed_seed, hashed_signature, initial_owner, initial_owner)]

    def last_transaction(self): return self.chain[-1]

    def last_owner(self) -> Owner: return self.last_transaction().current_owner

    def transfer(self, next_owner: Owner) -> None:
        previous_transaction = self.last_transaction()
        data_to_sign = previous_transaction.transaction_hash + next_owner.default_public_bytes()

        signed_data = previous_transaction.current_owner.private_key.sign(data_to_sign, self.signature_algorithm)
        hasher = Hash(self.signature_algorithm.algorithm)
        hasher.update(signed_data)
        hashed_data = hasher.finalize()

        self.chain.append(
            Transaction(
                signed_data, hashed_data, self.last_owner(), next_owner
            )
        )

    def verify_link(self, t1: Transaction, t2: Transaction):
        expected_data = t1.transaction_hash + t2.previous_owner.default_public_bytes()

        t1.current_owner.public_key().verify(
            t1.signature,
            expected_data,
            self.signature_algorithm
        )
