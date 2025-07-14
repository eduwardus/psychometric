import networkx as nx
from node import PsychometricNode
from edge import PsychometricEdge

class PsychometricGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes = {}
        self.edges = {}
    
    def add_node(self, node_id, node_type, content=None, **properties):
        """Añade un nodo psicométrico al grafo"""
        node = PsychometricNode(node_id, node_type, content)
        
        # Añadir propiedades personalizadas
        for key, value in properties.items():
            if key in node.properties:
                node.properties[key] = value
            else:
                # Propiedades no estándar
                node.properties[key] = value
        
        self.graph.add_node(node_id)
        self.nodes[node_id] = node
        return node
    
    def add_edge(self, source_id, target_id, relationship_type, **properties):
        """Añade una relación psicométrica entre nodos"""
        if source_id not in self.nodes or target_id not in self.nodes:
            raise ValueError("Los nodos fuente o destino no existen")
        
        edge = PsychometricEdge(source_id, target_id, relationship_type)
        
        # Añadir propiedades personalizadas
        for key, value in properties.items():
            if key in edge.properties:
                edge.properties[key] = value
            else:
                edge.properties[key] = value
        
        self.graph.add_edge(source_id, target_id)
        self.edges[(source_id, target_id)] = edge
        return edge
    
    def get_node(self, node_id):
        """Obtiene un nodo por ID"""
        return self.nodes.get(node_id)
    
    def get_edges_from(self, node_id):
        """Obtiene todas las aristas que salen de un nodo"""
        return [self.edges[(node_id, target)] 
                for target in self.graph.successors(node_id) 
                if (node_id, target) in self.edges]
    
    def describe(self):
        """Provee una descripción básica del grafo"""
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "node_types": {node.type for node in self.nodes.values()}
        }
