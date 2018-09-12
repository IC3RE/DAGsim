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
from simulation.Tx0_helpers import anticone_test, check_inputs, useful_attributes, tx_inputs, anticone, conflict



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
            #Create list to store the results of the 3 acceptance tests
            self.test_results = []
        
            #Setup a list to store the accepted set of transactions
            self.Tx = []
        
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
        Initialises the agents, blocks, arrival times
        """

        #Create agents
        agent_counter = 0
        for agent in range(self.no_of_agents):
            self.agents.append(Agent(agent_counter))
            agent_counter += 1

        #Create directed graph object
        self.DG = nx.DiGraph()

        #Create list to store sequentially created graph objects
#        self.DG_store = []
        
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
            
#            DG_copy = self.DG.copy()
#            self.DG_store.append(DG_copy) 
                        
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
        
        #Generate the accepted set of transactions.  pairwise vote, taking the blockDAG as an input
#        print(type(self.DG))
#        nx.draw(self.DG, with_labels=True)
#        vote = self.CalcVotes(self.DG)
        
        #Transaction acceptance result storage
        
        """
        These need to go here rather than in setup because, when I artificially
        create and put a blockDAG in I don't call the setup method. So the storage
        needs to be created here
        """
        
        (accept_tx, all_tx) = self.Tx0(self.DG, self.DG)
        
        
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
            
        return (accept_tx, all_tx)
                       
    def Tx0(self, graph, subgraph):
        """
        Returns a set of accepted transactions, from an input 
        blockDAG and pairwise voting profile. This function operates recursively
        and is initially called with the full blockDAG.
        
        How it works:
            The transactions acceptance algorithm requires a given transaction 
            to pass 3 tests in order to be verified as an accepted transaction.
            This function prepares the ground for these tests and then 
            implements them.
            
            Test 1 and 2 are contained in the same function (due to the way that
            the algorithm is designed), whilst test 3 is in a seperate function. 
            
            Each test outputs a boolean - 'True' or 'False'. 
            
            True refers to the transaction having passed the test, False refers
            to the transaction having failed the test.
            
            A transaction is accepted if all three tests return 'True' responses. 
            Each response is stored in a list, and the list of responses checked
            after all the tests for the transaction have been run.
            
            The list is emptied for each new transaction being tested.
        """
        #First generate the pairwise vote over all blocks
        voting_profile = self.CalcVotes(graph)
        
        #Execute the accepted transactions (consensus) protocol
#        self.Tx = []

        
        #Extract useful attributes of the input graph, for use later
        graph_set, all_transactions = useful_attributes(subgraph)
        print('All transactions in the blockDAG', all_transactions)
    #    print('all_transactions', all_transactions)
        
        counter = 0 #Used to determine where in the loops the code is up to
        
        #Iterate through blocks in the DAG
        for block_1 in subgraph:
#            print('')
#            print('block', block_1.id)
            
    #        print('counter', counter)
            
            for tx in block_1.transactions:
                self.test_results = []
#                print('')
#                print('transaction', tx)
                
                #Insert acceptance test functions here
                
                #Test_1 and Test 2 (contains lines 5 - 10 of algorithm 2)
                test_1, test_2 = anticone_test(self, graph, tx, block_1, voting_profile)
#                print(test_1)
                self.test_results.append(test_1) 
                self.test_results.append(test_2)
                print('finished test 1, result is', test_1, 'finished test 2, result is', test_2)
                
                
                #Test_3
                test_3 = check_inputs(self, graph, tx, block_1, voting_profile)
                self.test_results.append(test_3)
                print('finished test 3 and the result is', test_3)

                
#                print('tx', tx)
    
                
                #counter allows me to track where everything is up to
                counter += 1
                    
                """
                Need to correctly implement the recursion, insert and modify the 
                past(block) function below and sort out the input arguments generally
                for the Tx0 function
                
                
                for tx_2 in Tx0(graph, past(block_1)) != 0:
    
                    
                for tx_3 in tx_inputs(graph, block_1):
                    if (set(tx_3).intersection(Tx0(graph, past(block_1)))) = 0:
    
                """
                print('test results', self.test_results)
                #Add the transaction to the accepted set of transactions if it passes 
                #all 3 tests
                if all(item == True for item in self.test_results):
                    self.Tx.append(tx)
            print('accepted set', self.Tx)
        
        return (self.Tx, all_transactions)
    
    
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
        
#        print('input graph nodes', graph.nodes) # - Nodes not topologically sorted yet
        
        #If the blockDAG is empty, return an empty ordering
        if graph.number_of_nodes() == 0:
            self.voting_profile.clear()
        
        ######################################################################
        # RUN VOTING ALGORITHM
        ######################################################################
                    
        #Perform a topological sort of the blockDAG
        self.topo_sort = list(nx.topological_sort(graph))
        
        """
