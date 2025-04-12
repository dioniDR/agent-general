# __init__.py

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
    """
    Función para inicializar configuraciones o recursos necesarios
    para el paquete.
    """
    pass
