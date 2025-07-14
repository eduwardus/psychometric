from psychometric_graph import PsychometricGraph
from validator import PsychometricValidator
from evaluator import PsychometricEvaluator
from graph_generator import GraphGenerator
from genetic_optimizer import GeneticOptimizer
import json
import numpy as np
import matplotlib.pyplot as plt

def build_valid_graph():
    """Construye un grafo psicométrico válido con metadatos"""
    graph = PsychometricGraph()
    
    # 1. Constructos con dominios definidos
    depression = graph.add_node(
        "depression", "construct",
        content_domains=["afecto negativo", "déficit cognitivo", "alteraciones somáticas"],
        theoretical_framework="DSM-5"
    )
    
    anxiety = graph.add_node(
        "anxiety", "construct",
        content_domains=["preocupación excesiva", "tensión muscular", "hiperactivación autonómica"],
        theoretical_framework="Teoría de Barlow"
    )
    
    # 2. Método de respuesta
    graph.add_node(
        "likert_5", "method",
        response_options=["Nunca", "Raramente", "A veces", "Frecuentemente", "Siempre"]
    )
    
    # 3. Ítems para depresión (3+)
    dep_items = [
        {"id": "dep1", "d": 0.7, "a": 1.2, "content": "Me siento triste"},
        {"id": "dep2", "d": 0.8, "a": 1.4, "content": "Pérdida de interés"},
        {"id": "dep3", "d": 0.6, "a": 0.9, "content": "Problemas de sueño"},
        {"id": "dep4", "d": 0.5, "a": 1.1, "content": "Fatiga constante"}
    ]
    
    for item in dep_items:
        graph.add_node(
            item["id"], "item",
            content=item["content"],
            irt_parameters={
                "difficulty": item["d"],
                "discrimination": item["a"],
                "guessing": 0.0
            }
        )
        graph.add_edge(
            item["id"], "depression", "measures",
            strength=item["a"],
            meta_reliability=np.random.uniform(0.7, 0.9)
        )
        graph.add_edge(item["id"], "likert_5", "uses_method")
    
    # 4. Ítems para ansiedad (3+)
    anx_items = [
        {"id": "anx1", "d": 0.4, "a": 1.3, "content": "Preocupación excesiva"},
        {"id": "anx2", "d": 0.7, "a": 1.5, "content": "Sensación de peligro"},
        {"id": "anx3", "d": 0.3, "a": 0.8, "content": "Taquicardias"}
    ]
    
    for item in anx_items:
        graph.add_node(
            item["id"], "item",
            content=item["content"],
            irt_parameters={
                "difficulty": item["d"],
                "discrimination": item["a"],
                "guessing": 0.0
            }
        )
        graph.add_edge(
            item["id"], "anxiety", "measures",
            strength=item["a"],
            meta_reliability=np.random.uniform(0.7, 0.9)
        )
        graph.add_edge(item["id"], "likert_5", "uses_method")
    
    # 5. Correlación con soporte empírico
    graph.add_edge(
        "anxiety", "depression", "correlates_with",
        correlation=0.72,
        strength=0.65,
        empirical_support="Estudio de comorbilidad (2020), DOI:10.1037/1234-5678"
    )
    
    return graph

def main():
    # 1. Construir grafo válido
    print("=== CONSTRUYENDO GRAFO VÁLIDO ===")
    base_graph = build_valid_graph()
    validator = PsychometricValidator()
    
    # 2. Validación
    print("\n=== VALIDACIÓN ===")
    validation = validator.validate(base_graph)
    valid = True
    
    for check, result in validation.items():
        status = "✅" if result["valid"] else "❌"
        print(f"{check}: {status}")
        if not result["valid"]:
            valid = False
            for error in result["errors"]:
                print(f"  - {error}")
    
    if not valid:
        print("\nCorrige los errores antes de continuar")
        return
    
    # 3. Evaluación inicial
    print("\n=== EVALUACIÓN INICIAL ===")
    evaluator = PsychometricEvaluator(n_respondents=3000, n_simulations=3)
    base_metrics = evaluator.evaluate_graph(base_graph)
    print("Métricas iniciales:")
    for metric, value in base_metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    # 4. Optimización Genética
    print("\n=== OPTIMIZACIÓN GENÉTICA ===")
    optimizer = GeneticOptimizer(
        base_graph=base_graph,
        population_size=12,
        mutation_rate=0.2
    )
    
    best_graph, best_score, history = optimizer.evolve(generations=10)
    print(f"\n● Mejor puntuación: {best_score:.4f}")
    print(f"● Mejora: {(best_score - base_metrics['overall_score'])*100:.2f}%")
    
    # 5. Análisis de resultados
    print("\n=== ANÁLISIS DE RESULTADOS ===")
    
    # 5.1. Comparación de métricas
    optimized_metrics = evaluator.evaluate_graph(best_graph)
    print("\nComparación de métricas:")
    print(f"{'Métrica':<20} {'Original':<10} {'Optimizado':<10} {'Mejora':<10}")
    for metric in base_metrics:
        orig = base_metrics[metric]
        opt = optimized_metrics[metric]
        improvement = opt - orig
        print(f"{metric:<20} {orig:.4f}     {opt:.4f}     {improvement:+.4f}")
    
    # 5.2. Cambios en parámetros IRT
    print("\nCambios significativos en parámetros IRT:")
    for node_id in base_graph.nodes:
        if base_graph.get_node(node_id).type == "item":
            orig_node = base_graph.get_node(node_id)
            best_node = best_graph.get_node(node_id)
            
            orig_params = orig_node.properties.get("irt_parameters", {})
            best_params = best_node.properties.get("irt_parameters", {})
            
            diff_dif = best_params.get("difficulty", 0) - orig_params.get("difficulty", 0)
            diff_disc = best_params.get("discrimination", 0) - orig_params.get("discrimination", 0)
            
            if abs(diff_dif) > 0.05 or abs(diff_disc) > 0.1:
                print(f"Ítem {node_id}:")
                print(f"  Original: difficulty={orig_params.get('difficulty', 0):.2f}, discrimination={orig_params.get('discrimination', 0):.2f}")
                print(f"  Optimizado: difficulty={best_params.get('difficulty', 0):.2f}, discrimination={best_params.get('discrimination', 0):.2f}")
    
    # 5.3. Evolución de la optimización
    generations = [h["generation"] for h in history]
    scores = [h["best_score"] for h in history]
    
    plt.figure(figsize=(10, 6))
    plt.plot(generations, scores, 'o-', label="Mejor por generación")
    plt.axhline(y=base_metrics["overall_score"], color='r', linestyle='--', label="Original")
    plt.xlabel("Generación")
    plt.ylabel("Puntuación")
    plt.title("Evolución de la Optimización Genética")
    plt.legend()
    plt.grid(True)
    plt.savefig("optimization_evolution.png")
    print("\nGráfico de evolución guardado en 'optimization_evolution.png'")
    
    # 6. Exportar resultados
    print("\n=== EXPORTANDO RESULTADOS ===")
    results = {
        "validation": validation,
        "metrics": {
            "initial": base_metrics,
            "optimized": optimized_metrics
        },
        "best_graph": {
            "nodes": {n_id: vars(n) for n_id, n in best_graph.nodes.items()},
            "edges": {f"{s}-{t}": vars(e) for (s,t), e in best_graph.edges.items()}
        },
        "optimization_history": history
    }
    
    with open("optimized_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Proceso completado. Resultados en 'optimized_results.json'")

if __name__ == "__main__":
    main()