"""Genera tree.txt con la estructura del repositorio.

Lista los archivos que git conoce (respeta .gitignore), así el resultado es el mismo
en cualquier computadora.

Uso (desde la raíz del repositorio):
    python scripts/actualizar_tree.py           reescribe tree.txt
    python scripts/actualizar_tree.py --check   falla si tree.txt no está al día (lo usa el CI)
"""

import argparse
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "tree.txt"


def archivos_del_repo():
    """Archivos que git conoce o que son nuevos y no están ignorados."""
    resultado = subprocess.run(
        ["git", "-c", "core.quotepath=false", "ls-files", "--cached", "--others",
         "--exclude-standard"],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    existentes = {ruta for ruta in resultado.stdout.splitlines() if (RAIZ / ruta).is_file()}
    # tree.txt se lista a sí mismo aunque todavía no exista.
    return existentes | {DESTINO.name}


def construir_arbol(rutas):
    """Convierte rutas como "apps/cuentas/models.py" en el texto del árbol."""
    raiz = {}
    for ruta in rutas:
        nodo = raiz
        for parte in ruta.split("/"):
            nodo = nodo.setdefault(parte, {})
    lineas = ["."]
    dibujar(raiz, "", lineas)
    return "\n".join(lineas) + "\n"


def dibujar(nodo, sangria, lineas):
    """Agrega a `lineas` el contenido de una carpeta: primero subcarpetas, después archivos."""
    nombres = sorted(nodo, key=lambda nombre: (not nodo[nombre], nombre.lower(), nombre))
    for posicion, nombre in enumerate(nombres):
        es_ultimo = posicion == len(nombres) - 1
        es_carpeta = bool(nodo[nombre])
        rama = "└── " if es_ultimo else "├── "
        lineas.append(f"{sangria}{rama}{nombre}{'/' if es_carpeta else ''}")
        dibujar(nodo[nombre], sangria + ("    " if es_ultimo else "│   "), lineas)


def main():
    parser = argparse.ArgumentParser(description="Genera o verifica tree.txt.")
    parser.add_argument("--check", action="store_true", help="solo verifica, no escribe")
    opciones = parser.parse_args()

    esperado = construir_arbol(archivos_del_repo())
    if opciones.check:
        actual = DESTINO.read_text(encoding="utf-8") if DESTINO.exists() else ""
        if actual != esperado:
            sys.exit("tree.txt no está al día. Corre: python scripts/actualizar_tree.py")
        return
    DESTINO.write_text(esperado, encoding="utf-8", newline="\n")
    print("tree.txt actualizado.")


if __name__ == "__main__":
    main()
