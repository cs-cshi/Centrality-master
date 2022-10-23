import networkx as nx
from simulator.graph_extractor import *
import matplotlib.pyplot as plt

G = nx.MultiDiGraph()
data_path = '../../data/test.flows'
# data_path = '../../data/rg17_data/raw/rg17_mentions.csv'
extractor = GraphExtractor(data_path)
flows = extractor.extract_edges()
edges = []
for flow in flows:
    edges.append((flow.get_src, flow.get_dst, {'timestamp': flow.get_timestamp}))
print(edges)
G.add_edges_from(edges)
print(len(G.edges))
print(len(G.nodes))
# graphml_output_path = '../../data/graph/test_flow.graphml'
# nx.write_graphml(G, graphml_output_path)
pos = nx.spring_layout(G)
#pos = nx.random_layout(G)
nx.draw(G, pos, node_color='b', edge_color='r', with_labels=False, font_size=18, node_size=20)
#nx.draw(G,  node_color='b', edge_color='r', with_labels=False, font_size=18, node_size=20)

plt.show()
# connectionstyle='arc3, rad = 0.2'arc控制双向，rad调线条弧度
