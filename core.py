from simulation.simulation import Simulation


#Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency (h), distance, tip_selection_algo
#Tip selection algorithms are "random", "weighted", "unweighted"

simu = Simulation(200, 5, 1, 0.005, 1, 0, "weighted")
simu.setup()
simu.run()
simu.calc_confirmation_confidence()
simu.print_graph()
simu.print_tips_over_time()
