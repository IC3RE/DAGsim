import sys
import timeit
import random
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from simulation.helpers import update_progress, common_elements
from simulation.agent import Agent
from simulation.transaction import Transaction
from simulation.plot import print_info


class Multi_Agent_Simulation:
    def __init__(self, _no_of_transactions, _lambda, _no_of_agents, _alpha, _latency, _distances, _tip_selection_algo):
        self.no_of_transactions = _no_of_transactions
        self.lam = _lambda
        self.no_of_agents = _no_of_agents
        self.alpha = _alpha
        self.latency = _latency
        self.distances = _distances
        self.tip_selection_algo = _tip_selection_algo

        if (self.no_of_agents < 1):
            print("ERROR:  The number of agents can not be less than 1")
            sys.exit()

        elif (self.no_of_agents == 1):
            print("ERROR:  Use a Single_Agent_Simulation()")
            sys.exit()

        self.transactions = []
        self.agents = []
        self.arrival_times = []
        self.record_tips = []
        self.not_visible_transactions = []


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
        self.distance_matrix = nx.Graph()

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
        print_info(self)

        #Start with first transaction (NOT genesis)
        for transaction in self.transactions[1:]:

            #Change distance after a certain number of transactions
            # if(int(str(transaction)) == 50):
            #     self.distances = [[0, 2000], [2000, 0]]
            # elif (int(str(transaction)) == 150):
            #     self.distances = [[0, 0], [0, 0]]

            #Choose an agent
            transaction.agent = np.random.choice(self.agents)

            colors = ['#ffadad', '#dbeeff', '#e5d1e6', '#e6ff99'] #For four max. four agents

            #Add to directed graph object (with random y coordinate for plotting the graph)
            self.DG.add_node(transaction,pos=(transaction.arrival_time, random.uniform(0, 1)-int(str(transaction.agent))*1.3), node_color=colors[int(str(transaction.agent))])#'#ffadad')

            #Select tips
            self.tip_selection(transaction)

            #Update weights (of transactions referenced by the current transaction)
            self.update_weights_multiple_agents(transaction)
            #self.update_weights(transaction)

            #Progress bar update
            update_progress(int(str(transaction))/self.no_of_transactions, transaction)

        self.calc_exit_probabilities_multiple_agents()

        print("\nSimulation time: " + str(np.round(timeit.default_timer() - start_time, 3)) + " seconds")
        # print("\nGraph information:\n" + nx.info(self.DG))

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

    def get_visible_transactions(self, incoming_transaction_time, incoming_transaction_agent):

        #Initialize empty lists (for each transaction these are populated again)
        self.not_visible_transactions = []
        for agent in self.agents:
            agent.visible_transactions = []

        #Loop through all transactions in DAG
        for transaction in self.DG.nodes:

            #For EACH agent record the currently visible and not visible transactions
            for agent in self.agents:

                #Genesis always visible
                if (transaction.arrival_time == 0):

                    agent.visible_transactions.append(transaction)

                else:
                    #Get distance from agent to agent of transaction from distance matrix
                    distance = self.distances[int(str(agent))][int(str(transaction.agent))]

                    #Determine if the transaction is visible (incoming_transaction.arrival_time determines current time)
                    if (transaction.arrival_time + self.latency + distance <= incoming_transaction_time):

                        agent.visible_transactions.append(transaction)

                    #Record not visible transactions for 'current agent' only (reduces overhead, only needed once)
                    elif(incoming_transaction_agent == agent):
                        self.not_visible_transactions.append(transaction)
                        #agent.not_visible_transactions.append(transaction)

        # for agent in self.agents:
        #     print("AGENT   " + str(agent) + "  VISIBLE " + str(agent.visible_transactions))

    def get_valid_tips(self, incoming_transaction):

        valid_tips = []

        for transaction in incoming_transaction.agent.visible_transactions:

            #Transaction has no approvers at all
            if(len(list(self.DG.predecessors(transaction))) == 0
            #Transaction can't approve itself
            and transaction != incoming_transaction):

                valid_tips.append(transaction)

            #Add to valid tips if all approvers not visible yet
            elif(len(list(self.DG.predecessors(transaction))) >= 1
            #Transaction can't approve itself
            and transaction != incoming_transaction
            and self.all_approvers_not_visible(transaction)):

                valid_tips.append(transaction)

        return valid_tips

    def get_valid_tips_multiple_agents(self, agent):

        valid_tips = []

        for transaction in agent.visible_transactions:

            #Transaction has no approvers at all
            if(len(list(self.DG.predecessors(transaction))) == 0):

                valid_tips.append(transaction)

            #Add to valid tips if all approvers not visible yet
            elif(len(list(self.DG.predecessors(transaction))) >= 1
            and self.all_approvers_not_visible(transaction)):

                valid_tips.append(transaction)

        return valid_tips

    def all_approvers_not_visible(self, transaction):
        #Return true if all approvers not visible yet, false otherwise
        return set(self.DG.predecessors(transaction)).issubset(set(self.not_visible_transactions))

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
        self.get_visible_transactions(transaction.arrival_time, transaction.agent)
        valid_tips = self.get_valid_tips(transaction)

        if (valid_tips == []):
            return

        #Reference two random valid tips
        tip1 = np.random.choice(valid_tips)
        tip2 = np.random.choice(valid_tips)

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
        self.get_visible_transactions(transaction.arrival_time, transaction.agent)
        valid_tips = self.get_valid_tips(transaction)

        #If only genesis a valid tip, approve genesis
        if (valid_tips == [walker_on]):
            return walker_on

        while (walker_on not in valid_tips):

            approvers = list(self.DG.predecessors(walker_on))
            if approvers == []:
                return self.weighted_random_walk(self.transactions[0], transaction)

            walker_on = np.random.choice(approvers)

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
        self.get_visible_transactions(transaction.arrival_time, transaction.agent)
        valid_tips = self.get_valid_tips(transaction)

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
    # CONFIRMATION CONFIDENCE: MULTI AGENT
    #############################################################################

    def update_weights_multiple_agents(self, incoming_transaction):

        #Update all descendants of incoming_transaction only (cum_weight += 1)
        for transaction in nx.descendants(self.DG, incoming_transaction):

            #Update for each agent separately
            for agent in self.agents:

                if(transaction in agent.visible_transactions):
                    transaction.cum_weight_multiple_agents[agent] += 1

        #For all current tips set cum_weight to 1 (default value)
        tips = self.get_tips()

        for transaction in tips:
            for agent in self.agents:
                if (agent not in transaction.cum_weight_multiple_agents):
                    transaction.cum_weight_multiple_agents[agent] = 1

    def calc_exit_probabilities_multiple_agents(self):

        #Determine visible transaction for t + 1, so that all transactions (h = 1) are included
        self.get_visible_transactions(self.transactions[-1].arrival_time + 1, self.transactions[-1].agent)

        #Start at genesis, tips in the end
        sorted = list(reversed(list(nx.topological_sort(self.DG))))

        #Initialize genesis to 100% for both agents
        for agent in self.agents:
            self.transactions[0].exit_probability_multiple_agents[agent] = 1.0

        for transaction in sorted:

            #Update for each agent separately
            for agent in self.agents:

                if (transaction in agent.visible_transactions):

                    approvers = list(self.DG.predecessors(transaction))
                    visible_approvers = common_elements(approvers, agent.visible_transactions)

                    transition_probabilities = self.calc_transition_probabilities(visible_approvers)

                    for (approver, transition_probability) in zip(visible_approvers, transition_probabilities):
                        approver.exit_probability_multiple_agents[agent] += (transaction.exit_probability_multiple_agents[agent] * transition_probability)

    def calc_confirmation_confidence_multiple_agents(self):

        #Update for each agent separately
        for agent in self.agents:

            self.get_visible_transactions(self.transactions[-1].arrival_time + 1, agent)

            tips = self.get_valid_tips_multiple_agents(agent)

            for transaction in self.DG.nodes:
                for tip in tips:

                    #if (tip in agent.visible_transactions):

                    #Tips have 0 confirmation confidence by default
                    tip.confirmation_confidence_multiple_agents[agent] = 0

                    if(nx.has_path(self.DG,tip,transaction) and tip != transaction):

                        transaction.confirmation_confidence_multiple_agents[agent] += tip.exit_probability_multiple_agents[agent]

                print(str(transaction) + "   " + str(transaction.cum_weight_multiple_agents))
                print(str(transaction) + "   " + str(transaction.exit_probability_multiple_agents))
                print(str(transaction) + "   " + str(transaction.confirmation_confidence_multiple_agents) + "\n")

        #print(str(agent) + "   " + str(sum(tx.exit_probability_multiple_agents[agent] for tx in tips)))

        # (Potentially move the whole coloring to the end, after Tangle is created)
        # if (np.round(transaction.confirmation_confidence_multiple_agents[agent], 2) == 1.0):
        #     self.DG.node[transaction]["node_color"] = '#b4ffa3'
        #
        # elif(np.round(transaction.confirmation_confidence_multiple_agents[agent],2) >= 0.50):
        #     self.DG.node[transaction]["node_color"] = '#fff694'

    def measure_partitioning(self):

        #Calculate average confirmation rate of a transaction
        #Calculate confirmation rate variance of a transaction and global confirmation rate variance
        tx_confirmation_confidence_variances = []

        for transaction in self.DG.nodes:

            transaction.tx_average_confirmation_confidence \
                = (sum(transaction.confirmation_confidence_multiple_agents.values()) / len(self.agents))

            total = 0
            for agent in self.agents:

                total += (transaction.confirmation_confidence_multiple_agents[agent] \
                         - transaction.tx_average_confirmation_confidence) ** 2

            transaction.tx_confirmation_confidence_variance = total / len(self.agents)
            #print("Check NP:   " + str(np.var(list(transaction.confirmation_confidence_multiple_agents.values()))))
            tx_confirmation_confidence_variances.append(transaction.tx_confirmation_confidence_variance)

        return (np.mean(tx_confirmation_confidence_variances))

        # Calculate average confirmation rate of an agent
        # for agent in self.agents:
        #     total = 0
        #     agent_no_of_transactions = 0
        #
        #     for transaction in self.DG.nodes:
        #
        #         if(agent in transaction.confirmation_confidence_multiple_agents):
        #             total += transaction.confirmation_confidence_multiple_agents[agent]
        #             agent_no_of_transactions += 1
        #
        #     if(agent_no_of_transactions != 0):
        #         agent.agent_average_confirmation_confidence = total / agent_no_of_transactions
        #     else:
        #         print("Agent has no transactions")
        #
        #     print(total)
        #     print(agent_no_of_transactions)
        #     print(str(agent) + "   " + str(agent.agent_average_confirmation_confidence))