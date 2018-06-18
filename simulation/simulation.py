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
        self.agents = []
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

        self.arrival_times = []
        self.record_tips = []

    #############################################################################
    # SIMULATION: SETUP
    #############################################################################

    def setup(self):
        #Create agents
        agent_counter = 0
        for agent in range(self.no_of_agents):
            self.agents.append(Agent(agent_counter))
            agent_counter += 1

        #Create directed graph object
        self.DG = nx.DiGraph()

        #Create random arrival times
        random_values = np.random.exponential(1 / self.lam, self.no_of_transactions)
        arrival_times = np.round(np.cumsum(random_values),3)
        self.arrival_times = arrival_times

        #Create genesis transaction object, store in list and add to graph object
        transaction_counter = 0
        self.transactions.append(Transaction(0, transaction_counter))
        self.DG.add_node(self.transactions[0], pos=(0, 0), no=transaction_counter)
        transaction_counter += 1

        #Create other transaction objects and store in list
        for i in range(len(arrival_times)):
            self.transactions.append(Transaction(arrival_times[i], transaction_counter))
            transaction_counter += 1

    #############################################################################
    # SIMULATION: MAIN LOOP
    #############################################################################

    def run(self):

        #Start with first real transaction (not genesis)
        for transaction in self.transactions[1:]:
            #Just to check
            print("Transaction " + str(transaction) + " arrived")

            #Add to directed graph object (with random y coordinate for plotting the graph), assume one agent for now
            transaction.agent = self.agents[0]
            self.DG.add_node(transaction,pos=(transaction.arrival_time, random.uniform(-1, 1)))

            #Select tips
            self.tip_selection(transaction)

        #Plotting number of tips
        # lens = []
        # for i in self.record_tips:
        #     lens.append(len(i))
        # plt.plot(self.arrival_times, lens)
        # plt.show()

        #Plot the graph
        pos = nx.get_node_attributes(self.DG, 'pos')
        nx.draw_networkx(self.DG, pos, with_labels=True)
        plt.title("Transactions = " + str(self.no_of_transactions) + ",  " + r'$\lambda$' + " = " + str(self.lam))
        plt.show()

        #Save the graph
        #plt.savefig('graph.png')

    def tip_selection(self, transaction):

        if(self.tip_selection_algo == "random"):
            self.random_selection(transaction)
        elif (self.tip_selection_algo == "unweighted"):
            self.unweighted_MCMC(transaction)
        elif(self.tip_selection_algo == "weighted"):
            self.weighted_MCMC(transaction)

    #############################################################################
    # TIP-SELECTION: RANDOM
    #############################################################################

    def random_selection(self, transaction):

        #A tip can be selected if:
        # 1. it is visible
        # 2. it has no approvers at all OR it has some approvers, but all approvers are technically not visible yet
        visible_transactions, not_visible_transactions = self.get_visible_transactions(transaction)
        valid_tips = self.get_valid_tips(visible_transactions, not_visible_transactions)

        if (valid_tips == []):
            return

        #Reference two random valid tips
        self.DG.add_edge(transaction,random.choice(valid_tips))

        #Include here a check to not add double edges?

        self.DG.add_edge(transaction,random.choice(valid_tips))
        # self.record_tips.append(self.get_tips())
        # print("Tips: " + str(self.get_tips()))

    def get_visible_transactions(self, incoming_transaction):

        visible_transactions = []
        not_visible_transactions = []

        for transaction in self.DG.nodes:

            if((transaction.arrival_time + self.latency <= incoming_transaction.arrival_time
            or transaction.arrival_time == 0)                                       #Genesis always visible
            and transaction != incoming_transaction):                               #Transaction can't approve itself

                visible_transactions.append(transaction)

            else:
                not_visible_transactions.append(transaction)

        #print("Visible tips: " + str(visible_transactions))
        return visible_transactions, not_visible_transactions

    def get_valid_tips(self, visible_transactions, not_visible_transactions):

        valid_tips = []

        for transaction in visible_transactions:

            if(len(list(self.DG.predecessors(transaction))) == 0):                  #Transaction has no approvers at all

                valid_tips.append(transaction)

            elif(len(list(self.DG.predecessors(transaction))) >= 1                  #All approvers tech. not visible yet
            and self.all_approvers_not_visible(transaction, not_visible_transactions)):

                valid_tips.append(transaction)

        #print("Valid tips: " + str(valid_tips))
        return valid_tips

    def all_approvers_not_visible(self, transaction, not_visible_transactions):
        return set(self.DG.predecessors(transaction)).issubset(set(not_visible_transactions))

    #############################################################################
    # TIP-SELECTION: UNWEIGHTED
    #############################################################################

    def unweighted_MCMC(self, transaction):

        # Start at genesis
        start = self.transactions[0]

        tip1 = self.random_walk(start, transaction)
        tip2 = self.random_walk(start, transaction)

        self.DG.add_edge(transaction,tip1)
        if(tip1 != tip2):
            self.DG.add_edge(transaction,tip2)

        self.record_tips.append(self.get_tips())

        '''
        Algorithm:
        0. Start at genesis
        1. Call random walk
        2. Check which tips are currently visible
        3. Check which transactions are directly approving the current one (= next)
        4. If next == tips that are currently visible
            Walk towards next transaction with random probability and store as approver
           Else
            Walk towards next transaction with random probability and repeat
        '''

    def random_walk(self, start, transaction):

        walker_on = start
        visible_transactions, not_visible_transactions = self.get_visible_transactions(transaction)
        valid_tips = self.get_valid_tips(visible_transactions, not_visible_transactions)

        #print("Valid tips: " + str(valid_tips))

        #If only genesis a valid tip, approve genesis
        if (valid_tips == [walker_on]):
            #print("Return early: " + str(walker_on))
            return walker_on


        #print("Walker on: " + str(walker_on))
        while (walker_on not in valid_tips):

            approvers = list(self.DG.predecessors(walker_on))
            #print("Approvers: " + str(approvers))
            if approvers == []:
                return walker_on

            walker_on = random.choice(approvers)
            #print("Walk to: " + str(walker_on))

        #print("Return after loop: " + str(walker_on))
        return walker_on

    #############################################################################
    # TIP-SELECTION: WEIGHTED
    #############################################################################

    def weighted_MCMC(self, transaction):
        '''
        Algorithm:

        TBD

        '''
        print("Placeholder")

    #For printing number of tips per time
    def get_tips(self):

        tips = []

        for transaction in self.DG.nodes:
            if (len(list(self.DG.predecessors(transaction))) == 0):
                tips.append(transaction)

        return tips