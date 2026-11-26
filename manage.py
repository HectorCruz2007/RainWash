#!/usr/bin/env python
"""Punto de entrada para los comandos de Django (runserver, migrate, check...)."""

import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as error:
        raise ImportError(
            "No se pudo importar Django. Activa el entorno virtual e instala requirements.txt."
        ) from error
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
