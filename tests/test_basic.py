import networkx as nx
import unittest

from simulation.simulation import Simulation


class SimulationSetupAndRunTestSuite(unittest.TestCase):
    def setUp(self):
        self.simu = Simulation(200, 5, 1, 0.005, 1, 0, "random")

    def tearDown(self):
        pass
        #self.simu.dispose()
        #self.simu = None

    def test_simulation_setup(self):
        self.simu.setup()
        # Test to be written

    def test_simulation_run(self):
        self.simu.setup()
        self.simu.run()
        # Test to be written

class AfterSimulationWeightedRandomWalkTestSuite(unittest.TestCase):
    def setUp(self):
        self.simu = Simulation(200, 5, 1, 0.005, 1, 0, "weighted")
        self.simu.setup()
        self.simu.run()

    def tearDown(self):
        pass
        #self.simu.dispose()
        #self.simu = None

    def test_calculation_cum_weight(self):
        for transaction in self.simu.DG.nodes:
            self.assertEqual(transaction.cum_weight, len(list(nx.ancestors(self.simu.DG, transaction))) + 1)

    def test_calculation_conf_conf(self):
        self.simu.calc_confirmation_confidence()
        #Test to be written

if __name__ == '__main__':
    unittest.main()