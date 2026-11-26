# Plataforma web para el análisis del escurrimiento superficial

Proyecto final de Cálculo de Varias Variables. La plataforma toma la elevación de un
terreno agrícola, más datos de lluvia y de suelo, y estima por dónde corre el agua,
cuánta escurre y dónde se acumula o erosiona.

## Estado actual

Esqueleto del proyecto (Día 1 del plan):

- Inicio y cierre de sesión (RF-11.1).
- Usuario propio con cinco roles: administrador, técnico agrícola, analista
  hidrológico, productor agrícola y usuario de consulta.
- Modelo `Parcela` (nombre, descripción, polígono GeoJSON, superficie y propietario),
  administrable desde `/admin/`.
- `ProcedenciaMixin`: campos comunes para saber de dónde salió un dato y si es una
  medición o una estimación.
- CI en GitHub Actions y scripts de apoyo para `tree.txt` y para los videos.

## Tecnología

Python 3.12, Django 5.2 y SQLite en desarrollo. Las pruebas usan pytest y el estilo
se revisa con ruff. La interfaz usa Bootstrap 5.

## Puesta en marcha

Necesitas Python 3.12 y Git. En Windows (PowerShell):

```powershell
git clone URL_DEL_REPOSITORIO
cd NOMBRE_DE_LA_CARPETA
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Después abre <http://127.0.0.1:8000/> e inicia sesión con el usuario que creaste.

- Si PowerShell no deja activar el entorno, corre una vez
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- En macOS o Linux cambian tres líneas: `python3.12 -m venv .venv`,
  `source .venv/bin/activate` y `cp .env.example .env`.

## Antes de abrir un Pull Request

Estos son los mismos pasos que corre el CI. Todos deben pasar en tu computadora:

```powershell
ruff check .
python -m compileall -q apps config motor scripts tests manage.py
python manage.py check
python manage.py makemigrations --check --dry-run
python scripts/actualizar_tree.py
pytest
```

`ruff check --fix .` corrige solo la mayoría de los avisos de estilo.

## Reglas de trabajo

1. Nadie hace push directo a `main`. Todo entra por un Pull Request revisado por otro
   integrante y con el CI en verde.
2. Un commit solo importa archivos que ya están en `main`. Nada de stubs ni de código
   que dependa de archivos futuros.
3. Una rama por tarea, con la letra del integrante: `a/rf01-poligonos`, `b/flujo-d8`.
   Antes de abrir el PR: `git pull --rebase origin main`.
4. Cada quien genera migraciones solo de sus apps, siempre después del rebase.
5. `motor/` es Python puro y no importa Django. Las apps llaman al motor, nunca al revés.
6. Estos archivos son compartidos y en ellos solo se agregan líneas: `config/settings.py`
   (lista `INSTALLED_APPS`, en orden alfabético), `config/urls.py`, `templates/base.html`
   (menú), `requirements.txt`, `README.md` y `tree.txt`.
7. `tree.txt` no se edita a mano: se genera con `python scripts/actualizar_tree.py`.
   Si hay un conflicto en ese archivo, se resuelve corriendo el script otra vez.

## Videos explicativos

Cada archivo nuevo con código lleva un video corto de quien lo creó. El nombre es
`INTEGRANTE_ruta.del.archivo.mp4`: cada `.` es un nivel de carpeta desde la raíz y la
extensión del archivo se omite. Por ejemplo, `motor/flujo.py` creado por B se llama
`B_motor.flujo.mp4`.

```powershell
python scripts/videos_pendientes.py A                 # archivos nuevos de mi rama
python scripts/videos_pendientes.py A --todos         # todos los archivos del repositorio
python scripts/videos_pendientes.py A --carpeta RUTA  # oculta los que ya están en RUTA
```

- Cuentan los archivos `.py`, `.js`, `.html`, `.css` y `.yml`.
- No cuentan las migraciones que genera Django ni los archivos vacíos (`__init__.py`).
- Los videos no se suben a git. Van a la carpeta compartida del equipo y el PR lleva
  la lista que imprime el script.

## Estructura

La estructura completa está en `tree.txt`. Cada carpeta tiene un responsable:

| Carpeta | Responsable | Contenido |
| --- | --- | --- |
| `config/` | A | Configuración y rutas principales |
| `apps/comun/` | A | Piezas de modelo compartidas (`ProcedenciaMixin`) |
| `apps/cuentas/` | A | Usuarios, roles e inicio de sesión (RF-11) |
| `apps/parcelas/` | A | Parcelas agrícolas (RF-01) |
| `motor/` | A, B y C | Cálculo en Python puro, un módulo por responsable |
| `templates/` | A | Plantilla base y páginas generales |
| `scripts/` | A | Utilidades para `tree.txt` y para los videos |
| `tests/` | Todos | Una carpeta por módulo; cada quien escribe las suyas |

## Equipo

| Letra | Integrante | Área |
| --- | --- | --- |
| A | Hector | Plataforma y geografía |
| B | Daniela | Terreno y flujo |
| C | Abimael | Hidrología y simulación |
