import json
from pathlib import Path
from typing import Dict, Any
from ..core.psychometric_graph import PsychometricGraph

class TemplateLoader:
    @staticmethod
    def load_from_file(file_path: str) -> PsychometricGraph:
        """Carga plantilla desde archivo local"""
        with open(file_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        return PsychometricGraph.from_dict(template_data)
    
    @staticmethod
    def load_builtin(template_name: str) -> PsychometricGraph:
        """Carga plantillas incluidas en el paquete"""
        builtin_path = Path(__file__).parent / 'builtin_templates' / f"{template_name}.json"
        return TemplateLoader.load_from_file(builtin_path)
