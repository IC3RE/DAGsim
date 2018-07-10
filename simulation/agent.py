class Agent:
    def __init__(self, counter):
        self.id = counter
        self.visible_transactions = []

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

