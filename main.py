# main.py

import os
from agent.executor import Executor
from utils.logger import get_logger  # Corrected import
from providers.openai_provider import OpenAIProvider

# Placeholder simples mientras se crean los otros módulos
def get_objective():
    return "Escribir una documentación básica para el proyecto."

def build_context():
    return {"archivos": os.listdir(".")}

def load_settings():
    return {"openai_api_key": os.getenv("OPENAI_API_KEY")}

def main():
    logger = get_logger()  # Corrected logger initialization

    # Cargar configuración
    settings = load_settings()
    api_key = settings.get("openai_api_key")

    if not api_key:
        logger.error("❌ No se encontró la clave de API de OpenAI.")  # Added logging for error
        raise ValueError("❌ No se encontró la clave de API de OpenAI.")

    # Inicializar proveedor
    provider = OpenAIProvider(api_key)

    # Obtener contexto y objetivo
    contexto = build_context()
    objetivo = get_objective()

    # Simulación de tareas (temporal)
    try:
        tareas = provider.generar_tareas(objetivo, contexto)
    except Exception as e:
        logger.error(f"Error al generar tareas: {e}")  # Added error handling
        raise

    executor = Executor(tareas)
    executor.execute()

if __name__ == "__main__":
    main()
