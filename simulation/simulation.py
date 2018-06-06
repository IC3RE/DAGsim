import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import helpers
import constants
from agent import Agent
from transaction import Transaction
from plot import Plot

class Simulation:
    def __init__(self):
        print("Hello, I'm a simulation")

    def setup(self):
        try:
            random_values = np.random.exponential(1 / constants.LAMDBA, constants.NO_OF_TRANSACTIONS)
            self.cum_random_values = np.cumsum(random_values)

            self.DG = nx.DiGraph()

        except Exception as e:
            print(e)

    def run(self):
        try:
            if(constants.NO_OF_AGENTS < 1):
                print("The number of agents can not be less than 1!")
                sys.exit()
            elif(constants.NO_OF_AGENTS == 1):
                constants.DISTANCE = 0

            arrival_times = self.cum_random_values

            #plot = Plot(arrival_times)
            #plot.show_plot()

            transactions = []
            for i in range(len(arrival_times)):
                transactions.append(Transaction(arrival_times[i]))

            transactions[0].is_genesis = True

            for transaction in transactions:
                print(transaction)

            '''
            TO-DO:
            
            1. Create nodes in the networkx graph with each transaction being a node?
            
            2. Simulate time, how? While-loop with a time variable that is increased? 
            
            3. At each time in point check if new transaction is coming in, which tips are visible and run tip-selection?
            
            '''

            '''
            DG.add_node(1)
            nx.draw(DG, with_labels=True)
            plt.show()
            plt.savefig('graph.png')
            '''
        except Exception as e:
            print(e)

    def unweighted_random_walk(self):
        '''

        Algorithm:
        0. Start at genesis
        1. Check which tips are currently visible
        2. Check which transactions are directly approving the current one (= next)
        3. If next == tips that are currently visible
            Walk towards next transaction with random probability and store as tip
           Else
            Walk towards next transaction with random probability and repeat

        '''
        print("Placeholder")

    def weighted_random_walk(self):
        '''

        Algorithm:

        '''
        print("Placeholder")



