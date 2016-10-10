#!/usr/bin/python

import Graph

g = Graph.graph("A")
g.insert_edge("A", "B", 2)
g.insert_edge("A", "C", 5)
g.insert_edge("A", "D", 1)
g.insert_edge("B", "C", 3)
g.insert_edge("B", "D", 2)
g.insert_edge("C", "D", 3)
g.insert_edge("C", "E", 1)
g.insert_edge("C", "F", 5)
g.insert_edge("D", "E", 1)
g.insert_edge("E", "F", 2)

print g.dijkstra("A")

h = Graph.graph("A")
h.insert_edge("A", "B", 2)
h.insert_edge("A", "G", 3)
h.insert_edge("A", "F", 3)
h.insert_edge("B", "C", 5)
h.insert_edge("C", "G", 2)
h.insert_edge("C", "D", 2)
h.insert_edge("D", "G", 7)
h.insert_edge("D", "E", 4)
h.insert_edge("E", "G", 1)
h.insert_edge("E", "F", 2)
h.insert_edge("F", "G", 3)

print h.dijkstra("A")

#print g.graph, g.num_edges, g.num_nodes
