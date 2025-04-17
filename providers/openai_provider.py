# providers/openai_provider.py
import os
import datetime
from openai import OpenAI
from dotenv import load_dotenv
from .base_provider import ProviderBase
from .prompt_templates import PromptTemplates

# Asegurarse de que el directorio logs existe
os.makedirs("logs", exist_ok=True)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class OpenAIProvider(ProviderBase):
    def __init__(self, api_key=None):
        # Obtener clave API desde entorno si no se proporciona
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ No se encontró la clave de API de OpenAI.")
        self.client = OpenAI(api_key=self.api_key)
        self.default_model = "gpt-3.5-turbo"

    def generate_text(self, prompt, model=None, max_tokens=150, temperature=0.7, **kwargs):
        try:
            model = model or self.default_model

            # Crear el objeto de petición (request) para poder imprimirlo
            request_data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }

            # Guardar en logs la petición completa
            import json
            with open("logs/openai_requests.log", "a") as f:
                f.write(f"\n\n--- NUEVA PETICIÓN: {datetime.datetime.now()} ---\n")
                f.write(json.dumps(request_data, indent=2))
                f.write("\n\n")

            # También imprimir en la consola
            print("\n=== PETICIÓN A OPENAI ===")
            print(json.dumps(request_data, indent=2))

            # Realizar la petición a la API
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )

            # Guardar también la respuesta en logs
            with open("logs/openai_responses.log", "a") as f:
                f.write(f"\n\n--- RESPUESTA: {datetime.datetime.now()} ---\n")
                f.write(str(response))
                f.write("\n\n")

            # Imprimir la respuesta en la consola
            print("\n=== RESPUESTA DE OPENAI ===")
            print(response)

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"\n=== ERROR EN PETICIÓN A OPENAI ===")
            print(f"Error: {e}")
            raise RuntimeError(f"Failed to generate text: {e}")

    def list_models(self):
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            raise RuntimeError(f"Failed to list models: {e}")

    def generar_tareas(self, objetivo, contexto):
        """
        Genera una lista de tareas basadas en un objetivo y un contexto utilizando OpenAI API.

        :param objetivo: Descripción del objetivo.
        :param contexto: Información de contexto.
        :return: Lista de tareas generadas.
        """
        # Generar un prompt especializado basado en el objetivo
        prompt = self._crear_prompt_especializado(objetivo, contexto)
        
        # Generar la respuesta usando la API
        try:
            response = self.generate_text(prompt, max_tokens=300)
            
            # Procesar la respuesta para extraer comandos
            comandos = []
            for linea in response.strip().split('\n'):
                # Eliminar numeración y espacios
                if '.' in linea[:3]:  # Detectar líneas como "1. comando"
                    comando = linea.split('.', 1)[1].strip()
                    comandos.append({"tarea": f"Ejecutar: {comando}", "comando": comando})
            
            # Si no se encontraron comandos, crear tareas genéricas
            if not comandos:
                tareas = [{"tarea": tarea.strip()} for tarea in response.split("\n") if tarea.strip()]
                return tareas
                
            return comandos
        except Exception as e:
            raise RuntimeError(f"Error al generar tareas: {e}")
    
    def _crear_prompt_especializado(self, objetivo, contexto):
        """
        Crea un prompt especializado basado en el tipo de objetivo.
        
        :param objetivo: Descripción del objetivo.
        :param contexto: Información de contexto.
        :return: Prompt especializado para el modelo.
        """
        # Detectar el tipo de objetivo
        objetivo_lower = objetivo.lower()
        
        # Prompt para información del sistema
        if any(kw in objetivo_lower for kw in ['info sistema', 'información sistema']):
            return (
                "Actúa como un experto en sistemas Linux. "
                "Necesito comandos para mostrar información completa del sistema. "
                "Genera comandos bash que muestren: información del host, CPU, memoria RAM, "
                "uso de disco y versión del sistema operativo. "
                "Usa comandos como hostnamectl, lscpu, free, df, etc. "
                "Preferiblemente en un solo comando con && para encadenarlos. "
                "Lista solo los comandos sin explicaciones adicionales:\n\n"
                "1. [comando]\n"
            )
        
        # Prompt para abrir aplicaciones
        elif any(word in objetivo_lower for word in ['abre', 'abrir', 'ejecuta', 'ejecutar']):
            return (
                "Actúa como un experto en sistemas Linux. "
                f"Necesito comandos para abrir o ejecutar aplicaciones basado en esta solicitud: '{objetivo}'. "
                "Genera comandos que funcionen para la mayoría de distribuciones Linux. "
                "Si es un navegador, considera alternativas como sensible-browser. "
                "Lista solo los comandos sin explicaciones adicionales:\n\n"
                "1. [comando]\n"
            )
        
        # Prompt para operaciones de archivos
        elif any(word in objetivo_lower for word in ['archivo', 'carpeta', 'directorio', 'crear']):
            return (
                "Actúa como un experto en sistemas Linux. "
                f"Necesito comandos para realizar operaciones con archivos o directorios para: '{objetivo}'. "
                "Genera comandos bash que realicen la operación solicitada de manera segura. "
                "Verifica la existencia de archivos/directorios cuando sea necesario. "
                "Añade confirmación del resultado cuando sea posible. "
                "Lista solo los comandos sin explicaciones adicionales:\n\n"
                "1. [comando]\n"
            )
        
        # Prompt por defecto para otras solicitudes
        return PromptTemplates.task_generation_prompt(objetivo, contexto)