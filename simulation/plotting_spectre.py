import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


#############################################################################
# PRINTING AND PLOTTING
#############################################################################

def print_info(self):
    text = "\nParameters:  blocks = " + str(self.no_of_blocks) + \
             ",  Lambda = " + str(self.lam)
#",  Tip-Selection = " + str(self.tip_selection_algo).upper() + \
            
#    if(self.tip_selection_algo == "weighted"):
#        text += ",  Alpha = " + str(self.alpha)
    text += " | Simulation started...\n"
    print(text)

def print_graph(self):

    #Positioning and text of labels
    pos = nx.get_node_attributes(self.DG, 'pos')
    lower_pos = {key: (x, y - 0.07) for key, (x, y) in pos.items()} #For label offset (0.1)

    #Create labels with the confirmation confidence of every block (of the issueing agent)
    labels = {
        # block: str(str(np.round(block.exit_probability_multiple_agents[block.agent], 2)) + "  " +
        #                  str(np.round(block.confirmation_confidence_multiple_agents[block.agent], 2)))
        block : str(np.round(block.exit_probability_multiple_agents[block.agent],2))
        for block in self.DG.nodes if block.agent != None
    }
    #For genesis take agent 0 as default (always same value)
    labels[self.blocks[0]] = str(np.round(self.blocks[0].exit_probability_multiple_agents[self.agents[0]],2))

    #pos = graphviz_layout(self.DG, prog="dot", args="")
    #col = [['r','b'][int(np.round(block.confirmation_confidence,1))] for block in self.DG.nodes()] #Color change for 100% confidence

    #Coloring of nodes
    tips = self.get_tips()
    for tip in tips:
        # self.DG.node[tip]["node_color"] = '#ffdbb8'
        self.DG.node[tip]["node_color"] = self.agent_tip_colors[int(str(tip.agent))]

    # col = list(nx.get_node_attributes(self.DG, 'node_color').values()) #Didn't work on Linux
    col = []
    for block in self.DG:
        col.append(self.DG.node[block]["node_color"])

    #Creating figure
    plt.figure(figsize=(14, 8))
    nx.draw_networkx(self.DG, pos, with_labels=True, node_size = 100, font_size=5.5, node_color = col)
    # nx.draw_networkx_labels(self.DG, lower_pos, labels=labels, font_size=6)

    #Print title
    title = "blocks = " + str(self.no_of_blocks) +\
            ",  " + r'$\lambda$' + " = " + str(self.lam)
#    if(self.tip_selection_algo == "weighted"):
#        title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
    plt.xlabel("Time (s)")
    plt.yticks([])
    plt.title(title)
    plt.show()
    #Save the graph
    #plt.savefig('graph.png')

def print_tips_over_time(self):

    plt.figure(figsize=(14, 8))

    #Get no of tips per time
    no_tips = []
    for i in self.record_tips:
        no_tips.append(len(i))

    plt.plot(self.arrival_times, no_tips, label="Tips")

    #Cut off first 250 blocks for mean and best fit
    if(self.no_of_blocks >= 250):
        cut_off = 250
    else:
        cut_off = 0

    #Plot mean
    x_mean = [self.arrival_times[cut_off], self.arrival_times[-1]]
    y_mean = [np.mean(no_tips[cut_off:]), np.mean(no_tips[cut_off:])]
    plt.plot(x_mean, y_mean, label="Average Tips", linestyle='--')

    #Plot best fitted line
    plt.plot(np.unique(self.arrival_times[cut_off:]), \
    np.poly1d(np.polyfit(self.arrival_times[cut_off:], no_tips[cut_off:], 1))\
    (np.unique(self.arrival_times[cut_off:])), label="Best Fit Line", linestyle='--')

    #Print title
    title = "blocks = " + str(self.no_of_blocks) + \
            ",  " + r'$\lambda$' + " = " + str(self.lam)
#    if (self.tip_selection_algo == "weighted"):
#        title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
    plt.xlabel("Time (s)")
    plt.ylabel("Number of tips")
    plt.legend(loc='upper left')
    plt.title(title)
    plt.show()

