"""Rendre le graphe acyclique."""
import pickle
import random
from os.path import exists
from networkx import DiGraph, NetworkXNoCycle, find_cycle, dag_longest_path
from citation_graph import get_subgraph
from print_demo import print_demo


def to_acyclic(G: DiGraph) -> None:
    """
    Converts graph G to an acyclic graph inplace.
    :param G: graph
    """
    k = 0
    try:
        while True:  # remove node from a cycle until no more cycle
            cycle = find_cycle(G)  # really long process
            # e = random.choice(cycle)
            e = cycle[0]  # not random, but faster
            k += 1
            G.remove_edge(*e)
            if k % 100 == 0:
                print(k)
    except NetworkXNoCycle:
        print(k)
        pass


if __name__ == '__main__':  # tester la function `to_acyclic`
    if exists('acyclic_graph.pickle'):
        _, authors = get_subgraph()
        with open('acyclic_graph.pickle', 'rb') as f:
            G = pickle.load(f)
    else:
        G, authors = get_subgraph()
        to_acyclic(G)
        with open('acyclic_graph.pickle', 'wb') as f:
            pickle.dump(G, f, protocol=pickle.HIGHEST_PROTOCOL)

    # * Plus longue démonstration possible - approximation avec DAG *
    path = dag_longest_path(G)
    print_demo(path, authors)
    print(len(path))

    # essayer de trouver mieux, avec des marches aléatoires dans le graphe original
    G, authors = get_subgraph()  # reprendre le graphe original
    current_max = 0
    k = 0
    while True:  # interruption manuelle
        k += 1
        random_node = random.choice(list(G.nodes()))  # choisir le noeud de depart au hasard
        steps = {random_node}
        steps_list = [random_node]
        while True:  # marche aléatoire
            neighbors = [node for node in G.neighbors(random_node) if node not in steps]
            if len(neighbors) == 0:
                break
            else:
                random_node = random.choice(neighbors)
                steps.add(random_node)
                steps_list.append(random_node)

        if len(steps_list) >= current_max:  # si cette marche aléatoire est plus grande que celle d'avant
            current_max = len(steps_list)
            print(f'max={current_max}, k={k}')  # courbe d'évolution de la longueur max trouvée des marches aléatoires


# * DFS method, recursion limit always reached *
# def to_acyclic(G: DiGraph) -> None:
#     """
#     Converts graph G to an acyclic graph inplace.
#     :param G: graph
#     """
#     def dfs_visit(G, u, discovered, finished) -> None:
#         """
#         One step of DFS traversal.
#         :param G:
#         :param u:
#         :param discovered:
#         :param finished:
#         """
#         discovered.add(u)
#
#         for v in G.adj[u]:
#             if v in discovered:  # Detect cycles
#                 nodes_to_remove.append((u, v))
#
#             if v not in finished:  # Recurse into DFS tree
#                 dfs_visit(G, v, discovered, finished)
#
#         discovered.remove(u)
#         finished.add(u)
#
#     nodes_to_remove = []
#     discovered = set()
#     finished = set()
#
#     for u in G.adj:
#         if u not in discovered and u not in finished:
#             dfs_visit(G, u, discovered, finished)
#
#     G.remove_edges_from(nodes_to_remove)
