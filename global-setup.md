# Configuración Global de Agent General

Esta guía te mostrará cómo configurar Agent General como un comando global accesible desde cualquier ubicación con el alias simple "y".

## Visión General

La configuración global te permite:
- Ejecutar Agent General desde cualquier directorio con el comando "y"
- Mantener una sola instalación del proyecto
- Actualizar fácilmente cuando haya cambios

## Requisitos Previos

- Python 3.8 o superior
- pipx (`sudo apt install pipx`)
- Permisos de administrador (para algunas instalaciones)

## Instalación Automática (Recomendado)

La forma más sencilla de configurar la instalación global es usar nuestro script automatizado:

```bash
cd ~/proyectos/agent-general  # O la ubicación de tu proyecto
python install_global.py
```

El script se encargará de todo:
- Verificar/instalar dependencias
- Crear el archivo setup.py si no existe
- Instalar el paquete globalmente
- Configurar el alias "y"

## Instalación Manual

Si prefieres seguir los pasos manualmente:

### 1. Preparar setup.py

Crea un archivo `setup.py` en la raíz del proyecto con el siguiente contenido:

```python
from setuptools import setup, find_packages

setup(
    name="agent-general",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["main"],  # Incluir main.py de la raíz
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "PyYAML>=6.0",
        "click>=8.1.3",
        "requests>=2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'agent-general=main:main',
        ],
    },
)
```

### 2. Instalar con pipx

```bash
# Instalar pipx si no lo tienes
sudo apt install pipx
pipx ensurepath

# Instalar el paquete en modo editable
cd ~/proyectos/agent-general  # La ubicación de tu proyecto
pipx install -e .
```

### 3. Configurar el alias "y"

Añade el siguiente alias a tu archivo de configuración de shell:

Para Bash (edita ~/.bashrc):
```bash
echo 'alias y="agent-general"' >> ~/.bashrc
source ~/.bashrc
```

Para Zsh (edita ~/.zshrc):
```bash
echo 'alias y="agent-general"' >> ~/.zshrc
source ~/.zshrc
```

Para Fish (edita ~/.config/fish/config.fish):
```bash
echo 'alias y="agent-general"' >> ~/.config/fish/config.fish
source ~/.config/fish/config.fish
```

## Uso

Una vez completada la instalación, puedes ejecutar el agente desde cualquier ubicación con:

```bash
y
```

## Actualización

Si realizas cambios en el código del proyecto:

1. **La ventaja del modo editable (-e)**: Los cambios que hagas en el código se reflejan automáticamente en el comando global, sin necesidad de reinstalar.

2. **Si quieres actualizar desde GitHub**:
```bash
cd ~/proyectos/agent-general
git pull
# No necesitas reinstalar si usaste pipx install -e .
```

## Solución de Problemas

### El comando "y" no funciona

- Verifica que recargaste tu shell: `source ~/.bashrc` (o el archivo de tu shell)
- Comprueba que pipx está en tu PATH: `echo $PATH`
- Verifica que la instalación fue exitosa: `pipx list`

### Errores en la ejecución

- Verifica que tienes acceso a la API de OpenAI: comprueba tu archivo .env
- Asegúrate de que todas las dependencias están instaladas

### Desinstalación

Si necesitas desinstalar el paquete global:

```bash
pipx uninstall agent-general
```

Y elimina el alias de tu archivo de configuración de shell.

## Notas Adicionales

- Los logs y archivos temporales se guardan en tu directorio home
- Las configuraciones específicas del usuario se guardan en ~/.agent-general/ (si está configurado)
- Para depuración, puedes ejecutar con el flag completo: `agent-general --verbose`