#        BEWARE: The order of the graph has now been flipped. Previously it went
#        z = 0 to z = 6. Now, due to the topological sort, it goes z = 6 to z = 0
        """      
        
        ############################## Recursion ##############################
        #Recursive call of CalcVotes
#        for z in self.topo_sort:
            
#        self.past_dag = graph.subgraph(nx.descendants(graph, z))
#            print('z', z.id, 'past dag nodes', self.past_dag.nodes())
#            plt.figure()
#            plt.title(z.id)
#            nx.draw(past_dag, with_labels=True)
            
#           Perform the recursion
#            recurs_vote = self.CalcVotes(self.past_dag)
#            recurs_vote_copy = copy.copy(recurs_vote)
            
            #Record the past voting profile
#            self.past_voting_profile.append(recurs_vote_copy)
            
#            print('vote', z.id, vote) 
        
        ############### Main section of the pairwise vote #####################
        #Iterate through each block in the topo_sort
        for z in self.topo_sort:
#            if z.id == 1:

            #This will be overwritten at each z
            self.z_vote = np.zeros((self.no_of_nodes, self.no_of_nodes))
            
            #Storage for relevant future votes
            self.future_votes = []
            
            #Creat storage for position indices
            self.position = []
#            print('z',z, 'block ancestors', self.block_ancestors)
            
            #For each block, look at every other pair of blocks (x, y)
            for x in graph:
                for y in graph:
                    
                    #If the blocks are not the same
                    if x != y:
                        
                        #past(z) - descendants of z (needed multiple times)
                        past_z = nx.descendants(graph, z)
#                            print('z', z, 'past z', past_z)
                        future_z = nx.ancestors(graph, z)
#                            print('z', z, 'future z', future_z)                        
                        # Implement the rules of the pairwise vote algorithm #
                        
                        #Line 7 of algo
                        if ((x in future_z) and (y not in past_z)) or \
                        ((x in past_z) and (y == z)):
                            self.z_vote[x.id, y.id] = int(-1) #Using the block number to determine the position of the vote in the profile
#                            print('z', z, 'x', x, 'y', y, 'vote', self.z_vote[x.id, y.id])
                        
                        #Line 9 of algo
                        elif ((y in future_z) and (x not in past_z)) or \
                        ((y in past_z) and (x == z)):
                            self.z_vote[x.id, y.id] = int(1)
#                            print('z', z, 'x', x, 'y', y, 'vote', self.z_vote[x.id, y.id])

                        
                        #Line 11 of algo
#                        elif ((x in past_z) and (y in past_z)):
#                            self.z_vote[x.id, y.id] = self.past_voting_profile[z.id][x.id, y.id]#need to work out what to do
                        
                        
                        #Line 13 of algo
                        elif ((x not in past_z) and (y not in past_z)):
                            
                            #Overall for loop is iterating from leaves to root - so future z 
                            #correspond to all the z's for which votes were previously calculated 
                            #and stored in self.z_vote 

                            if graph.in_degree(z) != 0: #Remove the tips - these have no ancestors (no future) and so no associated voting profile
                                        
                                #Iterate through each of z's ancestors
                                for ancestor in nx.ancestors(graph, z):
                                    
                                    #Get the index position of each ancestor's vote (determined by the 
                                    #position of the ancestor in the topological sort)
                                    position = self.get_position(self.topo_sort, ancestor.id)  
#                                    print('topo sort', self.topo_sort, 'ancestor id', ancestor.id)
                                    
                                    #Append to a list, for storage
                                    self.future_votes.append(self.voting_profile[position])
    #                                    print('future votes', self.future_votes)
                            
                                #Add up all these votes
                                self.sum_future_votes = sum(self.future_votes)
                                
                                #Determine the sign of each vote
                                self.sign_sum_future_votes = np.sign(self.sum_future_votes)
                                
                                #Input the vote required for this particular x, y combination
                                self.z_vote[x.id, y.id] = self.sign_sum_future_votes[x.id, y.id]
                        
                        
 
            # Store the voting profile for that particular z
            z_vote_copy = copy.copy(self.z_vote)
            self.voting_profile.append(z_vote_copy)
                
        #Create the aggregated vote of the entire blockDAG
        self.aggregate_vote = sum(self.voting_profile) #Sum the votes of all z for each x,y
        
        #Take the sign of each aggregated vote - this is the pairwise vote
        self.virtual_vote = np.sign(self.aggregate_vote)

        return self.virtual_vote


    #############################################################################
    # SIMULATION: HELPERS
    #############################################################################
     
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
                 
    def get_position(self, topo_sort, index):  
        counter = -1 #counter is used to store the index of the desired node in the 
                    #topological sort. Start at -1, so that when we add one to the counter
                    #it correctly labels the first entry in the topo sort as being 
                    #position zero
        
        for block in topo_sort:
            counter += 1
            if block.id == index:
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
