"""
Router node class
"""

from Graph import graph
import socket, time, re

class node:

    def __init__(self, node_id, node_port, config):
        self.id = str(node_id)
        self.n_start = time.time()

        # initialise node's socket
        self.s_port = int(node_port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(("127.0.0.1", int(node_port)))
        self._socket.settimeout(0.1)

        self.lsp = "" 
        self.net_topology = graph(self.id)
        self.neighbours = {} # => {node_id: (cost, port, KA_count)}
        self.neighbour_ka = {}

        # iterate through config file and insert nieghbours
        # Assume the config file is in the same directory 

        config_file = open(config, "r")
        config_file.readline() # Get rid of the first line, it's junk

        for line in config_file:
            line = line.rstrip('\n')
            line = line.split(" ")
            self.neighbours[line[0]] = (float(line[1]), int(line[2]))
            self.neighbour_ka[line[0]] = 0
            self.net_topology.insert_edge(self.id, line[0], line[1])

        #print self.net_topology.graph
    
    """
    LSP structure
    "source_port:destinaiton_port:source_id:<data>"
    <data> = "(node_id,cost)"
    """
    def make_lsp(self, dest_port): # don't want to add the neighbour you're sending to
        # iterate through a dict with the 
        # node's nieghbours and return a string
        # to send.
        # make static header as extra feature

        result = "LSP:%s:%s:%s" % (str(self.s_port), str(dest_port), str(self.id))
        for node_id in self.neighbours.keys():
            result += ":(%s,%s)" % (node_id, self.neighbours[node_id][0])

        return result
   
    def parse_lsp(self, lsp_string):
        # read in a LSP
        # return the edges from a node
        
        result = {}
        lsp_id = ""
        lsp = lsp_string.split(":")
        for field in list(enumerate(lsp)): 
            if field[0] in range(3):
                continue
            elif field[0] == 3:
                lsp_id = field[1]
                result[field[1]] = []
            else:
                # convert string to tuple
                field = tuple(re.sub("[\(\)]", "", field[1]).split(","))
                result[lsp_id].append(field)

        return result


    def broadcast_lsp(self):
        for n_id in self.neighbours.keys():
            self.lsp = self.make_lsp(self.neighbours[n_id][1])
            #print self.lsp
            self._socket.sendto(self.lsp, ("127.0.0.1", self.neighbours[n_id][1]))

    def broadcast_ka(self):
        for n_id in self.neighbours.keys():
            KA_message = "KA:%s:%s:%s" % (self.s_port, self.neighbours[n_id][1], self.id)   
            self._socket.sendto(KA_message, ("127.0.0.1", self.neighbours[n_id][1]))
            self._socket.sendto(KA_message, ("127.0.0.1", self.neighbours[n_id][1]))

    def parse_ka(self, packet):
        data = packet.split(":")
        self.neighbour_ka[data[3]] += 1

    def clear_ka(self):
        for n_id in self.neighbour_ka.keys():
            self.neighbour_ka[n_id] = 0

    def check_neighbours(self):
        for n_id in self.neighbour_ka.keys():
            if self.neighbour_ka[n_id] == 0:
                del self.neighbours[n_id]
                del self.neighbour_ka[n_id]
                self.net_topology.remove_edge(self.id, n_id)

    def update_net_topology(self, new_edges):
        # get node id, get its edges in the graph, get its edges from new_edges
        n_id = (new_edges.keys())[0]
        # print new_edges

        if n_id == self.id:
            return

        # edges in lsp
        lsp_neighbours = [edge[0] for edge in new_edges[n_id]] #edges in packet    
        #print "lsp", n_id, lsp_neighbours
        # edges in graph
        grph_neighbours = [edge[0] for edge in self.net_topology.graph[n_id]] # kind of dodge
        #print "grph", n_id, grph_neighbours

        # lsp diff 
        lsp_diff = [item for item in lsp_neighbours if item not in grph_neighbours]
        #print "lsp_diff", n_id, lsp_diff
        # grph diff
        grph_diff = [item for item in grph_neighbours if item not in lsp_neighbours]
        #print "grph_diff", n_id, grph_diff

        if len(lsp_diff) == 0 and len(grph_diff) == 0:
            return 

        # if there's an edge in new_edges that isn't in then insert
        if len(lsp_diff) > 0:
            #print "insert"
            for edge_id in lsp_diff:
                cost = ([item for item in new_edges[n_id] if item[0] == edge_id])[0][1]
                #print n_id, edge_id, cost
                self.net_topology.insert_edge(n_id, edge_id, cost)

        # if there's an edge in the neighbours then remove an edge
        if len(grph_diff) > 0:
            #print "remove"
            for edge_id in grph_diff:
                #print n_id, edge_id
                self.net_topology.remove_edge(n_id, edge_id)

    # need to test
    def forward_lsp(self, source, packet):
        for n_id in self.neighbours.keys():
            if not self.net_topology.has_edge(source, n_id) or n_id != source:
                self._socket.sendto(packet, ("127.0.0.1", self.neighbours[n_id][1]))

    # print routes
    def route(self):
        dist, prev = self.net_topology.dijkstra(self.id)    
        
        for n_id in dist.keys():
           
            path = []
            curr_n = n_id
            if n_id != self.id:
                while curr_n != self.id:
                    path.append(prev[curr_n])
                    curr_n = prev[curr_n]

            path.reverse()
            path.append(n_id)
            #print n_id, path
            print "least-cost path to node %s: %s and the cost is %.1f" % (n_id, "".join(path), dist[n_id])

