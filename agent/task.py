#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Definición de la clase Task y enumeraciones relacionadas.
"""

from enum import Enum, auto
from typing import Dict, Any, Optional
import uuid

class TaskStatus(Enum):
    """Estado de una tarea"""
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()

class TaskPriority(Enum):
    """Prioridad de una tarea"""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

class Task:
    """
    Representa una tarea ejecutable por el agente.
    Contiene toda la información necesaria para ejecutar y dar seguimiento
    a una unidad de trabajo.
    """
    
    def __init__(self, 
                description: str, 
                command: Optional[str] = None,
                id: Optional[str] = None,
                priority: TaskPriority = TaskPriority.MEDIUM,
                critical: bool = False,
                params: Optional[Dict[str, Any]] = None):
        """
        Inicializa una nueva tarea.
        
        Args:
            description: Descripción de la tarea
            command: Comando a ejecutar (opcional)
            id: Identificador único (se genera automáticamente si no se proporciona)
            priority: Prioridad de la tarea
            critical: Indica si la tarea es crítica para el objetivo
            params: Parámetros adicionales para la ejecución
        """
        self.id = id or str(uuid.uuid4())
        self.description = description
        self.command = command
        self.priority = priority
        self.critical = critical
        self.params = params or {}
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.created_at = None  # Se podría usar datetime.now()
        self.started_at = None
        self.completed_at = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la tarea a un diccionario.
        
        Returns:
            Diccionario con los atributos de la tarea
        """
        return {
            'id': self.id,
            'description': self.description,
            'command': self.command,
            'priority': self.priority.name,
            'critical': self.critical,
            'status': self.status.name,
            'result': self.result,
            'error': self.error,
            'params': self.params
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Crea una tarea a partir de un diccionario.
        
        Args:
            data: Diccionario con los atributos de la tarea
            
        Returns:
            Nueva instancia de Task
        """
        task = cls(
            id=data.get('id'),
            description=data['description'],
            command=data.get('command'),
            priority=TaskPriority[data.get('priority', 'MEDIUM')],
            critical=data.get('critical', False),
            params=data.get('params', {})
        )
        
        if 'status' in data:
            task.status = TaskStatus[data['status']]
        if 'result' in data:
            task.result = data['result']
        if 'error' in data:
            task.error = data['error']
            
        return task
    
    def __str__(self) -> str:
        """
        Representación en string de la tarea.
        
        Returns:
            String que representa la tarea
        """
        return f"Task({self.id}): {self.description} [{self.status.name}]"
    
    def __repr__(self) -> str:
        """
        Representación oficial de la tarea.
        
        Returns:
            Representación oficial como string
        """
        return f"Task(id='{self.id}', description='{self.description}', status={self.status.name})"