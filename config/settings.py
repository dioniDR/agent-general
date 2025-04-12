import os
import yaml
from pathlib import Path

def load_settings(config_file="config/settings.yaml"):
    """
    Carga la configuración desde un archivo YAML.
    Si el archivo no existe, crea una configuración por defecto.
    """
    config_path = Path(config_file)
    
    if not config_path.exists():
        # Crear configuración por defecto
        create_default_settings(config_path)
    
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def create_default_settings(config_path):
    """
    Crea un archivo de configuración por defecto.
    """
    default_settings = {
        'debug': True,
        'log_level': 'INFO',
        'providers': {
            'openai': {
                'model': 'text-davinci-003',
                'max_tokens': 150,
                'temperature': 0.7
            },
            'claude': {
                'enabled': False
            }
        }
    }
    
    # Asegurar que existe el directorio
    os.makedirs(config_path.parent, exist_ok=True)
    
    # Escribir configuración por defecto
    with open(config_path, 'w') as file:
        yaml.dump(default_settings, file, default_flow_style=False)
