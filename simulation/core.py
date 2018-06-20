import helpers
import constants
import networkx as nx
from simulation import Simulation

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency, distance, tip_selection_algo
#Tip selection algorithms are "random", "weighted", "unweighted"

simu = Simulation(20, 2, 1, 0, 1, 0, "weighted")

simu.setup()

simu.run()

print(nx.info(simu.DG))

simu.print_graph()
