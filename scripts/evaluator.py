import numpy as np
from scipy.stats import pearsonr

class PsychometricEvaluator:
    def __init__(self, n_respondents=3000, n_simulations=3, theta_mean=0, theta_std=1):
        self.n_respondents = n_respondents
        self.n_simulations = n_simulations
        self.theta_mean = theta_mean
        self.theta_std = theta_std
        
    def evaluate_graph(self, graph):
        """Evalúa el grafo psicométrico con múltiples simulaciones"""
        all_metrics = []
        for _ in range(self.n_simulations):
            metrics = self._evaluate_single_run(graph)
            all_metrics.append(metrics)
        
        # Calcular promedios
        avg_metrics = {}
        for key in all_metrics[0].keys():
            avg_metrics[key] = np.mean([m[key] for m in all_metrics])
        
        # Ponderación de métricas (Asegúrate de que coincida con las métricas calculadas)
        weights = {
            "reliability": 0.35,
            "validity": 0.25,
            "discrimination_power": 0.15,
            "model_fit": 0.15,
            "bias_indicators": 0.10
        }
        
        # Calcular puntuación global solo si las métricas existen
        avg_metrics["overall_score"] = sum(avg_metrics[k] * weights[k] for k in weights if k in avg_metrics)
        return avg_metrics
    
    def _evaluate_single_run(self, graph):
        """Ejecuta una sola evaluación del grafo"""
        response_data = self.simulate_responses(graph)
        return {
            "reliability": self.calculate_reliability(graph, response_data),
            "validity": self.calculate_validity(graph),
            "discrimination_power": self.calculate_discrimination(graph),
            "model_fit": self.calculate_model_fit(graph),
            "bias_indicators": self.calculate_bias_indicators(graph, response_data)
        }
    
    # --- Métodos de simulación y cálculo (copiados desde test_graph.py) ---
    def simulate_responses(self, graph):
        """Simula respuestas para todos los ítems del grafo usando modelos IRT"""
        items = [node_id for node_id, node in graph.nodes.items() if node.type == "item"]
        n_items = len(items)
        
        if n_items == 0:
            return {
                'theta': np.array([]),
                'responses': np.zeros((self.n_respondents, 0)),
                'item_ids': []
            }
        
        # Generar habilidades latentes (theta)
        theta = np.random.normal(self.theta_mean, self.theta_std, self.n_respondents)
        responses = np.zeros((self.n_respondents, n_items))
        
        for j, item_id in enumerate(items):
            item_node = graph.get_node(item_id)
            params = item_node.properties.get("irt_parameters", {})
            difficulty = params.get("difficulty", 0.5)
            discrimination = params.get("discrimination", 1.0)
            guessing = params.get("guessing", 0.0)
            
            logit = discrimination * (theta - difficulty)
            prob = guessing + (1 - guessing) / (1 + np.exp(-logit))
            responses[:, j] = (prob > np.random.uniform(0, 1, self.n_respondents)).astype(int)
        
        return {
            'theta': theta,
            'responses': responses,
            'item_ids': items
        }
    
    def calculate_reliability(self, graph, response_data):
        """Calcula la fiabilidad promedio (Alfa de Cronbach) por constructo"""
        responses = response_data['responses']
        item_ids = response_data['item_ids']
        
        if responses.size == 0:
            return 0.0
        
        reliabilities = []
        construct_items = {}
        
        # Agrupar ítems por constructo
        for (source, target), edge in graph.edges.items():
            if edge.type == "measures":
                if target not in construct_items:
                    construct_items[target] = []
                if source in item_ids:
                    construct_items[target].append(item_ids.index(source))
        
        # Calcular fiabilidad para cada constructo
        for construct, item_indices in construct_items.items():
            if len(item_indices) < 2:
                continue
                
            construct_responses = responses[:, item_indices]
            n_items = len(item_indices)
            item_vars = np.var(construct_responses, axis=0, ddof=1)
            total_scores = np.sum(construct_responses, axis=1)
            total_var = np.var(total_scores, ddof=1)
            
            if total_var > 1e-10:
                alpha = (n_items / (n_items - 1)) * (1 - np.sum(item_vars) / total_var)
                reliabilities.append(max(0, min(1, alpha)))
        
        return np.mean(reliabilities) if reliabilities else 0.0
    
    def calculate_validity(self, graph):
        """Calcula la validez convergente promedio"""
        validities = []
        
        for (source, target), edge in graph.edges.items():
            if edge.type == "measures":
                strength = edge.properties.get("strength")
                if strength is None:
                    item_node = graph.get_node(source)
                    if item_node and item_node.type == "item":
                        strength = item_node.properties.get("irt_parameters", {}).get("discrimination", 1.0)
                    else:
                        strength = 1.0
                
                validity = min(1.0, max(0.3, abs(strength) * 0.7)) 
                validities.append(validity)
        
        return np.mean(validities) if validities else 0.0
    
    def calculate_discrimination(self, graph):
        """Calcula el poder discriminativo promedio"""
        discriminations = []
        
        for node_id, node in graph.nodes.items():
            if node.type == "item":
                discrimination = node.properties.get("irt_parameters", {}).get("discrimination", 0)
                normalized = (discrimination - 0.3) / (3.0 - 0.3)
                discriminations.append(max(0, min(1, normalized)))
        
        return np.mean(discriminations) if discriminations else 0.0
    
    def calculate_model_fit(self, graph):
        """Calcula el ajuste del modelo"""
        fit_score = 0.7  # Valor base
        
        for (source, target), edge in graph.edges.items():
            if edge.type == "correlates_with":
                if "empirical_support" in edge.properties:
                    fit_score += 0.05
                if "correlation" in edge.properties:
                    fit_score += 0.03
        
        # Penalizar constructos con pocos ítems
        construct_items = {}
        for (source, target), edge in graph.edges.items():
            if edge.type == "measures":
                if target not in construct_items:
                    construct_items[target] = 0
                construct_items[target] += 1
        
        for count in construct_items.values():
            if count < 3:
                fit_score -= 0.1
            elif count > 5:
                fit_score += 0.05
        
        return max(0.5, min(0.95, fit_score))
    
    def calculate_bias_indicators(self, graph, response_data):
        """Calcula indicadores de sesgo potencial (DIF simplificado)"""
        responses = response_data['responses']
        item_ids = response_data['item_ids']
        
        if responses.size == 0:
            return 1.0
        
        group = np.random.choice([0, 1], size=self.n_respondents)
        bias_scores = []
        
        for item_id in item_ids:
            item_idx = item_ids.index(item_id)
            item_responses = responses[:, item_idx]
            group0_mean = np.mean(item_responses[group == 0])
            group1_mean = np.mean(item_responses[group == 1])
            diff = abs(group0_mean - group1_mean)
            bias_score = 1.0 - min(1.0, diff * 3)
            bias_scores.append(bias_score)
        
        return np.mean(bias_scores) if bias_scores else 1.0