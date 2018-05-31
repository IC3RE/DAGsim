import helpers
import constants
import sha3

class Transaction:
    def __init__(self):
        print("Hello, I'm a transaction")
        self.arrival_time, self.agent, self.trunk, self.branch = None, None, None, None

        #data = "randomstring"
        #s = sha3.keccak_256(data.encode('utf-8')).hexdigest()
        #print(s)