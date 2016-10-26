#!/usr/bin/python 

from Node import node
import sys, time, socket, re

"""
update interval == 1s
update route interval == 30s
"""

# Initialise node, ARGS => (node_id, node_port, config_file)
n = node(sys.argv[1], sys.argv[2], sys.argv[3])
n_time = time.time()
r_time = time.time()

# send initial broadcast
n.broadcast_lsp()

print "Link state routing" # Indicate that the script has started

while True:
   
    c_time = time.time()
    time_diff = c_time - n_time

    try:

        if c_time - r_time >= 30:
            n.route()
            print 
            r_time = c_time

        if time_diff >= 1: # if at least a second has passed
            n.broadcast_lsp()
            n_time = c_time
            n.check_neighbours()
            n.clear_ka()
            time.sleep(0.1)

        n.broadcast_ka() # not sure if this is a good idea here
                         # this makes the previous broadcasts redundant

        data, addr = n._socket.recvfrom(n.s_port)

        if re.match("^LSP", data):
            in_edges = n.parse_lsp(data)
            n.update_net_topology(in_edges)
            n.forward_lsp((in_edges.keys())[0], data)
        elif re.match("^KA", data):
            n.parse_ka(data)




    except socket.timeout:
        pass
