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

print g.dijkstra_route("A")

#print g.graph, g.num_edges, g.num_nodes
