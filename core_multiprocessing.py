import multiprocessing
import sys
import timeit
import numpy as np

from simulation.helpers import update_progress, csv_export
from simulation.plotting import print_graph, print_tips_over_time, \
print_tips_over_time_multiple_agents, print_tips_over_time_multiple_agents_with_tangle
from simulation.simulation_multi_agent import Multi_Agent_Simulation


def simulation(data):
    simu = Multi_Agent_Simulation(5000, 25, 2, 0.005, 500, "weighted")
    simu.setup()
    simu.run()
    # print_tips_over_time_multiple_agents(simu, simu.no_of_transactions)


    averages = []

    for agent in simu.agents:
        no_tips = [0]
        for i in agent.record_tips:
            no_tips.append(len(i))

        averages.append(np.mean(no_tips))

    print("Done")

    return (data, averages)

def start_process():
    print("Starting", multiprocessing.current_process().name, "\n")

if __name__ == '__main__':
    start_time = timeit.default_timer()

    #Specify here how many simultaneous simulations to run
    number_of_runs = 30
    input_list = list(range(number_of_runs))

    print("Runs:", len(input_list))

    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(
        processes=pool_size,
        initializer=start_process,
    )

    pool_outputs = pool.map(simulation,input_list)
    pool.close()
    pool.join()

    print("Results: ", pool_outputs, "\n")
    print("TOTAL simulation time: " + str(np.round(timeit.default_timer() - start_time, 3)) + " seconds\n")

    agent_1 = []
    agent_2 = []

    for i in pool_outputs:
        agent_1.append(i[1][0])
        agent_2.append(i[1][1])

    # print(agent_1)
    # print(agent_2)
    print(np.mean(agent_1))
    print(np.mean(agent_2))
