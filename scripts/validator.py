class PsychometricValidator:
    def __init__(self):
        self.constraints = [
            self.check_content_validity,
            self.check_construct_coverage,
            self.check_method_assignment,
            self.check_irt_parameters,
            self.check_correlation_strength
        ]
    
    def validate(self, graph):
        """Ejecuta todas las validaciones en el grafo"""
        results = {}
        for constraint in self.constraints:
            constraint_name = constraint.__name__
            try:
                results[constraint_name] = constraint(graph)
            except Exception as e:
                results[constraint_name] = {
                    "valid": False,
                    "errors": [f"Error durante la validación: {str(e)}"]
                }
        return results
    
    def check_content_validity(self, graph):
        """Verifica que los constructos tengan cobertura de contenido"""
        errors = []
        for node_id, node in graph.nodes.items():
            if node.type == "construct":
                # Verificar que tiene dominios de contenido definidos
                content_domains = node.properties.get("content_domains", [])
                if not content_domains:
                    errors.append(f"Constructo {node_id} no tiene dominios de contenido definidos")
                
                # Verificar que tiene marco teórico
                theoretical_framework = node.properties.get("theoretical_framework", "")
                if not theoretical_framework:
                    errors.append(f"Constructo {node_id} no tiene marco teórico definido")
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def check_construct_coverage(self, graph):
        """Verifica que cada constructo tenga al menos 3 ítems que lo midan"""
        construct_items = {}
        
        # Contar cuántos ítems tiene cada constructo
        for (source, target), edge in graph.edges.items():
            if edge.type == "measures":
                if target not in construct_items:
                    construct_items[target] = 0
                construct_items[target] += 1
        
        errors = []
        for node_id, node in graph.nodes.items():
            if node.type == "construct":
                item_count = construct_items.get(node_id, 0)
                if item_count < 3:
                    errors.append(f"Constructo {node_id} tiene solo {item_count} ítems (mínimo requerido: 3)")
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def check_method_assignment(self, graph):
        """Verifica que todos los ítems tengan un método de respuesta asignado"""
        items_with_method = set()
        items_without_method = set()
        
        # Identificar todos los ítems
        for node_id, node in graph.nodes.items():
            if node.type == "item":
                items_without_method.add(node_id)
        
        # Verificar relaciones "uses_method"
        for (source, target), edge in graph.edges.items():
            if edge.type == "uses_method":
                if source in items_without_method:
                    items_without_method.remove(source)
                    items_with_method.add(source)
        
        errors = [f"El ítem {item_id} no tiene método de respuesta asignado" 
                 for item_id in items_without_method]
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def check_irt_parameters(self, graph):
        """Verifica que los parámetros IRT de los ítems estén dentro de rangos válidos"""
        errors = []
        
        for node_id, node in graph.nodes.items():
            if node.type == "item":
                irt_params = node.properties.get("irt_parameters", {})
                
                # Verificar dificultad
                difficulty = irt_params.get("difficulty")
                if difficulty is not None:
                    if not (-3.0 <= difficulty <= 3.0):
                        errors.append(f"Ítem {node_id}: Dificultad {difficulty} fuera de rango [-3.0, 3.0]")
                
                # Verificar discriminación
                discrimination = irt_params.get("discrimination")
                if discrimination is not None:
                    if discrimination < 0.3 or discrimination > 3.0:
                        errors.append(f"Ítem {node_id}: Discriminación {discrimination} fuera de rango [0.3, 3.0]")
                
                # Verificar guessing
                guessing = irt_params.get("guessing")
                if guessing is not None:
                    if guessing < 0.0 or guessing > 0.5:
                        errors.append(f"Ítem {node_id}: Parámetro de azar {guessing} fuera de rango [0.0, 0.5]")
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def check_correlation_strength(self, graph):
        """Verifica que las correlaciones entre constructos sean razonables"""
        errors = []
        
        for (source, target), edge in graph.edges.items():
            if edge.type == "correlates_with":
                strength = edge.properties.get("strength")
                correlation = edge.properties.get("correlation")
                
                # Verificar que al menos una medida de fuerza esté presente
                if strength is None and correlation is None:
                    errors.append(f"Relación {source}-{target}: Falta especificar strength o correlation")
                    continue
                
                # Usar correlation si está disponible, sino usar strength
                value = correlation if correlation is not None else strength
                
                if value is not None:
                    # Verificar rango
                    if not (-1.0 <= value <= 1.0):
                        errors.append(f"Relación {source}-{target}: Valor {value} fuera de rango [-1.0, 1.0]")
                    
                    # Verificar que no sea correlación perfecta
                    if abs(value) > 0.95:
                        errors.append(f"Relación {source}-{target}: Correlación {value} demasiado alta (>0.95)")
                    
                    # Verificar soporte empírico para correlaciones fuertes
                    if abs(value) > 0.7:
                        empirical_support = edge.properties.get("empirical_support")
                        if not empirical_support:
                            errors.append(f"Relación {source}-{target}: Correlación fuerte ({value}) sin soporte empírico")
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def validate_metadata(self, graph):
        errors = []
        for edge in graph.edges.values():
            if edge.type == "measures" and not edge.metadata.get("psychometric_properties.reliability"):
                errors.append(f"Falta confiabilidad en relación {edge.source}->{edge.target}")
            
            if "effect_size" in edge.metadata["empirical_support"]:
                es = edge.metadata["empirical_support"]["effect_size"]
                if not (-1 <= es <= 1):
                    errors.append(f"Tamaño de efecto inválido en {edge.source}->{edge.target}")
        
        return {"valid": len(errors) == 0, "errors": errors}