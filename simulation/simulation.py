import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import helpers
import constants

NO_OF_TRANSACTIONS = 10
LAMDBA = 2

class Simulation:
    def __init__(self):
        print("Hello, I'm a simulation")

    def setup(self):
        try:
            random_values = np.random.exponential(1 / constants.LAMDBA, constants.NO_OF_TRANSACTIONS)
            self.cum_random_values = np.cumsum(random_values)
            DG = nx.DiGraph()
        except Exception as e:
            print(e)

    def run(self):
        try:
            arrival_times = self.cum_random_values
            print(arrival_times)
            '''
            DG.add_node(1)
            nx.draw(DG, with_labels=True)
            plt.show()
            plt.savefig('graph.png')
            '''
        except Exception as e:
            print(e)



