import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pickle

no = "4_3_4"
path = "Evaluation/"+ str(no) + ".pkl"

with open(path, 'rb') as handle:
    record_attachment_probabilities = pickle.load(handle)


title = "Transactions = " + str(22000) + \
            ",  " + r'$\lambda$' + " = " + str(50) + ",  " + r'$\alpha$' + " = " + str(0.1)#+ \
            # ",  " + r'$d$' + " = " + str(self.distances[1][0])


plt.figure(figsize=(20, 10))

# plt.subplot(1, 2, 1)

print(record_attachment_probabilities)

x = np.squeeze([i[0] for i in record_attachment_probabilities])
y = np.squeeze([i[1] for i in record_attachment_probabilities])

# print(self.record_attachment_probabilities)

# labels = ["Agent " + str(i) for i in range(len(y))]

# ax = plt.axes()
# ax.set_color_cycle([plt.cm.tab20c(i) for i in np.linspace(0, 1, len(y))])
plt.plot(x,y,label="Attachment probability sub-Tangle branch")
plt.ylim(0, 0.6)



print(len(y))
alpha = 0.005
index = 0
for i in list(y):
    if i < 0.5 - alpha or i > 0.5 + alpha:
        index = list(y).index(i)
        break

print(index)
list = list(x)
start_average = list[index]
plt.axvline(x=start_average, color='silver', linestyle=":")


x = x[index:51]
y = y[index:51]

x_mean = [i for i in x]
y_mean = [np.mean(y) for i in y]

print(np.mean(y))
print(np.std(y))
plt.plot(x_mean, y_mean,\
label="Average <20,000 transactions", linestyle='-')


# plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),\
# label="Best Fit", linestyle='--')

textstr = '\n'.join((
    r'mean = %.3f' % (np.mean(y), ),
    r'std = %.3f' % (np.std(y), )))
print(textstr)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
plt.text(start_average+(max(x)-start_average)/2, 0.5, textstr, fontsize=12,
        verticalalignment='top', bbox=props)

######################


x = np.squeeze([i[0] for i in record_attachment_probabilities])
y = np.squeeze([i[1] for i in record_attachment_probabilities])
counter = 0
for i in x:
    if i == 20000:
        index = counter
        print(index)
        break
    counter += 1

start_average = 20000
plt.axvline(x=start_average, color='silver', linestyle=":")


x = x[50:]
y = y[50:]

x_mean = [i for i in x]
y_mean = [np.mean(y) for i in y]

print(np.mean(y))
print(np.std(y))
plt.plot(x_mean, y_mean,\
label="Average >20,000 transactions", linestyle='-')


# plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),\
# label="Best Fit", linestyle='--')

textstr = '\n'.join((
    r'mean = %.3f' % (np.mean(y), ),
    r'std = %.3f' % (np.std(y), )))
print(textstr)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
plt.text(start_average+(max(x)-start_average)/2, 0.4, textstr, fontsize=12,
        verticalalignment='top', bbox=props)

######################
plt.xlabel("Transactions")
# plt.xticks([])
plt.ylabel("Probability to attach to sub-Tangle branch")
plt.legend(loc="upper left")
# plt.legend(labels, loc="upper right", ncol=2)
# plt.legend(labels, loc='upper right')

# plt.subplot(1, 2, 2)
#
# data = []
#
# for agent in range(10):
#     agent_data = [i[1][agent] for i in record_attachment_probabilities]
#     data.append(agent_data)
#     print(str(agent) + "     " + str(agent_data))
#
# print(data)
#
# plt.boxplot(data, 0, '+')
# plt.xlabel("Agents")
# plt.xticks(np.arange(1, 11), np.arange(0, 10))
# plt.suptitle(title)
plt.title(title)
plt.tight_layout()
# plt.subplots_adjust(top=0.94)
# plt.show()
plt.savefig(str(no) + '.png')

# averages = []
#
# for agent in range(10):
#     average = np.round(np.mean([i[1][agent] for i in list]),3)
#     print(str(agent) + "     " + str(average))


