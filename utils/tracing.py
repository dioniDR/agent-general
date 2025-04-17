# utils/tracing.py

import os
import logging
import json
from functools import wraps
from datetime import datetime
from typing import Callable, Any

class ExecutionTracer:
    """
    Clase para gestionar el seguimiento de la ejecución de la aplicación.
    """
    def __init__(self, log_file='app_trace.log', json_report='execution_trace.json'):
        """
        Inicializar el trazador de ejecución.
        
        :param log_file: Archivo de log para trazas detalladas
        :param json_report: Archivo JSON para reporte resumido
        """
        # Configurar directorios de logs
        logs_dir = 'logs'
        os.makedirs(logs_dir, exist_ok=True)
        
        self.log_file = os.path.join(logs_dir, log_file)
        self.json_report = os.path.join(logs_dir, json_report)
        
        # Configurar logging
        self.logger = logging.getLogger('execution_tracer')
        self.logger.setLevel(logging.INFO)
        
        # Limpiar handlers existentes para evitar duplicados
        self.logger.handlers.clear()
        
        # Configurar handlers
        file_handler = logging.FileHandler(self.log_file)
        console_handler = logging.StreamHandler()
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def trace(self, func: Callable) -> Callable:
        """
        Decorador para trazar la ejecución de funciones.
        
        :param func: Función a trazar
        :return: Función envuelta con capacidades de traza
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generar ID de traza único
            trace_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
            
            try:
                # Registrar entrada
                self.logger.info(f"[TRACE:{trace_id}] Entering: {func.__name__}")
                self.logger.info(f"[TRACE:{trace_id}] Args: {args}")
                self.logger.info(f"[TRACE:{trace_id}] Kwargs: {kwargs}")
                
                # Ejecutar función
                result = func(*args, **kwargs)
                
                # Registrar salida
                self.logger.info(f"[TRACE:{trace_id}] Exiting: {func.__name__}")
                self.logger.info(f"[TRACE:{trace_id}] Result: {result}")
                
                return result
            
            except Exception as e:
                # Registrar errores
                self.logger.error(f"[TRACE:{trace_id}] Error in {func.__name__}: {e}")
                raise
        
        return wrapper
    
    def generate_report(self):
        """
        Genera un reporte JSON a partir del archivo de log.
        """
        try:
            with open(self.log_file, 'r') as log_file:
                log_lines = log_file.readlines()
            
            # Procesar líneas de log
            report = {
                "timestamp": datetime.now().isoformat(),
                "traces": []
            }
            
            current_trace = None
            for line in log_lines:
                if "Entering:" in line:
                    current_trace = {"entry": line.strip()}
                elif "Args:" in line and current_trace:
                    current_trace["args"] = line.strip()
                elif "Kwargs:" in line and current_trace:
                    current_trace["kwargs"] = line.strip()
                elif "Exiting:" in line and current_trace:
                    current_trace["exit"] = line.strip()
                    report["traces"].append(current_trace)
                    current_trace = None
            
            # Guardar reporte JSON
            with open(self.json_report, 'w') as json_file:
                json.dump(report, json_file, indent=2)
            
            self.logger.info(f"Trace report generated: {self.json_report}")
        
        except Exception as e:
            self.logger.error(f"Error generating trace report: {e}")
    
    def clear_logs(self):
        """
        Limpia los archivos de log y reporte.
        """
        try:
            # Limpiar archivo de log
            open(self.log_file, 'w').close()
            
            # Limpiar archivo JSON
            open(self.json_report, 'w').close()
            
            self.logger.info("Log files cleared")
        except Exception as e:
            self.logger.error(f"Error clearing log files: {e}")

# Crear una instancia global para uso conveniente
tracer = ExecutionTracer()