"""Projet - "démonstrations philosophiques."""
import random
from citation_graph import get_subgraph
from print_demo import print_demo

if __name__ == '__main__':
    sg, auteurs = get_subgraph()  # génère le graphe des citations (voir le code dans `citation_graph.py`)

    MIN_STEPS = 4
    MAX_STEPS = 15

    # * generation loop : generate philosophical demos that match some criterias *
    answer = True
    while answer:
        random_node = random.choice(list(sg.nodes()))  # choisir le noeud de depart au hasard
        steps = {random_node}
        steps_l = [random_node]
        for i in range(MAX_STEPS):  # generer un random walk
            voisins = [node for node in sg.neighbors(random_node) if node not in steps]  # make sure node not already visited
            if len(voisins) == 0:  # if random_node having no outgoing edges
                break
            else:
                random_node = random.choice(voisins)  # choose a node randomly from neighbors
                steps.add(random_node)
                steps_l.append(random_node)
        if len(steps_l) >= max(MIN_STEPS, 2):  # whatever the value of `MIN_STEPs`, cannot be lower than 2
            print_demo(steps_l, auteurs)
            answer = input('Continuer ? (O/N)') in {'O', 'o', 'oui', 'OUI', ''}
