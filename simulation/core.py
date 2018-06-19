import helpers
import constants
from simulation import Simulation

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency, distance, tip_selection_algo
#Tip selection algorithms are "random", "weighted", "unweighted"

simu = Simulation(10000, 50, 1, 0.05, 1, 0, "weighted")

simu.setup()

simu.run()

simu.print_graph()


