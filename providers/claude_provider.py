# providers/claude_provider.py
import os
import requests
from .base_provider import ProviderBase
from .prompt_templates import PromptTemplates

class ClaudeProvider(ProviderBase):
    def __init__(self, api_key=None, base_url="https://api.anthropic.com/v1"):
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided")
        self.base_url = base_url
        self.default_model = "claude-3-haiku-20240307"

    def generate_text(self, prompt, model=None, max_tokens=150, temperature=0.7, **kwargs):
        try:
            model = model or self.default_model
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(f"{self.base_url}/messages", headers=headers, json=data)
            response.raise_for_status()
            
            return response.json()["content"][0]["text"]
        except Exception as e:
            raise RuntimeError(f"Failed to generate text: {e}")

    def list_models(self):
        # Claude API might not support listing models directly
        # Return hardcoded list of known models
        return ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]

    def generar_tareas(self, objetivo, contexto):
        """
        Genera una lista de tareas basadas en un objetivo y un contexto utilizando Claude API.

        :param objetivo: Descripción del objetivo.
        :param contexto: Información de contexto.
        :return: Lista de tareas generadas.
        """
        # Usar el mismo método que en OpenAIProvider para crear prompt especializado
        prompt = self._crear_prompt_especializado(objetivo, contexto)
        
        try:
            response = self.generate_text(prompt, max_tokens=300)
            
            # Procesar la respuesta (mismo código que en OpenAIProvider)
            comandos = []
            for linea in response.strip().split('\n'):
                if '.' in linea[:3]:
                    comando = linea.split('.', 1)[1].strip()
                    comandos.append({"tarea": f"Ejecutar: {comando}", "comando": comando})
            
            if not comandos:
                tareas = [{"tarea": tarea.strip()} for tarea in response.split("\n") if tarea.strip()]
                return tareas
                
            return comandos
        except Exception as e:
            raise RuntimeError(f"Error al generar tareas: {e}")
    
    # Reutilizamos la lógica de crear prompts especializados
    def _crear_prompt_especializado(self, objetivo, contexto):
        # La misma implementación que en OpenAIProvider
        # (Podríamos extraer esto a una clase auxiliar para evitar duplicación)
        objetivo_lower = objetivo.lower()
        
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
        
        # ...resto de la lógica igual que en OpenAIProvider...
        
        # Prompt por defecto
        return PromptTemplates.task_generation_prompt(objetivo, contexto)