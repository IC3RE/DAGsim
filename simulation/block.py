from collections import defaultdict
import random

class Block:
    def __init__(self, _arrival_time, _counter, _transactions = random.sample(range(5), 2)):
        """
        Class to setup a block object. The transactions input has a default random value(s)
        assigned  - for the case when a deterministic set of transactions is not required and 
        instead a random set is needed.
        """
        self.arrival_time = _arrival_time
        self.id = _counter
        self.agent = None
        
        #For storing a list of transactions in the block. Transactions represented
        #as a list of 10 integers, each randomly chosen from 1 - 49
        self.transactions = _transactions
        
        #For tip selection and calculating confirmation_confidence
        self.cum_weight = 1
        self.cum_weight_multiple_agents  = defaultdict(lambda: 1)
        self.exit_probability = 0
        self.exit_probability_multiple_agents  = defaultdict(lambda: 0)
        self.confirmation_confidence = 0
        self.confirmation_confidence_multiple_agents = defaultdict(lambda: 0)

        #For measuring partitioning
        self.tx_average_confirmation_confidence = 0
        self.tx_confirmation_confidence_variance = 0

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)
