import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy


def vote_execute(self, graph, z):
    """
    Executes lines 5 - 16 in the pairwise voting algorithm. Doesn't include a for 
    loop because the function is called within a for loop
    """
    
    ############### Main section of the pairwise vote #####################
    #Iterate through each block in the topo_sort
    
#        print('above the main loop')
#        print('topological sort', self.topo_sort)
    
#    print('entered main loop and block ID is', z.id)

    #This will be overwritten at each z
    self.z_vote = np.zeros((self.no_of_nodes, self.no_of_nodes))
    
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
                    print('z', z, 'x', x, 'y', y, 'vote', self.z_vote[x.id, y.id])
                
                #Line 9 of algo
                elif ((y in future_z) and (x not in past_z)) or \
                ((y in past_z) and (x == z)):
                    self.z_vote[x.id, y.id] = int(1)
                    print('z', z, 'x', x, 'y', y, 'vote', self.z_vote[x.id, y.id])

                
                #Line 11 of algo
#                        elif ((x in past_z) and (y in past_z)):
#                            self.z_vote[x.id, y.id] = self.past_voting_profile[z.id][x.id, y.id]#need to work out what to do
                
                """
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
                """
                
 
    # Store the voting profile for that particular z
    z_vote_copy = copy.copy(self.z_vote)
    self.voting_profile.append(z_vote_copy)
            
    #Create the aggregated vote of the entire blockDAG
    self.aggregate_vote = sum(self.voting_profile) #Sum the votes of all z for each x,y
    
    #Take the sign of each aggregated vote - this is the pairwise vote
    self.virtual_vote = np.sign(self.aggregate_vote)
    
#    print('at end of method')
    return self.virtual_vote
