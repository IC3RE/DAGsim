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
    def __init__(self, _no_of_transactions, _lambda, _no_of_agents, _alpha, _latency, _distance):
        self.no_of_transactions = _no_of_transactions
        self.lam = _lambda
        self.no_of_agents = _no_of_agents
        self.alpha = _alpha
        self.latency = _latency

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

            #Create transactions
            transactions = []
            counter = 0
            for i in range(len(arrival_times)):
                transactions.append(Transaction(arrival_times[i], counter))
                counter += 1

            #Initialize genesis
            transactions[0].is_genesis = True

            #Run simulation
            time = 0
            transaction_count = 0
            while(transaction_count < self.no_of_transactions):
                time += 0.001
                #print(np.round(time,3))

                #Check if transaction arrives
                if(np.round(time,3) == transactions[transaction_count].arrival_time):
                    print("Transaction " + str(transaction_count) + " arrived") #Just to check

                    #Add to graph object
                    self.DG.add_node(transactions[transaction_count])

                    #Select tips
                    self.tip_selection(transactions, transactions[transaction_count], time)

                    transaction_count += 1

            # nx.draw(self.DG, with_labels=True)
            # plt.show()
            # plt.savefig('graph.png')

            '''
            TO-DO:
            
            1. Create nodes in the networkx graph with each transaction being a node?
            
            2. Simulate time, how? While-loop with a time variable that is increased? 
            
            3. At each time in point check if new transaction is coming in, which tips are visible and run tip-selection?
            
            '''
        except Exception as e:
            print(e)

    def tip_selection(self, transactions, transaction, time):

        visible_transactions = self.get_visible_transactions(transactions, time)

        #self.unweighted_random_walk(transactions, transactions[transaction_count], time)


    def unweighted_random_walk(self, transactions, transaction, time):

        # Genesis transaction is a special case
        if(transaction.is_genesis == False):
            if (self.DG.number_of_edges() < 1):
                self.DG.add_edge(transaction,transactions[0])
            else:

                #WIP

                #rand1 = np.random.random_integers(0,transaction.id-1)
                #if (len(list(self.DG.predecessors(transactions[0])))) ==

                tips = self.get_tips(self.DG, transactions)

                '''
                found1 = False
                while(found1 == False):
                    random_no = np.random.random_integers(0,transaction.id-1)
                    print(random_no)
                    if(len(list(self.DG.predecessors(transactions[random_no]))) == 0):
                        self.DG.add_edge(transaction,transactions[random_no])
                        found1 = True
                '''

                # From current transaction to 2 other random transactions (but not itself)
                #self.DG.add_edge(transaction,transactions[np.random.random_integers(0,transaction.id-1)])
                #self.DG.add_edge(transaction,transactions[np.random.random_integers(0,transaction.id-1)])

            # Pick two random transactions to approve (could be the same)

        '''

        Algorithm:
        0. Start at genesis
        1. Check which tips are currently visible
        2. Check which transactions are directly approving the current one (= next)
        3. If next == tips that are currently visible
            Walk towards next transaction with random probability and store as approver
           Else
            Walk towards next transaction with random probability and repeat

        '''

    def weighted_random_walk(self):
        '''

        Algorithm:

        TBD

        '''
        print("Placeholder")


    def get_tips(self, DG, transactions):
        tips = []
        for transaction in self.DG.nodes:
            if (len(list(self.DG.predecessors(transaction))) == 0):
                tips.append(transaction)
        return tips


    def get_visible_transactions(self, transactions, time):

        visible_transactions = []

        for transaction in transactions:
            if(time + self.latency < transaction.arrival_time):
                visible_transactions.append(transaction)

        return visible_transactions





