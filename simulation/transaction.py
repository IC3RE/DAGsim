from collections import defaultdict

class Transaction:
    def __init__(self, _arrival_time, counter):
        self.arrival_time = _arrival_time
        self.agent = None

        #For tip selection and calculating confirmation_confidence
        self.cum_weight = 1
        self.cum_weight_multiple_agents  = defaultdict(lambda: 1)
        self.exit_probability = 0
        self.exit_probability_multiple_agents  = defaultdict(lambda: 0)
        self.confirmation_confidence = 0
        self.confirmation_confidence_multiple_agents = defaultdict(lambda: 0)

        #For measuring partitioning
        self.average_confirmation_confidence = 0

        #Give transaction a random hash as identifier? For now just using numbers
        self.id = counter #self.id = sha3.keccak_256(self.arrival_time).hexdigest()

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)


