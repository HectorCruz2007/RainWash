"""Lista los videos explicativos que hay que grabar.

Cada archivo nuevo con código lleva un video llamado INTEGRANTE_ruta.del.archivo.mp4:
cada "." es un nivel de carpeta desde la raíz y la extensión del archivo se omite.
Ejemplo: motor/flujo.py creado por B  ->  B_motor.flujo.mp4

Uso (desde la raíz del repositorio):
    python scripts/videos_pendientes.py A                  archivos nuevos de mi rama
    python scripts/videos_pendientes.py A --todos          todos los archivos del repositorio
    python scripts/videos_pendientes.py A --carpeta RUTA   oculta los videos que ya están en RUTA
"""

import argparse
import subprocess
import sys
from collections import Counter
from pathlib import Path, PurePosixPath

RAIZ = Path(__file__).resolve().parent.parent
EXTENSIONES_DE_CODIGO = {".py", ".js", ".html", ".css", ".yml", ".yaml"}


def es_codigo(ruta, contenido):
    """Cuenta si tiene extensión de código, no es una migración de Django y no está vacío."""
    ruta = PurePosixPath(ruta)
    if ruta.suffix not in EXTENSIONES_DE_CODIGO or "migrations" in ruta.parts:
        return False
    return contenido.strip() != ""


def nombres_de_video(integrante, rutas):
    """Devuelve {ruta: nombre del video} para la lista completa de archivos con código."""
    veces = Counter(PurePosixPath(ruta).with_suffix("") for ruta in rutas)
    nombres = {}
    for ruta in rutas:
        sin_extension = PurePosixPath(ruta).with_suffix("")
        nombre = ".".join(sin_extension.parts)
        # Si dos archivos solo difieren en la extensión, se agrega para distinguirlos.
        if veces[sin_extension] > 1:
            nombre += "-" + PurePosixPath(ruta).suffix.lstrip(".")
        nombres[ruta] = f"{integrante}_{nombre}.mp4"
    return nombres


def git(*argumentos):
    """Ejecuta git en la raíz del repositorio y devuelve las líneas de su salida."""
    resultado = subprocess.run(
        ["git", "-c", "core.quotepath=false", *argumentos],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return resultado.stdout.splitlines()


def archivos_con_codigo():
    """Archivos con código que git conoce o que son nuevos y no están ignorados."""
    rutas = git("ls-files", "--cached", "--others", "--exclude-standard")
    existentes = [ruta for ruta in rutas if (RAIZ / ruta).is_file()]
    return [
        ruta
        for ruta in existentes
        if es_codigo(ruta, (RAIZ / ruta).read_text(encoding="utf-8", errors="ignore"))
    ]


def archivos_nuevos(base):
    """Archivos que están en la rama actual (confirmados o no) y no en la rama base."""
    punto_comun = git("merge-base", base, "HEAD")[0]
    agregados = git("diff", "--name-only", "--diff-filter=A", punto_comun)
    sin_seguimiento = git("ls-files", "--others", "--exclude-standard")
    return set(agregados) | set(sin_seguimiento)


def main():
    parser = argparse.ArgumentParser(description="Lista los videos explicativos por grabar.")
    parser.add_argument("integrante", type=str.upper, choices=["A", "B", "C"])
    parser.add_argument("--base", default="origin/main", help="rama contra la que se compara")
    parser.add_argument("--todos", action="store_true", help="incluye todos los archivos")
    parser.add_argument("--carpeta", type=Path, help="carpeta local con los videos ya grabados")
    opciones = parser.parse_args()

    con_codigo = archivos_con_codigo()
    nombres = nombres_de_video(opciones.integrante, con_codigo)

    candidatos = con_codigo
    if not opciones.todos:
        try:
            nuevos = archivos_nuevos(opciones.base)
        except subprocess.CalledProcessError:
            sys.exit(
                f"No encontré la rama '{opciones.base}'. Usa --todos o indica otra con --base."
            )
        candidatos = [ruta for ruta in con_codigo if ruta in nuevos]

    grabados = set()
    if opciones.carpeta:
        grabados = {video.name for video in opciones.carpeta.glob("*.mp4")}
    pendientes = [ruta for ruta in candidatos if nombres[ruta] not in grabados]

    for ruta in pendientes:
        print(f"{nombres[ruta]}  <-  {ruta}")
    print(f"\n{len(pendientes)} video(s) por grabar de {len(candidatos)} archivo(s) con código.")


if __name__ == "__main__":
    main()
