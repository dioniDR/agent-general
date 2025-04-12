import os
from dotenv import load_dotenv

class Context:
    def __init__(self, env_file='.env'):
        self.config = {}
        self.load_environment_variables(env_file)

    def load_environment_variables(self, env_file):
        # Cargar variables de entorno desde el archivo .env
        load_dotenv(env_file)
        for key, value in os.environ.items():
            self.config[key] = value

    def get(self, key, default=None):
        return self.config.get(key, os.getenv(key, default))
def build_context(env_file='.env'):
    """
    Construye y devuelve un objeto Context inicializado con el archivo
    de entorno especificado.
    """
    return Context(env_file)
