import helpers
import constants
from simulation import Simulation

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency, distance, tip_selection_algo
#Tip selection algorithms are "random", "weighted", "unweighted"

simu = Simulation(1000, 50, 1, 0, 1, 0, "unweighted")

simu.setup()

simu.run()



