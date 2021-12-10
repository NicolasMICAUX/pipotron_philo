"""Compute some statistics/display some vizualisations about the graph."""
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import entropy
from citation_graph import get_subgraph
import igraph as ig

sg, _ = get_subgraph()  # generer le graphe


# * vizualize graph *
g = ig.Graph()
g = g.from_networkx(sg)
ig.plot(g,
        bbox=(1000, 1000),
        vertex_size=4,
        edge_width=0.25,
        edge_arrow_size=0.25,
        target='citation_graph.png'
        )

# * initial incident degree value distribution *
# https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.in_degree.html
degrees = [degree for _, degree in sg.in_degree()]
plt.hist(degrees, bins=52)  # density=False
plt.xlabel("Number of incident nodes")
plt.ylabel("Number of nodes having this much incident nodes")
plt.show()

# * initial PageRank value distribution *
alpha = 0.85  # Damping parameter for PageRank, default=0.85.
pr = nx.pagerank(sg, alpha=alpha)

plt.hist(pr.values(), bins=50, log=True)
plt.xlabel("Page rank value")
plt.ylabel("Number of nodes with that PageRank value")
plt.show()
print(np.std(list(pr.values())))

# ajuster les poids des arêtes incidentes de change rien au résultat de PageRank (voir explication dans le rapport)
inverse_weight = {key: np.power(score, alpha - 1) for key, score in pr.items()}  # theorical value
for node, inv_score in inverse_weight.items():  # setting a weight=1/pagerank_score for all incident edges
    incident_edges = sg.in_edges(node)
    # attr = {edge: inv_score for edge in incident_edges}
    attr = {edge: 1/(len(incident_edges)+1) for edge in incident_edges}
    nx.set_edge_attributes(sg, attr, 'weight')

inverse_weight = {key: 1 / score for key, score in pr.items()}
pagerank_after = nx.pagerank(sg, alpha=alpha, personalization=inverse_weight)
plt.hist(pagerank_after.values(), bins=50, log=True, alpha=0.8)
plt.xlabel("Page rank value")
plt.ylabel("Number of nodes with that PageRank value")
plt.show()
print(np.std(list(pagerank_after.values())))

# * quelques statistiques utiles *
print('max/mean PageRank score', np.max(list(pr.values())) / np.mean(list(pr.values())))
print('entropy', entropy(list(pr.values())))
print('therorical max', entropy([1 for _ in pr]))
