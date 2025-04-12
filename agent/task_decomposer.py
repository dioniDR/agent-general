#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Descomponedor de tareas para el Agente Inteligente.
Este módulo se encarga de descomponer objetivos en tareas específicas
que pueden ser ejecutadas por el agente.
"""

import logging
from typing import List, Dict, Any, Optional

from providers.openai_provider import OpenAIProvider
from .task import Task, TaskStatus, TaskPriority

logger = logging.getLogger(__name__)

class TaskDecomposer:
    """
    Descompone objetivos en tareas específicas utilizando modelos de IA.
    """
    
    def __init__(self, providers_config: Dict[str, Any]):
        """
        Inicializa el descomponedor de tareas.
        
        Args:
            providers_config: Configuración de los proveedores de IA
        """
        self.providers_config = providers_config
        self.provider = OpenAIProvider(api_key=providers_config.get('openai', {}).get('api_key'))
        
    def decompose(self, objective: Dict[str, Any], 
                 context: Optional[Dict[str, Any]] = None) -> List[Task]:
        """
        Descompone un objetivo en tareas específicas.
        
        Args:
            objective: Objetivo a descomponer
            context: Contexto adicional (opcional)
            
        Returns:
            Lista de tareas
        """
        logger.info(f"Descomponiendo objetivo: {objective['description']}")
        
        # Determinar la estrategia de descomposición según el tipo de objetivo
        if objective['type'] == 'SYSTEM_FILE_OPERATION':
            return self._decompose_file_operation(objective, context)
        elif objective['type'] == 'SYSTEM_MOUNT':
            return self._decompose_mount_operation(objective, context)
        elif objective['type'] == 'SYSTEM_COMMAND':
            return self._decompose_command_operation(objective, context)
        else:
            return self._decompose_using_ai(objective, context)
    
    def _decompose_file_operation(self, objective: Dict[str, Any], 
                                context: Optional[Dict[str, Any]] = None) -> List[Task]:
        """
        Descompone una operación de archivos en tareas específicas.
        
        Args:
            objective: Objetivo relacionado con archivos
            context: Contexto adicional
            
        Returns:
            Lista de tareas para operaciones de archivos
        """
        tasks = []
        description = objective['description'].lower()
        
        # Identificar el tipo de operación y el directorio
        directory = '.'  # Directorio actual por defecto
        
        # Extraer el directorio si se menciona
        # En una implementación real, usaríamos NLP más avanzado aquí
        if 'en el directorio' in description:
            parts = description.split('en el directorio')
            if len(parts) > 1:
                directory = parts[1].strip().split()[0]
        
        # Tarea para validar que el directorio existe
        tasks.append(Task(
            id='validate_directory',
            description=f"Validar que el directorio '{directory}' existe",
            command=f"test -d {directory}",
            priority=TaskPriority.HIGH,
            critical=True
        ))
        
        # Tarea principal según la operación
        if 'archivos ocultos' in description:
            tasks.append(Task(
                id='list_hidden_files',
                description=f"Listar archivos ocultos en '{directory}'",
                command=f"ls -la {directory} | grep '^\\.'"
            ))
        elif 'listar' in description or 'mostrar' in description:
            tasks.append(Task(
                id='list_files',
                description=f"Listar archivos en '{directory}'",
                command=f"ls -la {directory}"
            ))
        
        return tasks
    
    def _decompose_mount_operation(self, objective: Dict[str, Any], 
                                 context: Optional[Dict[str, Any]] = None) -> List[Task]:
        """
        Descompone una operación de montaje en tareas específicas.
        
        Args:
            objective: Objetivo relacionado con montaje
            context: Contexto adicional
            
        Returns:
            Lista de tareas para operaciones de montaje
        """
        # En una implementación real, extraeríamos detalles como
        # dispositivo y punto de montaje usando NLP o prompts específicos
        
        # Por ahora, solo devolvemos tareas genéricas
        return [
            Task(
                id='list_available_devices',
                description="Listar dispositivos disponibles",
                command="lsblk"
            ),
            Task(
                id='check_mount_points',
                description="Verificar puntos de montaje existentes",
                command="mount | column -t"
            ),
            # Aquí añadiríamos la tarea real de montaje después de validación
        ]
    
    def _decompose_command_operation(self, objective: Dict[str, Any], 
                                   context: Optional[Dict[str, Any]] = None) -> List[Task]:
        """
        Descompone una operación de comando en tareas específicas.
        
        Args:
            objective: Objetivo relacionado con ejecución de comandos
            context: Contexto adicional
            
        Returns:
            Lista de tareas para operaciones de comandos
        """
        # Extraer el comando (en una implementación real, usaríamos NLP/prompts)
        command = objective['description']
        if 'ejecutar' in command.lower():
            command = command.lower().split('ejecutar')[1].strip()
        
        return [
            Task(
                id='validate_command',
                description="Validar la seguridad del comando",
                command=f"echo '{command}'",  # Placeholder para validación
                critical=True
            ),
            Task(
                id='execute_command',
                description=f"Ejecutar: {command}",
                command=command
            )
        ]
    
    def _decompose_using_ai(self, objective: Dict[str, Any], 
                          context: Optional[Dict[str, Any]] = None) -> List[Task]:
        """
        Descompone un objetivo general usando IA.
        
        Args:
            objective: Objetivo general
            context: Contexto adicional
            
        Returns:
            Lista de tareas generadas por IA
        """
        prompt = f"""
        Descompón la siguiente petición en tareas ejecutables en un sistema Linux:
        "{objective['description']}"
        
        Genera entre 2 y 5 tareas en formato JSON:
        [
            {{
                "id": "task_id",
                "description": "descripción de la tarea",
                "command": "comando a ejecutar",
                "priority": "HIGH/MEDIUM/LOW",
                "critical": true/false
            }},
            ...
        ]
        
        Solo devuelve el JSON, sin texto adicional.
        """
        
        # Llamar a la API para descomponer la tarea
        try:
            response = self.provider.generate_text(prompt, max_tokens=500)
            # Aquí parsearíamos el JSON de la respuesta y crearíamos las tareas
            # Por simplicidad, devolvemos una tarea genérica
            return [
                Task(
                    id='generic_task',
                    description=objective['description'],
                    command=f"echo 'Procesando: {objective['description']}'"
                )
            ]
        except Exception as e:
            logger.error(f"Error al descomponer usando IA: {e}")
            # Fallback a tarea genérica
            return [
                Task(
                    id='fallback_task',
                    description=f"Procesar: {objective['description']}",
                    command=f"echo 'Procesando: {objective['description']}'"
                )
            ]