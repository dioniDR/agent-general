#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manejadores de operaciones del sistema para el Agente Inteligente.
Este módulo proporciona funciones para interactuar con el sistema operativo
de manera segura y controlada.
"""

import os
import subprocess
import shutil
import logging
from typing import Dict, Any, Tuple, List, Optional
import platform

from utils.command_validator import validate_command
from utils.security import sanitize_path

logger = logging.getLogger(__name__)

def execute_command(command: str, timeout: int = 30, 
                   working_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Ejecuta un comando del sistema de forma segura.
    
    Args:
        command: Comando a ejecutar
        timeout: Tiempo máximo de ejecución en segundos
        working_dir: Directorio de trabajo para la ejecución
        
    Returns:
        Diccionario con el resultado de la ejecución
    """
    # Validar el comando antes de ejecutarlo
    validation = validate_command(command)
    if not validation['valid']:
        logger.warning(f"Comando no válido: {command}. Razón: {validation['reason']}")
        return {
            'success': False,
            'output': None,
            'error': f"Comando no válido: {validation['reason']}",
            'command': command
        }
    
    try:
        # Ejecutar el comando
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=working_dir
        )
        
        # Procesar el resultado
        if process.returncode == 0:
            logger.info(f"Comando ejecutado exitosamente: {command}")
            return {
                'success': True,
                'output': process.stdout.strip(),
                'error': None,
                'command': command,
                'returncode': process.returncode
            }
        else:
            logger.warning(f"Error al ejecutar comando: {command}. Error: {process.stderr}")
            return {
                'success': False,
                'output': process.stdout.strip(),
                'error': process.stderr.strip(),
                'command': command,
                'returncode': process.returncode
            }
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout al ejecutar comando: {command}")
        return {
            'success': False,
            'output': None,
            'error': f"El comando excedió el tiempo máximo de ejecución ({timeout}s)",
            'command': command
        }
    except Exception as e:
        logger.error(f"Excepción al ejecutar comando: {command}. Error: {str(e)}")
        return {
            'success': False,
            'output': None,
            'error': str(e),
            'command': command
        }

def list_files(directory: str = '.', 
              show_hidden: bool = False, 
              pattern: Optional[str] = None) -> Dict[str, Any]:
    """
    Lista archivos en un directorio.
    
    Args:
        directory: Directorio a listar
        show_hidden: Si se deben mostrar archivos ocultos
        pattern: Patrón para filtrar archivos (e.g., '*.py')
        
    Returns:
        Diccionario con el listado de archivos
    """
    # Sanitizar la ruta para evitar ataques
    directory = sanitize_path(directory)
    
    # Validar que el directorio existe
    if not os.path.exists(directory):
        return {
            'success': False,
            'error': f"El directorio '{directory}' no existe",
            'files': []
        }
    
    if not os.path.isdir(directory):
        return {
            'success': False,
            'error': f"La ruta '{directory}' no es un directorio",
            'files': []
        }
    
    try:
        # Listar archivos
        files = os.listdir(directory)
        
        # Filtrar archivos ocultos si es necesario
        if not show_hidden:
            files = [f for f in files if not f.startswith('.')]
        
        # Filtrar por patrón si se proporciona
        if pattern:
            import fnmatch
            files = [f for f in files if fnmatch.fnmatch(f, pattern)]
        
        # Obtener información adicional de cada archivo
        file_info = []
        for filename in files:
            path = os.path.join(directory, filename)
            try:
                info = {
                    'name': filename,
                    'path': path,
                    'size': os.path.getsize(path),
                    'is_dir': os.path.isdir(path),
                    'is_file': os.path.isfile(path),
                }
                file_info.append(info)
            except (PermissionError, FileNotFoundError) as e:
                # Manejar errores de permisos o si el archivo desaparece
                logger.warning(f"Error al acceder a '{path}': {str(e)}")
        
        return {
            'success': True,
            'directory': directory,
            'files': file_info,
            'count': len(file_info)
        }
    except Exception as e:
        logger.error(f"Error al listar archivos en '{directory}': {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'files': []
        }

def mount_partition(device: str, mount_point: str, 
                   options: Optional[str] = None) -> Dict[str, Any]:
    """
    Monta una partición en un punto de montaje.
    
    Args:
        device: Dispositivo a montar (e.g., /dev/sda1)
        mount_point: Punto de montaje
        options: Opciones de montaje (e.g., 'ro,noexec')
        
    Returns:
        Diccionario con el resultado de la operación
    """
    # Sanitizar entradas
    device = sanitize_path(device)
    mount_point = sanitize_path(mount_point)
    
    # Validar que el dispositivo existe
    if not os.path.exists(device):
        return {
            'success': False,
            'error': f"El dispositivo '{device}' no existe"
        }
    
    # Validar que el punto de montaje existe
    if not os.path.exists(mount_point):
        return {
            'success': False,
            'error': f"El punto de montaje '{mount_point}' no existe"
        }
    
    # Construir el comando
    command = f"sudo mount"
    
    if options:
        command += f" -o {options}"
        
    command += f" {device} {mount_point}"
    
    # Ejecutar el comando
    return execute_command(command)

def get_system_info() -> Dict[str, Any]:
    """
    Obtiene información básica del sistema.
    
    Returns:
        Diccionario con información del sistema
    """
    info = {
        'platform': platform.platform(),
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
    }
    
    # Información específica según el sistema operativo
    if platform.system() == 'Linux':
        # Añadir información específica de Linux
        try:
            # Información de la distribución
            info['distribution'] = ' '.join(platform.linux_distribution())
        except:
            # platform.linux_distribution() está obsoleto en Python 3.8+
            pass
            
        # Información de CPU
        try:
            cpu_info = execute_command("cat /proc/cpuinfo | grep 'model name' | uniq")
            if cpu_info['success']:
                info['cpu_model'] = cpu_info['output'].split(':')[1].strip()
        except:
            pass
            
        # Información de memoria
        try:
            mem_info = execute_command("free -h")
            if mem_info['success']:
                info['memory_info'] = mem_info['output']
        except:
            pass
    
    return info