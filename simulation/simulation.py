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
    def __init__(self, _no_of_transactions, _lambda, _no_of_agents, _alpha, _distance):
        self.no_of_transactions = _no_of_transactions
        self.lam = _lambda
        self.no_of_agents = _no_of_agents
        self.alpha = _alpha

        if (self.no_of_agents < 1):
            print("The number of agents can not be less than 1!")
            sys.exit()

        elif (self.no_of_agents == 1):
            self.distance = 0

        self.distance = _distance

    def setup(self):
        try:
            random_values = np.random.exponential(1 / self.lam, self.no_of_transactions)
            self.cum_random_values = np.round(np.cumsum(random_values),3)

            self.DG = nx.DiGraph()

        except Exception as e:
            print(e)

    def run(self):
        try:
            arrival_times = self.cum_random_values

            #plot = Plot(arrival_times, self.no_of_transactions)
            #plot.show_plot()

            transactions = []
            for i in range(len(arrival_times)):
                transactions.append(Transaction(arrival_times[i]))

            transactions[0].is_genesis = True

            self.DG.add_nodes_from(transactions)

            '''
            for transaction in transactions:
                #Genesis transaction is a special case
                if (transaction.is_genesis == False):
                    if(self.DG.number_of_edges() < 1):
            '''
            #for transaction in transactions:
                #print(transaction)

            print(len(transactions))

            test_time = 0
            transaction_count = 0
            while(transaction_count < 100):
                test_time += 0.001
                #print(np.round(test_time,3))

                if(np.round(test_time,3) == transactions[transaction_count].arrival_time):

                    self.unweighted_random_walk(transactions[transaction_count])

                    transaction_count += 1


            '''
            TO-DO:
            
            1. Create nodes in the networkx graph with each transaction being a node?
            
            2. Simulate time, how? While-loop with a time variable that is increased? 
            
            3. At each time in point check if new transaction is coming in, which tips are visible and run tip-selection?
            
            '''

            #nx.draw(self.DG, with_labels=False)
            #plt.show()
            #plt.savefig('graph.png')

        except Exception as e:
            print(e)

    def unweighted_random_walk(self, transaction):

        # Genesis transaction is a special case
        if(transaction.is_genesis == False):
            print(transaction)

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

        TBD

        '''
        print("Placeholder")



