"""Démontrer une citation Y à partir d'une citation X, si possible."""
from networkx import shortest_path, NetworkXNoPath
from citation_graph import get_subgraph
from print_demo import print_demo

G, auteurs = get_subgraph()

premisse = ''
while premisse not in G.nodes():
    premisse = input('Prémisse ? ')  # 'Les mauvaises lois sont la pire forme de tyrannie.'
conjecture = ''
while conjecture not in G.nodes():
    conjecture = input('Conjecture ? ')  # 'Le destin qui s'applique à tous peut-il être néfaste à un seul ?'

try:
    path = shortest_path(G, source=premisse, target=conjecture)
    print_demo(path, auteurs)
except NetworkXNoPath:
    print(f'Impossible de prouver {conjecture} à partir de {premisse}.')

# Tout d’abord, les mauvaises lois sont la pire forme de tyrannie. (Edmund Burke)
# Il est vrai que la tyrannie est de vouloir avoir par une voie ce qu'on ne peut avoir que par une autre. (Blaise Pascal)
# Pourtant, ce qu'on dit de soi est toujours poésie. (Ernest Renan)
# Néanmoins, la poésie est quelque chose de plus philosophique et de plus grande importance que l'histoire. (Aristote)
# D’ailleurs, toute l'histoire du monde se conçoit comme la biographie d'un seul homme. (Friedrich Nietzsche)
# Et, ce qu&#039;un homme pense de lui-même, voilà ce qui règle ou plutôt indique son destin.  (Henry David Thoreau)
# En résumé, le destin qui s'applique à tous peut-il être néfaste à un seul ? (Cicéron)
