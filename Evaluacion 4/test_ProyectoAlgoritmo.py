def test_buscar_proyecto():
    proyectos = [
        Proyecto("1", "Proyecto 1", "Descripción 1", datetime(2022, 1, 1), datetime(2022, 1, 31), "Activo", "Empresa 1", "Gerente 1", "Equipo 1"),
        Proyecto("2", "Proyecto 2", "Descripción 2", datetime(2022, 2, 1), datetime(2022, 2, 28), "Inactivo", "Empresa 2", "Gerente 2", "Equipo 2"),
        Proyecto("3", "Proyecto 3", "Descripción 3", datetime(2022, 3, 1), datetime(2022, 3, 31), "Activo", "Empresa 3", "Gerente 3", "Equipo 3"),
    ]
    manager = ProyectoManager(proyectos)

    # Test case 1: Searching by valid ID
    proyecto = manager.buscar_proyecto("id", "2")
    assert proyecto is not None
    assert proyecto.id == "2"

    # Test case 2: Searching by valid nombre
    proyecto = manager.buscar_proyecto("nombre", "Proyecto 3")
    assert proyecto is not None
    assert proyecto.nombre == "Proyecto 3"

    # Test case 3: Searching by valid fecha_inicio
    proyecto = manager.buscar_proyecto("fecha inicio", "2022-02-01")
    assert proyecto is not None
    assert proyecto.fecha_inicio == datetime(2022, 2, 1)

    # Test case 4: Searching by valid estado
    proyecto = manager.buscar_proyecto("estado", "Activo")
    assert proyecto is not None
    assert proyecto.estado == "Activo"

    # Test case 5: Searching by invalid criterio
    proyecto = manager.buscar_proyecto("invalido", "valor")
    assert proyecto is None

    # Test case 6: Searching by invalid valor
    proyecto = manager.buscar_proyecto("nombre", "Proyecto 4")
    assert proyecto is None

    # Test case 7: Searching by invalid fecha_inicio format
    proyecto = manager.buscar_proyecto("fecha inicio", "2022/02/01")
    assert proyecto is None

    # Test case 8: Searching by invalid fecha_inicio value
    proyecto = manager.buscar_proyecto("fecha inicio", "2022-02-31")
    assert proyecto is None

    # Test case 9: Searching by valid criterio and valor, but no matching proyecto
    proyecto = manager.buscar_proyecto("estado", "Finalizado")
    assert proyecto is None

test_buscar_proyecto()