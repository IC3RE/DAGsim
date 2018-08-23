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
from simulation.block import Block


class Multi_Agent_Simulation:
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
        #This is creating a list of block objects, with as many objects as there are 
        #arrival times
        for i in range(len(self.arrival_times)):
            self.blocks.append(Block(self.arrival_times[i], block_counter))
            block_counter += 1
            
        return(self.blocks, self.agents, self.DG)
            
            
            
    #############################################################################
    # SIMULATION: HELPERS
    #############################################################################

    def get_tips(self):

        tips = []
        for block in self.DG.nodes:
            if (len(list(self.DG.predecessors(block))) == 0):
                tips.append(block)

        return tips


    def get_visible_blocks(self, incoming_block_time, incoming_block_agent):

        #Initialize empty lists (for each block these are populated again)
        self.not_visible_blocks = []
        for agent in self.agents:
            agent.visible_blocks = []

        #Loop through all blocks in DAG
        for block in self.DG.nodes:

            #For EACH agent record the currently visible and not visible blocks
            for agent in self.agents:

                #Genesis always visible
                if (block.arrival_time == 0):

                    agent.visible_blocks.append(block)

                else:
                    #Get distance from agent to agent of block from distance matrix
                    distance = self.distances[int(str(agent))][int(str(block.agent))]

                    #Determine if the block is visible (incoming_block.arrival_time determines current time)
                    if (block.arrival_time + self.latency + distance <= incoming_block_time):

                        agent.visible_blocks.append(block)

                    #Record not visible blocks for 'current agent' only (reduces overhead)
                    elif(incoming_block_agent == agent):
                        self.not_visible_blocks.append(block)


    # def get_valid_tips(self, incoming_block):
    #
    #     valid_tips = []
    #
    #     for block in incoming_block.agent.visible_blocks:
    #
    #         #block has no approvers at all
    #         if(len(list(self.DG.predecessors(block))) == 0
    #         #block can't approve itself
    #         and block != incoming_block):
    #
    #             valid_tips.append(block)
    #
    #         #Add to valid tips if all approvers not visible yet
    #         elif(len(list(self.DG.predecessors(block))) >= 1
    #         #block can't approve itself
    #         and block != incoming_block
    #         and self.all_approvers_not_visible(block)):
    #
    #             valid_tips.append(block)
    #
    #     return valid_tips


    def get_valid_tips_multiple_agents(self, agent):

        valid_tips = []

        for block in agent.visible_blocks:

            #Add to valid tips if block has no approvers at all
            if(len(list(self.DG.predecessors(block))) == 0):

                valid_tips.append(block)

            #Add to valid tips if all approvers not visible yet
            elif(self.all_approvers_not_visible(block)):

                valid_tips.append(block)

        return valid_tips


    def all_approvers_not_visible(self, block):

        #Edge case: if not genesis
        # if(block.arrival_time != 0):
        #     approvers = list(self.DG.predecessors(block))
        #     visible_approvers = common_elements(approvers, block.agent.visible_blocks)
        #     #Return true if all approvers not visible yet, false otherwise
        #     return set(visible_approvers).issubset(set(self.not_visible_blocks))
        # else:
        return set(list(self.DG.predecessors(block))).issubset(set(self.not_visible_blocks))
