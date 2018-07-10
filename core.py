from simulation.simulation import Simulation
from simulation.simulation_multi_agent import Multi_Simulation


# Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency (h), distances (see note below), tip_selection_algo
# Tip selection algorithms: Choose among "random", "weighted", "unweighted" as input
# Distances: input a list, e.g. with 2 agents just [5], with 3 agents [5,5,5], denoting the distance of A to B, A to C, B to C

# simu = Simulation(20000, 50, 1, 0.001, 1, 0, "weighted")
# simu.setup()
# simu.run()
# #simu.calc_confirmation_confidence()
# #simu.print_graph()
# simu.print_tips_over_time()

# distances = [[0,2],[2,0]]
distances = [[0,100],[100,0]]
# distances = [[0,2,2],[2,0,2],[2,2,0]]
# distances = [[0,100,100,100],[100,0,100,100],[100,100,0,100],[100,100,100,0]]

simu2 = Multi_Simulation(10, 3, 2, 0.005, 1, distances, "weighted")
simu2.setup()
simu2.run()

simu2.calc_confirmation_confidence_multiple_agents()
simu2.measure_partitioning()

simu2.print_graph()
#simu2.print_tips_over_time()


