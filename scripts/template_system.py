# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 23:18:33 2025

@author: eggra
"""

# En archivo template_system.py
class PsychometricTemplate:
    TEMPLATES = {
        "depression_scale": {
            "description": "Escala breve de depresión (6 ítems)",
            "constructs": {
                "depression": {
                    "domains": ["afecto", "cognición", "somático"],
                    "min_items": 3
                }
            },
            "items": [
                {
                    "id": "dep1",
                    "content": "Me siento triste",
                    "irt_params": {"difficulty": 0.5, "discrimination": 1.0},
                    "required": True
                },
                {
                    "id": "dep2",
                    "content": "Pérdida de interés",
                    "irt_params": {"difficulty": 0.7, "discrimination": 1.2}
                }
            ],
            "relationships": [
                {
                    "source": "dep1", 
                    "target": "depression", 
                    "type": "measures",
                    "metadata": {
                        "factor_loading": 0.7,
                        "validation": {"study": "PMID:123456"}
                    }
                }
            ],
            "validation_rules": {
                "min_reliability": 0.7,
                "max_difficulty_variance": 0.3
            }
        },
        "big5": {
            "description": "Modelo de 5 factores de personalidad",
            "constructs": ["extraversion", "neuroticism", "conscientiousness", "agreeableness", "openness"],
            # ... estructura similar
        }
    }

    @classmethod
    def create_from_template(cls, template_name, custom_params={}):
        """Genera un grafo psicométrico desde una plantilla"""
        template = cls.TEMPLATES.get(template_name)
        if not template:
            raise ValueError(f"Plantilla {template_name} no encontrada")

        graph = PsychometricGraph()
        
        # 1. Añadir constructos
        for construct, config in template["constructs"].items():
            graph.add_node(
                construct, "construct",
                content_domains=config["domains"],
                theoretical_framework="From template"
            )
        
        # 2. Añadir ítems
        for item in template["items"]:
            graph.add_node(
                item["id"], "item",
                content=item["content"],
                irt_parameters=item.get("irt_params", {})
            )
        
        # 3. Establecer relaciones
        for rel in template["relationships"]:
            graph.add_edge(
                rel["source"], rel["target"], rel["type"],
                **rel.get("metadata", {})
            )
        
        return graph