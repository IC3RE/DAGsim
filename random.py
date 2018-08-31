import matplotlib.pyplot as plt
from networkx import nx

n = 50  #number nodes
m = 50  #number edges

G = nx.gnm_random_graph(n, m)

while not nx.is_connected(G):
    G = nx.gnm_random_graph(n, m)

print(nx.floyd_warshall_numpy(G))

distances = nx.floyd_warshall_numpy(G).tolist()
print(distances)

nx.draw(G, with_labels=True)
plt.show()
