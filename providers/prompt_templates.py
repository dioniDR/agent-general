"""
prompt_templates.py

Este módulo contiene plantillas de prompts reutilizables para los proveedores.
"""

class PromptTemplates:
    """
    Clase que almacena plantillas de prompts para diferentes casos de uso.
    """
    @staticmethod
    def basic_prompt(context, objective):
        """
        Genera un prompt básico basado en el contexto y el objetivo.

        :param context: Información de contexto.
        :param objective: Descripción del objetivo.
        :return: Cadena con el prompt generado.
        """
        return f"Contexto: {context}\n\nObjetivo: {objective}\n\nPor favor, genera una respuesta adecuada."

    @staticmethod
    def task_generation_prompt(objective, constraints):
        """
        Genera un prompt para la creación de tareas basado en un objetivo y restricciones.

        :param objective: Descripción del objetivo.
        :param constraints: Restricciones o condiciones para las tareas.
        :return: Cadena con el prompt generado.
        """
        return (
            f"Objetivo: {objective}\n\n"
            f"Restricciones: {constraints}\n\n"
            "Por favor, genera una lista de tareas que cumplan con el objetivo y las restricciones."
        )

    @staticmethod
    def evaluation_prompt(task, result):
        """
        Genera un prompt para evaluar el resultado de una tarea.

        :param task: Descripción de la tarea.
        :param result: Resultado obtenido de la tarea.
        :return: Cadena con el prompt generado.
        """
        return (
            f"Tarea: {task}\n\n"
            f"Resultado: {result}\n\n"
            "Por favor, evalúa si el resultado cumple con los requisitos de la tarea."
        )


# Ejemplos de uso
if __name__ == "__main__":
    # Ejemplo 1: Prompt básico
    context = "El proyecto es un sistema de gestión de tareas."
    objective = "Crear un módulo para gestionar usuarios."
    print(PromptTemplates.basic_prompt(context, objective))

    # Ejemplo 2: Prompt para generación de tareas
    constraints = "Debe ser escalable y fácil de mantener."
    print(PromptTemplates.task_generation_prompt(objective, constraints))

    # Ejemplo 3: Prompt para evaluación
    task = "Implementar autenticación de usuarios."
    result = "Se implementó autenticación con JWT y almacenamiento seguro de contraseñas."
    print(PromptTemplates.evaluation_prompt(task, result))
