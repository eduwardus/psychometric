"""
Demo del Sistema de Versionado
Ejecutar con: python -m scripts.examples.versioning_demo
"""
from ..versioning.graph_vc import GraphVersionControl
from ..psychometric_graph import PsychometricGraph

def demo_version_system():
    print("🔄 Iniciando demo del sistema de versionado...")
    
    # 1. Crear grafo de prueba
    graph = PsychometricGraph.example()  # Asume que tienes este método
    
    # 2. Inicializar control de versiones
    vc = GraphVersionControl()
    v1_hash = vc.commit(graph, "Versión inicial")
    print(f"✅ Commit inicial: {v1_hash}")
    
    # 3. Simular cambio (ej: optimización)
    graph.nodes["item1"].params["difficulty"] = 0.7
    v2_hash = vc.commit(graph, "Ajuste de parámetros")
    
    # 4. Mostrar diferencias
    diff = vc.diff(v1_hash, v2_hash)
    print(f"\n📊 Diferencias entre versiones:")
    print(f"Fisher Info: {diff['delta_fisher']:+.3f}")
    print(f"Confiabilidad: {diff['delta_reliability']:+.3f}")

if __name__ == "__main__":
    demo_version_system()
