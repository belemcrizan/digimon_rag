import networkx as nx
import matplotlib.pyplot as plt
import json

def plot_digimon_graph(digimon_name):
    with open("data/digimons.json", "r") as f:
        data = json.load(f)
    G = nx.Graph()

    for d in data:
        if d["nome"].lower() == digimon_name.lower():
            G.add_node(d["nome"])
            for pf in d["pontos_fortes"]:
                G.add_node(pf)
                G.add_edge(d["nome"], pf, label="forte contra")
            for pf in d["pontos_fracos"]:
                G.add_node(pf)
                G.add_edge(d["nome"], pf, label="fraco contra")

    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(f"Grafo do {digimon_name}")
    plt.tight_layout()
    plt.savefig("graph.png")
