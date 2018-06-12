import sys
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import helpers
import constants
from agent import Agent
from transaction import Transaction

class Simulation:
    def __init__(self, _no_of_transactions, _lambda, _no_of_agents, _alpha, _latency, _distance, _tip_selection_algo):
        self.transactions = []
        self.no_of_transactions = _no_of_transactions
        self.lam = _lambda
        self.no_of_agents = _no_of_agents
        self.alpha = _alpha
        self.latency = _latency
        self.distance = _distance
        self.tip_selection_algo = _tip_selection_algo

        if (self.no_of_agents < 1):
            print("The number of agents can not be less than 1!")
            sys.exit()

        elif (self.no_of_agents == 1):
            self.distance = 0

    #############################################################################
    # SIMULATION: SETUP
    #############################################################################

    def setup(self):
        #Create directed graph object
        self.DG = nx.DiGraph()

        #Create random arrival times
        random_values = np.random.exponential(1 / self.lam, self.no_of_transactions)
        arrival_times = np.round(np.cumsum(random_values),3)

        #Create genesis transaction object, store in list and add to graph object
        counter = 0
        self.transactions.append(Transaction(0, counter))
        counter += 1
        self.no_of_transactions += 1
        self.DG.add_node(self.transactions[0], pos=(0, 0))

        #Create other transaction objects and store in list
        for i in range(len(arrival_times)):
            self.transactions.append(Transaction(arrival_times[i], counter))
            counter += 1

    #############################################################################
    # SIMULATION: MAIN LOOP
    #############################################################################

    def run(self):

        #Start with first real transaction (not genesis)
        for transaction in self.transactions[1:]:
            #Just to check
            print("Transaction " + str(transaction) + " arrived")

            #Add to directed graph object (with random y coordinate for plotting the graph)
            self.DG.add_node(transaction,pos=(transaction.arrival_time, random.uniform(-1, 1)))

            #Select tips
            self.tip_selection(transaction, transaction.arrival_time)

        #Plot the graph
        pos = nx.get_node_attributes(self.DG, 'pos')
        nx.draw_networkx(self.DG, pos, with_labels=True)
        plt.show()

        #Save the graph
        #plt.savefig('graph.png')

    def tip_selection(self, transaction, time):

        if(self.tip_selection_algo == "random"):
            self.random_selection(transaction, time)
        elif(self.tip_selection_algo == "weighted"):
            self.weighted_random_walk(transaction, time)
        elif(self.tip_selection_algo == "unweighted"):
            self.unweighted_random_walk(transaction, time)

    #############################################################################
    # TIP-SELECTION: RANDOM
    #############################################################################

    def random_selection(self, transaction, time):

        #A tip can be selected if:
        # 1. it is visible
        # 2. it has no approvers at all OR it has some approvers, but all approvers are technically not visible yet
        visible_transactions, not_visible_transactions = self.get_visible_transactions(transaction, time)
        valid_tips = self.get_valid_tips(visible_transactions, not_visible_transactions)

        if (valid_tips == []):
            return

        #Reference two random valid tips
        self.DG.add_edge(transaction,random.choice(valid_tips))
        self.DG.add_edge(transaction,random.choice(valid_tips))

    def get_visible_transactions(self, incoming_transaction, time):

        visible_transactions = []
        not_visible_transactions = []

        for transaction in self.DG.nodes:

            if((transaction.arrival_time + self.latency <= time
            or transaction.arrival_time == 0)                                       #Genesis always visible
            and transaction != incoming_transaction):                               #Transaction can't approve itself

                visible_transactions.append(transaction)

            else:
                not_visible_transactions.append(transaction)

        print("Visible tips: " + str(visible_transactions))
        return visible_transactions, not_visible_transactions

    def get_valid_tips(self, visible_transactions, not_visible_transactions):

        valid_tips = []

        for transaction in visible_transactions:

            if(len(list(self.DG.predecessors(transaction))) == 0):                  #Transaction has no approvers at all

                valid_tips.append(transaction)

            elif(len(list(self.DG.predecessors(transaction))) >= 1                  #All approvers tech. not visible yet
            and self.all_approvers_not_visible(transaction, not_visible_transactions)):

                valid_tips.append(transaction)

        print("Valid tips: " + str(valid_tips))
        return valid_tips

    def all_approvers_not_visible(self, transaction, not_visible_transactions):
        return set(self.DG.predecessors(transaction)).issubset(set(not_visible_transactions))

    #############################################################################
    # TIP-SELECTION: UNWEIGHTED
    #############################################################################

    def unweighted_random_walk(self, transaction, time):
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
        print("Placeholder")

    #############################################################################
    # TIP-SELECTION: WEIGHTED
    #############################################################################

    def weighted_random_walk(self, transaction, time):
        '''
        Algorithm:

        TBD

        '''
        print("Placeholder")