import matplotlib.pyplot as plt
from networkx import nx


def create_random_graph_distances():
    n = 20  #number nodes
    m = 20  #number edges

    G = nx.gnm_random_graph(n, m)

    while not nx.is_connected(G):
        G = nx.gnm_random_graph(n, m)

    distances = nx.floyd_warshall_numpy(G).tolist()

    nx.draw(G, with_labels=True)
    plt.show()

    return distances


print(create_random_graph_distances())
