import numpy as np
import matplotlib.pyplot as plt
import helpers
import constants

class Plot:
    def __init__(self, x, _no_of_transactions):
        self.x = x
        self.y = np.random.rand(_no_of_transactions)

    def show_plot(self):
        plt.scatter(self.x, self.y)
        plt.xlabel('$Time$')
        #plt.ylabel('$y$')
        plt.show()
