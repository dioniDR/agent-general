# Agent General

Agent General es un asistente inteligente impulsado por IA que te permite ejecutar tareas, obtener respuestas y automatizar acciones mediante lenguaje natural.

## 📋 Índice
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso Básico](#uso-básico)
- [Modos de Operación](#modos-de-operación)
- [Ejemplos Prácticos](#ejemplos-prácticos)
- [Comandos Avanzados](#comandos-avanzados)
- [Configuración](#configuración)
- [Solución de Problemas](#solución-de-problemas)
- [Instalación Global](#instalación-global)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuir](#contribuir)

## ✨ Características

- **Interacción Natural**: Comunícate con el agente usando lenguaje natural
- **Múltiples Proveedores**: Compatible con OpenAI GPT-4, Claude y otros modelos de IA
- **Seguridad Integrada**: Validación de comandos para operaciones seguras
- **Modos Flexibles**: Operación en modo visualización, interactivo o automático
- **Extensible**: Arquitectura modular para añadir nuevas funcionalidades
- **Instalación Global**: Disponible como comando global "y" para acceso rápido

## 🔧 Requisitos

- Python 3.8 o superior
- Clave API de OpenAI (y/o otras APIs según los proveedores configurados)
- Dependencias listadas en `requirements.txt`

## 📥 Instalación

### Instalación Básica

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/agent-general.git
cd agent-general

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key (crea un archivo .env)
echo "OPENAI_API_KEY=tu-clave-api-aquí" > .env
```

### Instalación Global (uso rápido)

Para instalar Agent General como comando global "y", consulta [GLOBAL_SETUP.md](GLOBAL_SETUP.md) o ejecuta el script automático:

```bash
cd agent-general
python install_global.py
```

## 🚀 Uso Básico

### Ejecutar Localmente

```bash
python main.py
```

### Ejecutar desde Cualquier Ubicación (si está instalado globalmente)

```bash
y
```

Al iniciar el agente, verás un mensaje de bienvenida y un menú para seleccionar el modo de operación.

## 🔄 Modos de Operación

Agent General ofrece tres modos de operación que puedes seleccionar al iniciar:

### 1. Modo Visualización (Display)

```bash
python main.py --mode display
# O globalmente:
y --mode display
```

Este modo solo muestra las tareas generadas sin ejecutarlas, ideal para:
- Ver qué haría el agente sin ejecutar acciones
- Entender cómo descompone un objetivo complejo
- Aprender qué comandos se utilizarían

### 2. Modo Interactivo (Interactive)

```bash
python main.py --mode interactive
# O globalmente:
y --mode interactive
```

Este modo es el predeterminado y solicita confirmación antes de ejecutar cada tarea:
- Te muestra cada tarea y pide confirmación (s/n)
- Puedes aprobar o rechazar tareas individualmente
- Proporciona control granular sobre las acciones

### 3. Modo Automático (Auto)

```bash
python main.py --mode auto
# O globalmente:
y --mode auto
```

Este modo ejecuta todas las tareas automáticamente:
- No requiere intervención del usuario
- Ejecuta todas las tareas en secuencia
- Ideal para procesos automatizados o scripts

## 💡 Ejemplos Prácticos

### Ejemplo 1: Información del Sistema

```bash
y

# Al ver el prompt "¿Qué quieres que haga?", escribe:
Muéstrame información detallada sobre el sistema
```

El agente generará y ejecutará tareas como:
1. Mostrar información del host
2. Comprobar el uso de CPU y memoria
3. Listar espacio en disco
4. Mostrar versión del sistema operativo

### Ejemplo 2: Operaciones con Archivos

```bash
y

# Al prompt, escribe:
Encuentra todos los archivos PDF en el directorio actual y sus subdirectorios
```

El agente creará tareas como:
1. Verificar que el comando find está disponible
2. Ejecutar una búsqueda recursiva de archivos PDF
3. Contar y mostrar los resultados

### Ejemplo 3: Asistencia en Programación

```bash
y

# Al prompt, escribe:
Escribe un script en Python para descargar una imagen de una URL
```

El agente generará código Python similar a:

```python
import requests

def download_image(url, file_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Imagen descargada correctamente en {file_path}")
    else:
        print(f"Error al descargar la imagen: {response.status_code}")

# Ejemplo de uso
url = "https://ejemplo.com/imagen.jpg"
download_image(url, "imagen_descargada.jpg")
```

### Ejemplo 4: Tareas Creativas

```bash
y

# Al prompt, escribe:
Genera un nombre para una aplicación de gestión de proyectos
```

El agente proporcionará sugerencias creativas como:
- TaskFlow
- ProjectPilot
- MilestoneManager
- CollabTrack

## ⌨️ Comandos Avanzados

### Banderas de Línea de Comandos

Agent General acepta varias banderas para personalizar su comportamiento:

```bash
# Ejecutar en modo detallado con logs adicionales
y --verbose

# Especificar un archivo de configuración alternativo
y --config mi_config.yaml

# Combinar banderas
y --mode auto --verbose --config mi_config.yaml
```

### Comandos Especiales

Durante la interacción, puedes usar comandos especiales:

- `!help`: Muestra ayuda sobre comandos disponibles
- `!exit` o `!quit`: Sale del agente
- `!mode [display|interactive|auto]`: Cambia el modo de operación
- `!history`: Muestra historial de comandos recientes

## ⚙️ Configuración

### Archivo .env

El archivo `.env` almacena claves API y otras configuraciones sensibles:

```
OPENAI_API_KEY=sk-tu-clave-aquí
CLAUDE_API_KEY=sk-tu-clave-aquí
DEBUG=false
```

### Archivo config/settings.yaml

El archivo `config/settings.yaml` contiene configuraciones generales:

```yaml
# Modo debug (True/False)
debug: False

# Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
log_level: INFO

# Configuración de proveedores
providers:
  # Configuración para OpenAI
  openai:
    model: gpt-4
    max_tokens: 150
    temperature: 0.7
  
  # Configuración para Claude
  claude:
    enabled: False
```

## 🔍 Solución de Problemas

### API Key no encontrada

```
❌ Error: No se encontró la clave de API de OpenAI.
```

**Solución**: Verifica que el archivo `.env` existe y contiene la clave correcta.

### Errores de dependencias

```
ModuleNotFoundError: No module named 'xyz'
```

**Solución**: Asegúrate de haber instalado todas las dependencias con `pip install -r requirements.txt`.

### Comando "y" no disponible

**Solución**: Verifica la instalación global siguiendo las instrucciones en `GLOBAL_SETUP.md`.

## 🌐 Instalación Global

Para una guía detallada sobre cómo instalar Agent General como comando global "y", consulta el archivo [GLOBAL_SETUP.md](GLOBAL_SETUP.md).

## 📁 Estructura del Proyecto

```
agent-general/
├── agent/                  # Módulos principales del agente
│   ├── __init__.py
│   ├── core.py             # Componente central
│   ├── context.py          # Manejo de contexto
│   ├── executor.py         # Ejecutor de tareas
│   └── objectives.py       # Definición de objetivos
├── providers/              # Proveedores de IA
│   ├── __init__.py
│   ├── base_provider.py    # Clase base para proveedores
│   ├── openai_provider.py  # Integración con OpenAI
│   ├── claude_provider.py  # Integración con Claude
│   └── fake_provider.py    # Proveedor de pruebas
├── utils/                  # Utilidades
│   ├── __init__.py
│   ├── logger.py           # Configuración de logging
│   ├── security.py         # Funciones de seguridad
│   └── command_validator.py # Validación de comandos
├── config/                 # Configuración
│   ├── settings.yaml       # Configuración principal
│   └── settings.py         # Funciones para cargar configuración
├── tests/                  # Pruebas
│   ├── test_core.py
│   └── test_providers.py
├── main.py                 # Punto de entrada principal
├── setup.py                # Configuración para instalación
├── install_global.py       # Script de instalación global
├── requirements.txt        # Dependencias
├── README.md               # Documentación principal
├── GLOBAL_SETUP.md         # Guía de instalación global
└── .env                    # Variables de entorno
```

## 👥 Contribuir

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

---

*¿Preguntas o problemas? Abre un issue en el repositorio o contacta con el equipo de desarrollo.*
