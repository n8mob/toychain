from typing import List

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA, EllipticCurveSignatureAlgorithm
from cryptography.hazmat.primitives.hashes import SHA256, HashAlgorithm, Hash

DEFAULT_HASH_ALGORITHM = SHA256()
DEFAULT_SIGNATURE_ALGORITHM = ECDSA

from owner import Owner
from transaction import Transaction


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
        data_to_hash = self.last_transaction().transaction_hash + next_owner.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        signed_data = self.last_owner().private_key.sign(data_to_hash, self.signature_algorithm)
        hasher = Hash(self.signature_algorithm.algorithm)
        hasher.update(signed_data)
        hashed_data = hasher.finalize()

        self.chain.append(
            Transaction(
                signed_data, hashed_data, self.last_owner(), next_owner
            )
        )
