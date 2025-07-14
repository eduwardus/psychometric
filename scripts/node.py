class PsychometricNode:
    def __init__(self, node_id, node_type, content=None):
        self.id = node_id
        self.type = node_type  # 'construct', 'item', 'method', 'trait'
        self.content = content
        
        # Propiedades psicométricas básicas
        self.properties = {
            "description": "",
            "irt_parameters": {
                "difficulty": None,
                "discrimination": None,
                "guessing": None
            },
            "classical_metrics": {
                "p_value": None,
                "item_total_correlation": None
            },
            "bias_risk": {
                "dif": None,
                "cultural_bias": None
            }
        }
    
    def set_irt_parameters(self, difficulty, discrimination, guessing=0.0):
        """Establece parámetros de Teoría de Respuesta al Ítem"""
        self.properties["irt_parameters"] = {
            "difficulty": difficulty,
            "discrimination": discrimination,
            "guessing": guessing
        }
    
    def __repr__(self):
        return f"<PsychometricNode: {self.id} ({self.type})>"
