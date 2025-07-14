# genetic_optimizer.py
import copy
import random
import numpy as np
from graph_generator import GraphGenerator
from validator import PsychometricValidator
from evaluator import PsychometricEvaluator

class GeneticOptimizer:
    def __init__(self, base_graph, population_size=12, mutation_rate=0.2):
        self.base_graph = base_graph
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.evaluator = PsychometricEvaluator(n_respondents=3000, n_simulations=3)
        self.validator = PsychometricValidator()
        self.population = self._initialize_population()
        self.best_solution = copy.deepcopy(base_graph)
        self.best_score = self._evaluate_graph(base_graph)
    
    def _evaluate_graph(self, graph):
        """Evalúa un grafo y devuelve su puntuación"""
        if self.validator.validate(graph):
            return self.evaluator.evaluate_graph(graph)["overall_score"]
        return -1
    
    def _initialize_population(self):
        """Crea población inicial con el grafo base y variantes conservadoras"""
        population = [copy.deepcopy(self.base_graph)]  # Grafo original
        
        generator = GraphGenerator(mutation_rate=self.mutation_rate/2)
        for i in range(self.population_size - 1):
            variant = generator.generate_variant(self.base_graph)
            population.append(variant)
        
        return population
    
    def evaluate_population(self):
        """Evalúa y ordena la población por puntuación"""
        evaluated = []
        for graph in self.population:
            # Validar antes de evaluar
            validation_results = self.validator.validate(graph)
            all_valid = all(result["valid"] for result in validation_results.values())
            
            if all_valid:
                score = self._evaluate_graph(graph)
                evaluated.append((score, graph))
                
                # Actualizar mejor solución global
                if score > self.best_score:
                    self.best_score = score
                    self.best_solution = copy.deepcopy(graph)
            else:
                evaluated.append((-1, graph))
        
        # Ordenar de mejor a peor
        evaluated.sort(key=lambda x: x[0], reverse=True)
        return evaluated
    
    def select_parents(self, evaluated_population, elite_size=3):
        """Selección con preservación de élite y diversidad"""
        parents = []
        
        # Élite: los mejores pasan directamente
        elite = [graph for score, graph in evaluated_population[:elite_size] if score > 0]
        parents.extend(elite)
        
        # Mantener diversidad: seleccionar individuos diversos
        valid_candidates = [item for item in evaluated_population if item[0] > 0]
        if len(valid_candidates) > elite_size:
            diverse_sample = random.sample(valid_candidates[elite_size:], 
                                          min(2, len(valid_candidates)-elite_size))
            parents.extend([graph for _, graph in diverse_sample])
        
        # Completar con selección por torneo
        while len(parents) < self.population_size and len(valid_candidates) > 1:
            candidates = random.sample(valid_candidates, min(3, len(valid_candidates)))
            best_candidate = max(candidates, key=lambda x: x[0])
            parents.append(best_candidate[1])
            # Remover para evitar duplicados
            valid_candidates.remove(best_candidate)
        
        # Completar con copias del base si es necesario
        while len(parents) < self.population_size:
            parents.append(copy.deepcopy(self.base_graph))
        
        return parents
    
    def crossover(self, parent1, parent2):
        """Combina dos grafos heredando los mejores parámetros"""
        child_graph = copy.deepcopy(parent1)
        
        for node_id, parent2_node in parent2.nodes.items():
            if node_id in child_graph.nodes and child_graph.nodes[node_id].type == "item":
                child_params = child_graph.nodes[node_id].properties["irt_parameters"]
                parent2_params = parent2_node.properties["irt_parameters"]
                
                # Heredar la mejor discriminación
                if parent2_params["discrimination"] > child_params["discrimination"]:
                    child_params["discrimination"] = parent2_params["discrimination"]
                
                # Heredar dificultad si está más cerca del rango óptimo [-1,1]
                if abs(parent2_params["difficulty"]) < abs(child_params["difficulty"]):
                    child_params["difficulty"] = parent2_params["difficulty"]
        
        return child_graph
    
    def evolve(self, generations=10):
        """Ejecuta el proceso evolutivo mejorado"""
        history = []
        
        for gen in range(generations):
            evaluated = self.evaluate_population()
            best_in_gen = evaluated[0][0]
            
            history.append({
                "generation": gen+1,
                "best_score": best_in_gen,
                "global_best": self.best_score
            })
            
            print(f"Generación {gen+1}: Mejor en Generación = {best_in_gen:.4f}, Mejor Global = {self.best_score:.4f}")
            
            # Seleccionar padres
            parents = self.select_parents(evaluated)
            
            # Crear nueva generación
            new_population = []
            generator = GraphGenerator(mutation_rate=self.mutation_rate)
            
            # Élite directa (los mejores padres)
            new_population.extend(parents[:3])
            
            # Cruzar y mutar
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(parents, 2)
                child = self.crossover(parent1, parent2)
                mutated_child = generator.generate_variant(child)
                new_population.append(mutated_child)
            
            self.population = new_population
        
        return self.best_solution, self.best_score, history