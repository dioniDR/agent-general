#!/usr/bin/env python3
"""
Script de instalación global para agent-general.
Este script automatiza todo el proceso de instalación para hacer
que el proyecto sea accesible como un comando global "y".
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path


def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    print("✓ Verificando dependencias...")
    
    # Verificar Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("✗ Error: Se requiere Python 3.8 o superior.")
        sys.exit(1)
    
    # Verificar pipx
    try:
        subprocess.run(["pipx", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("  ✓ pipx está instalado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ✗ pipx no está instalado. Intentando instalar...")
        try:
            subprocess.run(["sudo", "apt", "install", "-y", "pipx"], check=True)
            subprocess.run(["pipx", "ensurepath"], check=True)
            print("  ✓ pipx instalado correctamente")
        except subprocess.CalledProcessError:
            print("  ✗ Error al instalar pipx. Por favor, instálalo manualmente:")
            print("    sudo apt install pipx")
            print("    pipx ensurepath")
            sys.exit(1)


def create_setup_py(project_dir):
    """Crea el archivo setup.py si no existe."""
    setup_path = os.path.join(project_dir, "setup.py")
    
    if os.path.exists(setup_path):
        print(f"✓ Archivo setup.py encontrado en {setup_path}")
        return
    
    print(f"✓ Creando setup.py en {setup_path}...")
    
    setup_content = """from setuptools import setup, find_packages

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
"""
    
    with open(setup_path, "w") as f:
        f.write(setup_content)
    
    print("  ✓ setup.py creado correctamente")


def install_package(project_dir):
    """Instala el paquete globalmente usando pipx."""
    print("✓ Instalando el paquete con pipx...")
    
    os.chdir(project_dir)
    
    try:
        # Desinstalar primero si ya existe para evitar conflictos
        subprocess.run(["pipx", "uninstall", "agent-general"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        # Es normal que falle si no está instalado
        pass
    
    try:
        # Instalar en modo editable
        result = subprocess.run(["pipx", "install", "-e", "."], 
                               check=True, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        print(f"  ✓ Paquete instalado correctamente")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error al instalar el paquete: {e}")
        print(f"  Salida: {e.stdout.decode() if e.stdout else ''}")
        print(f"  Error: {e.stderr.decode() if e.stderr else ''}")
        sys.exit(1)


def create_alias(shell_type=None):
    """Crea un alias para el comando en el archivo de configuración del shell."""
    print("✓ Configurando el alias 'y'...")
    
    # Detectar automáticamente el shell si no se especifica
    if not shell_type:
        shell = os.environ.get("SHELL", "")
        if "bash" in shell:
            shell_type = "bash"
        elif "zsh" in shell:
            shell_type = "zsh"
        elif "fish" in shell:
            shell_type = "fish"
        else:
            shell_type = "bash"  # Por defecto
    
    # Configurar según el tipo de shell
    if shell_type == "bash":
        config_file = os.path.expanduser("~/.bashrc")
        alias_line = 'alias y="agent-general"\n'
    elif shell_type == "zsh":
        config_file = os.path.expanduser("~/.zshrc")
        alias_line = 'alias y="agent-general"\n'
    elif shell_type == "fish":
        config_file = os.path.expanduser("~/.config/fish/config.fish")
        alias_line = 'alias y="agent-general"\n'
    else:
        print(f"  ✗ Shell no soportado: {shell_type}")
        print("  Por favor, añade manualmente el alias 'y' a tu shell:")
        print('  alias y="agent-general"')
        return
    
    # Comprobar si el alias ya existe
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            content = f.read()
            if 'alias y="agent-general"' in content:
                print(f"  ✓ El alias ya existe en {config_file}")
                return
    
    # Añadir el alias
    with open(config_file, "a") as f:
        f.write("\n# Alias para agent-general\n")
        f.write(alias_line)
    
    print(f"  ✓ Alias añadido a {config_file}")
    print(f"  Para activar el alias inmediatamente, ejecuta: source {config_file}")


def create_global_readme(project_dir):
    """Crea un archivo GLOBAL_SETUP.md con instrucciones de instalación."""
    readme_path = os.path.join(project_dir, "GLOBAL_SETUP.md")
    
    print(f"✓ Creando archivo de instrucciones en {readme_path}...")
    
    readme_content = """# Configuración Global de agent-general

