from apps.comun.models import Origen, ProcedenciaMixin


def campo(nombre):
    return ProcedenciaMixin._meta.get_field(nombre)


def test_es_abstracto_y_no_crea_tabla():
    assert ProcedenciaMixin._meta.abstract


def test_un_dato_nuevo_es_manual_y_medido_por_defecto():
    assert campo("origen").default == Origen.MANUAL
    assert campo("es_estimado").default is False


def test_fuente_y_fecha_de_consulta_son_opcionales():
    assert campo("fuente").blank
    assert campo("fecha_consulta").null
