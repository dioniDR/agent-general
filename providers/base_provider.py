# providers/base_provider.py
from abc import ABC, abstractmethod

class ProviderBase(ABC):
    """
    Clase base abstracta para los proveedores de IA.
    Cualquier proveedor debe implementar estos métodos.
    """
    
    @abstractmethod
    def generate_text(self, prompt, **kwargs):
        """
        Genera texto a partir de un prompt.
        
        :param prompt: Prompt para generar texto.
        :param kwargs: Parámetros adicionales específicos del proveedor.
        :return: Texto generado.
        """
        pass
    
    @abstractmethod
    def list_models(self):
        """
        Lista los modelos disponibles para este proveedor.
        
        :return: Lista de modelos disponibles.
        """
        pass
    
    @abstractmethod
    def generar_tareas(self, objetivo, contexto):
        """
        Genera una lista de tareas basadas en un objetivo y un contexto.
        
        :param objetivo: Descripción del objetivo.
        :param contexto: Información de contexto.
        :return: Lista de tareas generadas.
        """
        pass