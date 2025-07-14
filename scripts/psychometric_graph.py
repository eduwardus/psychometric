import networkx as nx
from node import PsychometricNode
from edge import PsychometricEdge

class PsychometricGraph:
    def __init__(self):
        """Grafo psicométrico con soporte para metadatos estructurados"""
        self.graph = nx.DiGraph()
        self.nodes = {}  # Dict {node_id: PsychometricNode}
        self.edges = {}  # Dict {(source, target): PsychometricEdge}

    def add_node(self, node_id, node_type, content=None, **kwargs):
        """
        Añade un nodo al grafo.
        Args:
            node_id: Identificador único
            node_type: 'construct', 'item' o 'method'
            content: Descripción/texto del nodo
            kwargs: Propiedades adicionales
        """
        node = PsychometricNode(node_id, node_type, content)
        
        # Añadir propiedades estándar y personalizadas
        for key, value in kwargs.items():
            if hasattr(node, key):
                setattr(node, key, value)
            else:
                node.properties[key] = value
        
        self.graph.add_node(node_id)
        self.nodes[node_id] = node
        return node

    def add_edge(self, source_id, target_id, relationship_type, **kwargs):
        """
        Añade una relación entre nodos con soporte para:
        - Propiedades directas (kwargs sin prefijo)
        - Metadatos (kwargs con prefijo 'meta_')
        """
        if source_id not in self.nodes or target_id not in self.nodes:
            raise ValueError(f"Nodos no encontrados: {source_id} o {target_id}")

        edge = PsychometricEdge(source_id, target_id, relationship_type)
        
        # Separar propiedades de metadatos
        properties = {}
        metadata = {}
        
        for key, value in kwargs.items():
            if key.startswith('meta_'):
                metadata[key[5:]] = value  # Eliminar prefijo
            else:
                properties[key] = value
        
        # Actualizar objetos
        edge.properties.update(properties)
        edge.update_metadata(metadata)
        
        # Registrar en la estructura
        self.graph.add_edge(source_id, target_id)
        self.edges[(source_id, target_id)] = edge
        return edge

    def get_node(self, node_id):
        """Obtiene un nodo por su ID"""
        return self.nodes.get(node_id)

    def get_edges_from(self, node_id):
        """Lista de aristas que salen de un nodo"""
        return [
            self.edges[(node_id, target)] 
            for target in self.graph.successors(node_id)
            if (node_id, target) in self.edges
        ]

    def describe(self):
        """Resumen estadístico del grafo"""
        return {
            'nodes': len(self.nodes),
            'edges': len(self.edges),
            'node_types': {n.type for n in self.nodes.values()},
            'relationship_types': {e.type for e in self.edges.values()}
        }