#!/usr/bin/env python3
"""
Script para corregir problemas identificados en el proyecto agent-general.
Ejecutar desde la raíz del proyecto.
"""

import os
import sys
from pathlib import Path

def print_colored(text, color_code):
    """Imprime texto con color en la terminal."""
    print(f"\033[{color_code}m{text}\033[0m")

def print_header(text):
    """Imprime un encabezado."""
    print_colored(f"\n{'=' * 50}", 36)
    print_colored(f" {text}", 36)
    print_colored(f"{'=' * 50}", 36)

def ensure_directory_exists(path):
    """Asegura que un directorio exista."""
    os.makedirs(path, exist_ok=True)
    return path

def fix_agent_context():
    """Corrige agent/context.py añadiendo la importación de os."""
    file_path = "agent/context.py"
    print(f"Corrigiendo {file_path}...")
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    if 'import os' not in content:
        new_content = "import os\n" + content
        with open(file_path, 'w') as file:
            file.write(new_content)
        print_colored("✅ Añadida importación 'import os'", 32)
    else:
        print_colored("⚠️ La importación 'import os' ya existe", 33)

def fix_providers_openai():
    """Corrige providers/openai_provider.py eliminando comillas invertidas."""
    file_path = "providers/openai_provider.py"
    print(f"Corrigiendo {file_path}...")
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    if '````' in content:
        new_content = content.replace('````', '')
        with open(file_path, 'w') as file:
            file.write(new_content)
        print_colored("✅ Eliminadas comillas invertidas al final del archivo", 32)
    else:
        print_colored("⚠️ No se encontraron comillas invertidas para eliminar", 33)

def fix_agent_init():
    """Corrige agent/__init__.py para exponer las clases principales."""
    file_path = "agent/__init__.py"
    print(f"Corrigiendo {file_path}...")
    
    expected_content = """# Inicialización del paquete
from .core import Core
from .executor import Executor
from .context import Context
from .objectives import Objective, SpecificObjective

# Definir versión
__version__ = '0.1.0'
"""
    
    with open(file_path, 'w') as file:
        file.write(expected_content)
    print_colored("✅ Actualizado para exponer las clases principales", 32)

def fix_providers_init():
    """Corrige providers/__init__.py para exponer los proveedores."""
    file_path = "providers/__init__.py"
    print(f"Corrigiendo {file_path}...")
    
    expected_content = """# Inicialización del paquete 
from .openai_provider import OpenAIProvider
from .claude_provider import ClaudeProvider
from .fake_provider import FakeProvider

# Definir versión
__version__ = '0.1.0'
"""
    
    with open(file_path, 'w') as file:
        file.write(expected_content)
    print_colored("✅ Actualizado para exponer los proveedores", 32)

def create_missing_functions():
    """Crea las funciones faltantes que se importan en main.py."""
    # Crear get_objective en agent/objectives.py
    print("Creando funciones faltantes...")
    
    # Añadir get_objective a objectives.py
    file_path = "agent/objectives.py"
    with open(file_path, 'a') as file:
        file.write("""
def get_objective(name=None, description=None):
    \"\"\"
    Obtiene o crea un objetivo basado en los parámetros dados.
    Si no se proporcionan parámetros, se crea un objetivo por defecto.
    \"\"\"
    if not name:
        name = "Objetivo por defecto"
        description = "Objetivo creado por defecto"
    
    return SpecificObjective(name, description, "parámetro_default")
""")
    print_colored("✅ Añadida función get_objective en agent/objectives.py", 32)
    
    # Crear build_context en agent/context.py
    with open("agent/context.py", 'a') as file:
        file.write("""
def build_context(env_file='.env'):
    \"\"\"
    Construye y devuelve un objeto Context inicializado con el archivo
    de entorno especificado.
    \"\"\"
    return Context(env_file)
""")
    print_colored("✅ Añadida función build_context en agent/context.py", 32)
    
    # Crear settings.py en config/
    os.makedirs("config", exist_ok=True)
    with open("config/settings.py", 'w') as file:
        file.write("""import os
import yaml
from pathlib import Path

def load_settings(config_file="config/settings.yaml"):
    \"\"\"
    Carga la configuración desde un archivo YAML.
    Si el archivo no existe, crea una configuración por defecto.
    \"\"\"
    config_path = Path(config_file)
    
    if not config_path.exists():
        # Crear configuración por defecto
        create_default_settings(config_path)
    
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def create_default_settings(config_path):
    \"\"\"
    Crea un archivo de configuración por defecto.
    \"\"\"
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
""")
    print_colored("✅ Creado archivo config/settings.py con funciones necesarias", 32)

