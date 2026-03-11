#!/usr/bin/env python3
"""Hierholzer's algorithm — find Eulerian path/circuit in directed/undirected graphs."""
import sys
from collections import defaultdict

class EulerGraph:
    def __init__(self, directed=True):
        self.directed = directed
        self.adj = defaultdict(list)
        self.in_deg = defaultdict(int)
        self.out_deg = defaultdict(int)
    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.out_deg[u] += 1; self.in_deg[v] += 1
        if not self.directed:
            self.adj[v].append(u)
            self.out_deg[v] += 1; self.in_deg[u] += 1
    def has_euler_circuit(self):
        nodes = set(self.adj)
        if self.directed:
            return all(self.in_deg[v] == self.out_deg[v] for v in nodes)
        return all(self.out_deg[v] % 2 == 0 for v in nodes)
    def has_euler_path(self):
        if self.has_euler_circuit(): return True
        nodes = set(self.adj) | set(self.in_deg)
        if self.directed:
            starts = sum(1 for v in nodes if self.out_deg[v] - self.in_deg[v] == 1)
            ends = sum(1 for v in nodes if self.in_deg[v] - self.out_deg[v] == 1)
            return starts == 1 and ends == 1
        odd = sum(1 for v in nodes if self.out_deg[v] % 2 == 1)
        return odd == 2
    def find_path(self):
        if not self.has_euler_path(): return None
        adj = {v: list(es) for v, es in self.adj.items()}
        start = next(iter(self.adj))
        if self.directed:
            for v in self.adj:
                if self.out_deg[v] - self.in_deg.get(v, 0) == 1: start = v; break
        else:
            for v in self.adj:
                if self.out_deg[v] % 2 == 1: start = v; break
        stack = [start]; path = []
        while stack:
            v = stack[-1]
            if adj.get(v):
                u = adj[v].pop()
                if not self.directed:
                    try: adj[u].remove(v)
                    except ValueError: pass
                stack.append(u)
            else:
                path.append(stack.pop())
        return path[::-1]

if __name__ == "__main__":
    g = EulerGraph(directed=True)
    for u, v in [(0,1),(1,2),(2,0),(0,3),(3,4),(4,0)]:
        g.add_edge(u, v)
    print(f"Has circuit: {g.has_euler_circuit()}")
    print(f"Euler path: {g.find_path()}")
