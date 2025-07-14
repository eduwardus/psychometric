import hashlib
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass
from ..psychometric_graph import PsychometricGraph

@dataclass
class GraphVersion:
    hash: str
    timestamp: str
    message: str
    metrics: Dict[str, float]  # Información de Fisher, confiabilidad, etc.

class GraphVersionControl:
    def __init__(self):
        self.versions: List[GraphVersion] = []
    
    def commit(self, graph: PsychometricGraph, message: str = "") -> str:
        """Guarda una versión del grafo con sus métricas clave"""
        version_hash = self._generate_hash(graph)
        version = GraphVersion(
            hash=version_hash,
            timestamp=datetime.now().isoformat(),
            message=message,
            metrics=self._calculate_metrics(graph)
        )
        self.versions.append(version)
        return version_hash

    def _generate_hash(self, graph: PsychometricGraph) -> str:
        """Genera un hash único basado en el contenido del grafo"""
        graph_data = graph.serialize()
        return hashlib.sha256(graph_data.encode()).hexdigest()[:8]

    def _calculate_metrics(self, graph: PsychometricGraph) -> Dict[str, float]:
        """Calcula métricas psicométricas usando teoría de la información"""
        from .info_theory import calculate_fisher_info
        return {
            "fisher_info": calculate_fisher_info(graph),
            "reliability": graph.calculate_reliability(),
            "validity": graph.calculate_validity()
        }
