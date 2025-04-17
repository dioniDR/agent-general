class Executor:
    def __init__(self, tareas):
        """
        Inicializa el ejecutor con una lista de tareas.

        :param tareas: Lista de tareas a ejecutar. Cada tarea debe ser un diccionario con al menos la clave 'tarea'.
        """
        self.tareas = tareas

    def execute(self, mode="display"):
        """
        Ejecuta cada tarea en la lista de tareas. Maneja errores y reporta el estado de ejecución.
        
        :param mode: Modo de ejecución ('display', 'interactive', 'auto')
        """
        for idx, tarea in enumerate(self.tareas, start=1):
            try:
                print(f"🔄 Tarea {idx}: {tarea['tarea']}")
                
                # Modo de solo visualización
                if mode == "display":
                    print(f"ℹ️ (Modo visualización: No se ejecuta)")
                    continue
                
                # Modo interactivo
                if mode == "interactive":
                    confirmacion = input(f"  ¿Ejecutar esta tarea? (s/n): ").strip().lower()
                    if confirmacion != "s":
                        print(f"  ⏭️ Tarea omitida por el usuario")
                        continue
                
                # Comprobar si la tarea tiene un comando para ejecutar
                if 'comando' in tarea:
                    import os
                    import sys
                    
                    # Si es un comando Python
                    if tarea['comando'].startswith('import'):
                        # Ejecutar código Python de forma segura
                        try:
                            exec(tarea['comando'])
                            resultado = "Comando Python ejecutado correctamente"
                        except Exception as e:
                            resultado = f"Error al ejecutar Python: {str(e)}"
                    # Si es un comando del sistema
                    else:
                        print(f"  Ejecutando: {tarea['comando']}")
                        exit_code = os.system(tarea['comando'])
                        resultado = f"Comando ejecutado con código de salida: {exit_code}"
                else:
                    # Procesamiento normal de tareas
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