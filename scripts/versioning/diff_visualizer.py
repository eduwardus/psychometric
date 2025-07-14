import matplotlib.pyplot as plt
from typing import List

def plot_version_diffs(versions: List[dict]):
    """
    Compara métricas clave entre versiones
    
    Args:
        versions: Lista de dicts con:
            - fisher_info
            - reliability
            - validity
    """
    fig, ax = plt.subplots(3, 1, figsize=(10, 8))
    
    metrics = ["fisher_info", "reliability", "validity"]
    for i, metric in enumerate(metrics):
        ax[i].plot([v[metric] for v in versions], 'o-')
        ax[i].set_title(metric.capitalize())
    
    plt.tight_layout()
    return fig
