import requests
from .template_loader import TemplateLoader
from ..core.validator import PsychometricValidator

class PsyToolkitAdapter:
    BASE_URL = "https://www.psytoolkit.org/api/v2"
    
    @classmethod
    def search_templates(cls, query: str) -> list:
        response = requests.get(f"{cls.BASE_URL}/search", params={"q": query})
        return response.json().get("items", [])
    
    @classmethod
    def import_template(cls, toolkit_id: str) -> PsychometricGraph:
        response = requests.get(f"{cls.BASE_URL}/questionnaires/{toolkit_id}")
        raw_data = response.json()
        
        # Transformación básica
        graph_data = {
            "metadata": {
                "source": "PsyToolkit",
                "original_id": toolkit_id
            },
            "nodes": cls._convert_nodes(raw_data),
            "edges": cls._convert_relationships(raw_data)
        }
        
        graph = PsychometricGraph.from_dict(graph_data)
        return PsychometricValidator.validate(graph)
    
    @staticmethod
    def _convert_nodes(toolkit_data: dict) -> list:
        # Implementa la conversión específica aquí
        pass
