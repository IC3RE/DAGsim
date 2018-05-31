import numpy as np
import helpers
import constants

NO_OF_TRANSACTIONS = 10
LAMDBA = 2

class Simulation:
    def __init__(self):
        print("Hello, I'm a simulation")

    random_values = np.random.exponential(1/constants.LAMDBA,constants.NO_OF_TRANSACTIONS)
    cum_random_values = np.cumsum(random_values)
