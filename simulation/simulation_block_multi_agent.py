import sys
import timeit
import random
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from simulation.helpers import update_progress, create_distance_matrix, common_elements, load_file
from simulation.plotting import print_info, print_graph, print_tips_over_time, print_tips_over_time_multiple_agents
from simulation.agent import Agent
from simulation.transaction import Transaction
from siulation.block import Block


class Block_Multi_Agent_Simulation:
    def __init__(self, _no_of_blocks, _lambda, _no_of_agents, \
                 _alpha, _distance, _tip_selection_algo, _latency = 1, \
                 _agent_choice=None, _printing=False):

        #Use configuration file when provided
        if(len(sys.argv) != 1):
            self.config = load_file(sys.argv[1])
            self.no_of_blocks = self.config[0][0]
            self.lam = self.config[0][1]
            self.no_of_agents = self.config[0][2]
            self.alpha = self.config[0][3]
            self.latency = self.config[0][4]
            self.distances = self.config[0][5]
            self.tip_selection_algo = self.config[0][6]
            self.agent_choice = self.config[0][7]
            self.printing = self.config[0][8]
        #Otherwise use the provided parameters
        else:
            self.no_of_blocks = _no_of_blocks
            self.lam = _lambda
            self.no_of_agents = _no_of_agents
            self.alpha = _alpha
            self.latency = _latency
            if (type(_distance) is float or type(_distance) is int):
                self.distances = create_distance_matrix(self.no_of_agents, _distance)
            else:
                self.distances = _distance
            self.tip_selection_algo = _tip_selection_algo
            if _agent_choice is None:
                _agent_choice = list(np.ones(self.no_of_agents)/self.no_of_agents)
            self.agent_choice = _agent_choice
            self.printing = _printing

        if (round(sum(self.agent_choice), 3) != 1.0):
            print("Agent choice not summing to 1.0: {}".format(sum(self.agent_choice)))
            sys.exit(1)
        if (len(self.agent_choice) != self.no_of_agents):
            print("Agent choice not matching no_of_agents: {}".format(len(self.agent_choice)))
            sys.exit(1)
        if (self.no_of_agents == 1):
            print("ERROR:  Use a Single_Agent_Simulation()")
            sys.exit()

        self.blocks = []
        self.agents = []
        self.arrival_times = []
        self.not_visible_blocks = []

        #For analysis only
        self.record_tips = []
        self.record_partitioning = []

        #For max. four agents same colors, for more agents random colors
        self.agent_colors = ['#a8d6ff', '#ff9494', '#dcc0dd', '#e0ff80']
        self.agent_tip_colors = ['#f5faff', '#ffe0e0', '#f8f2f8', '#f9ffe6']
        for i in range(self.no_of_agents-4):
            r = lambda: random.randint(0,255)
            color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
            self.agent_colors.append(color)

    #############################################################################
    # SIMULATION: SETUP
    #############################################################################

    def setup(self):

        #Create agents
        agent_counter = 0
        for agent in range(self.no_of_agents):
            self.agents.append(Agent(agent_counter))
            agent_counter += 1

        #Create directed graph object
        self.DG = nx.DiGraph()

        #Create random arrival times
        inter_arrival_times = np.random.exponential(1 / self.lam, self.no_of_blocks)
        self.arrival_times = np.cumsum(inter_arrival_times)

        #Create genesis block object, store in list and add to graph object
        block_counter = 0
        self.blocks.append(Block(0, block_counter))
        self.DG.add_node(self.blocks[0], pos=(0, 0), no=block_counter, node_color='#99ffff')

        block_counter += 1

        #Create other block objects and store in list
        for i in range(len(self.arrival_times)):
            self.blocks.append(Block(self.arrival_times[i], block_counter))
            block_counter += 1
