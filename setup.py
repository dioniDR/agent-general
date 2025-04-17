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