def print_tips_over_time_multiple_agents(self, no_current_blocks):

    plt.figure(figsize=(14, 8))
    plt.subplot(2, 1, 1)

    #Get no of tips per time
    for agent in self.agents:
        no_tips = [0]
        for i in agent.record_tips:
            no_tips.append(len(i))
            label = "Tips agent " + str(agent)
        #plt.subplot(2, 1, int(str(agent))+1)
        plt.plot(self.arrival_times[:no_current_blocks], no_tips[:no_current_blocks], label=label)

        #Cut off first 60% of blocks
        if(no_current_blocks >= 500):
            cut_off = int(no_current_blocks * 0.6)
        else:
            cut_off = 0

        #Plot mean
        x_mean = [self.arrival_times[cut_off], self.arrival_times[no_current_blocks-1]]
        y_mean = [np.mean(no_tips[cut_off:no_current_blocks-1]), np.mean(no_tips[cut_off:no_current_blocks-1])]
        plt.plot(x_mean, y_mean, label="Average Tips", linestyle='--')

        #Plot best fitted line
        plt.plot(np.unique(self.arrival_times[cut_off:no_current_blocks-1]), \
        np.poly1d(np.polyfit(self.arrival_times[cut_off:no_current_blocks-1], no_tips[cut_off:no_current_blocks-1], 1))\
        (np.unique(self.arrival_times[cut_off:no_current_blocks-1])), label="Best Fit Line", linestyle='--')

    # no_tips = []
    # for i in self.record_tips:
    #     no_tips.append(len(i))
    #
    # plt.plot(self.arrival_times[:no_current_blocks-1], no_tips, label="Tips issueing agent")

    #Print title
    title = "blocks = " + str(self.no_of_blocks) + \
            ",  " + r'$\lambda$' + " = " + str(self.lam)
#    if (self.tip_selection_algo == "weighted"):
#        title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
    plt.xlabel("Time (s)")
    plt.ylabel("Number of tips")
    plt.legend(loc='upper left')
    plt.title(title)


    plt.subplot(2, 1, 2)

    #Positioning and text of labels
    pos = nx.get_node_attributes(self.DG, 'pos')
    lower_pos = {key: (x, y - 0.1) for key, (x, y) in pos.items()} #For label offset (0.1)

    #Create labels with the confirmation confidence of every block (of the issueing agent)
    labels = {
        block: str(str(np.round(block.exit_probability_multiple_agents[block.agent], 2)) + "  " +
                         str(np.round(block.confirmation_confidence_multiple_agents[block.agent], 2)))
        for block in self.DG.nodes if block.agent != None
    }
    #For genesis take agent 0 as default (always same value)
    labels[self.blocks[0]] = str(np.round(self.blocks[0].exit_probability_multiple_agents[self.agents[0]],2))

    #pos = graphviz_layout(self.DG, prog="dot", args="")
    #col = [['r','b'][int(np.round(block.confirmation_confidence,1))] for block in self.DG.nodes()] #Color change for 100% confidence

    #Coloring of tips
    tips = self.get_tips()
    for tip in tips:
        # self.DG.node[tip]["node_color"] = '#ffdbb8'
        self.DG.node[tip]["node_color"] = self.agent_tip_colors[int(str(tip.agent))]


    # col = list(nx.get_node_attributes(self.DG, 'node_color').values()) #Didn't work on Linux
    col = []
    for block in self.DG:
        col.append(self.DG.node[block]["node_color"])

    #Creating figure
    #plt.figure(figsize=(12, 6))
    nx.draw_networkx(self.DG, pos, with_labels=True, node_size = 100, font_size=5.5, node_color = col)
    #nx.draw_networkx_labels(self.DG, lower_pos, labels=labels, font_size=6)

    #Print title
    # title = "blocks = " + str(self.no_of_blocks) +\
    #         ",  " + r'$\lambda$' + " = " + str(self.lam)
    # if(self.tip_selection_algo == "weighted"):
    #     title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
    plt.xlabel("Time (s)")
    plt.yticks([])
    # plt.title(title)

    plt.show()
