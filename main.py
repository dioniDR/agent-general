# main.py

import os
import sys
from agent.executor import Executor
from utils.logger import get_logger
from providers.openai_provider import OpenAIProvider

def load_settings():
    return {"openai_api_key": os.getenv("OPENAI_API_KEY")}

def build_context():
    return {"archivos": os.listdir(".")}

def print_modes():
    print("🤖 Asistente Inteligente - Modos disponibles:")
    print("1) 📋 Mostrar - Solo muestra las tareas sin ejecutar")
    print("2) 👥 Interactivo - Solicita confirmación antes de ejecutar")
    print("3) 🚀 Automático - Ejecuta las tareas automáticamente (con validación)")
    print("q) ❌ Salir")

def get_user_mode():
    while True:
        print_modes()
        mode = input("\nSelecciona un modo (1-3, q para salir): ").strip()
        
        if mode == "q":
            print("¡Hasta pronto!")
            sys.exit(0)
        
        if mode in ["1", "2", "3"]:
            return {
                "1": "display",
                "2": "interactive",
                "3": "auto"
            }[mode]
        
        print("❌ Opción no válida. Intenta de nuevo.\n")

def get_user_request():
    print("\n💬 ¿Qué quieres que haga? (q para salir)")
    request = input("> ").strip()
    
    if request.lower() == "q":
        print("¡Hasta pronto!")
        sys.exit(0)
        
    return request

def main():
    logger = get_logger()
    
    print("\n🤖 Bienvenido al Asistente Inteligente 🤖\n")
    
    # Cargar configuración
    settings = load_settings()
    api_key = settings.get("openai_api_key")

    if not api_key:
        logger.error("❌ No se encontró la clave de API de OpenAI.")
        print("❌ Se requiere una clave de API de OpenAI para continuar.")
        print("Por favor, configura la variable de entorno OPENAI_API_KEY.")
        return
    
    # Inicializar proveedor
    try:
        provider = OpenAIProvider(api_key)
    except Exception as e:
        logger.error(f"Error al inicializar el proveedor: {e}")
        print(f"❌ Error al inicializar: {e}")
        return
    
    # Obtener modo y petición
    mode = get_user_mode()
    objetivo = get_user_request()
    
    print(f"\n✅ Modo seleccionado: {mode}")
    print(f"📝 Petición: {objetivo}\n")
    
    # Obtener contexto
    contexto = build_context()
    
    # Generar tareas
    try:
        print("🧠 Generando tareas...\n")
        tareas = provider.generar_tareas(objetivo, contexto)
        
        # Mostrar tareas generadas
        print("📋 Tareas generadas:")
        for idx, tarea in enumerate(tareas, start=1):
            print(f"  {idx}. {tarea['tarea']}")
        print()
        
        # Ejecutar según el modo seleccionado
        executor = Executor(tareas)
        
        if mode == "display":
            print("ℹ️ Modo MOSTRAR: Estas tareas pueden ser ejecutadas manualmente.")
        
        elif mode == "interactive":
            confirmacion = input("¿Deseas ejecutar estas tareas? (s/n): ").strip().lower()
            if confirmacion == "s":
                print("\n🚀 Ejecutando tareas...\n")
                executor.execute(mode="interactive")
            else:
                print("\nℹ️ Ejecución cancelada por el usuario.")
        
        elif mode == "auto":
            print("\n🚀 Ejecutando tareas automáticamente...\n")
            executor.execute(mode="auto")
            
    except Exception as e:
        logger.error(f"Error al procesar la petición: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()