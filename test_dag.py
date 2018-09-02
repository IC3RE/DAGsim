"""
This script deterministically builds a blockDAG. The CalcVotes method is then 
called from simulation_spectre_multi_agent.py and the result outputted.

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


from simulation.plotting_spectre import print_info, print_graph, print_tips_over_time, print_tips_over_time_multiple_agents
from simulation.agent import Agent
from simulation.block import Block

def build_test_dag():
    """
    Builds the DAG according to the SPECTRE paper
    """
    ########################### SETUP ######################################
    #Define the graph structure
    test_graph = nx.DiGraph()
    
    #Setup list for blocks
    blocks = []
    
    #Define the number of nodes
    number_of_blocks = 11

    #Create random arrival times
    arrival_times = np.arange(0, number_of_blocks+1)
    
    #Define y position of the node (building a chain that seperates into 2)
    y_position = []
    
    for i in range(number_of_blocks+1):
        if i <= 4:
            y_position.append(0)
            
        elif i > 4 and i <= 8:
            y_position.append(1)
            
        elif i > 8:
            y_position.append(0) 

    #Create other block objects and store in list
    #This is creating a list of block objects, with as many objects as there are 
    #arrival times
    
    block_counter = 0
    
    for i in range(len(arrival_times)):
        blocks.append(Block(arrival_times[i], block_counter))
        block_counter += 1
        
    counter = 0
    #Add the graph nodes
    for block in blocks:
#        print(node)
#        print(counter)
        test_graph.add_node(block, pos = (block.arrival_time, y_position[counter]), no=counter, node_color='#99ffff')
#        print('x', block.arrival_time, 'y', y_position[counter], 'counter', counter)
#        print(type(block))
        counter += 1
        
    #Add the edges in
    test_graph.add_edges_from([(blocks[1], blocks[0]), (blocks[2], blocks[1]), (blocks[3], blocks[2]), \
                               (blocks[4], blocks[3]), (blocks[5], blocks[4]), \
                               (blocks[6], blocks[5]), (blocks[7], blocks[6]), (blocks[8], blocks[7]), \
                               (blocks[9], blocks[4]), (blocks[10], blocks[9]), (blocks[11], blocks[10])])
    
    #Visualise the graph
    nx.draw(test_graph, with_labels=True)
    plt.show()
    
    return(test_graph)
    """
    #Define the number of nodes
    number_of_blocks = 11
    
    #Define x position of the node (time)
    x_position = np.arange(0, number_of_blocks+1)
    
    #Define number of blocks
    blocks = []
    
    #Define y position of the node (building a chain that seperates into 2)
    y_position = []
    
    for i in range(number_of_blocks+1):
        if i <= 4:
            y_position.append(0)
            
        elif i > 4 and i <= 8:
            y_position.append(1)
            
        elif i > 8:
            y_position.append(0)      

#    print('y-position', y_position)
        #Create other block objects and store in list
        #This is creating a list of block objects, with as many objects as there are 
        #arrival times
        
    block_counter = 0
    
    for i in range(number_of_blocks+1):
        blocks.append(Block(x_position[i], block_counter))
        
        block_counter += 1
        
    ############################# BUILD DAG ###################################
    print('blocks', blocks)
    print('x list', x_position)
    print('y list', y_position, 'length', len(y_position))
    counter = 0
    #Add the graph nodes
    for block in blocks:
#        print(node)
#        print(counter)
        test_graph.add_node(block, pos = (x_position[counter], y_position[counter]))
        print('x', x_position[counter], 'y', y_position[counter], 'counter', counter)
        counter += 1
        
     

    

    """
    
#result = build_test_dag()

    #print_graph(dag)
        
    
    