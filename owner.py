from __future__ import annotations

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey


class Owner:
    def __init__(self, private_key: EllipticCurvePrivateKey):
        self.private_key = private_key

    def public_key(self):
        return self.private_key.public_key()

    def default_public_bytes(self):
        return self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

