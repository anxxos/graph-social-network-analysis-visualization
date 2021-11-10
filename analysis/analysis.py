# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 22:32:44 2019

@author: Ángeles Blanco Fernández
@title: SWIFT Graph Analytics

Análisis de Grafos y Redes Sociales
Máster en Data Science
ETSII - URJC
"""
#%%
# Libraries

import json
import pandas as pd
import networkx as nx
from networkx.readwrite import json_graph
from networkx.algorithms import community
#from infomap import infomap

#%%
# Reading and transforming data

swift_messages = pd.read_csv('../data/tokenized_df.csv', delimiter=',')
#swift_messages = swift_messages[swift_messages.swift_value_date < '14/02/2019']

debtor_to_sender = swift_messages.drop(['swift_receiver_message_id',
                                       'swift_beneficiary_customer_desc'], 
                                       axis=1)
debtor_to_sender.rename(columns={'swift_debtor_desc': 'source',
                                 'swift_sender_message_id': 'target'},
                        inplace=True)

sender_to_receiver = swift_messages.drop(['swift_beneficiary_customer_desc',
                                         'swift_debtor_desc'], axis=1)
sender_to_receiver.rename(columns={'swift_sender_message_id': 'source',
                                   'swift_receiver_message_id': 'target'},
                          inplace=True)

debtor_to_receiver = swift_messages.drop(['swift_beneficiary_customer_desc',
                                          'swift_sender_message_id'], axis=1)
debtor_to_receiver.rename(columns={'swift_debtor_desc': 'source',
                                   'swift_receiver_message_id': 'target'},
                          inplace=True)

receiver_to_beneficiary = swift_messages.drop(['swift_sender_message_id',
                                              'swift_debtor_desc'], axis=1)
receiver_to_beneficiary.rename(columns={'swift_receiver_message_id': 'source',
                                        'swift_beneficiary_customer_desc': 'target'},
                               inplace=True)

edges_messages = pd.concat([debtor_to_sender, sender_to_receiver, 
                            receiver_to_beneficiary], ignore_index=True)
#edges_messages = pd.concat([debtor_to_receiver, 
#                            receiver_to_beneficiary], ignore_index=True)
#%%
# Generating graph from dataframe

DG = nx.from_pandas_edgelist(edges_messages, source='source', target='target',
                             edge_attr=True, create_using=nx.DiGraph())

#%%
# Adding attributes from analysis

# Dijkstra for distances calculation

# Degree centrality 
# Normalized number of incoming and outgoing edges
# Definex the 'strongest' vertex in DG
in_centrality = nx.in_degree_centrality(DG)
out_centrality = nx.out_degree_centrality(DG)
nx.set_node_attributes(DG, in_centrality, 'in-degree')
nx.set_node_attributes(DG, out_centrality, 'out-degree')

# Closeness centrality CL(v) = 1/cumsum(dist(v,u))
# This meassure assumes that our graph is connected, which in this case
# is a good assumption
# Defines the most reachable vertex in DG
closeness_centrality = nx.closeness_centrality(DG)
nx.set_node_attributes(DG, closeness_centrality, 'closeness')

# Betweenness centrality BC(v) = cumsum(q(s,t|v)/q(s,t))
# It's the number of shortest paths between s and t passing by v,
# divided by the number of shortest paths between s and t
# Based on the importance of a vertex appearing in many paths
# Defines the flux controller of DG
betweenness_centrality = nx.betweenness_centrality(DG)
nx.set_node_attributes(DG, betweenness_centrality, 'betweenness')
# Edge betweenness centrality
edge_betweenness_centrality = nx.edge_betweenness_centrality(DG)
nx.set_edge_attributes(DG, edge_betweenness_centrality, 'edge_betweenness')

# Eigenvector centrality 
# Calculated from the adjacency matrix
# Based upon the importance of each vertex incoming neighbours
eigenvector_centrality = nx.eigenvector_centrality(DG, max_iter=200)
nx.set_node_attributes(DG, eigenvector_centrality, 'eigenvector')

# Pagerank centrality
# First algorithm used by Google Search to rank web pages 
# in their search engine results
# PageRank works by counting the number and quality of links 
# to determine a rough estimate of how important the node is. 
# The underlying assumption is that more important nodes are likely 
# to receive more links from other nodes
pagerank_centrality = nx.pagerank(DG)
nx.set_node_attributes(DG, pagerank_centrality, 'pagerank')

# Let's check the best ones
bestDG = max(in_centrality, key=lambda key: in_centrality[key])
bestDG2  = max(out_centrality, key=lambda key: out_centrality[key])
bestCL = max(closeness_centrality, key=lambda key: closeness_centrality[key])
bestBT = max(betweenness_centrality, key=lambda key: betweenness_centrality[key])
bestEG = max(eigenvector_centrality, key=lambda key: eigenvector_centrality[key])
bestPR = max(pagerank_centrality, key=lambda key: pagerank_centrality[key])

print("In-degree: "+ bestDG + " -> {0:.2f}".format(in_centrality[bestDG]))
print("Out-degree: "+ bestDG2 + " -> {0:.2f}".format(out_centrality[bestDG]))
print("Closeness: "+ bestCL + " -> {0:.2f}".format(closeness_centrality[bestCL]))
print("Betweenness: "+ bestBT + " -> {0:.2f}".format(betweenness_centrality[bestBT]))
print("Eigenvector: "+ bestEG + " -> {0:.2f}".format(eigenvector_centrality[bestEG]))
print("PageRank: "+ bestPR + " -> {0:.2f}".format(pagerank_centrality[bestPR]))

# Adding communities with Girvan-Newman algorithm

# The Girvan–Newman algorithm detects communities by progressively removing 
# edges from the original network. The connected components of the remaining 
# network are the communities. Instead of trying to construct a measure that 
# tells us which edges are the most central to communities, the Girvan–Newman 
# algorithm focuses on edges that are most likely "between" communities.
communities_generator = community.girvan_newman(DG)
top = next(communities_generator)
middle = next(communities_generator)
last = next(communities_generator)
bottom = next(communities_generator)
communities = {}
iterator = 0
for community_dict in bottom:
    for node in community_dict:
        communities[node] = iterator
    iterator += 1
nx.set_node_attributes(DG, communities, 'community')   

#%%

# Community detection with Infomap algorithm

# This would be the best option, 
# but it does not work with current versions of the library in the PIP 
# repository and gives problems when installing directly from GitHub package

def findCommunities(G):
	"""
    Author: Che Yulin https://github.com/YcheCourseProject
	Partition network with the Infomap algorithm.
	Annotates nodes with 'community' id and returns number of communities found.
	"""
	conf = infomap.init("--two-level");
	# Input data
	network = infomap.Network(conf);
	# Output data
	tree = infomap.HierarchicalNetwork(conf)

	print("Building network...")
	for e in G.edges_iter():
		network.addLink(*e)

	network.finalizeAndCheckNetwork(True, nx.number_of_nodes(G));

	# Cluster network
	infomap.run(network, tree);

	print("Found %d top modules with codelength: %f" % (tree.numTopModules(), tree.codelength()))

	communities = {}
	clusterIndexLevel = 1 # 1, 2, ... or -1 for top, second, ... or lowest cluster level
	for node in tree.leafIter(clusterIndexLevel):
		communities[node.originalLeafIndex] = node.clusterIndex()

	nx.set_node_attributes(G, 'community', communities)
    
	return tree.numTopModules()

findCommunities(DG)

#%%
# Writing JSON

data = json_graph.node_link_data(DG)
nodes = data['nodes']
for node in nodes:
    if node['id'].startswith('bank') == True:
        node['icon'] = 'icons/bank_2.PNG'
        node['font'] = '\uf19c'
        node['type'] = 'bank'
    elif node['id'] in list(swift_messages.swift_debtor_desc):
        node['icon'] = 'icons/building.PNG'
        node['font'] = '\uf594'
        node['type'] = 'client'
    else:
        node['icon'] = 'icons/person.PNG'
        node['type'] = 'customer'
        node['font'] = '\uf508'
data['nodes'] = nodes
   
with open('data/data.json', 'w') as outfile:
    json.dump(data, outfile)