"""
Pythonic graph implementation for link state routing.
"""

class graph:
    
    """
    Graph is a dict.
    key -> node_id
    value -> list of (connected node, cost) tuples
    """

    def __init__(self, node_id):
        self.graph = {}
        self.num_edges = 0
        self.num_nodes = 0

        self.graph[str(node_id)] = []
        self.num_nodes += 1

    # will also duplicate existing edges
    def insert_edge(self, start_id, end_id, cost):
        
        self.num_edges += 1

        edge = (str(end_id), int(cost))

        if start_id in self.graph.keys():
            self.graph[str(start_id)].append(edge)
        else:
            self.num_nodes += 1
            self.graph[str(start_id)] = []
            self.graph[str(start_id)].append(edge)
             
        edge = (str(start_id), int(cost))     

        if end_id in self.graph.keys():
            self.graph[str(end_id)].append(edge)
        else:
            self.num_nodes += 1
            self.graph[str(end_id)] = []
            self.graph[str(end_id)].append(edge)

    def dijkstra(self, source):    
        
        dist = {}
        prev = {}
        unvisited = []
        visited = []

        for node in self.graph.keys():
            dist[node] = float("inf")
            prev[node] = None

        unvisited.append((source, 0))
        dist[source] = 0
        prev[source] = source

        while unvisited:
            # select min cost from a list of (node, cost) tuples
            node, cost = min(unvisited, key = lambda tup: tup[1])
            unvisited.remove((node, cost))
            visited.append(node)

            for n_node, n_cost in self.graph[node]:
                if n_node in visited or n_node in unvisited:
                    continue
                
                unvisited.append((n_node, n_cost))
                new_dist = dist[node] + n_cost
                
                if new_dist < dist[n_node]:
                    dist[n_node] = new_dist
                    prev[n_node] = node

        return dist, prev


