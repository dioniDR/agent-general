class Executor:
    def __init__(self, tareas):
        """
        Inicializa el ejecutor con una lista de tareas.

        :param tareas: Lista de tareas a ejecutar. Cada tarea debe ser un diccionario con al menos la clave 'tarea'.
        """
        self.tareas = tareas

    def execute(self):
        """
        Ejecuta cada tarea en la lista de tareas. Maneja errores y reporta el estado de ejecución.
        """
        for idx, tarea in enumerate(self.tareas, start=1):
            try:
                print(f"🔄 Ejecutando tarea {idx}: {tarea['tarea']}")
                # Simulación de ejecución de la tarea
                # Aquí se puede agregar lógica específica para cada tarea
                resultado = self._procesar_tarea(tarea)
                print(f"✅ Tarea {idx} completada: {resultado}")
            except Exception as e:
                print(f"❌ Error al ejecutar la tarea {idx}: {e}")

    def _procesar_tarea(self, tarea):
        """
        Procesa una tarea específica. Este método puede ser extendido para manejar diferentes tipos de tareas.

        :param tarea: Diccionario con la información de la tarea.
        :return: Resultado de la tarea.
        """
        # Simulación de procesamiento (puede ser reemplazado con lógica real)
        if not tarea.get("tarea"):
            raise ValueError("La tarea no contiene una descripción válida.")
        return f"Resultado de '{tarea['tarea']}'"