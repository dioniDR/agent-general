# Flujo de Ejecución del Proyecto Agent General

## Diagrama de Flujo

```mermaid
flowchart TD
    A["main.py"] --> B["load_settings()"]
    A --> C["build_context()"]
    A --> D["get_objective()"]
    
    B --> E["OpenAIProvider"]
    E --> F["generar_tareas()"]
    
    C --> G["Obtener lista de archivos del directorio"]
    
    D --> H["Definir objetivo específico"]
    
    F --> I["Executor"]
    I --> J["execute()"]
    
    subgraph "Archivos Involucrados"
        main["main.py"]
        settings["config/settings.py"]
        context["agent/context.py"]
        objectives["agent/objectives.py"]
        provider["providers/openai_provider.py"]
        executor["agent/executor.py"]
    end
    
    main --> settings
    main --> context
    main --> objectives
    main --> provider
    main --> executor
    
    subgraph "Flujo de Ejecución"
        K["1. Cargar configuración"]
        L["2. Obtener contexto"]
        M["3. Definir objetivo"]
        N["4. Generar tareas con IA"]
        O["5. Ejecutar tareas"]
    end
    
    B --> K
    C --> L
    D --> M
    F --> N
    J --> O
```

## Descripción del Flujo

### Archivos Principales
- `main.py`: Punto de entrada principal
- `config/settings.py`: Gestión de configuraciones
- `agent/context.py`: Manejo de contexto
- `agent/objectives.py`: Definición de objetivos
- `providers/openai_provider.py`: Interacción con IA
- `agent/executor.py`: Ejecución de tareas

### Pasos de Ejecución
1. **Cargar Configuración**: 
   - Obtiene configuraciones y clave de API de OpenAI
2. **Obtener Contexto**: 
   - Recopila información contextual (lista de archivos)
3. **Definir Objetivo**: 
   - Convierte la solicitud en un objetivo estructurado
4. **Generar Tareas con IA**: 
   - Descompone el objetivo en tareas específicas
5. **Ejecutar Tareas**: 
   - Procesa y ejecuta cada tarea generada

## Notas
- El diagrama muestra el flujo de control desde `main.py`
- Cada módulo tiene una responsabilidad específica
- La IA (OpenAI) ayuda a descomponer objetivos en tareas