class PsychometricEdge:
    def __init__(self, source_id, target_id, relationship_type):
        """
        Representa una relación en el grafo psicométrico con:
        - source: Nodo origen
        - target: Nodo destino
        - type: Tipo de relación ('measures', 'correlates_with', etc.)
        - properties: Atributos operacionales (dict)
        - metadata: Información auxiliar estructurada (dict)
        """
        self.source = source_id
        self.target = target_id
        self.type = relationship_type
        self.properties = {}  # Propiedades directas (ej: strength, correlation)
        self.metadata = {     # Metadatos estructurados
            'psychometric': {
                'reliability': None,
                'validity': {
                    'convergent': None,
                    'discriminant': None
                }
            },
            'empirical': {
                'studies': [],
                'effect_size': None,
                'confidence_interval': None
            }
        }

    def update_metadata(self, metadata_dict):
        """Actualiza metadatos con soporte para anidación mediante puntos"""
        for key, value in metadata_dict.items():
            if '.' in key:
                # Manejo de metadatos anidados (ej: 'psychometric.reliability')
                keys = key.split('.')
                current = self.metadata
                for k in keys[:-1]:
                    if k not in current:
                        current[k] = {}
                    current = current[k]
                current[keys[-1]] = value
            else:
                # Metadatos de primer nivel
                self.metadata[key] = value

    def __repr__(self):
        return f"<Edge {self.source}→{self.target} ({self.type})>"