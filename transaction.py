from owner import Owner


class Transaction:
    signature: bytes
    transaction_hash: bytes

    def __init__(self, signature: bytes, transaction_hash: bytes, previous_owner: Owner, current_owner: Owner):
        self.signature = signature
        self.transaction_hash = transaction_hash
        self.previous_owner = previous_owner
        self.current_owner = current_owner
