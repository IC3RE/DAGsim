import helpers
import constants
from simulation import Simulation
from agent import Agent
from transaction import Transaction
from plot import Plot

simu = Simulation()
arrival_times = simu.cum_random_values

print(arrival_times)

plot = Plot(arrival_times)
plot.show_plot()
