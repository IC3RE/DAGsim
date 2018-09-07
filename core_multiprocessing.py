import pickle
import multiprocessing
import sys
import timeit
import numpy as np

from simulation.helpers import update_progress, csv_export, create_random_graph_distances
from simulation.plotting import print_graph, print_tips_over_time, \
print_tips_over_time_multiple_agents, print_tips_over_time_multiple_agents_with_tangle, \
print_attachment_probabilities_alone, print_attachment_probabilities_all_agents
from simulation.simulation_multi_agent import Multi_Agent_Simulation


def simulation(data):

    number_of_agents = 10
    distances = [[0.0, 10.0, 30.0, 20.0, 10.0, 10.0, 40.0, 10.0, 20.0, 20.0], [10.0, 0.0, 40.0, 30.0, 20.0, 20.0, 50.0, 20.0, 30.0, 30.0], [30.0, 40.0, 0.0, 30.0, 40.0, 20.0, 10.0, 40.0, 30.0, 10.0], [20.0, 30.0, 30.0, 0.0, 30.0, 10.0, 40.0, 30.0, 20.0, 20.0], [10.0, 20.0, 40.0, 30.0, 0.0, 20.0, 50.0, 20.0, 30.0, 30.0], [10.0, 20.0, 20.0, 10.0, 20.0, 0.0, 30.0, 20.0, 10.0, 10.0], [40.0, 50.0, 10.0, 40.0, 50.0, 30.0, 0.0, 50.0, 40.0, 20.0], [10.0, 20.0, 40.0, 30.0, 20.0, 20.0, 50.0, 0.0, 10.0, 30.0], [20.0, 30.0, 30.0, 20.0, 30.0, 10.0, 40.0, 10.0, 0.0, 20.0], [20.0, 30.0, 10.0, 20.0, 30.0, 10.0, 20.0, 30.0, 20.0, 0.0]]

    simu = Multi_Agent_Simulation(10000, 50, number_of_agents, 0.1, distances, "weighted")
    simu.setup()
    simu.run()

    averages = []

    print("Done with one simu")

    return (data, simu.record_attachment_probabilities)

def start_process():
    print("Starting", multiprocessing.current_process().name, "\n")

if __name__ == '__main__':
    start_time = timeit.default_timer()

    #Specify here how many simultaneous simulations to run
    number_of_runs = 20
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

    with open('1.pkl', 'wb') as handle:
        pickle.dump(pool_outputs, handle, protocol=pickle.HIGHEST_PROTOCOL)
