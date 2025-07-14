# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 22:04:16 2025

@author: eggra
"""

# En un nuevo archivo metadata.py
class MetadataFactory:
    @staticmethod
    def create_metadata(edge_type):
        templates = {
            "measures": {
                "factor_loading": None,
                "cross_loadings": {}
            },
            "correlates_with": {
                "partial_correlation": None,
                "mediation_analysis": {}
            },
            "uses_method": {
                "response_bias_analysis": {
                    "mean_response_time": None,
                    "social_desirability": None
                }
            }
        }
        return templates.get(edge_type, {})

class MetadataBuilder:
    @staticmethod
    def build_edge_metadata(edge_type, **kwargs):
        """Construye metadatos estructurados para cualquier tipo de arista"""
        base = {
            "measures": {"factor_loading": None},
            "correlates_with": {"empirical_support": {}},
            # ... otros tipos
        }.get(edge_type, {})
        
        # Actualizar con valores proporcionados
        for key, value in kwargs.items():
            keys = key.split('__')  # Separador para anidación
            current = base
            for k in keys[:-1]:
                current = current.setdefault(k, {})
            current[keys[-1]] = value
            
        return base