def fix_tests():
    """Corrige las importaciones en los archivos de test."""
    # Corregir test_core.py
    file_path = "tests/test_core.py"
    print(f"Corrigiendo {file_path}...")
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    new_content = content.replace("from core import", "from agent.core import")
    
    with open(file_path, 'w') as file:
        file.write(new_content)
    print_colored("✅ Corregidas importaciones en test_core.py", 32)
    
    # Corregir test_providers.py
    file_path = "tests/test_providers.py"
    print(f"Corrigiendo {file_path}...")
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    new_content = content.replace("from providers import", "from providers import OpenAIProvider as")
    
    with open(file_path, 'w') as file:
        file.write(new_content)
    print_colored("✅ Corregidas importaciones en test_providers.py", 32)

def move_dangerous_notebooks():
    """Mueve notebooks potencialmente peligrosos a una carpeta 'scripts'."""
    print("Moviendo notebooks potencialmente peligrosos...")
    
    scripts_dir = ensure_directory_exists("scripts")
    
    for notebook in ["flujo-en-una-celda.ipynb", "vaciar-archivo.ipynb.ipynb"]:
        if os.path.exists(notebook):
            new_path = os.path.join(scripts_dir, notebook)
            os.rename(notebook, new_path)
            print_colored(f"✅ Movido {notebook} a scripts/", 32)
        else:
            print_colored(f"⚠️ No se encontró {notebook}", 33)

def create_minimal_settings_yaml():
    """Crea un archivo settings.yaml básico."""
    file_path = "config/settings.yaml"
    print(f"Creando {file_path} con configuración mínima...")
    
    ensure_directory_exists("config")
    
    minimal_content = """# Configuración para el proyecto agent-general

# Modo debug (True/False)
debug: True

# Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
log_level: INFO

# Configuración de proveedores
providers:
  # Configuración para OpenAI
  openai:
    model: gpt-4o
    max_tokens: 150
    temperature: 0.7
  
  # Configuración para Claude
  claude:
    enabled: False
"""
    
    with open(file_path, 'w') as file:
        file.write(minimal_content)
    print_colored("✅ Creado config/settings.yaml con configuración mínima", 32)

def fix_utils_init():
    """Corrige las importaciones en utils/__init__.py."""
    file_path = "utils/__init__.py"
    print(f"Corrigiendo {file_path}...")
    
    expected_content = """# __init__.py

# Nombre del Proyecto: agent-general
# Descripción: Conjunto de utilidades para el proyecto agent-general.

# Importar submódulos reales
from .logger import get_logger

# Definir la versión del paquete
__version__ = '0.1.0'

# Inicializar configuraciones globales si es necesario
configuracion_global = {
    'opcion1': True,
    'opcion2': 'valor_predeterminado'
}

# Funciones de inicialización
def inicializar():
    \"\"\"
    Función para inicializar configuraciones o recursos necesarios
    para el paquete.
    \"\"\"
    pass
"""
    
    with open(file_path, 'w') as file:
        file.write(expected_content)
    print_colored("✅ Corregidas importaciones en utils/__init__.py", 32)

def fix_cli_run_agent():
    """Corrige cli/run_agent.py para usar Core en lugar de Agent."""
    file_path = "cli/run_agent.py"
    print(f"Corrigiendo {file_path}...")
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    new_content = content.replace("from agent import Agent", "from agent import Core")
    new_content = new_content.replace("agent = Agent", "agent = Core")
    
    with open(file_path, 'w') as file:
        file.write(new_content)
    print_colored("✅ Corregida importación en cli/run_agent.py", 32)

def main():
    print_header("Corrección de Problemas - Proyecto agent-general")
    
    # Verificar que estamos en la raíz del proyecto
    if not os.path.exists("agent") or not os.path.exists("providers"):
        print_colored("❌ Error: Este script debe ejecutarse desde la raíz del proyecto.", 31)
        sys.exit(1)
    
    # Aplicar correcciones
    fix_agent_context()
    fix_providers_openai()
    fix_agent_init()
    fix_providers_init()
    create_missing_functions()
    fix_tests()
    move_dangerous_notebooks()
    create_minimal_settings_yaml()
    fix_utils_init()
    fix_cli_run_agent()
    
    print_header("Correcciones Completas")
    print_colored("✅ Todas las correcciones han sido aplicadas correctamente.", 32)
    print_colored("Por favor, revisa los cambios y ejecuta las pruebas para verificar que todo funcione correctamente.", 33)

if __name__ == "__main__":
    main()