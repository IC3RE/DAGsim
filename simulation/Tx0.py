import numpy as np
import random
import networkx as nx
import copy

from test_dag import build_test_dag



def Tx0(graph, subgraph, voting_profile):
    """
    Returns a set of accepted transactions, from an input 
    blockDAG and pairwise voting profile
    
    For the time being, using graph as the sub-graph
    """
    
    #Setup a list to store the accepted set of transactions
    Tx = []
    
    #Graph as a set
    graph_set, all_transactions = useful_attributes(graph)
    
    counter = 0
    #Iterate through nodes in the subgraph
    for block_1 in subgraph:
        print('counter', counter)
        for tx in block_1.transactions:
#            print(tx)
            #Identify transactions that conflict with tx and the blocks they are contained in
            conflict_dict = conflict(graph, tx)
#            print('block', block_1, 'tx', tx, 'conflicting transaction', list(conflict_dict.values()))
#            print(graph_set.intersection(list(conflict_dict.values())))
            
            for tx_2 in list(conflict_dict.values()):
#                print(tx_2)
#                print('reached line 36')
                
                #Identify the blocks and transactions that conflict with tx2
                conflict_dict_2 = conflict(graph, tx_2)                
                
                #Convert the conflicting blocks to a set
                block_conflict_tx2 = set(list(conflict_dict_2.keys()))
                
                #Determine the anticone of block_1
                anticone_block_1 = anticone(block_1, graph) 
                
                #Calculate the intersection of conflicting blocks and anticone of block_1
                intersection = block_conflict_tx2.intersection(anticone_block_1)
                
#                print('blocks conflicting with tx_2', block_conflict_tx2)
#                print('anticone of block 1', anticone_block_1)
#                print('intersection', intersection)
                
                for block_2 in intersection: 
#                    print('reached line 42')
                    if voting_profile[block_1.id, block_2.id] >= 0:
#                        print('reached line 44')
                        break
                    
                break
            counter += 1
                
            """
            Need to correctly implement the recursion, insert and modify the 
            past(block) function below and sort out the input arguments generally
            for the Tx0 function
            
            
            for tx_2 in Tx0(graph, past(block_1)) != 0:
                break
            break
                
            for tx_3 in tx_inputs(graph, block_1):
                if (set(tx_3).intersection(Tx0(graph, past(block_1)))) = 0:
                    break
                break
            """
            #Add the transaction to the accepted set of transactions
            Tx.append(tx)
    
    return Tx
            
##############################################################################
# HELPER FUNCTIONS
##############################################################################
        
def useful_attributes(graph):
    """
    General purpose function that takes an input graph and returns useful attributes 
    of the graph, including: 
        - the graph nodes as a set
        - a list of all the transactions in the graph
    """
    
    #Store the graph nodes
    graph_list = []
    
    #Store the transactions in the graph
    all_tx = []
    
    #Iterate through the graph and append useful attributes to relevant lists
    for block in graph:
        graph_list.append(block)
        all_tx.append(block.transactions)
        
    #Flatten the transactions list
    all_tx_flatten = [item for sublist in all_tx for item in sublist]
#    print('original', all_tx)
#    print('flattened', all_tx_flatten)
        
    #Convert to sets
    graph_set = set(graph_list)
#    print('all transactions', all_tx)
    all_tx_set = set(all_tx_flatten)
    
    return (graph_set, all_tx_set)

"""
def past(self, z):
    
#    Returns the past blockDAG of z - past(z)     
    #Indexing for the appropriate z. If z = 5 is inputted, then past(z) should
    #be returning the DAG that contains 4 nodes (i.e. the DAG for z = 4)
#        if z.id >= 1: #Accounting for the fact the genesis does not have a past
    #To index through the DAG list, z needs to be an integer
    if z.id == 0:
        past_z_dag = nx.DiGraph()
        
    if z.id > 0:
        past_z_dag = self.DG_store[z.id-1]
          
    return past_z_dag 
"""

def tx_inputs(graph, block):
    """
    Returns all the input transactions to a block in the graph. This is a 
    work in progress - really it should be calculating the inputs to a particular
    transaction in a given block. For the time being, assuming that the inputs to a 
    particular transaction are all the transactions in the input blocks
    """
    #List to store input transactions
    transactions = []
    
    #Inputs to a block; in the directed blockDAG architecture are the immediate
    #descendants of the block
    successor_blocks = list(graph.successors(block))
    
    #Append the transactions of each successor block
    for block in successor_blocks:
        transactions.append(block.transactions)    
    
    #Flatten the resulting list of lists
#    successors_flatten = [item for sublist in successor_blocks for item in sublist]

    
    return transactions
    
    
             
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
                conflicts[block] = transaction
    
    return conflicts

##############################################################################
# RUN
##############################################################################

# Setup
    
#Load voting profile
voting_profile = np.load('C:/Users/thoma/Documents/GitHub/iota_simulation/voting_profile_of_test.npy')    

#Build test DAG
trial = build_test_dag()

#Input transactions

test_list = []
for block in trial:
    test_list.append(tx_inputs(trial, block))
    

# Determine accepted transactions
#accept_transact = Tx0(trial, voting_profile)

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

            
