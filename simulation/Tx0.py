import numpy as np
import random

from test_dag import build_test_dag



#def Tx0(graph, sub_graph, voting_profile):
"""
Returns a set of accepted transactions, from an input 
blockDAG and pairwise voting profile
"""
    
    #Setup a list to store the accepted set of transactions
#    Tx = []
    
    #Iterate through nodes in the subgraph
#    for block in sub_graph:
#        for tx in block.transactions:
#            for tx_2 in graph.intersection(conflict(graph, tx)):
                
                
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
    
trial = build_test_dag()

result = conflict(trial, 4)
print('result', result)

#Print out all the transactions
for block in trial:
    print(block.transactions)

            
