import pymc3 as pm
import numpy as np
from ..psychometric_graph import PsychometricGraph

def bayesian_irt_analysis(graph: PsychometricGraph, responses: dict):
    """
    Estima parámetros usando inferencia bayesiana jerárquica
    
    Args:
        responses: {item_id: [respuestas de participantes]}
    
    Returns:
        - Distribuciones posteriores de a, b
        - Intervalos de credibilidad
    """
    with pm.Model() as irt_model:
        # Hiperparámetros
        mu_a = pm.Normal("mu_a", mu=1.0, sigma=0.5)
        sigma_a = pm.HalfNormal("sigma_a", sigma=0.5)
        mu_b = pm.Normal("mu_b", mu=0.0, sigma=1.0)
        
        # Parámetros por ítem
        a = pm.Normal("a", mu=mu_a, sigma=sigma_a, shape=len(graph.items))
        b = pm.Normal("b", mu=mu_b, sigma=1.0, shape=len(graph.items))
        
        # Modelo IRT
        theta = pm.Normal("theta", mu=0, sigma=1, shape=len(responses))
        p = pm.Deterministic("p", 1 / (1 + pm.math.exp(-a * (theta - b))))
        
        # Likelihood
        pm.Bernoulli("obs", p=p, observed=responses)
        
        # Muestreo
        trace = pm.sample(2000, tune=1000, target_accept=0.9)
    
    return trace
