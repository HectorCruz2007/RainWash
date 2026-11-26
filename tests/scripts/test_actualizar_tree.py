from scripts.actualizar_tree import construir_arbol


def test_carpetas_primero_y_orden_alfabetico():
    rutas = ["manage.py", "apps/parcelas/models.py", "apps/cuentas/models.py", "README.md"]
    assert construir_arbol(rutas) == (
        ".\n"
        "├── apps/\n"
        "│   ├── cuentas/\n"
        "│   │   └── models.py\n"
        "│   └── parcelas/\n"
        "│       └── models.py\n"
        "├── manage.py\n"
        "└── README.md\n"
    )


def test_el_orden_de_entrada_no_cambia_el_resultado():
    rutas = ["b.py", "a/x.py", "a/y.py"]
    assert construir_arbol(rutas) == construir_arbol(list(reversed(rutas)))
