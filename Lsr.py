#!/usr/bin/python 

from Node import node
import sys, time, socket, re

"""
update interval == 1s
update route interval == 0.5s
"""

# Initialise node, ARGS => (node_id, node_port, config_file)
n = node(sys.argv[1], sys.argv[2], sys.argv[3])
n_time = time.time()

# send initial broadcast
n.broadcast_lsp()

while True:
   
    c_time = time.time()

    try:
        if (c_time - n_time) >= 1: # if at least a second has passed
            #print "c_time -> ", c_time
            n.broadcast_lsp()
            n_time = c_time
            # broadcast and check neighbours
    
        elif (c_time - n_time) <= 0.5 and (c_time - n_time) >= 0.45: # approximately 30s interval
            #print "c_time => ", c_time
            pass
            # run dijkstra's and print out paths
        
        data, addr = n._socket.recvfrom(n.s_port)
        print data

        if re.match("^LSP", data):
            in_edges = n.parse_lsp(data)
            # update net_topology
            n.update_net_topology(in_edges)
            # forward lsp
            n.forward_lsp((in_edges.keys())[0], data)
            n.net_topology.show()


        #elif data[0] == "KA":
         #   print "KA"




    except socket.timeout:
        pass
        #print "T.O"

