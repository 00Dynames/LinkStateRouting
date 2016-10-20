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
    time_diff = c_time - n_time

    try:
        if time_diff >= 1: # if at least a second has passed
            print n.id, " time_diff -> ", time_diff
            #print n.lsp
            #print n.neighbours
            print n.neighbour_ka
            n.net_topology.show()
            
            #print n.neighbour_ka
            #print n.neighbours.keys()
            n.broadcast_lsp()
            #n.broadcast_ka()
            n_time = c_time
            n.check_neighbours()
            n.clear_ka()
            # broadcast and check neighbours
    
        elif time_diff <= 0.51 and time_diff >= 0.5: # approximately 30s interval
            #print "c_time => ", c_time, prev_time
            #print n.net_topology.dijkstra(n.id)
            # parse dijkstra's outpun into correct format
            time.sleep(0.1) 
            #n.route()
            # run dijkstra's and print out paths
            #n.broadcast_ka()
        
        elif (time_diff <= 0.26 and time_diff >= 0.23
           or time_diff <= 0.76 and time_diff >= 0.73):
            # broadcast KA message
            #print "KA", time.time()
            time.sleep(0.1)
            #n.broadcast_ka()

        n.broadcast_ka() # not sure if this is a good idea here
                         # this makes the previous broadcasts redundant

        data, addr = n._socket.recvfrom(n.s_port)
        #print n.id + " " + str(addr[1]) + " => " + data

        if re.match("^LSP", data):
            in_edges = n.parse_lsp(data)
            # update net_topology
            n.update_net_topology(in_edges)
            # forward lsp
            n.forward_lsp((in_edges.keys())[0], data)
            #n.net_topology.show()
        elif re.match("^KA", data):
            n.parse_ka(data)
         #   print "KA"




    except socket.timeout:
        pass
        #print "T.O"
