import numpy as np
from .info_theory import fisher_information

def select_items(graph, theta: float, n_items: int = 5) -> List[Dict]:
    """
    Selecciona los ítems más informativos para un nivel de habilidad theta
    
    Returns:
        Lista de ítems ordenados por información descendente
        Ejemplo: [{'id': 'item1', 'info': 1.34, 'content': "Pregunta..."}, ...]
    """
    items_with_info = []
    for item in graph.items:
        info = fisher_information(item, theta)
        items_with_info.append({
            'id': item.id,
            'info': info,
            'content': item.content,
            'params': item.params
        })
    
    # Ordenar por información y seleccionar top N
    items_with_info.sort(key=lambda x: x['info'], reverse=True)
    return items_with_info[:n_items]

def adaptive_test(graph, theta_estimate: float, items_to_select: int = 5) -> Dict:
    """
    Test adaptativo: selecciona ítems basados en la estimación actual de theta
    
    Returns:
        Dict con ítems seleccionados y nueva estimación de theta
    """
    selected_items = select_items(graph, theta_estimate, items_to_select)
    
    # Simulación: nueva estimación de theta (usando promedio ponderado)
    total_info = sum(item['info'] for item in selected_items)
    new_theta = theta_estimate + sum(
        (item['params']['difficulty'] * item['info'] for item in selected_items)
    ) / total_info if total_info > 0 else theta_estimate
    
    return {
        'selected_items': selected_items,
        'new_theta_estimate': new_theta,
        'total_information': total_info
    }
