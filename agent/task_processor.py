#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Procesador de tareas para el Agente Inteligente.
Este módulo se encarga de procesar peticiones, descomponerlas en tareas
y coordinar su ejecución.
"""

import logging
from typing import List, Dict, Any, Optional

from .task_decomposer import TaskDecomposer
from .executor import Executor
from .task import Task, TaskStatus

logger = logging.getLogger(__name__)

class TaskProcessor:
    """
    Procesa peticiones del usuario y las convierte en tareas ejecutables.
    Coordina todo el flujo desde la petición hasta la respuesta final.
    """
    
    def __init__(self, providers_config: Dict[str, Any], task_decomposer=None, executor=None):
        """
        Inicializa el procesador de tareas.
        
        Args:
            providers_config: Configuración de los proveedores de IA
            task_decomposer: Descomponedor de tareas (opcional)
            executor: Ejecutor de tareas (opcional)
        """
        self.providers_config = providers_config
        self.task_decomposer = task_decomposer or TaskDecomposer(providers_config)
        self.executor = executor or Executor()
        
    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una petición del usuario.
        
        Args:
            request: Petición en lenguaje natural
            context: Contexto adicional para la petición (opcional)
            
        Returns:
            Dict con los resultados del procesamiento
        """
        logger.info(f"Procesando petición: {request}")
        
        # Paso 1: Analizar la petición
        objective = self._analyze_request(request, context)
        
        # Paso 2: Descomponer en tareas
        tasks = self.task_decomposer.decompose(objective, context)
        
        # Paso 3: Ejecutar tareas
        results = {}
        for task in tasks:
            result = self.executor.execute_task(task)
            task.status = TaskStatus.COMPLETED if result.get('success') else TaskStatus.FAILED
            task.result = result.get('output')
            results[task.id] = task.result
            
            # Si una tarea falla y es crítica, detenemos la ejecución
            if task.status == TaskStatus.FAILED and task.critical:
                logger.error(f"Tarea crítica fallida: {task.id}")
                break
        
        # Paso 4: Integrar resultados
        final_result = self._integrate_results(objective, tasks, results)
        
        return {
            'objective': objective,
            'tasks': tasks,
            'task_results': results,
            'final_result': final_result
        }
    
    def _analyze_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analiza la petición para entender el objetivo.
        
        Args:
            request: Petición en lenguaje natural
            context: Contexto adicional
            
        Returns:
            Objetivo estructurado
        """
        # En una implementación real, aquí podríamos usar el proveedor de IA
        # para entender mejor la petición
        return {
            'description': request,
            'type': self._determine_request_type(request),
            'context': context or {}
        }
    
    def _determine_request_type(self, request: str) -> str:
        """
        Determina el tipo de petición (sistema, información, etc.)
        
        Args:
            request: Petición en lenguaje natural
            
        Returns:
            Tipo de petición
        """
        # Implementación básica, en producción usaríamos NLP/clasificación
        if any(kw in request.lower() for kw in ['listar', 'mostrar', 'archivos', 'directorio']):
            return 'SYSTEM_FILE_OPERATION'
        elif any(kw in request.lower() for kw in ['montar', 'partición', 'disco']):
            return 'SYSTEM_MOUNT'
        elif any(kw in request.lower() for kw in ['ejecutar', 'correr', 'comando']):
            return 'SYSTEM_COMMAND'
        else:
            return 'GENERAL'
    
    def _integrate_results(self, objective: Dict[str, Any], tasks: List[Task], 
                         results: Dict[str, Any]) -> str:
        """
        Integra los resultados de las tareas en una respuesta coherente.
        
        Args:
            objective: Objetivo original
            tasks: Lista de tareas ejecutadas
            results: Resultados de cada tarea
            
        Returns:
            Resultado final integrado
        """
        # En una implementación completa, podríamos usar IA para generar
        # una respuesta coherente basada en los resultados
        
        # Versión simple para empezar
        success_tasks = [t for t in tasks if t.status == TaskStatus.COMPLETED]
        failed_tasks = [t for t in tasks if t.status == TaskStatus.FAILED]
        
        response = []
        
        if failed_tasks:
            response.append(f"Completadas {len(success_tasks)} de {len(tasks)} tareas.")
            response.append("Se encontraron los siguientes problemas:")
            for task in failed_tasks:
                response.append(f" - {task.description}: {task.result}")
        else:
            response.append(f"Se completaron todas las tareas correctamente.")
        
        response.append("\nResultados:")
        for task in success_tasks:
            response.append(f"\n--- {task.description} ---")
            response.append(str(task.result))
        
        return "\n".join(response)