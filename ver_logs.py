#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para observar logs de llamadas a la API de OpenAI en tiempo real.
Ejecutar en una terminal separada mientras se usa el agente principal.
"""

import os
import time
import json
import datetime
import colorama
from colorama import Fore, Style
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Inicializar colorama para salida coloreada
colorama.init()

# Configuración
LOGS_DIR = "logs"
REQUEST_LOG = os.path.join(LOGS_DIR, "openai_requests.log")
RESPONSE_LOG = os.path.join(LOGS_DIR, "openai_responses.log")

# Crear directorio de logs si no existe
os.makedirs(LOGS_DIR, exist_ok=True)

# Asegurar que los archivos de log existan
for log_file in [REQUEST_LOG, RESPONSE_LOG]:
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write(f"# Log creado: {datetime.datetime.now()}\n")

class LogReader:
    def __init__(self):
        self.last_request_position = os.path.getsize(REQUEST_LOG)
        self.last_response_position = os.path.getsize(RESPONSE_LOG)
        self.requests_seen = set()
        self.responses_seen = set()
        print(f"{Fore.GREEN}Observador de logs iniciado.{Style.RESET_ALL}")
        print(f"Monitoreando {Fore.CYAN}{REQUEST_LOG}{Style.RESET_ALL} y {Fore.CYAN}{RESPONSE_LOG}{Style.RESET_ALL}")
        print(f"Esperando nuevas llamadas a la API...\n")

    def check_for_new_content(self):
        """Verifica si hay nuevo contenido en los archivos de log"""
        # Verificar nuevas peticiones
        current_request_size = os.path.getsize(REQUEST_LOG)
        if current_request_size > self.last_request_position:
            with open(REQUEST_LOG, "r") as f:
                f.seek(self.last_request_position)
                new_content = f.read()
                self.process_request_log(new_content)
            self.last_request_position = current_request_size

        # Verificar nuevas respuestas
        current_response_size = os.path.getsize(RESPONSE_LOG)
        if current_response_size > self.last_response_position:
            with open(RESPONSE_LOG, "r") as f:
                f.seek(self.last_response_position)
                new_content = f.read()
                self.process_response_log(new_content)
            self.last_response_position = current_response_size

    def process_request_log(self, content):
        """Procesa y muestra nuevas entradas de peticiones"""
        entries = content.split("--- NUEVA PETICIÓN:")
        for entry in entries:
            if entry.strip() and "messages" in entry:
                # Extraer fecha/hora si está disponible
                timestamp = entry.split("---")[0].strip() if "---" in entry else "Sin fecha"
                
                # Intentar analizar el JSON
                try:
                    # Encontrar el inicio del JSON
                    json_start = entry.find("{")
                    if json_start != -1:
                        json_content = entry[json_start:]
                        data = json.loads(json_content)
                        
                        # Crear un identificador único para esta petición
                        request_id = hash(json.dumps(data))
                        
                        # Verificar si ya hemos visto esta petición
                        if request_id not in self.requests_seen:
                            self.requests_seen.add(request_id)
                            
                            # Mostrar información relevante
                            print(f"\n{Fore.YELLOW}==== NUEVA PETICIÓN ({timestamp}) ===={Style.RESET_ALL}")
                            print(f"{Fore.CYAN}Modelo:{Style.RESET_ALL} {data['model']}")
                            print(f"{Fore.CYAN}Prompt:{Style.RESET_ALL}")
                            
                            # Mostrar cada mensaje con formato
                            for msg in data['messages']:
                                role = msg.get('role', 'unknown')
                                content = msg.get('content', '')
                                role_color = Fore.GREEN if role == 'user' else Fore.BLUE
                                print(f"{role_color}{role}{Style.RESET_ALL}: {content}")
                            
                            print(f"{Fore.CYAN}Configuración:{Style.RESET_ALL} max_tokens={data.get('max_tokens', 'N/A')}, temperature={data.get('temperature', 'N/A')}")
                except json.JSONDecodeError:
                    print(f"{Fore.RED}Error al decodificar JSON en el log de peticiones{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error al procesar log de peticiones: {e}{Style.RESET_ALL}")

    def process_response_log(self, content):
        """Procesa y muestra nuevas entradas de respuestas"""
        entries = content.split("--- RESPUESTA:")
        for entry in entries:
            if entry.strip() and "content" in entry:
                # Extraer fecha/hora si está disponible
                timestamp = entry.split("---")[0].strip() if "---" in entry else "Sin fecha"
                
                # Crear un identificador único para esta respuesta
                response_id = hash(entry)
                
                # Verificar si ya hemos visto esta respuesta
                if response_id not in self.responses_seen:
                    self.responses_seen.add(response_id)
                    
                    print(f"\n{Fore.YELLOW}==== RESPUESTA RECIBIDA ({timestamp}) ===={Style.RESET_ALL}")
                    
                    # Extraer el contenido del mensaje
                    content_start = entry.find("content='")
                    if content_start != -1:
                        content_start += 9  # Longitud de "content='"
                        content_end = entry.find("'", content_start)
                        if content_end != -1:
                            message_content = entry[content_start:content_end]
                            print(f"{Fore.MAGENTA}Contenido:{Style.RESET_ALL} {message_content}")
                    else:
                        # Si no podemos extraer limpiamente, mostrar todo
                        print(entry.strip())

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, log_reader):
        self.log_reader = log_reader
        
    def on_modified(self, event):
        if not event.is_directory and event.src_path in [REQUEST_LOG, RESPONSE_LOG]:
            self.log_reader.check_for_new_content()

def main():
    # Crear el lector de logs
    log_reader = LogReader()
    
    # Configurar observador de archivos
    event_handler = LogFileHandler(log_reader)
    observer = Observer()
    observer.schedule(event_handler, LOGS_DIR, recursive=False)
    observer.start()
    
    try:
        # Verificar periódicamente aunque no haya eventos
        while True:
            log_reader.check_for_new_content()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print(f"\n{Fore.GREEN}Observador de logs detenido.{Style.RESET_ALL}")
    
    observer.join()

if __name__ == "__main__":
    main()