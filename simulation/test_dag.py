"""
This script deterministically builds a blockDAG

The blockDAG generated in the SPECTRE paper - figure 1, page 7 - is built as the 
test object.

Following this, the result can be used to manually determine if the correct 
voting profile is being returned.
"""
import sys
import timeit
import random
import math
import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


#from simulation.plotting_spectre import print_info, print_graph, print_tips_over_time, print_tips_over_time_multiple_agents
from simulation.agent import Agent
from simulation.block import Block

def build_test_dag(complexity):
    """
    Deterministically builds a testDAG
    
    Takes as input a complexity parameter. Has to be a string and can be 
    two options:
        - 'simple' 
        - 'complex'
    
    'simple' builds and outputs a 4 block graph
    'complex' builds and outputs a more complex 11 block graph
    """
    ########################### SETUP ######################################
    #Check that the input is one of the possible options
    if (complexity != 'simple') and (complexity != 'complex') and (complexity != 'chain'):
        raise ValueError('Input value must either be: simple or: complex in string format')
    
    if complexity == 'chain':
        number_of_blocks = 4
        
        #Define the graph structure
        test_graph = nx.DiGraph()
        
        #Setup list for blocks
        blocks = []
        
        #Create random arrival times (x position)
        arrival_times = np.arange(0, number_of_blocks)
        
        #Deterministically create the set of input transactions
        transactions = [[1, 2], [3, 2], [5, 1], [7, 9]]
        
        #Define y position of the node (building a chain that seperates into 2)
        y_position = []
        
        ##########################################################################
        # BUILD DAG
        ##########################################################################
        #Note: the following behaviour diverges, depending on whether a complex 
        #or simple DAG is required
                    
        #Construct the y position of the blocks - seperating a single chain
        #into 2 chains part way down
        for i in range(number_of_blocks+1):
            if i <= 1:
                y_position.append(0)
                
            elif i == 2:
                y_position.append(0)
                
            elif i == 3:
                y_position.append(0) 
    
     
#        print('y position', y_position)
        block_counter = 0
        
        #Create list of blocks, with their arrival times and counters as IDs
        for i in range(len(arrival_times)):
            blocks.append(Block(arrival_times[i], block_counter, transactions[i]))
            block_counter += 1
#        print('blocks', blocks)
            
        counter = 0
        
        #Add the blocks to a graph
        for block in blocks:
            test_graph.add_node(block, pos = (block.arrival_time, y_position[counter]), no=counter, node_color='#99ffff')
            counter += 1
            
        #Add the edges between the blocks on the graph
        test_graph.add_edges_from([(blocks[1], blocks[0]), (blocks[2], blocks[1]), (blocks[3], blocks[2])])
    
    
    
    #Build different DAGs depending on whether the input requests a simple or complex one
    
    if complexity == 'simple':
        number_of_blocks = 4
        
        #Define the graph structure
        test_graph = nx.DiGraph()
        
        #Setup list for blocks
        blocks = []
        
        #Deterministically chosen set of transactions
        transactions = [[1, 2], [3, 2], [2, 1], [7, 2]]

        
        #Create random arrival times (x position)
        arrival_times = np.arange(0, number_of_blocks)
        
        #Define y position of the node (building a chain that seperates into 2)
        y_position = []
        
        ##########################################################################
        # BUILD DAG
        ##########################################################################
        #Note: the following behaviour diverges, depending on whether a complex 
        #or simple DAG is required
                    
        #Construct the y position of the blocks - seperating a single chain
        #into 2 chains part way down
        for i in range(number_of_blocks+1):
            if i <= 1:
                y_position.append(0)
                
            elif i == 2:
                y_position.append(0)
                
            elif i == 3:
                y_position.append(1) 
    
     
#        print('y position', y_position)
        block_counter = 0
        
        #Create list of blocks, with their arrival times and counters as IDs
        for i in range(len(arrival_times)):
            blocks.append(Block(arrival_times[i], block_counter, transactions[i]))
            block_counter += 1
#        print('blocks', blocks)
            
        counter = 0
        
        #Add the blocks to a graph
        for block in blocks:
            test_graph.add_node(block, pos = (block.arrival_time, y_position[counter]), no=counter, node_color='#99ffff')
            counter += 1
            
        #Add the edges between the blocks on the graph
        test_graph.add_edges_from([(blocks[1], blocks[0]), (blocks[2], blocks[1]), (blocks[3], blocks[1])])
    
    #Build the graph in the complex case
    elif complexity == 'complex':
        number_of_blocks = 11
        
        #Define the graph structure
        test_graph = nx.DiGraph()
        
        #Setup list for blocks
        blocks = []
        
        #Create random arrival times (x position)
        arrival_times = np.arange(0, number_of_blocks)
        
        #Define y position of the node (building a chain that seperates into 2)
        y_position = []
        
        ##########################################################################
        # BUILD DAG
        ##########################################################################
        #Note: the following behaviour diverges, depending on whether a complex 
        #or simple DAG is required
                    
        #Construct the y position of the blocks - seperating a single chain
        #into 2 chains part way down
        for i in range(number_of_blocks+1):
            if i <= 4:
                y_position.append(0)
                
            elif i > 4 and i <= 8:
                y_position.append(1)
                
            elif i > 8:
                y_position.append(0) 
    
     
        
        block_counter = 0
        
        #Create list of blocks, with their arrival times and counters as IDs
        for i in range(len(arrival_times)):
            blocks.append(Block(arrival_times[i], block_counter))
            block_counter += 1
            
        counter = 0
        
        #Add the blocks to a graph
        for block in blocks:
            test_graph.add_node(block, pos = (block.arrival_time, y_position[counter]), no=counter, node_color='#99ffff')
            counter += 1
            
        #Add the edges between the blocks on the graph
        test_graph.add_edges_from([(blocks[1], blocks[0]), (blocks[2], blocks[1]), (blocks[3], blocks[2]), \
                                   (blocks[4], blocks[3]), (blocks[5], blocks[4]), \
                                   (blocks[6], blocks[5]), (blocks[7], blocks[6]), (blocks[8], blocks[7]), \
                                   (blocks[9], blocks[4]), (blocks[10], blocks[9])])
        
   
    
    #Visualise the graph
    nx.draw(test_graph, with_labels=True)
    plt.show()
    
    return(test_graph)
        
    
    