import sys
import timeit
import random
import math
import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from simulation.helpers_spectre import update_progress, create_distance_matrix, common_elements, load_file
from simulation.plotting_spectre import print_info, print_graph, print_tips_over_time, print_tips_over_time_multiple_agents
from simulation.agent import Agent
from simulation.block import Block


class Multi_Agent_Simulation:
    def __init__(self, _no_of_blocks, _lambda, _no_of_agents, \
                 _alpha, _distance, _latency = 1, \
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
            self.agent_choice = self.config[0][6]
            self.printing = self.config[0][7]
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
        """
        Initialises the agents, blocks, arrival times, pairwise vote lists and 
        """

        #Create agents
        agent_counter = 0
        for agent in range(self.no_of_agents):
            self.agents.append(Agent(agent_counter))
            agent_counter += 1

        #Create directed graph object
        self.DG = nx.DiGraph()

        #Create list to store sequentially created graph objects
        self.DG_store = []
        
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

    #############################################################################
    # SIMULATION: MAIN LOOP
    #############################################################################

    def run(self):
        """
        Forms the ledger according to the SPECTRE mining protocol
        """

        start_time = timeit.default_timer()

        if self.printing:
            print_info(self)

        #Create dictionary with simulation parameter changes when provided
        if(len(sys.argv) != 1):
            dic = {x[0]: x[1:] for x in self.config[1:]}

        ###################################################################
        # FORMATION OF LEDGER
        ###################################################################
            
        #Start with first block (NOT genesis)
        for block in self.blocks[1:]:

            #Execute simulation parameter changes when provided
            if(len(sys.argv) != 1):
                self.check_parameters_changes(block, dic)

            #Do something every 100th transition
            # if (int(str(block)) % 100 == 0):
            #     self.calc_exit_probabilities_multiple_agents(block)
            #     self.calc_confirmation_confidence_multiple_agents(block)
            #     self.record_partitioning.append(self.measure_partitioning())

            #Choose an agent
            block.agent = np.random.choice(self.agents, p=self.agent_choice)
#            print(block.agent)     
            
            """
            This HAS to come before you add a block - otherwise everything goes out of sync for the 
            recursion            
            
            Create a copy independent to the graph instance (otherwise you can't append the graph - 
            if you append self.DG then you're appending an instance, which is a pointer to the same underlying 
            object)
            """
            
            DG_copy = self.DG.copy()
            self.DG_store.append(DG_copy) 
                        
            #Add block to directed graph object (with random y coordinate for plotting the graph)
            self.DG.add_node(block,pos=(block.arrival_time, random.uniform(0, 1)-int(str(block.agent))*1.3), node_color=self.agent_colors[int(str(block.agent))])#'#ffadad')

            #Select tips
            self.tip_selection(block)            
            
            #Update weights (of blocks referenced by the current block) - not needed in SPECTRE
#            self.update_weights_multiple_agents(block)

            #Progress bar update
            if self.printing:
                update_progress(int(str(block))/self.no_of_blocks, block)
        
        #######################################################################
        # CONSENSUS PROTOCOL
        #######################################################################
        
        #Generate the pairwise vote, taking the blockDAG as an input
#        print(type(self.DG))
        
        (voting_profile, virtual_vote, sign_sum_future_votes, z_vote) = self.CalcVotes(self.DG)
        
        
        #Determine the accepted set of transactions, taking the pairwise vote as 
        #input
        

        #print_tips_over_time_multiple_agents(self, int(str(block)))

        if self.printing:
            print("Simulation time: " + str(np.round(timeit.default_timer() - start_time, 3)) + " seconds\n")

        #For measuring partitioning
        start_time2 = timeit.default_timer()
        # self.calc_exit_probabilities_multiple_agents(block)
        # self.calc_confirmation_confidence_multiple_agents(block)
        # self.measure_partitioning()

        if self.printing:
            print("Calculation time confirmation confidence: " + str(np.round(timeit.default_timer() - start_time2, 3)) + " seconds\n")
            # print("\nGraph information:\n" + nx.info(self.DG))
            
        return (voting_profile, virtual_vote, sign_sum_future_votes, z_vote)
            
    
    def tip_selection(self, block):
        
        #Get visible blocks and valid tips (and record these)
        self.get_visible_blocks(block.arrival_time, block.agent)
#        print('block arrival time', block.arrival_time)
#        print('block agent', block.agent)
#        print('visible blocks', self.get_visible_blocks)
        valid_tips = self.get_valid_tips_multiple_agents(block.agent)
        self.record_tips.append(valid_tips)
        
#        print('valid tips', valid_tips)
        #Reference all visible tips
        for tip in valid_tips:
            self.DG.add_edge(block, tip)    
        
#        else:
#            print("ERROR:  No tips available")
#            sys.exit()
    
    def CalcVotes(self, graph):
        """
        Returns a pairwise ordering of all blocks in the blockDAG
        
        Input: G - a blockDAG
        Output: a pairwise ordering of blocks in G
        
        x, y and z throughout this refer to blocks
        
        This code is an implementation of the pairwise voting algorithm in 
        the SPECTRE whitepaper titled 'Algorithm 1 - Calc votes'
        
        """
        ######################################################
        # SETUP
        ######################################################
        
        #Current voting profile
        self.voting_profile = []
               
        #Past voting profile for recursive calls
        self.past_voting_profile = [] 
        
        #List for created past(z) DAGs
        self.past_dags = []
        
        #Calculate number of blocks, for use later
        self.no_of_nodes = graph.number_of_nodes()
        
        print('input graph nodes', graph.nodes) # - Nodes not topologically sorted yet
        
        #If the blockDAG is empty, return an empty ordering
        if graph.number_of_nodes() == 0:
            self.voting_profile.clear()
        """
        #Recursive call of CalcVotes
        for z in graph:
            
            #Check that the correct past(z) DAGs are being called
            print('node', z.id, self.past(z).nodes) 
            self.past_dags.append(self.past(z).nodes)
            
            #Perform the recursion
            vote = self.CalcVotes(self.past(z))
            vote_copy = copy.copy(vote)
            
            #Record the past voting profile
            self.past_voting_profile.append(vote_copy)
            
            print('vote', z.id, vote) 
        """

            
        ######################################################################
        # RUN VOTING ALGORITHM
        ######################################################################
                    
        #Perform a topological sort of the blockDAG
        self.topo_sort = list(nx.topological_sort(graph))
#        print('type topo sort', type(self.topo_sort[0]))
#        print('topo sort', self.topo_sort)
        
        """
        BEWARE: The order of the graph has now been flipped. Previously it went
        z = 0 to z = 6. Now, due to the topological sort, it goes z = 6 to z = 0
        """        
        #Iterate through each block in the topo_sort
        for z in self.topo_sort:

            #This will be overwritten at each z
            self.z_vote = np.zeros((self.no_of_nodes, self.no_of_nodes))
            
            #For each block, look at every other pair of blocks (x, y)
            for x in graph:
                for y in graph:
                    
                    #If the blocks are not the same
                    if x != y:
                        
                        #past(z) - descendants of z (needed multiple times)
                        past_z = nx.descendants(graph, z)
#                        print('z=', z.id, past_z)
                        
                        # Implement the rules of the pairwise vote algorithm #
                        
                        #Line 7 of algo
                        if ((x in past_z) and (y not in past_z)) or \
                        ((x in past_z) and (y == z)):
                            self.z_vote[x.id, y.id] = int(-1) #Using the block number to determine the position of the vote in the profile
                        
                        #Line 9 of algo
                        elif ((y in past_z) and (x not in past_z)) or \
                        ((y in past_z) and (x == z)):
                            self.z_vote[x.id, y.id] = int(1)
                        
                        #Line 11 of algo
#                        elif ((x in past_z) and (y in past_z)):
#                            self.z_vote[x.id, y.id] = self.past_voting_profile[z.id][x.id, y.id]#need to work out what to do
                        
                        
                        #Line 13 of algo
                        elif ((x not in past_z) and (y not in past_z)):
                            
                            #Overall for loop is iterating from leaves to root - so future z 
                            #correspond to all the z's for which votes were previously calculated 
                            #and stored in self.z_vote 
#                            if z.id != self.no_of_blocks:
#                                print('z_vote', self.z_vote)
#                                print('voting profile', self.voting_profile)
#                                print('sum', sum(self.voting_profile[z.id:]))
    #                            print('sum_sign', sum_sign_future_z
                                
                                #Find the index position of z.id in the topological sort
                                position = self.get_position(self.topo_sort, z.id)
                                
                                if graph.in_degree(z) != 0: #Remove the tips - these have not future and so no voting profile
#                                    print('z.id=', z.id, 'topo_sort=', self.topo_sort, 'position=', position)
                                        
                                
                                    future_votes = self.voting_profile[:position]
#                                    print('future votes=', future_votes)
                                    sum_future_votes = sum(future_votes)
    #                                print('sum future votes', sum_future_votes)
                                    sign_sum_future_votes = np.sign(sum_future_votes)
                                
    
#                                print('x=', x.id, 'y=', y.id, 'z = ', z.id, 'result', sign_sum_future_votes)
                                    self.z_vote[x.id, y.id] = sign_sum_future_votes[x.id, y.id]
                            
                                """
                                if len(sign_sum_future_votes) != 0: #Remove the cases where it equals 0
                                    print(type(sign_sum_future_votes))
                                    self.z_vote[x.id, y.id] = sign_sum_future_votes[x.id, y.id]
                                """
#                            print('np.sign(sign_sum_future_votes', type(np.sign(sum_future_votes)))
                            
                            #Make independent copies - see if that fixes things
     
#                            print('z = ', z.id, 'x =', x.id, 'y=', y.id, 'future votes', sign_sum_future_votes)
#                            print('type for sign_sum_future_votes', type(sign_sum_future_votes))
#                            print(type(x.id))
#                            print(sign_sum_future_votes)
#                            print(type(sign_sum_future_votes[x.id, y.id]))
#                            print('z_vote', self.z_vote)
                            
                            
                            
#                            sum_sign_future_z = list(np.sign(sum(self.voting_profile[z.id:])))
#                            print(type(sum_sign_future_z))
#                                print('sum_sign_future_z', sum_sign_future_z)
#                            self.z_vote[x.id, y.id] = sum_sign_future_z
                            
                        
#                        print('voting profile', self.z_vote)
                            #something (y == z):
            
            # Store the voting profile for that particular z
            z_vote_copy = copy.copy(self.z_vote)
            self.voting_profile.append(z_vote_copy)
            
        #Create the aggregated vote of the entire blockDAG
        self.aggregate_vote = sum(self.voting_profile)
        self.virtual_vote = np.sign(self.aggregate_vote)
#        print(self.voting_profile)
        return (self.voting_profile, self.virtual_vote, sign_sum_future_votes, self.z_vote)
                        
    def past(self, z):
        """
        This returns a blockDAG that is the past of z - past(z). It is used in 
        the CalcVotes method
        """
        #Indexing for the appropriate z. If z = 5 is inputted, then past(z) should
        #be returning the DAG that contains 4 nodes (i.e. the DAG for z = 4)
#        if z.id >= 1: #Accounting for the fact the genesis does not have a past
        #To index through the DAG list, z needs to be an integer
        if z.id == 0:
            past_z_dag = nx.DiGraph()
            
        if z.id > 0:
            past_z_dag = self.DG_store[z.id-1]
              
        return past_z_dag     

    def get_position(self, topo_sort, index):  
        counter = -1 #counter is used to store the index of the desired node in the 
                    #topological sort. Start at -1, so that when we add one to the counter
                    #it correctly labels the first entry in the topo sort as being 
                    #position zero
        
        for node in topo_sort:
            counter += 1
            if node.id == index:
                return counter

    def check_parameters_changes(self, block, dic):

        temp = (int(str(block)))

        #If change event for a block is provided
        if temp in dic:
            #If change of distance is provided
            if dic[temp][0] != False:
                self.distances = dic[temp][0]
            #If change of agent probabilities is provided
            if dic[temp][1] != False:
                self.agent_choice = dic[temp][1]

            print_tips_over_time_multiple_agents(self, int(str(block)))
            # self.calc_exit_probabilities_multiple_agents(block)
            # self.calc_confirmation_confidence_multiple_agents(block)
            # self.measure_partitioning()
            
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
#        print('incoming block time', incoming_block_time)
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
#                    print('distance from agent to agent of block', distance)

                    #Determine if the block is visible (incoming_block.arrival_time determines current time)
                    if (block.arrival_time + self.latency + distance <= incoming_block_time):

                        agent.visible_blocks.append(block)
#                        print('visible blocks for the agent', agent.visible_blocks)

                    #Record not visible blocks for 'current agent' only (reduces overhead)
                    elif(incoming_block_agent == agent):
                        self.not_visible_blocks.append(block)
#                        print('not visible blocks', self.not_visible_blocks)


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
