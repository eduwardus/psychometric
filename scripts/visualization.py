# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 22:19:24 2025

@author: eggra
"""

# Nuevo archivo visualization.py
import networkx as nx
import matplotlib.pyplot as plt

def plot_graph_with_metadata(graph):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph.graph)
    
    # Dibujar nodos
    nx.draw_networkx_nodes(graph.graph, pos, node_size=700)
    
    # Dibujar aristas con metadatos
    for (source, target), edge in graph.edges.items():
        label = f"{edge.type}\nES={edge.metadata['empirical_support']['effect_size']}"
        nx.draw_networkx_edges(
            graph.graph, pos,
            edgelist=[(source, target)],
            edge_color="gray",
            width=2,
            label=label
        )
    
    nx.draw_networkx_labels(graph.graph, pos, font_size=10)
    plt.legend()
    plt.show()