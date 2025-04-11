# __init__.py

"""
Nombre del Proyecto: MiProyecto
Descripción: Este módulo es parte del paquete MiProyecto, diseñado para [descripción del propósito del proyecto].
Autor: [Tu Nombre]
Fecha: [Fecha de creación]
Licencia: [Tipo de licencia]
"""

# Importar submódulos
from .modulo1 import *
from .modulo2 import *

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