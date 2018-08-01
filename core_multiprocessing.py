import multiprocessing
import sys
import timeit
import numpy as np

from simulation.simulation_multi_agent import Multi_Agent_Simulation

def simulation(data):
    distance = 50000

    distances = [
        [0,distance,distance],
        [distance,0,distance],
        [distance,distance,0]
    ]

    simu = Multi_Agent_Simulation(300, 2, 2, 0.005, 1, distances, "weighted", printing="OFF")
    simu.setup()
    simu.run()
    return (data, simu.measure_partitioning())

def start_process():
    print("Starting", multiprocessing.current_process().name, "\n")

if __name__ == '__main__':
    start_time = timeit.default_timer()

    number_of_runs = list(range(20))

    print("Runs:", len(number_of_runs))

    builtin_outputs = map(simulation,number_of_runs)
    #print('Built-in:', builtin_outputs)

    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(
        processes=pool_size,
        initializer=start_process,
    )
    pool_outputs = pool.map(simulation,number_of_runs)
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    print("Results: ", pool_outputs, "\n")
    print("TOTAL simulation time: " + str(np.round(timeit.default_timer() - start_time, 3)) + " seconds\n")
