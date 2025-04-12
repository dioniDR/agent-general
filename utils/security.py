#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilidades de seguridad para el Agente Inteligente.
Este módulo proporciona funciones para asegurar operaciones
y verificar permisos.
"""

import os
import re
import subprocess
import logging
import shlex
import hashlib
import random
import string
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

def sanitize_path(path: str) -> str:
    """
    Sanitiza una ruta para prevenir ataques.
    
    Args:
        path: Ruta a sanitizar
        
    Returns:
        Ruta sanitizada
    """
    # Eliminar caracteres de control y espacios al inicio/fin
    sanitized = path.strip()
    
    # Eliminar secuencias de escape shell
    sanitized = re.sub(r'[;&|><$`\\]', '', sanitized)
    
    # Convertir a ruta absoluta y normalizarla
    if sanitized:
        sanitized = os.path.normpath(sanitized)
        
    return sanitized

def get_file_hash(file_path: str) -> Optional[str]:
    """
    Calcula el hash SHA-256 de un archivo.
    
    Args:
        file_path: Ruta al archivo
        
    Returns:
        Hash SHA-256 o None si hay error
    """
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256()
            chunk = f.read(8192)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(8192)
        return file_hash.hexdigest()
    except Exception as e:
        logger.error(f"Error al calcular hash del archivo {file_path}: {e}")
        return None

def verify_command_output(command: str, output: str, 
                        expected_patterns: List[str]) -> bool:
    """
    Verifica que la salida de un comando contenga los patrones esperados.
    
    Args:
        command: Comando ejecutado
        output: Salida del comando
        expected_patterns: Patrones que se esperan encontrar en la salida
        
    Returns:
        True si todos los patrones esperados se encuentran en la salida
    """
    if not output:
        return False
    
    for pattern in expected_patterns:
        if not re.search(pattern, output):
            logger.warning(f"Patrón no encontrado en salida de comando: {pattern}")
            return False
    
    return True

def generate_secure_temp_dir() -> Dict[str, Any]:
    """
    Genera un directorio temporal seguro.
    
    Returns:
        Dict con la ruta del directorio y token de seguridad
    """
    import tempfile
    
    # Generar un token aleatorio
    random_token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    # Crear directorio temporal
    try:
        temp_dir = tempfile.mkdtemp(prefix=f"agent_{random_token}_")
        return {
            'success': True,
            'temp_dir': temp_dir,
            'token': random_token
        }
    except Exception as e:
        logger.error(f"Error al crear directorio temporal: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def clean_temp_dir(temp_dir: str) -> Dict[str, Any]:
    """
    Limpia un directorio temporal de forma segura.
    
    Args:
        temp_dir: Ruta al directorio temporal
        
    Returns:
        Dict con el resultado de la operación
    """
    import shutil
    
    # Verificar que la ruta es válida
    if not temp_dir or not os.path.exists(temp_dir):
        return {
            'success': False,
            'error': f"El directorio {temp_dir} no existe"
        }
    
    # Verificar que es un directorio temporal válido
    if not (os.path.basename(temp_dir).startswith('agent_') and 
            os.path.basename(temp_dir).count('_') >= 2):
        return {
            'success': False,
            'error': f"El directorio {temp_dir} no parece ser un directorio temporal válido"
        }
    
    try:
        shutil.rmtree(temp_dir)
        return {
            'success': True,
            'message': f"Directorio {temp_dir} eliminado correctamente"
        }
    except Exception as e:
        logger.error(f"Error al eliminar directorio temporal {temp_dir}: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def check_permissions(path: str, required_permissions: str) -> Dict[str, Any]:
    """
    Verifica los permisos de un archivo o directorio.
    
    Args:
        path: Ruta al archivo o directorio
        required_permissions: Permisos requeridos ('r', 'w', 'x')
        
    Returns:
        Dict con el resultado de la verificación
    """
    if not os.path.exists(path):
        return {
            'exists': False,
            'path': path,
            'error': f"La ruta {path} no existe"
        }
    
    result = {
        'exists': True,
        'path': path,
        'is_file': os.path.isfile(path),
        'is_dir': os.path.isdir(path),
        'permissions': {
            'read': os.access(path, os.R_OK),
            'write': os.access(path, os.W_OK),
            'execute': os.access(path, os.X_OK)
        },
        'owner': get_file_owner(path)
    }
    
    # Verificar permisos requeridos
    missing_permissions = []
    if 'r' in required_permissions and not result['permissions']['read']:
        missing_permissions.append('lectura')
    if 'w' in required_permissions and not result['permissions']['write']:
        missing_permissions.append('escritura')
    if 'x' in required_permissions and not result['permissions']['execute']:
        missing_permissions.append('ejecución')
    
    result['has_required_permissions'] = len(missing_permissions) == 0
    
    if missing_permissions:
        result['missing_permissions'] = missing_permissions
        result['error'] = f"Faltan permisos: {', '.join(missing_permissions)}"
    
    return result

def get_file_owner(path: str) -> Dict[str, Any]:
    """
    Obtiene el propietario de un archivo o directorio.
    
    Args:
        path: Ruta al archivo o directorio
        
    Returns:
        Dict con información del propietario
    """
    try:
        import pwd
        import grp
        
        stat_info = os.stat(path)
        uid = stat_info.st_uid
        gid = stat_info.st_gid
        
        try:
            user = pwd.getpwuid(uid).pw_name
        except KeyError:
            user = str(uid)
            
        try:
            group = grp.getgrgid(gid).gr_name
        except KeyError:
            group = str(gid)
        
        return {
            'user': user,
            'group': group,
            'uid': uid,
            'gid': gid
        }
    except Exception as e:
        logger.error(f"Error al obtener propietario de {path}: {e}")
        return {
            'error': str(e)
        }