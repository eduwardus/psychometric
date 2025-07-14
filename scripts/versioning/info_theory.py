import numpy as np
from typing import List, Dict
from ..psychometric_graph import Item

def fisher_information(item: Item, theta: float) -> float:
    """
    Calcula la información de Fisher para un ítem en un nivel de habilidad theta (IRT 2PL)
    
    Args:
        item: Objeto ítem con parámetros 'discrimination' (a) y 'difficulty' (b)
        theta: Nivel de habilidad del evaluado
    
    Returns:
        Información de Fisher para el ítem en theta
    """
    a = item.params['discrimination']
    b = item.params['difficulty']
    p = 1 / (1 + np.exp(-a * (theta - b)))  # Función de respuesta al ítem
    return (a ** 2) * p * (1 - p)

def test_information_curve(graph, theta_range: np.ndarray) -> Dict[str, List[float]]:
    """
    Genera curvas de información para todos los ítems
    
    Returns:
        Dict: {item_id: [info_theta1, info_theta2, ...]}
    """
    return {
        item.id: [fisher_information(item, theta) for theta in theta_range]
        for item in graph.items
    }
