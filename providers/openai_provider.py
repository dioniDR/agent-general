import openai
import os
from dotenv import load_dotenv

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
````