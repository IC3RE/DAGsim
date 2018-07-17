import numpy as np
import matplotlib.pyplot as plt

from simulation.simulation import Single_Agent_Simulation
from simulation.simulation_multi_agent import Multi_Agent_Simulation
from simulation.plot import print_graph, print_tips_over_time

#############################################################################
# SIMULATION: SINGLE
#############################################################################

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency (h), tip_selection_algo
#Tip selection algorithms: Choose among "random", "weighted", "unweighted" as input

# simu = Single_Agent_Simulation(1500, 50, 1, 0.005, 1, "weighted")
# simu.setup()
# simu.run()
# simu.calc_confirmation_confidence()


#############################################################################
# SIMULATION: MULTI
#############################################################################

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency (h), distances (see note below), tip_selection_algo
#Tip selection algorithms: Choose among "random", "weighted", "unweighted" as input
#Distances: input a list, e.g. with 2 agents just [5], with 3 agents [5,5,5], denoting the distance of A to B, A to C, B to C

distances = [
    [0,5],
    [5,0]
]

# distances = [
#     [0,2,2],
#     [2,0,2],
#     [2,2,0]
# ]
#
# distances = [
#     [0,100,100,100],
#     [100,0,100,100],
#     [100,100,0,100],
#     [100,100,100,0]
# ]

p = []
av = []
for i in range(500):
    simu2 = Multi_Agent_Simulation(200, 2, 2, 0.005, 1, distances, "weighted")
    simu2.setup()
    simu2.run()

    simu2.calc_confirmation_confidence_multiple_agents()

    p.append(simu2.measure_partitioning())
    av.append(np.mean(p))

#print(p)
# print(np.mean(p))
# print(np.var(p))
#
# plt.plot(p)
# plt.plot(av)
# plt.show()

#############################################################################
# PLOTTING
#############################################################################

# print_graph(simu)
print_graph(simu2)
# print_tips_over_time(simu)
# print_tips_over_time(simu2)
