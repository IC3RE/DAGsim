import numpy as np
import scipy.stats as st
import networkx as nx
import matplotlib.pyplot as plt
import time
from datetime import datetime

from simulation.helpers_spectre import update_progress, csv_export
from simulation.plotting_spectre import print_graph, print_tips_over_time, print_tips_over_time_multiple_agents
#from simulation.simulation import Single_Agent_Simulation
#from simulation.simulation_multi_agent import Multi_Agent_Simulation
from simulation.simulation_spectre_multi_agent import Multi_Agent_Simulation
from simulation.test_dag import build_test_dag
#from simulation.test_vote import 

#############################################################################
# SIMULATION: SINGLE AGENT
#############################################################################

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency (h), tip_selection_algo
#Tip selection algorithms: Choose among "random", "weighted", "unweighted" as input

# simu = Single_Agent_Simulation(15, 2, 1, 0.005, 1, "unweighted")
# simu.setup()
# simu.run()
# simu.calc_exit_probabilities()
# print_graph(simu)
# print_tips_over_time(simu)

# simu.calc_confirmation_confidence()

#############################################################################
# SIMULATION: MULTI AGENT
#############################################################################

#Parameters: no_of_blocks, lambda, no_of_agents, alpha, distance,
# latency (default value 1), agent_choice (default vlaue uniform distribution, printing)
#Tip selection algorithms: Choose among "random", "weighted", "unweighted" as input

#
#partitioning_values = []
#average_partitioning_across_simus = []

#runs = 1
#counter = 0

# distances = [[0,2,3],
#              [2,0,1],
#              [3,1,0]]

#for i in range(runs):
    #Distance set as large below to emulate two simulations (agents won't interact)
    #Large latency so that only genesis block should be referenced
#simu2 = Multi_Agent_Simulation(6, 2, 2, 0.005, 1000000000, 1, _printing=True) #This has a uniform agent distribution at the moment
#simu2.setup()
#(voting_profile, virtual_vote, output, z_vote) = simu2.run()

    # csv_export(simu2)

    # partitioning_values.append(simu2.measure_partitioning())
    # average_partitioning_across_simus.append(np.mean(partitioning_values))

    # update_progress(i/runs, str(i))
    # counter += 1

    #Sanity checks
    # print("SANITY CHECKS:\n")
    # for agent in simu2.agents:
        # print("VALID TIPS OF AGENT " + str(agent) + ":   " + str(agent.tips))
        # print("SUM OF EXIT PROBS FOR ALL TIPS:   " + str(sum(tip.exit_probability_multiple_agents[agent] for tip in agent.tips)) + "\n")
        #
        # for transaction in simu2.DG.nodes:
        #         # print(str(transaction) + "   " + str(transaction.cum_weight_multiple_agents[agent]))
        #         # print(str(transaction) + "   " + str(transaction.exit_probability_multiple_agents[agent]))
        #         print(str(transaction) + "   " + str(transaction.confirmation_confidence_multiple_agents[agent]))

# print(partitioning_values)
# print(np.mean(partitioning_values))
# print(np.var(partitioning_values))


###############################################################################
# TESTING
##############################################################################
#Close all pre-existing, open plots
plt.close('all')

dag = build_test_dag('simple')
simu3 = Multi_Agent_Simulation(11, 1, 2, 0.005, 100000000000, 1, _printing=True)
vote = simu3.CalcVotes(dag)
print('vote', vote)
#np.savetxt('voting_profile_excel'+(time.strftime("%H-%M-%S"))+"{:%B-%d-%Y}".format(datetime.now())+'.csv', vote, delimiter=',') 
plt.show()





#############################################################################
# PLOTTING
#############################################################################

#print_graph(simu2)
#print('test')
# print_tips_over_time(simu2)
# print_tips_over_time_multiple_agents(simu2, simu2.no_of_transactions)

#Plotting the partitioning values for multiple simulations, cumulative mean and 95% confidence interval
# plt.plot(simu2.record_partitioning)
# plt.plot(partitioning_values)
# plt.plot(average_partitioning_across_simus)
# lower_bound_95_confidence_interval = st.t.interval(0.80, len(partitioning_values)-1, loc=np.mean(partitioning_values), scale=st.sem(partitioning_values))[0]
# upper_bound_95_confidence_interval = st.t.interval(0.80, len(partitioning_values)-1, loc=np.mean(partitioning_values), scale=st.sem(partitioning_values))[1]
# plt.axhline(y=lower_bound_95_confidence_interval, color='r', linestyle='-')
# plt.axhline(y=upper_bound_95_confidence_interval, color='r', linestyle='-')
# plt.show()
