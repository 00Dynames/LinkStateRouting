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

    # does not add edges if they already exist 
    def insert_edge(self, start_id, end_id, cost):
        
        if self.has_edge(start_id, end_id):
            return 

        self.num_edges += 1

        edge = (str(end_id), float(cost))

        if start_id in self.graph.keys():
            self.graph[str(start_id)].append(edge)
        else:
            self.num_nodes += 1
            self.graph[str(start_id)] = []
            self.graph[str(start_id)].append(edge)
             
        edge = (str(start_id), float(cost))     

        if end_id in self.graph.keys():
            self.graph[str(end_id)].append(edge)
        else:
            self.num_nodes += 1
            self.graph[str(end_id)] = []
            self.graph[str(end_id)].append(edge)

    # def remove_edge(self, start_id, end_id)

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

    def get_nodes(self):
        return self.graph.keys()

    def has_edge(self, start_id, end_id):
        
        if start_id not in self.graph.keys():
            return False

        edges = [str(i[0]) for i in self.graph[str(start_id)]] 
        #print str(start_id), str(end_id), edges
        
        if str(end_id) in edges:
            return True
        else:
            return False
    
    def show(self):
        for node in self.graph.keys():
            print node
            for edge in self.graph[node]:
                print "    " + str(edge)

