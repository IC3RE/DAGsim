import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


#############################################################################
# PRINTING AND PLOTTING
#############################################################################

def print_info(self):
    text = "\nParameters:  Transactions = " + str(self.no_of_transactions) + \
            ",  Tip-Selection = " + str(self.tip_selection_algo).upper() + \
            ",  Lambda = " + str(self.lam)
    if(self.tip_selection_algo == "weighted"):
        text += ",  Alpha = " + str(self.alpha)
    text += " | Simulation started...\n"
    print(text)

def print_graph(self):

    #Positioning and text of labels
    pos = nx.get_node_attributes(self.DG, 'pos')
    lower_pos = {key: (x, y - 0.1) for key, (x, y) in pos.items()} #For label offset (0.1)

    #Create labels with the confirmation confidence of every transaction (of the issueing agent)
    labels = {
        transaction: str(str(np.round(transaction.exit_probability_multiple_agents[transaction.agent], 2)) + "  " +
                         str(np.round(transaction.confirmation_confidence_multiple_agents[transaction.agent], 2)))
        for transaction in self.DG.nodes if transaction.agent != None
    }
    #For genesis take agent 0 as default (always same value)
    labels[self.transactions[0]] = str(np.round(self.transactions[0].exit_probability_multiple_agents[self.agents[0]],2))

    #pos = graphviz_layout(self.DG, prog="dot", args="")
    #col = [['r','b'][int(np.round(transaction.confirmation_confidence,1))] for transaction in self.DG.nodes()] #Color change for 100% confidence

    #Coloring of nodes
    tips = self.get_tips()
    for tip in tips:
        self.DG.node[tip]["node_color"] = '#ffdbb8'
    col = list(nx.get_node_attributes(self.DG, 'node_color').values())

    #Creating figure
    plt.figure(figsize=(12, 6))
    nx.draw_networkx(self.DG, pos, with_labels=True, node_color = col)
    nx.draw_networkx_labels(self.DG, lower_pos, labels=labels)

    #Print title
    title = "Transactions = " + str(self.no_of_transactions) +\
            ",  " + r'$\lambda$' + " = " + str(self.lam)
    if(self.tip_selection_algo == "weighted"):
        title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
    plt.xlabel("Time (s)")
    plt.yticks([])
    plt.title(title)
    plt.show()
    #Save the graph
    #plt.savefig('graph.png')

def print_tips_over_time(self):

    #Get no of tips per time
    no_tips = []
    for i in self.record_tips:
        no_tips.append(len(i))

    plt.figure(figsize=(12, 6))

    plt.plot(self.arrival_times, no_tips, label="Tips")

    #Cut off first 250 transactions for mean and best fit
    if(self.no_of_transactions >= 250):
        cut_off = 250
    else:
        cut_off = 0

    #Plot mean
    x_mean = [self.arrival_times[cut_off], self.arrival_times[-1]]
    y_mean = [np.mean(no_tips[cut_off:]), np.mean(no_tips[cut_off:])]
    plt.plot(x_mean, y_mean, label="Average Tips", linestyle='--')

    #Plot best fitted line
    plt.plot(np.unique(self.arrival_times[cut_off:]), np.poly1d(np.polyfit(self.arrival_times[cut_off:], no_tips[cut_off:], 1))(np.unique(self.arrival_times[cut_off:])), label="Best Fit Line", linestyle='--')

    #Print title
    title = "Transactions = " + str(self.no_of_transactions) + \
            ",  " + r'$\lambda$' + " = " + str(self.lam)
    if (self.tip_selection_algo == "weighted"):
        title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
    plt.xlabel("Time (s)")
    plt.ylabel("Number of tips")
    plt.legend(loc='upper left')
    plt.title(title)
    plt.show()

# class Plot:
#     def __init__(self, x, _no_of_transactions):
#         self.x = x
#         self.y = np.random.rand(_no_of_transactions)
#
#     def show_plot(self):
#         plt.scatter(self.x, self.y)
#         plt.xlabel('$Time$')
#         #plt.ylabel('$y$')
#         plt.show()
