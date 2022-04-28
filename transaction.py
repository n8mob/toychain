from owner import Owner


class Transaction:
    def __init__(self, previous_hash, previous_owner: Owner, current_owner: Owner):
        self.transaction_hash = Transaction.make_hash(previous_hash, previous_owner, current_owner)
        self.previous_owner = previous_owner
        self.current_owner = current_owner

    @staticmethod
    def make_hash(previous_hash, previous_owner_key, new_owner_key) -> bytes:
        return b'fake'
