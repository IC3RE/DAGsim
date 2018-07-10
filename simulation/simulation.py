import sys
import timeit
import random
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from simulation.helpers import update_progress
from simulation.agent import Agent
from simulation.transaction import Transaction


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
            print("ERROR:  The number of agents can not be less than 1")
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
        arrival_times = np.cumsum(random_values)
        self.arrival_times = arrival_times

        #Create genesis transaction object, store in list and add to graph object
        transaction_counter = 0
        self.transactions.append(Transaction(0, transaction_counter))
        self.DG.add_node(self.transactions[0], pos=(0, 0), no=transaction_counter, node_color='#99ffff')

        transaction_counter += 1

        #Create other transaction objects and store in list
        for i in range(len(arrival_times)):
            self.transactions.append(Transaction(arrival_times[i], transaction_counter))
            transaction_counter += 1


    #############################################################################
    # SIMULATION: MAIN LOOP
    #############################################################################

    def run(self):

        start_time = timeit.default_timer()
        self.print_info()

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

        self.print_end_info(timeit.default_timer() - start_time)

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

        if (valid_tips == []):
            return

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
            if approvers == []:
                return self.weighted_random_walk(self.transactions[0], transaction)

            walker_on = random.choice(approvers)

        return walker_on


    #############################################################################
    # TIP-SELECTION: WEIGHTED
    #############################################################################

    def update_weights(self, transaction):

        for transaction in nx.descendants(self.DG, transaction):
            transaction.cum_weight += 1

        #Other approach 1, currently testing which is fastest
        # if(transaction == self.transactions[0]):
        #     return
        # else:
        #     for child in self.DG.successors(transaction):
        #
        #         child.ancestors = child.ancestors.union(transaction.ancestors).union({transaction})
        #         child.cum_weight = len(child.ancestors) + 1
        #         self.update_weights(child)
        #
        #Other approach 2
        # for transaction in transactions:
        #     transaction.cum_weight = len(list(nx.ancestors(self.DG, transaction))) + 1
        #
        #Other approach 3
        # sorted = nx.topological_sort(self.DG)
        # for transaction in sorted:
        #     children = self.DG.successors(transaction)
        #
        #     for child in children:
        #         child.ancestors = child.ancestors.union(transaction.ancestors).union({transaction})
        #
        #     transaction.cum_weight = len(transaction.ancestors) + 1

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
            if approvers == []:
                return self.weighted_random_walk(self.transactions[0], transaction)

            transition_probabilities = self.calc_transition_probabilities(approvers)

            #Choose with transition probabilities
            walker_on = np.random.choice(approvers, p=transition_probabilities)

        return walker_on


    #############################################################################
    # CONFIRMATION CONFIDENCE
    #############################################################################

    def calc_exit_probabilities(self):

        #Start at genesis, tips in the end
        sorted = list(reversed(list(nx.topological_sort(self.DG))))

        #Initialize genesis to 100%
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
                if(nx.has_path(self.DG,tip,transaction) and tip != transaction):

                    transaction.confirmation_confidence += tip.exit_probability

                    if (np.round(transaction.confirmation_confidence, 2) == 1.0):
                        self.DG.node[transaction]["node_color"] = '#b4ffa3'

                    elif(np.round(transaction.confirmation_confidence,2) >= 0.50):
                        self.DG.node[transaction]["node_color"] = '#fff694'

            #print(str(transaction) + "   " + str(transaction.confirmation_confidence))


    #############################################################################
    # PRINTING AND PLOTTING
    #############################################################################

    def print_info(self):
        text = "\nParameters:  Transactions = " + str(self.no_of_transactions) + \
                ",  Tip-Selection = " + str(self.tip_selection_algo).upper() + \
                ",  Lambda = " + str(self.lam)
        if(self.tip_selection_algo == "weighted"):
            text += ",  Alpha = " + str(self.alpha)
        text += " | Simulation started...\n"
        print(text)

    def print_end_info(self, elapsed_time):

        print("\nSimulation time: " + str(np.round(elapsed_time,3)) + " seconds")
        #print("\nGraph information:\n" + nx.info(self.DG))

    def print_graph(self):

        #Positioning and text of labels
        pos = nx.get_node_attributes(self.DG, 'pos')
        lower_pos = {key: (x, y-0.1) for key, (x, y) in pos.items()} #For label offset (0.1)

        labels = dict((transaction, str(np.round(transaction.confirmation_confidence,2))) for transaction in self.DG.nodes())

        #pos = graphviz_layout(self.DG, prog="dot", args="")
        #col = [['r','b'][int(np.round(transaction.confirmation_confidence,1))] for transaction in self.DG.nodes()] #Color change for 100% confidence

        #Coloring of nodes
        tips = self.get_tips()
        for tip in tips:
            self.DG.node[tip]["node_color"] = '#ffdbb8'
        col = list(nx.get_node_attributes(self.DG, 'node_color').values())

        #Creating figure
        plt.figure(figsize=(12, 6))
        nx.draw_networkx(self.DG, pos, with_labels=True, node_color = col)
        nx.draw_networkx_labels(self.DG, lower_pos, labels=labels)

        title = "Transactions = " + str(self.no_of_transactions) +\
                ",  " + r'$\lambda$' + " = " + str(self.lam)
        if(self.tip_selection_algo == "weighted"):
            title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
        plt.xlabel("Time (s)")
        plt.yticks([])
        plt.title(title)
        plt.show()
        #Save the graph
        #plt.savefig('graph.png')

    def print_tips_over_time(self):

        #Get no of tips per time
        no_tips = []
        for i in self.record_tips:
            no_tips.append(len(i))

        plt.figure(figsize=(12, 6))
        plt.plot(self.arrival_times, no_tips, label="Tips")

        #Cut off first 250 transactions for mean and best fit
        if(self.no_of_transactions >= 250):
            cut_off = 250
        else:
            cut_off = 0

        #Plot mean
        x_mean = [self.arrival_times[cut_off], self.arrival_times[-1]]
        y_mean = [np.mean(no_tips[cut_off:]), np.mean(no_tips[cut_off:])]
        plt.plot(x_mean, y_mean, label="Average Tips", linestyle='--')

        #Plot best fitted line
        plt.plot(np.unique(self.arrival_times[cut_off:]), np.poly1d(np.polyfit(self.arrival_times[cut_off:], no_tips[cut_off:], 1))(np.unique(self.arrival_times[cut_off:])), label="Best Fit Line", linestyle='--')

        title = "Transactions = " + str(self.no_of_transactions) + \
                ",  " + r'$\lambda$' + " = " + str(self.lam)
        if (self.tip_selection_algo == "weighted"):
            title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
        plt.xlabel("Time (s)")
        plt.ylabel("Number of tips")
        plt.legend(loc='upper left')
        plt.title(title)
        plt.show()