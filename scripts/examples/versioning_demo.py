from scripts.psychometric_graph import PsychometricGraph
from scripts.versioning.graph_vc import GraphVersionControl

# 1. Crear/importar grafo
graph = PsychometricGraph.load_from_file("test.json")

# 2. Inicializar control de versiones
vc = GraphVersionControl()
vc.commit(graph, "Versión inicial")

# 3. Optimizar y guardar nueva versión
optimized_graph = genetic_algorithm.optimize(graph)
vc.commit(optimized_graph, "Post-optimización")

# 4. Seleccionar mejores ítems para theta=0.5 (habilidad media)
best_items = select_optimal_items(optimized_graph, theta=0.5)
