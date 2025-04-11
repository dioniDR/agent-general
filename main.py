# main.py

import os
from dotenv import load_dotenv
from agent.executor import Executor
from agent.objectives import get_objective
from agent.context import build_context
from config.settings import load_settings
from providers.openai_provider import OpenAIProvider
from utils.logger import setup_logger

def main():
    # Configurar logger
    setup_logger()

    # Cargar configuración
    settings = load_settings()

    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener clave API desde entorno o settings
    api_key = os.getenv("OPENAI_API_KEY") or settings.get("openai_api_key")
    if not api_key:
        raise ValueError("❌ No se encontró la clave de API de OpenAI.")

    # Inicializar proveedor OpenAI
    provider = OpenAIProvider(api_key=api_key)

    # Construir contexto inicial del agente
    contexto = build_context()

    # Obtener objetivo desde settings o prompt
    objetivo = get_objective()

    # Preparar tareas
    tareas = provider.generar_tareas(objetivo, contexto)

    # Ejecutar tareas con el ejecutor
    executor = Executor(tareas)
    executor.execute()

if __name__ == "__main__":
    main()
