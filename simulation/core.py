import helpers
import constants
from simulation import Simulation
from plot import Plot

try:
    simu = Simulation()

    simu.setup()

    simu.run()

except Exception as e:
    print(e)

