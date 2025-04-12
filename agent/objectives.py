"""
objectives.py

Este módulo define los objetivos principales del proyecto. Cada objetivo se representa
como una clase que contiene la lógica necesaria para su ejecución y evaluación.
"""

class Objective:
    """
    Clase base para todos los objetivos. Define la interfaz común que todos los
    objetivos deben implementar.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def execute(self):
        """
        Ejecuta el objetivo. Debe ser implementado por las subclases.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def evaluate(self):
        """
        Evalúa el resultado del objetivo. Debe ser implementado por las subclases.
        """
        raise NotImplementedError("Subclasses should implement this method.")

class SpecificObjective(Objective):
    """
    Implementación de un objetivo específico del proyecto.
    """
    def __init__(self, name, description, parameter):
        super().__init__(name, description)
        self.parameter = parameter

    def execute(self):
        """
        Implementa la lógica de ejecución para este objetivo específico.
        """
        # Lógica de ejecución
        print(f"Ejecutando {self.name} con el parámetro {self.parameter}")

    def evaluate(self):
        """
        Implementa la lógica de evaluación para este objetivo específico.
        """
        # Lógica de evaluación
        print(f"Evaluando {self.name}")
        return True

# Ejemplo de uso
if __name__ == "__main__":
    objective = SpecificObjective("Objetivo 1", "Descripción del objetivo 1", "Parámetro X")
    objective.execute()
    result = objective.evaluate()
    print(f"Resultado de la evaluación: {result}")
def get_objective(name=None, description=None):
    """
    Obtiene o crea un objetivo basado en los parámetros dados.
    Si no se proporcionan parámetros, se crea un objetivo por defecto.
    """
    if not name:
        name = "Objetivo por defecto"
        description = "Objetivo creado por defecto"
    
    return SpecificObjective(name, description, "parámetro_default")
