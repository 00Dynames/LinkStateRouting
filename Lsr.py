#!/usr/bin/python 

from Node import node
import sys, time

# Initialise node, ARGS => (node_id, node_port, config_file)
n = node(sys.argv[1], sys.argv[2], sys.argv[3])

# send initial broadcast
for n_id in n.neighbours.keys():
    n.lsp = n.make_lsp(n.neighbours[n_id][1])
    print n.lsp

#while True:
    # if update interval 
        # broadcast
    # if update route
        # run update_route 
    # else
        # check for heartbeats
            # update neighbours if someone died

    #print time.time()
