# Inicialización
vc = PsychometricVersionControl()

# Primer commit
graph = PsychometricGraph()  # Grafo inicial
v1_hash = vc.commit(graph, "Versión inicial")

# Modificación y nuevo commit
graph.nodes["item1"].content = "Texto modificado"
v2_hash = vc.commit(graph, "Modificación ítem 1")

# Análisis bayesiano
responses = {"item1": [1,0,1,0,1], "item2": [0,1,0,1,0]}
vc.run_bayesian_analysis(v2_hash, responses)

# Visualización
vc.plot_version_history("fisher_information").savefig("evolucion.png")
