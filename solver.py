#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import List, Tuple
import random

class Color:

    index: int
    n_nodes: int

    def __init__(self, index) -> None:
        self.index = index
        self.n_nodes = 0

    def __repr__(self):
        return f"{self.index}"

    def add_node(self):
        self.n_nodes = self.n_nodes + 1


class Node:

    neighbors: List['Node']
    index: int
    color: Color

    def __init__(self, index):
        self.index = index
        self.neighbors = []
        self.color = None

    def __repr__(self) -> str:
        return f"N{self.index}|{self.color}"

    def add_neighbor(self, node: 'Node'):
        if node not in self.neighbors:
            self.neighbors.append(node)

    def set_color(self, color: Color):
        self.color = color
        color.add_node()

    @property
    def neighbor_colors(self):
        return [n.color for n in self.neighbors if n.color is not None]

    @property
    def saturation(self):
        return len(set((n.color for n in self.neighbors if n.color is not None)))

    @property
    def degree(self):
        return len(self.neighbors)


class GraphColor:

    N: List[Node]
    C: List[Color]
    history: List[Node]

    def __init__(self, nodes: List[int], edges: List[Tuple[int, int]]):
        N = [Node(i) for i in nodes]
        for e in edges:
            i, j = e
            N[i].add_neighbor(N[j])
            N[j].add_neighbor(N[i])
        self.N = N
        self.C = []
        self.history = []

    def find_next_color(self, node: Node) -> Color:
        next_color = None
        for c in self.C:
            if c not in node.neighbor_colors:
                next_color = c
                break
        if next_color is None:
            next_color = Color(len(self.C) + 1)
            self.C.append(next_color)
        return next_color

    def solve(self, save_history=False):
        Q = [n for n in self.N]  # Pool of uncolored nodes
        while len(Q) > 0:
            Q.sort(key=lambda x: (x.saturation, x.degree), reverse=True)
            n: Node = Q.pop(0)
            next_color = self.find_next_color(n)
            n.set_color(next_color)
            if save_history:
                self.history.append(n)
        self.C.sort(key=lambda x: x.n_nodes, reverse=True)

    def solve_random(self, save_history=False):
        Q = [n for n in self.N]  # Pool of uncolored nodes
        random.shuffle(Q)
        while len(Q) > 0:
            n: Node = Q.pop(0)
            next_color = self.find_next_color(n)
            n.set_color(next_color)
            if save_history:
                self.history.append(n)
        self.C.sort(key=lambda x: x.n_nodes, reverse=True)


    @property
    def cost(self):
        return len(self.C)


class NodeDS:

    def __init__(self, n):
        self.n = n
        self.color = -1
        self.neighbors = list()
        self.available_colors = list()

    def get_neighbors(self):
        return self.neighbors
    
    def add_neighbor(self, n):
        if not n in self.neighbors:
            self.neighbors.append(n)
    
    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color
    
    def initialize_colors(self, n):
        self.available_colors = [1 for i in range(n)]
        self.color = -1

    def exclude_color(self, n):
        self.available_colors[n] = 0

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def assign_color(self):
        avail_color = -1
        for c in range(len(self.available_colors)):
            if self.available_colors[c] == 1:
                avail_color = c
                break
        self.color = avail_color
        self.available_colors[avail_color] = 0
        return avail_color, self.neighbors

    def __str__(self):
        return f"Node: {self.n}, Color: {self.color}, Neighbors: {self.neighbors}, Available colors: {self.available_colors}"


class GraphDS:

    def __init__(self):
        self.nodes = dict()

    def add_edge(self, edge):
        
        if not edge[0] in self.nodes.keys():
            node = NodeDS(edge[0])
            self.nodes[edge[0]] = node
        if not edge[1] in self.nodes.keys():
            node = NodeDS(edge[1])
            self.nodes[edge[1]] = node
        self.nodes[edge[0]].add_neighbor(edge[1])      
        self.nodes[edge[1]].add_neighbor(edge[0])      

    def initialize_colors(self):
        for k in self.nodes.keys():
            self.nodes[k].initialize_colors(len(self.nodes.keys()))

    def colorize_random(self):
        nodes_list = list(self.nodes.keys())
        random.shuffle(nodes_list)
        for node in nodes_list:
            color, neighbors = self.nodes[node].assign_color()
            for neighb in neighbors:
                self.nodes[neighb].exclude_color(color)

    def colorize(self):
        nodes_list = sorted(self.nodes.keys(), key=lambda d: -len(self.nodes[d].neighbors))
        for node in nodes_list:
            color, neighbors = self.nodes[node].assign_color()
            for neighb in neighbors:
                self.nodes[neighb].exclude_color(color)

    def print_graph(self):
        for node in self.nodes.keys():
            print(self.nodes[node])

    def get_colors_list(self):
        colors_list = []
        for node in self.nodes.keys():
            colors_list.append(self.nodes[node].get_color())
        return colors_list


def solve_data_structure(edges):

    graph = GraphDS()
    for edge in edges:
        graph.add_edge(edge)

    best_solution = []
    for i in range(100):
        graph.initialize_colors()
        graph.colorize_random()
        solution = graph.get_colors_list()
        if len(best_solution) == 0 or len(set(solution)) < len(set(best_solution)):
            best_solution = solution
#    graph.print_graph()
    return best_solution


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    nodes = set()
    edges = []

    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
        nodes.add(int(parts[0]))
        nodes.add(int(parts[1]))

    nodes = sorted(nodes)
    graph = GraphColor(nodes, edges)

    if len(nodes) < 100:
        best_solution = []
        for i in range(1000):
            nodes = sorted(nodes)
            graph = GraphColor(nodes, edges)
            graph.solve_random()
            solution = []
            for node in graph.N:
                solution.append(int(node.color.index - 1))
            if len(best_solution) == 0 or len(set(best_solution)) > len(set(solution)):
                best_solution = solution
        solution = best_solution
    else:
        graph.solve()
        solution = []
        for node in graph.N:
            solution.append(int(node.color.index - 1))
    
    output_data = str(len(set(solution))) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

