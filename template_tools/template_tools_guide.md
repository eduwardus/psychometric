# 📚 Guía Completa del Sistema de Plantillas Psicométricas

## 🌟 Introducción
Sistema integrado para gestión de plantillas psicométricas con soporte para:
- Creación manual de tests
- Importación desde fuentes externas
- Optimización mediante algoritmos genéticos

```python
from template_tools import TemplateLoader, PsyToolkitAdapter
from core.genetic_algorithm import GeneticOptimizer


🛠 1. Creación Manual de Plantillas
Estructura Básica

Crea un archivo JSON con esta estructura:
json

{
    "metadata": {
        "name": "mi_test",
        "author": "Tu Nombre",
        "version": "1.0"
    },
    "nodes": [
        {
            "id": "item1",
            "type": "item",
            "content": "Me siento optimista sobre el futuro",
            "response_options": ["Nunca", "A veces", "Siempre"],
            "parameters": {
                "dificultad": 0.5,
                "discriminacion": 1.2
            }
        }
    ],
    "edges": [
        {
            "source": "item1",
            "target": "optimismo",
            "weight": 0.75
        }
    ]
}

Conversión a Grafo Psicométrico
python

mi_plantilla = TemplateLoader.load_from_file("mi_test.json")

# Edición directa
mi_plantilla.nodes["item1"].parameters["dificultad"] = 0.6

🧬 2. Integración con Algoritmo Genético
Optimización de Parámetros
python

from core.genetic_algorithm import GeneticOptimizer

# Configuración del algoritmo
optimizador = GeneticOptimizer(
    population_size=50,
    mutation_rate=0.1,
    elite_count=5
)

# Función de evaluación personalizada
def evaluar_test(grafo):
    return grafo.calculate_reliability() * 0.6 + grafo.validity_index() * 0.4

# Ejecutar optimización
mejor_grafo = optimizador.run(
    graph_template=mi_plantilla,
    evaluation_func=evaluar_test,
    generations=100
)

Mutaciones Personalizadas
python

# En genetic_algorithm.py
class CustomMutator:
    def mutate_item_parameters(self, item):
        # Mutación para parámetros IRT
        item.parameters["dificultad"] += random.gauss(0, 0.1)
        item.parameters["discriminacion"] = max(0.5, item.parameters["discriminacion"] * random.uniform(0.9, 1.1))
        
        # Mutación de contenido (ejemplo)
        if random.random() < 0.05:
            item.content = self.sinonimizar(item.content)
            
    def sinonimizar(self, texto):
        # Implementar lógica de sinonimización
        return texto_modificado

# Uso:
optimizador = GeneticOptimizer(mutator=CustomMutator())

🔄 3. Flujo Completo de Trabajo
Diagram
Code
📊 4. Ejemplo Avanzado: Optimización de Escala DEP-10
python

# 1. Importar plantilla base
dep10 = PsyToolkitAdapter.import_template("DEP10")

# 2. Configurar optimización
def evaluacion_depresion(grafo):
    fiabilidad = grafo.calculate_cronbach_alpha()
    validez = grafo.calculate_criterion_validity()
    return fiabilidad * 0.7 + validez * 0.3

optimizador = GeneticOptimizer(
    population_size=100,
    mutation_rate=0.15,
    selection_params={
        'tournament_size': 7,
        'elitism': True
    }
)
## 🔄 3a. Flujo Completo de Trabajo

```mermaid
graph TD
    A[Crear/Importar Plantilla] --> B[Validación Inicial]
    B --> C{¿Requiere optimización?}
    C -->|Sí| D[Ejecutar Algoritmo Genético]
    C -->|No| E[Usar Directamente]
    D --> F[Evaluar Resultados]
    F --> G[Exportar Test Final]
# 3b. Ejecutar por 200 generaciones
resultados = optimizador.run(
    graph_template=dep10,
    evaluation_func=evaluacion_depresion,
    generations=200,
    verbose=True
)

# 4. Exportar mejor versión
resultados.best_graph.export_to("dep10_optimized.json")

⚠️ 5. Troubleshooting Común

Problema: Error al importar de PsyToolkit
✅ Solución: Verifica:
python

print(PsyToolkitAdapter.check_api_status())  # Debe devolver 200

Problema: Baja fitness en algoritmo genético
✅ Solución: Ajustar:

    Aumentar population_size

    Reducir mutation_rate

    Revisar función de evaluación

📌 6. Mejores Prácticas

    Versionado: Guarda cada iteración del grafo

    Validación: Siempre valida después de mutaciones

    Logging: Registra los parámetros de cada ejecución

python

# Ejemplo de registro
with open("optimization_log.jsonl", "a") as f:
    f.write(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "params": optimizador.get_params(),
        "best_fitness": resultados.best_fitness
    }) + "\n")

🚀 7. Próximos Pasos

    Implementar más operadores de mutación

    Añadir soporte para Catell's 16PF

    Integrar con bancos de ítems públicos
