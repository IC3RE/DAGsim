import helpers
import constants
import sha3

class Transaction:
    def __init__(self, _arrival_time):
        self.arrival_time = _arrival_time
        self.is_genesis = False
        self.agent, self.trunk, self.branch = None, None, None

    def __str__(self):
        return "I'm a transaction with arrival time " + str(self.arrival_time)

        #data = "randomstring"
        #s = sha3.keccak_256(data.encode('utf-8')).hexdigest()
        #print(s)