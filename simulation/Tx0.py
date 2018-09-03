import numpy as np
import random
import networkx as nx
import copy

from test_dag import build_test_dag



def Tx0(graph, voting_profile):
    """
    Returns a set of accepted transactions, from an input 
    blockDAG and pairwise voting profile
    
    For the time being, using graph as the sub-graph
    """
    
    #Setup a list to store the accepted set of transactions
    Tx = []
        
    #Iterate through nodes in the subgraph
    for block_1 in graph:
        
        for tx in block_1.transactions:
            #Identify the conflicting transactions and blocks they are contained in
            conflict_dict = conflict(graph, tx)
            
            for tx_2 in graph.intersection(conflict_dict):
                
                for block_2 in ({list(conflict_dict.keys())}).intersection(anticone(block_1, graph)): 
                    
                    if voting_profile[block_1.id, block_2.id] >= 0:
                        break
                    
                break
            
            break
             
def anticone(block, graph):
    """
    Returns the anticone (the set of blocks that 
    the DAG does not directly orders with respect to z) of an input block
    
    First calculates the cone, and then the anti-cone. For the built in 
    Python set operators to work, all objects acted on need to be of type set
    """
    
    #Turn block into a set
    block_set = {block}
    
    #Find past of z
    """
    Have to iterate through the ancestors and append invididually to a list. This
    is because you can't convert nx.ancestors directly to a set, because it is
    not a hashable object and sets only allow hashable objects. 
    """
    past_list = []
    
    past = nx.ancestors(graph, block)
    
    for i in past:
        past_list.append(i)
    past_list = set(past_list)
#    print(past_list)
    
    #Find future of z
    future_list = []
    
    future = nx.descendants(graph, block)
    
    for j in future:
        future_list.append(j)
    future_list = set(future_list)
#    print(future_list)
    
    #Cone
    cone = block_set.union(past, future)
    
    #Convert the blockDAG to a set
    graph_set = []
    
    for k in graph:
        graph_set.append(k)
    graph_set = set(graph_set)
    
    #Anticone - difference between the blockDAG and the cone
    anticone_output = graph_set.difference(cone)
    
    return anticone_output
    
    
                
def conflict(graph, tx):
    """
    Returns a set of transactions that conflict with the 
    input transaction tx. 
    
    Outputs a dictionary that maps the conflicting block id to the conflicting 
    transaction - giving a record of both conflicting blocks and transactions
    """
    
    #Store the conflicting transactions
    conflicts = {}
    
    for block in graph:
        for transaction in block.transactions:
            if transaction == tx:
                conflicts[block.id] = transaction
    
    return conflicts

##############################################################################
# RUN
##############################################################################

# Setup
    
#Load voting profile
voting_profile = np.load('C:/Users/thoma/Documents/GitHub/iota_simulation/voting_profile_of_test.npy')    

#Build test DAG
trial = build_test_dag()

# Determine accepted transactions
accept_transact = Tx0(trial, voting_profile)

#result = conflict(trial, 4)
#print('result', result)

#Print out all the transactions
#for block in trial:
#    print(block.transactions)

#test = []
#Test anticone
#for block in trial:
#    test.append(anticone(block, trial))
#    print('block', block.id, 'anticone', anticone(block, trial))

            
