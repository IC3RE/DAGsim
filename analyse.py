import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pickle

no = "5_2_4"
path = "Evaluation/"+ str(no) + ".pkl"

with open(path, 'rb') as handle:
    record_attachment_probabilities = pickle.load(handle)


title = "Transactions = " + str(10000) + \
            ",  " + r'$\lambda$' + " = " + str(50) + ",  " + r'$\alpha$' + " = " + str(0.001)#+ \
            # ",  " + r'$d$' + " = " + str(self.distances[1][0])


plt.figure(figsize=(20, 10))

plt.subplot(1, 2, 1)

print(record_attachment_probabilities)

x = np.squeeze([i[0] for i in record_attachment_probabilities])
y = np.squeeze([i[1] for i in record_attachment_probabilities])

# print(self.record_attachment_probabilities)

labels = ["Agent " + str(i) for i in range(len(y))]

# ax = plt.axes()
# ax.set_color_cycle([plt.cm.tab20c(i) for i in np.linspace(0, 1, len(y))])
plt.plot(x,y)
# plt.ylim(0, 0.6)

# plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),\
# label="Best Fit", linestyle='--')
#
# x_mean = [i for i in x]
# y_mean = [np.mean(y) for i in y]
# print(np.mean(y))
# print(np.std(y))
# plt.plot(x_mean, y_mean,\
# label="Average", linestyle='-')

# lower_bound_95_confidence_interval = st.t.interval(0.80, len(partitioning_values)-1, loc=np.mean(partitioning_values), scale=st.sem(partitioning_values))[0]
# upper_bound_95_confidence_interval = st.t.interval(0.80, len(partitioning_values)-1, loc=np.mean(partitioning_values), scale=st.sem(partitioning_values))[1]
# plt.axhline(y=lower_bound_95_confidence_interval, color='r', linestyle='-')
# plt.axhline(y=upper_bound_95_confidence_interval, color='r', linestyle='-')

plt.xlabel("Transactions")
# plt.xticks([])
plt.ylabel("Probability to attach to sub-Tangle branch")
plt.legend(labels, loc="upper right", ncol=2)
# plt.legend(labels, loc='upper right')

plt.subplot(1, 2, 2)

data = []

for agent in range(10):
    agent_data = [i[1][agent] for i in record_attachment_probabilities]
    data.append(agent_data)
    print(str(agent) + "     " + str(agent_data))

print(data)



# labels = ["Agent " + str(i) for i in range(len(y))]

# ax = plt.axes()
# ax.set_color_cycle([plt.cm.tab20c(i) for i in np.linspace(0, 1, len(y))])
plt.boxplot(data, 0, '+')
# plt.ylim(0, 0.6)

# plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),\
# label="Best Fit", linestyle='--')
#
# x_mean = [i for i in x]
# y_mean = [np.mean(y) for i in y]
# print(np.mean(y))
# print(np.std(y))
# plt.plot(x_mean, y_mean,\
# label="Average", linestyle='-')

# lower_bound_95_confidence_interval = st.t.interval(0.80, len(partitioning_values)-1, loc=np.mean(partitioning_values), scale=st.sem(partitioning_values))[0]
# upper_bound_95_confidence_interval = st.t.interval(0.80, len(partitioning_values)-1, loc=np.mean(partitioning_values), scale=st.sem(partitioning_values))[1]
# plt.axhline(y=lower_bound_95_confidence_interval, color='r', linestyle='-')
# plt.axhline(y=upper_bound_95_confidence_interval, color='r', linestyle='-')

plt.xlabel("Agents")
plt.xticks(np.arange(1, 11), np.arange(0, 10))
# plt.ylabel("Probability to attach to sub-Tangle branch")
# plt.legend(loc='upper left')
# plt.legend(labels, loc='upper left')
plt.suptitle(title)

plt.tight_layout()
plt.subplots_adjust(top=0.94)

# plt.show()
plt.savefig(str(no) + '.png')

# averages = []
#
# for agent in range(10):
#     average = np.round(np.mean([i[1][agent] for i in list]),3)
#     print(str(agent) + "     " + str(average))


