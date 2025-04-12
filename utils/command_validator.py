#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validador de comandos para el Agente Inteligente.
Este módulo proporciona funciones para validar la seguridad de comandos
antes de ejecutarlos en el sistema.
"""

import re
import logging
import os
from typing import Dict, List, Set, Optional

logger = logging.getLogger(__name__)

# Lista de comandos prohibidos (comandos potencialmente peligrosos)
FORBIDDEN_COMMANDS: Set[str] = {
    'rm -rf /', 'rm -rf /*', 'rm -rf ~', 'rm -rf .', 'rm -rf --no-preserve-root /',
    'mkfs', 'dd if=/dev/random', ':(){:|:&};:', 'chmod -R 777 /', '> /dev/sda',
    'mv ~ /dev/null', 'wget -O- | sh', 'curl | sh', 'wget -O- | bash', 'curl | bash'
}

# Lista de patrones peligrosos en comandos
DANGEROUS_PATTERNS: List[str] = [
    r'rm\s+-rf\s+/(\s|$)',      # rm -rf / y variantes
    r'>\s+/dev/(sd|hd|xvd)',    # Sobrescribir dispositivos
    r'mkfs\.\w+\s+/dev/(sd|hd|xvd)', # Formatear dispositivos
    r'dd\s+if=/dev/\w+\s+of=/dev/(sd|hd|xvd)', # dd peligroso
    r';\s*rm\s',                # Comandos que terminan eliminando
    r'wget\s+.*\s*\|\s*(sh|bash)', # wget piped to shell
    r'curl\s+.*\s*\|\s*(sh|bash)',  # curl piped to shell
]

# Lista de comandos permitidos (comandos seguros)
ALLOWED_COMMANDS: Set[str] = {
    'ls', 'dir', 'pwd', 'cd', 'echo', 'cat', 'more', 'less', 'head', 'tail',
    'grep', 'find', 'cp', 'mv', 'mkdir', 'touch', 'chmod', 'chown', 'df', 'du',
    'ps', 'top', 'free', 'uname', 'whoami', 'date', 'uptime', 'which', 'whereis',
    'man', 'mount', 'umount', 'fdisk -l', 'lsblk', 'history', 'ping', 'traceroute'
}

def validate_command(command: str) -> Dict[str, bool]:
    """
    Valida si un comando es seguro para ejecutar.
    
    Args:
        command: Comando a validar
        
    Returns:
        Dict con el resultado de la validación y razón si es inválido
    """
    # Preprocesar el comando
    cleaned_command = command.strip().lower()
    base_command = cleaned_command.split()[0] if cleaned_command else ""
    
    # Verificar si el comando está en la lista de comandos prohibidos
    if any(forbidden in cleaned_command for forbidden in FORBIDDEN_COMMANDS):
        reason = "El comando está en la lista de comandos prohibidos"
        logger.warning(f"Comando prohibido: {command}")
        return {'valid': False, 'reason': reason}
    
    # Verificar patrones peligrosos
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, cleaned_command):
            reason = "El comando contiene un patrón peligroso"
            logger.warning(f"Patrón peligroso en comando: {command}, patrón: {pattern}")
            return {'valid': False, 'reason': reason}
    
    # Verificar comandos con tuberías (|), que pueden ser complejos
    if '|' in cleaned_command:
        pipe_commands = [cmd.strip().split()[0] for cmd in cleaned_command.split('|') if cmd.strip()]
        
        # Verificar cada comando en la tubería
        for cmd in pipe_commands:
            if cmd not in ALLOWED_COMMANDS:
                reason = f"El comando '{cmd}' en la tubería no está en la lista de permitidos"
                logger.warning(reason)
                return {'valid': False, 'reason': reason}
    
    # Verificar comandos con punto y coma (;), que son múltiples comandos
    elif ';' in cleaned_command:
        for cmd in cleaned_command.split(';'):
            if cmd.strip():
                subcmd_validation = validate_command(cmd.strip())
                if not subcmd_validation['valid']:
                    return subcmd_validation
    
    # Verificar si el comando base está en la lista de permitidos
    # o si parece una ruta a un ejecutable válido
    if (base_command in ALLOWED_COMMANDS or 
        (os.path.exists(base_command) and os.access(base_command, os.X_OK))):
        return {'valid': True, 'reason': None}
    
    # Por defecto, rechazar comandos desconocidos
    reason = f"El comando '{base_command}' no está en la lista de comandos permitidos"
    logger.warning(reason)
    return {'valid': False, 'reason': reason}

def is_safe_path(path: str) -> bool:
    """
    Verifica si una ruta es segura (no accede a directorios sensibles).
    
    Args:
        path: Ruta a verificar
        
    Returns:
        True si la ruta es segura, False en caso contrario
    """
    # Normalizar la ruta
    abs_path = os.path.abspath(os.path.normpath(path))
    
    # Lista de directorios sensibles
    sensitive_dirs = [
        '/etc', '/var/log', '/var/spool', '/boot',
        '/root', '/proc', '/sys', '/dev'
    ]
    
    # Verificar si la ruta está dentro de un directorio sensible
    for sensitive_dir in sensitive_dirs:
        if abs_path == sensitive_dir or abs_path.startswith(sensitive_dir + os.sep):
            logger.warning(f"Intento de acceso a directorio sensible: {path} -> {abs_path}")
            return False
    
    return True

def analyze_command_risk(command: str) -> Dict[str, any]:
    """
    Analiza el nivel de riesgo de un comando.
    
    Args:
        command: Comando a analizar
        
    Returns:
        Dict con nivel de riesgo y explicación
    """
    risk_level = "LOW"
    explanations = []
    
    # Verificar si contiene sudo
    if 'sudo' in command:
        risk_level = "HIGH"
        explanations.append("El comando usa sudo (privilegios elevados)")
    
    # Verificar si contiene operadores de redirección
    if '>' in command or '>>' in command:
        risk_level = max(risk_level, "MEDIUM")
        explanations.append("El comando usa redirección de salida")
    
    # Verificar si contiene caracteres especiales del shell
    if any(char in command for char in ['&', '|', ';', '$', '`']):
        risk_level = max(risk_level, "MEDIUM")
        explanations.append("El comando usa caracteres especiales del shell")
    
    # Verificar operaciones peligrosas
    danger_operations = {
        'rm': "Elimina archivos",
        'dd': "Operación de bajo nivel con dispositivos",
        'chmod': "Cambia permisos de archivos",
        'chown': "Cambia propietario de archivos",
        'mount': "Monta sistemas de archivos",
        'kill': "Termina procesos",
        'reboot': "Reinicia el sistema",
        'shutdown': "Apaga el sistema"
    }
    
    for op, desc in danger_operations.items():
        if re.search(r'\b' + op + r'\b', command):
            if op in ['rm', 'dd', 'reboot', 'shutdown']:
                risk_level = "HIGH"
            else:
                risk_level = max(risk_level, "MEDIUM")
            explanations.append(f"{desc}")
    
    return {
        'command': command,
        'risk_level': risk_level,
        'explanations': explanations,
        'is_validated': validate_command(command)['valid']
    }