from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey


class Owner:
    def __init__(self, private_key: EllipticCurvePrivateKey):
        self.private_key = private_key

    def public_key(self): return self.private_key.public_key()

