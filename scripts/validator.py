class PsychometricValidator:
    def __init__(self):
        self.constraints = [
            self.check_content_validity,
            self.check_construct_coverage
        ]
    
    def validate(self, graph):
        """Ejecuta todas las validaciones en el grafo"""
        results = {}
        for constraint in self.constraints:
            constraint_name = constraint.__name__
            results[constraint_name] = constraint(graph)
        return results
    
    def check_content_validity(self, graph):
        """Verifica que los constructos tengan cobertura de contenido"""
        errors = []
        for node_id, node in graph.nodes.items():
            if node.type == "construct":
                # Verificación simplificada
                if not node.properties.get("content_domains"):
                    errors.append(f"Constructo {node_id} no tiene dominios de contenido definidos")
        return {"valid": len(errors) == 0, "errors": errors}
    
    def check_construct_coverage(self, graph):
        """Verifica que cada constructo tenga ítems que lo midan"""
        coverage = {}
        for (source, target), edge in graph.edges.items():
            if edge.type == "measures":
                if target not in coverage:
                    coverage[target] = 0
                coverage[target] += 1
        
        errors = []
        for node_id, node in graph.nodes.items():
            if node.type == "construct" and coverage.get(node_id, 0) < 3:
                errors.append(f"Constructo {node_id} tiene menos de 3 ítems")
        
        return {"valid": len(errors) == 0, "errors": errors}
