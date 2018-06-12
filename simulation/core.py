import helpers
import constants
from simulation import Simulation

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency, distance, tip_selection_algo
#Tip selection algorithms are "random", "weighted", "unweighted

simu = Simulation(20, 2, 1, 0, 1, 0, "random")

simu.setup()

simu.run()



