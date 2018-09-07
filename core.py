import timeit
import pickle
import numpy as np
import scipy.stats as st
import networkx as nx
import matplotlib.pyplot as plt

from simulation.helpers import update_progress, csv_export, create_random_graph_distances
from simulation.plotting import print_graph, print_tips_over_time, \
print_tips_over_time_multiple_agents, print_tips_over_time_multiple_agents_with_tangle, \
print_attachment_probabilities_alone, print_attachment_probabilities_all_agents
from simulation.simulation import Single_Agent_Simulation
from simulation.simulation_multi_agent import Multi_Agent_Simulation

#############################################################################
# SIMULATION: SINGLE AGENT
#############################################################################

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency (h), tip_selection_algo
#Tip selection algorithms: Choose among "random", "weighted", "unweighted" as input

# simu = Single_Agent_Simulation(100, 50, 1, 0.005, 1, "weighted")
# simu.setup()
# simu.run()
# print_tips_over_time(simu)

#############################################################################
# SIMULATION: MULTI AGENT
#############################################################################

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, distance, tip_selection_algo
# latency (default value 1), agent_choice (default vlaue uniform distribution, printing)
#Tip selection algorithms: Choose among "random", "weighted", "unweighted" as input

start_time = timeit.default_timer()
runs = 1

number_of_agents = 10
distances = create_random_graph_distances(number_of_agents)

# distances = [[0.0, 80.0, 40.0, 60.0, 80.0, 40.0, 40.0, 20.0, 60.0, 40.0], [80.0, 0.0, 80.0, 60.0, 40.0, 80.0, 80.0, 60.0, 20.0, 40.0], [40.0, 80.0, 0.0, 60.0, 80.0, 40.0, 20.0, 20.0, 60.0, 40.0], [60.0, 60.0, 60.0, 0.0, 60.0, 60.0, 60.0, 40.0, 40.0, 20.0], [80.0, 40.0, 80.0, 60.0, 0.0, 80.0, 80.0, 60.0, 20.0, 40.0], [40.0, 80.0, 40.0, 60.0, 80.0, 0.0, 40.0, 20.0, 60.0, 40.0], [40.0, 80.0, 20.0, 60.0, 80.0, 40.0, 0.0, 20.0, 60.0, 40.0], [20.0, 60.0, 20.0, 40.0, 60.0, 20.0, 20.0, 0.0, 40.0, 20.0], [60.0, 20.0, 60.0, 40.0, 20.0, 60.0, 60.0, 40.0, 0.0, 20.0], [40.0, 40.0, 40.0, 20.0, 40.0, 40.0, 40.0, 20.0, 20.0, 0.0]]

for i in range(runs):

    simu2 = Multi_Agent_Simulation(1000, 50, 2, 0.005, 1, "weighted", _agent_choice=[0.7,0.3], _printing=True)
    simu2.setup()
    simu2.run()
    # csv_export(simu2)

print("TOTAL simulation time: " + str(np.round(timeit.default_timer() - start_time, 3)) + " seconds\n")

#############################################################################
# PLOTTING
#############################################################################

print_graph(simu2)
print_tips_over_time(simu2)
print_tips_over_time_multiple_agents(simu2, simu2.no_of_transactions)
print_tips_over_time_multiple_agents_with_tangle(simu2, simu2.no_of_transactions)