Este documento describe cómo instalar y configurar agent-general como un comando global accesible con el alias "y".

## Instalación Automatizada

La forma más sencilla de instalar agent-general globalmente es usar el script de instalación:

```bash
python install_global.py
```

## Instalación Manual

Si prefieres instalar manualmente, sigue estos pasos:

### 1. Requisitos Previos

Asegúrate de tener instalados:
- Python 3.8 o superior
- pipx (`sudo apt install pipx`)

### 2. Instalar con pipx

Desde el directorio raíz del proyecto:

```bash
pipx install -e .
```

### 3. Configurar el alias

Añade lo siguiente a tu archivo de configuración de shell (~/.bashrc, ~/.zshrc, etc.):

```bash
alias y="agent-general"
```

Luego recarga la configuración:

```bash
source ~/.bashrc  # o el archivo correspondiente
```

## Uso

Una vez instalado, puedes ejecutar la aplicación desde cualquier directorio con:

```bash
y
```

## Actualización

Si has modificado el código fuente y quieres que los cambios se reflejen:

1. Si instalaste con `-e` (editable): No necesitas hacer nada más, los cambios se reflejan automáticamente.

2. Si instalaste sin `-e`: Reinstala con `pipx install -e .`

## Desinstalación

Para eliminar la instalación global:

```bash
pipx uninstall agent-general
```

Y elimina el alias de tu archivo de configuración de shell.
"""
    
    with open(readme_path, "w") as f:
        f.write(readme_content)
    
    print(f"  ✓ Archivo GLOBAL_SETUP.md creado correctamente")


def main():
    """Función principal del script de instalación."""
    parser = argparse.ArgumentParser(description="Instalador global para agent-general")
    parser.add_argument("--directory", "-d", type=str, default=os.getcwd(),
                        help="Directorio del proyecto (por defecto: directorio actual)")
    parser.add_argument("--shell", "-s", type=str, choices=["bash", "zsh", "fish"],
                        help="Tipo de shell (por defecto: auto-detectado)")
    parser.add_argument("--no-alias", action="store_true",
                        help="No crear alias 'y'")
    
    args = parser.parse_args()
    
    # Convertir a ruta absoluta
    project_dir = os.path.abspath(args.directory)
    
    # Verificar que el directorio existe y contiene main.py
    if not os.path.exists(project_dir):
        print(f"✗ Error: El directorio {project_dir} no existe.")
        sys.exit(1)
    
    if not os.path.exists(os.path.join(project_dir, "main.py")):
        print(f"✗ Error: No se encontró main.py en {project_dir}.")
        print("Este script requiere que el archivo main.py esté en la raíz del proyecto.")
        sys.exit(1)
    
    print(f"🚀 Iniciando instalación global de agent-general desde {project_dir}")
    
    # Ejecutar pasos de instalación
    check_dependencies()
    create_setup_py(project_dir)
    install_package(project_dir)
    
    if not args.no_alias:
        create_alias(args.shell)
    
    create_global_readme(project_dir)
    
    print("\n✅ Instalación completada exitosamente!")
    print("Ahora puedes ejecutar el comando 'y' desde cualquier terminal.")
    print("Nota: Es posible que necesites reiniciar tu terminal o ejecutar:")
    print(f"source ~/.bashrc  # (o el archivo de configuración de tu shell)")
    print("\nPara más información, consulta el archivo GLOBAL_SETUP.md")


if __name__ == "__main__":
    main()
