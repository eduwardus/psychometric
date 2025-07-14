# En scripts/examples/info_theory_demo.py
import numpy as np
import matplotlib.pyplot as plt
from ..psychometric_graph import PsychometricGraph
from ..versioning.item_selector import adaptive_test

# 1. Crear grafo de prueba (ejemplo con ítems Big5)
graph = PsychometricGraph.example_big5()

# 2. Nivel de habilidad inicial estimado (theta = 0 es promedio)
theta = 0.0  

# 3. Ejecutar test adaptativo en 3 fases
print("🔍 Test Adaptativo Basado en Teoría de la Información")
for phase in range(1, 4):
    result = adaptive_test(graph, theta)
    theta = result['new_theta_estimate']
    
    print(f"\n📌 Fase {phase}: Theta estimado = {theta:.2f}")
    for item in result['selected_items']:
        print(f"  - {item['id']}: Info={item['info']:.2f} (a={item['params']['discrimination']:.1f}, b={item['params']['difficulty']:.1f})")

def plot_information_curve(graph, item_id: str):
    """Grafica la curva de información para un ítem"""
    theta_range = np.linspace(-3, 3, 100)
    item = next(item for item in graph.items if item.id == item_id)
    info = [fisher_information(item, theta) for theta in theta_range]
    
    plt.figure(figsize=(10, 5))
    plt.plot(theta_range, info)
    plt.title(f"Curva de Información - Ítem {item_id}")
    plt.xlabel("Habilidad (theta)")
    plt.ylabel("Información de Fisher")
    plt.grid()
    plt.show()

# Ejemplo:
plot_information_curve(graph, "big5_3")
