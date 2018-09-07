import sys
import timeit
import random
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from simulation.helpers import update_progress, common_elements
from simulation.plotting import print_info
from simulation.agent import Agent
from simulation.transaction import Transaction


class Single_Agent_Simulation:
    def __init__(self, _no_of_transactions, _lambda, _no_of_agents, _alpha, _latency, _tip_selection_algo):
        self.no_of_transactions = _no_of_transactions
        self.lam = _lambda
        self.no_of_agents = _no_of_agents
        self.alpha = _alpha
        self.latency = _latency
        self.tip_selection_algo = _tip_selection_algo

        if (self.no_of_agents < 1):
            print("ERROR:  The number of agents can not be less than 1")
            sys.exit()

        self.transactions = []
        self.agents = []
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
        inter_arrival_times = np.random.exponential(1 / self.lam, self.no_of_transactions)
        self.arrival_times = np.cumsum(inter_arrival_times)

        #Create genesis transaction object, store in list and add to graph object
        transaction_counter = 0
        self.transactions.append(Transaction(0, transaction_counter))
        self.DG.add_node(self.transactions[0], pos=(0, 0), no=transaction_counter, node_color='#99ffff')

        transaction_counter += 1

        #Create other transaction objects and store in list
        for i in range(len(self.arrival_times)):
            self.transactions.append(Transaction(self.arrival_times[i], transaction_counter))
            transaction_counter += 1


    #############################################################################
    # SIMULATION: MAIN LOOP
    #############################################################################


    def run(self):

        start_time = timeit.default_timer()
        print_info(self)

        #Start with first transaction (NOT genesis)
        for transaction in self.transactions[1:]:

            #Add to directed graph object (with random y coordinate for plotting the graph), assume one agent for now
            transaction.agent = self.agents[0]
            self.DG.add_node(transaction,pos=(transaction.arrival_time, random.uniform(-1, 1)), node_color='#ffadad')

            #Select tips
            self.tip_selection(transaction)

            #Update weights (of transactions referenced by the current transaction)
            self.update_weights(transaction)

            #Progress bar update
            update_progress(int(str(transaction))/self.no_of_transactions, str(transaction))

        self.calc_exit_probabilities()

        print("\nSimulation time: " + str(np.round(timeit.default_timer() - start_time, 3)) + " seconds")
        #print("\nGraph information:\n" + nx.info(self.DG))


    def tip_selection(self, transaction):

        if(self.tip_selection_algo == "random"):
            self.random_selection(transaction)
        elif (self.tip_selection_algo == "unweighted"):
            self.unweighted_MCMC(transaction)
        elif(self.tip_selection_algo == "weighted"):
            self.weighted_MCMC(transaction)
        else:
            print("ERROR:  Tip selection algorithms are 'random', 'weighted', 'unweighted'")
            sys.exit()


    #############################################################################
    # SIMULATION: HELPERS
    #############################################################################


    def get_tips(self):

        tips = []
        for transaction in self.DG.nodes:
            if (len(list(self.DG.predecessors(transaction))) == 0):
                tips.append(transaction)

        return tips


    def get_visible_transactions(self, incoming_transaction):

        visible_transactions = []
        not_visible_transactions = []

        for transaction in self.DG.nodes:

            if((transaction.arrival_time + self.latency <= incoming_transaction.arrival_time
            or transaction.arrival_time == 0)
            and transaction != incoming_transaction):

                visible_transactions.append(transaction)

            else:
                not_visible_transactions.append(transaction)

        #print("Visible tips: " + str(visible_transactions))
        return visible_transactions, not_visible_transactions


    def get_valid_tips(self, visible_transactions, not_visible_transactions):

        valid_tips = []

        for transaction in visible_transactions:

            #Add to valid tips if transaction has no approvers at all
            if(len(list(self.DG.predecessors(transaction))) == 0):

                valid_tips.append(transaction)

            #Add to valid tips if all approvers not visible yet
            elif(self.all_approvers_not_visible(transaction, not_visible_transactions)):

                valid_tips.append(transaction)

        return valid_tips


    def all_approvers_not_visible(self, transaction, not_visible_transactions):
        return set(self.DG.predecessors(transaction)).issubset(set(not_visible_transactions))


    def calc_transition_probabilities(self, approvers):

        weights = [approver.cum_weight for approver in approvers]
        normalized_weights = [weight - max(weights) for weight in weights]
        denominator_transition_probabilities = sum([math.exp(self.alpha * weight) for weight in normalized_weights])

        return [math.exp(self.alpha * (approver.cum_weight - max(weights))) / denominator_transition_probabilities for
                approver in approvers]


    #############################################################################
    # TIP-SELECTION: RANDOM
    #############################################################################


    def random_selection(self, transaction):

        #A tip can be selected if:
        # 1. it is visible
        # 2. it has no approvers at all OR it has some approvers, but all approvers are technically not visible yet
        visible_transactions, not_visible_transactions = self.get_visible_transactions(transaction)
        valid_tips = self.get_valid_tips(visible_transactions, not_visible_transactions)

        #Reference two random valid tips
        tip1 = random.choice(valid_tips)
        tip2 = random.choice(valid_tips)

        self.DG.add_edge(transaction, tip1)
        if (tip1 != tip2):
            self.DG.add_edge(transaction, tip2)

        self.record_tips.append(self.get_tips())


    #############################################################################
    # TIP-SELECTION: UNWEIGHTED
    #############################################################################


    def unweighted_MCMC(self, transaction):

        #Start at genesis
        start = self.transactions[0]

        tip1 = self.random_walk(start, transaction)
        tip2 = self.random_walk(start, transaction)

        self.DG.add_edge(transaction,tip1)
        if(tip1 != tip2):
            self.DG.add_edge(transaction,tip2)

        self.record_tips.append(self.get_tips())


    def random_walk(self, start, transaction):

        walker_on = start
        visible_transactions, not_visible_transactions = self.get_visible_transactions(transaction)
        valid_tips = self.get_valid_tips(visible_transactions, not_visible_transactions)

        #If only genesis a valid tip, approve genesis
        if (valid_tips == [walker_on]):
            return walker_on

        while (walker_on not in valid_tips):

            approvers = list(self.DG.predecessors(walker_on))
            visible_approvers = common_elements(approvers, visible_transactions)

            walker_on = random.choice(visible_approvers)

        return walker_on


    #############################################################################
    # TIP-SELECTION: WEIGHTED
    #############################################################################


    def weighted_MCMC(self, transaction):

        #Start at genesis
        start = self.transactions[0]

        tip1 = self.weighted_random_walk(start, transaction)
        tip2 = self.weighted_random_walk(start, transaction)

        self.DG.add_edge(transaction, tip1)
        if (tip1 != tip2):
            self.DG.add_edge(transaction, tip2)

        self.record_tips.append(self.get_tips())


    def weighted_random_walk(self, start, transaction):

        walker_on = start
        visible_transactions, not_visible_transactions = self.get_visible_transactions(transaction)
        valid_tips = self.get_valid_tips(visible_transactions, not_visible_transactions)

        #If only genesis a valid tip, approve genesis
        if (valid_tips == [walker_on]):
            return walker_on

        while (walker_on not in valid_tips):

            approvers = list(self.DG.predecessors(walker_on))
            visible_approvers = common_elements(approvers, visible_transactions)
            transition_probabilities = self.calc_transition_probabilities(visible_approvers)

            #Choose with transition probabilities
            walker_on = np.random.choice(visible_approvers, p=transition_probabilities)

        return walker_on


    #############################################################################
    # CONFIRMATION CONFIDENCE: SINGLE AGENT
    #############################################################################


    def update_weights(self, incoming_transaction):

        for transaction in nx.descendants(self.DG, incoming_transaction):
            transaction.cum_weight += 1

        # sorted = nx.topological_sort(self.DG)
        # for transaction in sorted:
        #     children = self.DG.successors(transaction)
        #
        #     for child in children:
        #         child.ancestors = child.ancestors.union(transaction.ancestors).union({transaction})
        #
        #     transaction.cum_weight = len(transaction.ancestors) + 1


    def calc_exit_probabilities(self):

        # Start at genesis, tips in the end
        sorted = list(reversed(list(nx.topological_sort(self.DG))))

        # Initialize genesis to 100%
        self.transactions[0].exit_probability = 1.0

        for transaction in sorted:
            approvers = list(self.DG.predecessors(transaction))
            transition_probabilities = self.calc_transition_probabilities(approvers)

            for (approver, transition_probability) in zip(approvers, transition_probabilities):
                approver.exit_probability += (transaction.exit_probability * transition_probability)


    def calc_confirmation_confidence(self):

        tips = self.get_tips()

        for transaction in self.DG.nodes:
            for tip in tips:
                if (nx.has_path(self.DG, tip, transaction) and tip != transaction):

                    transaction.confirmation_confidence += tip.exit_probability

                    # (Potentially move the whole coloring to the end, after Tangle is created)
                    if (np.round(transaction.confirmation_confidence, 2) == 1.0):
                        self.DG.node[transaction]["node_color"] = '#b4ffa3'

                    elif (np.round(transaction.confirmation_confidence, 2) >= 0.50):
                        self.DG.node[transaction]["node_color"] = '#fff694'
