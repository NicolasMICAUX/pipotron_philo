"""Longest path problem APPROXIMATION (reimplemented from https://github.com/topshik/longest_path/)"""
from collections import deque
from random import random, choice, sample, randint
from networkx import DiGraph
from numpy import exp, sqrt
from tqdm import tqdm

from citation_graph import get_subgraph

class Path:
    def __init__(self, graph: DiGraph):
        self.graph_ = graph
        self.path_ = deque(sample(graph.nodes(), randint(1, len(graph.nodes()))))

    def add(self, v):
        front_adjescent = self.graph_.neighbors(self.path_[0])
        back_adjescent = self.graph_.neighbors(self.path_[-1])
        is_front_adjescent = front_adjescent.index(v) != front_adjescent[-1]
        is_back_adjescent = back_adjescent.index(v) != back_adjescent[-1]
        if is_front_adjescent and is_back_adjescent:
            if random() < .5:
                self.path_.appendleft(v)
            else:
                self.path_.append(v)
        elif is_front_adjescent:
            self.path_.appendleft(v)
        elif is_back_adjescent:
            self.path_.append(v)

    def remove(self, v):
        if self.path_[0] == v:
            self.path_.popleft()
        elif self.path_[-1] == v:
            self.path_.pop()

    def cost(self):
        return len(self.path_)

    def front(self):
        return self.path_[0]

    def back(self):
        return self.path_[-1]




class Metropolis:
    """Metropolis."""
    def __init__(self):
        self.max_iterations = 1000000

    def solve(self, graph: DiGraph, K: float, T: float, fire: bool, debug_info: bool = True):
        path = Path(graph)
        for i in tqdm(range(self.max_iterations)):
            if path.cost() == 0:
                path = Path(graph)

            cands = set()
            cands.add(path.front())
            cands.add(path.back())

            for v in graph.neighbors(path.front()):
                if v == path.back():
                    cands.add(v)

            v = choice(list(cands))
            if v != path.front() and v != path.back():
                path.add(v)
            else:
                if random() < exp(-(1 / (K * T))):
                    path.remove(v)

            if fire:
                T = sqrt(T)

            if debug_info:
                print(path.cost())

        return path


if __name__ == '__main__':
    G, _ = get_subgraph()
    metropolis = Metropolis()
    path_metropolis1 = metropolis.solve(G, 1, 1000, False, False)
    print(path_metropolis1.cost())
    path_metropolis2 = metropolis.solve(G, 1, 1000, False, False)
    print(path_metropolis2.cost())
