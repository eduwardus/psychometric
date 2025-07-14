from psychometric_graph import PsychometricGraph

# Crear un nuevo grafo psicométrico
graph = PsychometricGraph()

# Añadir constructos (rasgos latentes)
depression = graph.add_node(
    "depression",
    "construct",
    description="Nivel de depresión",
    content_domains=["afecto", "cognición", "somatización"]
)

anxiety = graph.add_node(
    "anxiety",
    "construct",
    description="Nivel de ansiedad",
    content_domains=["afecto", "síntomas físicos"]
)

# Añadir ítems
item1 = graph.add_node(
    "item1",
    "item",
    content="Me siento triste la mayor parte del tiempo"
)

item2 = graph.add_node(
    "item2",
    "item",
    content="Me preocupo excesivamente por cosas pequeñas"
)

# Establecer relaciones
graph.add_edge("item1", "depression", "measures", strength=0.85)
graph.add_edge("item2", "anxiety", "measures", strength=0.78)
graph.add_edge("anxiety", "depression", "correlates_with", strength=0.65)

# Describir el grafo
print("Descripción del grafo:", graph.describe())

# Validar el grafo
from validator import PsychometricValidator
validator = PsychometricValidator()
validation_results = validator.validate(graph)
print("\nResultados de validación:", validation_results)
