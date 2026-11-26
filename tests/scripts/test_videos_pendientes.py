from scripts.videos_pendientes import es_codigo, nombres_de_video


def test_cada_punto_es_un_nivel_de_carpeta_y_se_omite_la_extension():
    nombres = nombres_de_video("A", ["core/domain/api/wathers.py"])
    assert nombres["core/domain/api/wathers.py"] == "A_core.domain.api.wathers.mp4"


def test_una_carpeta_oculta_conserva_su_punto():
    nombres = nombres_de_video("A", [".github/workflows/ci.yml"])
    assert nombres[".github/workflows/ci.yml"] == "A_.github.workflows.ci.mp4"


def test_si_solo_cambia_la_extension_se_agrega_para_distinguir():
    nombres = nombres_de_video("B", ["static/mapa.js", "static/mapa.css", "static/otro.js"])
    assert nombres["static/mapa.js"] == "B_static.mapa-js.mp4"
    assert nombres["static/mapa.css"] == "B_static.mapa-css.mp4"
    assert nombres["static/otro.js"] == "B_static.otro.mp4"


def test_cuenta_como_codigo_un_archivo_python_con_contenido():
    assert es_codigo("motor/flujo.py", "def d8(): ...")
    assert es_codigo("templates/base.html", "<html></html>")


def test_no_cuentan_vacios_migraciones_ni_documentos():
    assert not es_codigo("apps/cuentas/__init__.py", "")
    assert not es_codigo("apps/cuentas/migrations/0001_initial.py", "class Migration: ...")
    assert not es_codigo("README.md", "# Proyecto")
