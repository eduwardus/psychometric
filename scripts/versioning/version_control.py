"""
Sistema de Versionado para Grafos Psicométricos
Incorpora:
- Control de versiones al estilo Git
- Métricas de teoría de la información
- Integración con análisis bayesiano
- Visualización de diferencias
"""

import hashlib
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import numpy as np
import matplotlib.pyplot as plt
import pymc3 as pm
from .info_theory import calculate_fisher_information

# ----------------------------
# ESTRUCTURAS DE DATOS
# ----------------------------

@dataclass
class GraphVersion:
    """Representa una versión específica del grafo psicométrico"""
    hash: str
    timestamp: str
    message: str
    graph_data: dict
    metrics: Dict[str, float] = field(default_factory=dict)
    bayesian_data: Optional[dict] = None

    def add_metric(self, name: str, value: float):
        self.metrics[name] = value

    def add_bayesian_analysis(self, trace):
        """Almacena resultados del análisis bayesiano"""
        self.bayesian_data = {
            'item_params': {
                'a_mean': np.mean(trace['a'], axis=0),
                'b_hdi': pm.stats.hdi(trace['b'])
            },
            'theta_mean': np.mean(trace['theta'])
        }

# ----------------------------
# CONTROL DE VERSIONES
# ----------------------------

class PsychometricVersionControl:
    """Sistema de versionado Git-like para grafos psicométricos"""
    
    def __init__(self):
        self.versions: List[GraphVersion] = []
        self.current_branch = "main"
    
    def commit(self, graph, message: str = "", calculate_metrics: bool = True) -> str:
        """
        Registra una nueva versión del grafo
        
        Args:
            graph: PsychometricGraph a versionar
            message: Mensaje descriptivo del commit
            calculate_metrics: Si True, calcula métricas automáticamente
            
        Returns:
            Hash de la versión creada
        """
        # Generar hash único
        graph_data = graph.serialize()
        version_hash = self._generate_hash(graph_data)
        
        # Crear nueva versión
        new_version = GraphVersion(
            hash=version_hash[:8],
            timestamp=datetime.now().isoformat(),
            message=message,
            graph_data=graph_data
        )
        
        # Calcular métricas básicas
        if calculate_metrics:
            self._calculate_basic_metrics(new_version, graph)
        
        self.versions.append(new_version)
        return version_hash
    
    def _calculate_basic_metrics(self, version: GraphVersion, graph):
        """Calcula métricas psicométricas clave"""
        # Teoría de la información
        version.add_metric(
            'fisher_information',
            calculate_fisher_information(graph, theta=0.0)  # Punto medio de habilidad
        )
        
        # Métricas clásicas (ejemplo)
        version.add_metric('reliability', graph.calculate_reliability())
        version.add_metric('validity', graph.calculate_validity())
    
    def run_bayesian_analysis(self, version_hash: str, response_data: Dict[str, list]):
        """
        Ejecuta análisis bayesiano para una versión específica
        
        Args:
            version_hash: Hash de la versión a analizar
            response_data: Diccionario con respuestas {item_id: [0,1,1,...]}
        """
        version = self.get_version(version_hash)
        if not version:
            raise ValueError(f"Versión no encontrada: {version_hash}")
        
        with pm.Model() as irt_model:
            # Hiperparámetros (distribuciones previas)
            mu_a = pm.Normal('mu_a', mu=1.0, sigma=0.5)
            sigma_a = pm.HalfNormal('sigma_a', sigma=0.5)
            mu_b = pm.Normal('mu_b', mu=0.0, sigma=1.0)
            
            # Parámetros por ítem
            a = pm.Normal('a', mu=mu_a, sigma=sigma_a, shape=len(version.graph_data['items']))
            b = pm.Normal('b', mu=mu_b, sigma=1.0, shape=len(version.graph_data['items']))
            
            # Habilidad de los participantes
            theta = pm.Normal('theta', mu=0, sigma=1, shape=len(next(iter(response_data.values()))))
            
            # Modelo IRT
            p = pm.Deterministic(
                'p',
                1 / (1 + pm.math.exp(-a * (theta - b)[:, np.newaxis]))
            )
            
            # Likelihood
            pm.Bernoulli(
                'obs',
                p=p[list(response_data.keys())],
                observed=np.array(list(response_data.values())).T
            )
            
            # Muestreo MCMC
            trace = pm.sample(
                2000,
                tune=1000,
                target_accept=0.9,
                return_inferencedata=False
            )
        
        version.add_bayesian_analysis(trace)
    
    def diff(self, hash_a: str, hash_b: str) -> Dict[str, dict]:
        """
        Compara dos versiones del grafo
        
        Returns:
            Dict con:
            - metrics_diff: Diferencias en métricas
            - bayesian_diff: Comparación parámetros bayesianos
            - items_changed: Ítems modificados
        """
        v_a = self.get_version(hash_a)
        v_b = self.get_version(hash_b)
        
        if not v_a or not v_b:
            raise ValueError("Una o ambas versiones no existen")
        
        # Comparar métricas básicas
        metrics_diff = {
            metric: v_b.metrics.get(metric, 0) - v_a.metrics.get(metric, 0)
            for metric in set(v_a.metrics) | set(v_b.metrics)
        }
        
        # Comparar análisis bayesiano (si existen)
        bayesian_diff = {}
        if v_a.bayesian_data and v_b.bayesian_data:
            bayesian_diff = {
                'delta_a': v_b.bayesian_data['item_params']['a_mean'] - v_a.bayesian_data['item_params']['a_mean'],
                'delta_b': v_b.bayesian_data['item_params']['b_hdi'][0] - v_a.bayesian_data['item_params']['b_hdi'][0]
            }
        
        return {
            'metrics_diff': metrics_diff,
            'bayesian_diff': bayesian_diff,
            'items_changed': self._find_changed_items(v_a, v_b)
        }
    
    def plot_version_history(self, metric: str = 'fisher_information'):
        """Genera gráfico de evolución de una métrica"""
        if not self.versions:
            raise ValueError("No hay versiones registradas")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        x = [v.timestamp for v in self.versions]
        y = [v.metrics.get(metric, 0) for v in self.versions]
        
        ax.plot(x, y, 'o-')
        ax.set_title(f'Evolución de {metric}')
        ax.set_xlabel('Versión')
        ax.set_ylabel(metric)
        plt.xticks(rotation=45)
        
        return fig

