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
        self._socket.settimeout(0.05)

        self.lsp = "" 
        self.net_topology = graph(self.id)
        self.neighbours = {} # => {node_id: (cost, port)}

        # iterate through config file and insert nieghbours
        # Assume the config file is in the same directory 

        config_file = open(config, "r")
        config_file.readline() # Get rid of the first line, it's junk

        for line in config_file:
            line = line.rstrip('\n')
            line = line.split(" ")
            self.neighbours[line[0]] = (float(line[1]), int(line[2]))
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
            self._socket.sendto(self.lsp, ("127.0.0.1", self.neighbours[n_id][1]))

           
        
    def parse_packet(self, packet):
        # parse a packet and figure out which kind it is
        result = {}
        
        tmp_packet = packet.split(":")
        if tmp_packet[0] == "LSP":
            result = self.parse_lsp(packet)
        elif tmp_packet[0] == "HB":
            pass # parse heartbeat
        
        return result 

    # def send lsp
    
    #def update_neighbours

    def update_net_topology(self, new_edges):
        # iterate through each key in the new_edges dict
        # and add each edge in the lists

        for node in new_edges.keys():
            for edge in new_edges[node]:
                self.net_topology.insert_edge(node, edge[0], edge[1])
                #print edge

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

