import helpers
import constants
from simulation import Simulation
from agent import Agent
from transaction import Transaction
from plot import Plot

try:
    simu = Simulation()

    simu.setup()

    simu.run()

    # plot = Plot(arrival_times)
    # plot.show_plot()

    trans = Transaction()
except Exception as e:
    print(e)