# ----------------------------
# MÉTODOS AUXILIARES
# ----------------------------

    def _generate_hash(self, graph_data: dict) -> str:
        """Genera hash SHA-256 para el grafo"""
        serialized = str(graph_data).encode('utf-8')
        return hashlib.sha256(serialized).hexdigest()
    
    def get_version(self, version_hash: str) -> Optional[GraphVersion]:
        """Recupera una versión por su hash"""
        for version in self.versions:
            if version.hash == version_hash[:8]:
                return version
        return None
    
    def _find_changed_items(self, v_a: GraphVersion, v_b: GraphVersion) -> List[str]:
        """Identifica ítems con cambios significativos"""
        changed = []
        for item in v_a.graph_data['items']:
            item_b = next(
                (it for it in v_b.graph_data['items'] if it['id'] == item['id']),
                None
            )
            if item_b and item['content'] != item_b['content']:
                changed.append(item['id'])
        return changed

# ----------------------------
# INTERFAZ DE USUARIO
# ----------------------------

    def show_log(self):
        """Muestra historial de versiones al estilo git log"""
        print(f"Branch: {self.current_branch}")
        print("{:<8} {:<20} {}".format("Hash", "Fecha", "Mensaje"))
        for version in reversed(self.versions):
            print("{:<8} {:<20} {}".format(
                version.hash,
                version.timestamp[:19],
                version.message
            ))
