# En scripts/examples/info_theory_demo.py
import numpy as np
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
