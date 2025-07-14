class PsychometricEdge:
    def __init__(self, source_id, target_id, relationship_type):
        self.source = source_id
        self.target = target_id
        self.type = relationship_type  # 'measures', 'correlates_with', 'influences'
        
        # Propiedades de la relación
        self.properties = {
            "strength": None,
            "reliability": None,
            "empirical_support": None
        }
    
    def set_strength(self, value):
        """Establece la fuerza de la relación (ej. carga factorial)"""
        self.properties["strength"] = value
    
    def __repr__(self):
        return f"<Edge: {self.source} -> {self.target} ({self.type})>"
