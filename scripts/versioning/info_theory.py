import numpy as np
from ..psychometric_graph import PsychometricGraph

def calculate_fisher_info(graph: PsychometricGraph, theta: float = 0.0) -> float:
    """
    Calcula la información de Fisher para el grafo completo en un punto theta.
    Basado en el modelo de respuesta al ítem (IRT).
    """
    total_info = 0.0
    for item in graph.items:
        a = item.params["discrimination"]
        b = item.params["difficulty"]
        p = 1 / (1 + np.exp(-a * (theta - b)))  # Función logística
        total_info += (a ** 2) * p * (1 - p)
    return total_info

def select_optimal_items(graph: PsychometricGraph, theta: float, n_items: int = 5) -> List[str]:
    """Selecciona los ítems más informativos para un nivel de habilidad theta"""
    items = [(item.id, calculate_fisher_info(graph, theta)) for item in graph.items]
    items.sort(key=lambda x: x[1], reverse=True)
    return [item_id for item_id, _ in items[:n_items]]
