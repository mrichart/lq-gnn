import networkx as nx
from pyvis.network import Network
import json

# Load the graph from a JSON file
with open('data/raw/data_0.json', 'r') as file:
    graph_data = json.load(file)
graph = nx.node_link_graph(graph_data)

nt = Network('800px', '800px', directed=False)
nt.from_nx(graph)
for node in nt.nodes:
    entity = node["entity"]
    if entity == "task":
        node["color"] = "red"
    elif entity == "entry":
        node["color"] = "blue"
    elif entity == "activity":
        node["color"] = "green"
    elif entity == "path":
        node["color"] = "yellow"
nt.show_buttons(filter_=['physics'])
# nt.show_buttons(filter_=['nodes'])
# nt.show_buttons(filter_=['edges'])
nt.toggle_physics(True)
nt.save_graph('directed.html')