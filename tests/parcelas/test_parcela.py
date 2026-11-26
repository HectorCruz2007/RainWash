import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import ProtectedError

from apps.parcelas.models import Parcela

pytestmark = pytest.mark.django_db

# Un cuadrado pequeño; en GeoJSON cada posición es [longitud, latitud].
CUADRADO = {
    "type": "Polygon",
    "coordinates": [[[-99.0, 19.0], [-99.0, 19.001], [-98.999, 19.001], [-98.999, 19.0],
                     [-99.0, 19.0]]],
}


@pytest.fixture
def ana(django_user_model):
    return django_user_model.objects.create_user("ana")


@pytest.fixture
def luis(django_user_model):
    return django_user_model.objects.create_user("luis")


def test_parcela_valida_se_guarda(ana):
    parcela = Parcela(nombre="El Encino", propietario=ana, geometria=CUADRADO,
                      superficie_declarada_ha=1.2)
    parcela.full_clean()
    parcela.save()
    assert str(parcela) == "El Encino"
    assert list(ana.parcelas.all()) == [parcela]


def test_la_parcela_puede_registrarse_antes_de_dibujar_su_poligono(ana):
    Parcela(nombre="Sin mapa", propietario=ana).full_clean()


def test_un_propietario_no_repite_nombre_de_parcela(ana, luis):
    Parcela.objects.create(nombre="La Loma", propietario=ana)
    Parcela.objects.create(nombre="La Loma", propietario=luis)
    with pytest.raises(IntegrityError):
        Parcela.objects.create(nombre="La Loma", propietario=ana)


@pytest.mark.parametrize(
    "geometria",
    [
        {"type": "Point", "coordinates": [-99.0, 19.0]},
        {"type": "Polygon", "coordinates": [[[-99.0, 19.0], [-99.0, 19.001]]]},
        {"type": "Polygon", "coordinates": [5]},
        "no es geojson",
    ],
)
def test_geometria_que_no_es_poligono_se_rechaza(ana, geometria):
    with pytest.raises(ValidationError):
        Parcela(nombre="Mala", propietario=ana, geometria=geometria).full_clean()


def test_superficie_declarada_negativa_se_rechaza(ana):
    with pytest.raises(ValidationError):
        Parcela(nombre="Negativa", propietario=ana, superficie_declarada_ha=-1).full_clean()


def test_no_se_borra_un_usuario_que_tiene_parcelas(ana):
    Parcela.objects.create(nombre="El Encino", propietario=ana)
    with pytest.raises(ProtectedError):
        ana.delete()
