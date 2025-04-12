import openai
import os
from dotenv import load_dotenv
from .prompt_templates import PromptTemplates  # Importar las plantillas de prompts

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class OpenAIProvider:
    def __init__(self, api_key=None):
        # Obtener clave API desde entorno si no se proporciona
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ No se encontró la clave de API de OpenAI.")
        openai.api_key = self.api_key

    def generate_text(self, prompt, model="text-davinci-003", max_tokens=150, temperature=0.7):
        try:
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].text.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to generate text: {e}")

    def list_models(self):
        try:
            models = openai.Model.list()
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
        try:
            # Usar la plantilla de prompt para generación de tareas
            prompt = PromptTemplates.task_generation_prompt(objetivo, contexto)
            response = self.generate_text(prompt, model="text-davinci-003", max_tokens=200)
            # Procesar la respuesta para convertirla en una lista de tareas
            tareas = [{"tarea": tarea.strip()} for tarea in response.split("\n") if tarea.strip()]
            return tareas
        except Exception as e:
            raise RuntimeError(f"Error al generar tareas: {e}")
