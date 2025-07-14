class PsychometricNode:
    def __init__(self, node_id, node_type, content=None):
        self.id = node_id
        self.type = node_type
        self.content = content
        self.properties = self._create_initial_properties()
    
    def _create_initial_properties(self):
        # Propiedades base para todos los nodos
        base_props = {
            "description": "",
            "bias_risk": {
                "dif": None,
                "cultural_bias": None
            }
        }
        
        # Propiedades específicas por tipo de nodo
        if self.type == "construct":
            base_props.update({
                "content_domains": [],
                "theoretical_framework": ""
            })
        elif self.type == "item":
            base_props.update({
                "irt_parameters": {
                    "difficulty": None,
                    "discrimination": None,
                    "guessing": None
                },
                "classical_metrics": {
                    "p_value": None,
                    "item_total_correlation": None
                }
            })
        elif self.type == "method":
            base_props.update({
                "response_options": []
            })
            
        return base_props