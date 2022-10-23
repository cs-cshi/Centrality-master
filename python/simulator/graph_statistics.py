from simulator.graph_extractor import *
import networkx as nx

# 1. flows
# data_path = '../../data/equinix-chicago.dirA.20160121-125911.UTC.anon3.flows'
# data_path = '../../data/SAT-03-11-2018_01.flows'
data_path = '../../data/maccdc2012_00000.flows'
# data_path = '../../data/botnet-capture-20110815-fast-flux-2.flows'
graph_extractor = GraphExtractor(data_path)
edges = [(edge.get_src(), edge.get_dst(), {'timestamp': edge.get_timestamp(), 'size': edge.get_length()}) for edge in
         graph_extractor.extract_edges()]
print(edges)
G = nx.MultiDiGraph()
G.add_edges_from(edges)
print('number of nodes: ' + str(G.number_of_nodes()))
print('number of edges: ' + str(G.number_of_edges()))

# 2. tennis
# data_path = '../../data/rg17_data/raw/rg17_mentions_test.csv'
# graph_extractor = GraphExtractor(data_path)
# edges = [(edge.get_src(), edge.get_dst()) for edge in graph_extractor.extract_edges()]
# print(len(edges))
# G = nx.MultiDiGraph()
# G.add_edges_from(edges)
# print(G.number_of_nodes())
# print(G.number_of_edges())

# 3. flows src_dst test
# data_path = '../../data/equinix-chicago.dirA.20160121-125911.UTC.anon1.flows'
# graph_extractor = GraphExtractor(data_path)
# src_set = set([edge.get_src() for edge in graph_extractor.extract_edges()])
# dst_set = set([edge.get_dst() for edge in graph_extractor.extract_edges()])
# all_set = src_set | dst_set
# print('src_set: ' + str(len(src_set)))
# print('dst_set: ' + str(len(dst_set)))
# print('all_set: ' + str(len(all_set)))
# a = {1, 2, 3}
# b = {3, 4, 5}
# c = a | b
# print(c)
