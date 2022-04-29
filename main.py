from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA, EllipticCurvePrivateKey

ellipticCurve = ec.SECP256K1()
privateKey: EllipticCurvePrivateKey = ec.generate_private_key(ellipticCurve)
signature_algorithm = ECDSA(hashes.SHA256())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for s in [b'hello', b'hello!', b'hellp', b'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz']:
        signed = privateKey.sign(s, signature_algorithm)
        print(f'signing {s}\t{int(len(signed) / 2)} bytes: {signed.hex()}')
        print(f'verifying {signed.hex()}:')

        privateKey.public_key().verify(signed, s, signature_algorithm)


# DONE define a transaction
# WON'T serialize the transaction
# DONE hash the transaction
# DONE sign the hash
