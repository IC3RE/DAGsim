import networkx as nx
from simulation import Simulation

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency, distance, tip_selection_algo
#Tip selection algorithms are "random", "weighted", "unweighted"

# simu = Simulation(5000, 20, 1, 0, 1, 0, "unweighted")
# simu.setup()
# simu.run()
# simu.print_graph()
# simu.print_tips_over_time()

simu2 = Simulation(10, 2, 1, 0, 1, 0, "weighted")
simu2.setup()
simu2.run()
simu2.calc_confirmation_confidence()
simu2.print_graph()
#simu2.print_tips_over_time()

#Move this to tests
# for transaction in simu.DG.nodes:
#     print("Transaction " + str(transaction) + " has cum_weight " + str(transaction.cum_weight))
#     if (transaction.cum_weight != len(list(nx.ancestors(simu.DG, transaction))) + 1):
#         print("ERROR")

