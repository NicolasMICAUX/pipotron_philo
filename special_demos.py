"""Démonstrations particulières intéressantes"""
import random
import networkx as nx
from networkx import strongly_connected_components, all_simple_paths, simple_cycles
from citation_graph import get_subgraph
from print_demo import print_demo, pretty_print

G, auteurs = get_subgraph()  # génère le graphe des citations (voir le code dans `citation_graph.py`)


# * citations les plus importantes *
alpha = 0.85  # damping parameter for PageRank, default=0.85.
pr = nx.pagerank(G, alpha=alpha)
most_important_nodes = [k for k, _ in sorted(pr.items(), key=lambda item: item[1])]
pretty_print(most_important_nodes[:5], auteurs)


# * équivalences *
# print(len(list(simple_cycles(G))))  # too long to finish

# count how many (non trivial) strongly connected components
print(len([c for c in strongly_connected_components(G) if len(c) > 1]))  # 8

# display human-readable equivalences (not too long & interesting) : NONE MATCH REQUIREMENTS
MIN_EQUIV_LEN = 3
MAX_EQUIV_LEN = 8
G_no_same = G.subgraph([n for n in G.nodes() if not G.nodes[n]['same']])
for component in strongly_connected_components(G_no_same):
    if MIN_EQUIV_LEN <= len(component):
        if len(component) <= MAX_EQUIV_LEN:
            print(component)
        else:
            answer = True
            component_G = G.subgraph(component)
            choices = list(component_G.nodes())
            while answer:
                if len(choices):
                    source = random.choice(choices)
                    for cycle in all_simple_paths(component_G, source, source, cutoff=MAX_EQUIV_LEN):
                        if MIN_EQUIV_LEN <= len(cycle):
                            print(cycle)
                            answer = input('Continuer ? (O/N)') in {'O', 'o', 'oui', 'OUI', ''}
                            break
                    choices.remove(source)
                else:
                    break
