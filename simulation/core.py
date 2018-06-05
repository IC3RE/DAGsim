import helpers
import constants
from simulation import Simulation
from plot import Plot

try:
    simu = Simulation()

    simu.setup()

    simu.run()

    # plot = Plot(arrival_times)
    # plot.show_plot()

except Exception as e:
    print(e)

