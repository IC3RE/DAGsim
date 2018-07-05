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

#distances = [[0,2,2],[2,0,2],[2,2,0]]#[[0,100,100,100],[100,0,100,100],[100,100,0,100],[100,100,100,0]]
distances = [[0,0],[0,0]]

simu2 = Multi_Simulation(200, 5, 2, 0.005, 1, distances, "random")
simu2.setup()
simu2.run()
simu2.calc_confirmation_confidence()
# simu2.print_tips_over_time()

simu3 = Multi_Simulation(200, 5, 2, 0.005, 1, distances, "unweighted")
simu3.setup()
simu3.run()
simu3.calc_confirmation_confidence()

simu4 = Multi_Simulation(200, 5, 2, 0.005, 1, distances, "weighted")
simu4.setup()
simu4.run()
simu4.calc_confirmation_confidence()

simu2.print_graph()
simu3.print_graph()
simu4.print_graph()
