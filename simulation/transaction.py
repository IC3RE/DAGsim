import helpers
import constants
import sha3

class Transaction:
    def __init__(self, _arrival_time):
        self.arrival_time = _arrival_time
        self.is_genesis = False
        self.agent, self.trunk, self.branch = None, None, None

        #Give transaction a random hash as identifier?
        self.id = sha3.keccak_256(self.arrival_time).hexdigest()

    def __str__(self):
        return "Transaction with arrival time " + str(self.arrival_time) + " and hash " + self.id
