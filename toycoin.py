from typing import List

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA, EllipticCurveSignatureAlgorithm
from cryptography.hazmat.primitives.hashes import SHA256

from owner import Owner
from transaction import Transaction


class ToyCoin:
    signature_algorithm: EllipticCurveSignatureAlgorithm
    data: bytes

    def __init__(self, data: bytes, initial_owner: Owner, signature_algorithm=ECDSA(SHA256())):
        self.chain: List[Transaction] = [Transaction('seed', initial_owner, initial_owner)]
        self.data = data
        self.signature_algorithm = signature_algorithm

    def last_transaction(self): return self.chain[-1]

    def last_owner(self) -> Owner: return self.last_transaction().current_owner

    def transfer(self, next_owner: Owner) -> None:
        data_to_hash = self.data + next_owner.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        hashed_data = self.last_owner().private_key.sign(data_to_hash, self.signature_algorithm)

        self.chain.append(
            Transaction(
                hashed_data, self.last_owner(), next_owner
            )
        )
