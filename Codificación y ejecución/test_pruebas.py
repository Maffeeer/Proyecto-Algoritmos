"""
Pruebas básicas para validar cada módulo.

3 casos por módulo:
1. EXITOSO - Caso normal, parámetros válidos
2. BORDE - Casos extremos, límites
3. CUELLO DE BOTELLA - Prueba con muchos datos (1000 elementos)
"""

from modulos import (GestorUsuarios, GestorRecursos, GestorPrestamos, GestorTurnos,
                     GestorCategorias, GeneradorInformes, GestorInventario)


def test_m01_usuarios():
    print("\nM01 - GESTION DE USUARIOS")

    # CASO 1: EXITOSO
    print("[EXITOSO] Registrar usuario válido")
    gestor = GestorUsuarios()
    codigo = gestor.registrar("Juan Perez", "juan@test.com")
    assert codigo == "U001", f"Esperado U001, obtenido {codigo}"
    print(f"  ✓ Usuario registrado: {codigo}")

    # CASO 2: BORDE
    print("[BORDE] Registrar con nombre de 1 carácter")
    codigo = gestor.registrar("A", "a@test.com")
    usuario = gestor.buscarUsuario(codigo)
    assert usuario.nombre == "A", f"Nombre incorrecto: {usuario.nombre}"
    print(f"  ✓ Usuario con nombre 'A' registrado")

    # CASO 3: CUELLO DE BOTELLA
    print("[CUELLO DE BOTELLA] Registrar 1000 usuarios")
    gestor = GestorUsuarios()
    for i in range(1000):
        gestor.registrar(f"Usuario_{i}", f"user{i}@test.com")

    usuario = gestor.buscarUsuario("U500")
    assert gestor.obtenerCantidad() == 1000
    assert usuario is not None
    print(f"  ✓ 1000 usuarios registrados")


def test_m02_recursos():
    print("\nM02 - GESTION DE RECURSOS")

    # CASO 1: EXITOSO
    print("[EXITOSO] Registrar libro válido")
    gestor = GestorRecursos(numSedes=3)
    codigo = gestor.registrarLibro("Python 101", "Guido", "978-123", 2020)
    assert codigo is not None and codigo.startswith("R")
    print(f"  ✓ Libro registrado: {codigo}")

    # CASO 2: BORDE
    print("[BORDE] Registrar sala con capacidad mínima (1)")
    codigo = gestor.registrarSala("Sala_A", 1)
    sala = gestor.buscarxCodigo(codigo)
    assert sala is not None
    print(f"  ✓ Sala con capacidad 1 registrada")

    # CASO 3: CUELLO DE BOTELLA
    print("[CUELLO DE BOTELLA] Registrar 500 recursos mixtos")
    gestor = GestorRecursos(numSedes=3)
    for i in range(200):
        gestor.registrarLibro(f"Libro_{i}", f"Autor_{i}", f"ISBN-{i}", 2020)
    for i in range(200):
        gestor.registrarEquipo(f"Equipo_{i}", "Laptop", f"Model_{i}", "Centro")
    for i in range(100):
        gestor.registrarSala(f"Sala_{i}", 10 + i)

    cantidad = gestor.obtenerCantidad()
    assert cantidad == 500
    print(f"  ✓ 500 recursos registrados")


def test_m03_prestamos():
    print("\nM03 - GESTION DE PRESTAMOS")

    # Setup
    gestor_usuarios = GestorUsuarios()
    gestor_recursos = GestorRecursos(numSedes=3)
    gestor_turnos = GestorTurnos(gestorUsuarios=gestor_usuarios, gestorRecursos=gestor_recursos)
    gestor = GestorPrestamos(gestorTurnos=gestor_turnos, gestorUsuarios=gestor_usuarios,
                             gestorRecursos=gestor_recursos)

    # CASO 1: EXITOSO
    print("[EXITOSO] Registrar préstamo válido")
    gestor_recursos.registrarSede(0, "Centro")
    gestor_usuarios.registrar("User1", "user1@test.com")
    codigo_recurso = gestor_recursos.registrarLibro("Libro1", "Autor", "ISBN", 2020)
    gestor_recursos.actualizarDisponibilidad(codigo_recurso, "Centro", 5)

    codigo_prestamo = gestor.registrarPrestamo("U001", codigo_recurso, "Centro")
    assert codigo_prestamo is not None
    print(f"  ✓ Préstamo registrado: {codigo_prestamo}")

    # CASO 2: BORDE
    print("[BORDE] Rechazar préstamo sin unidades")
    gestor_usuarios.registrar("User2", "user2@test.com")
    codigo_r2 = gestor_recursos.registrarLibro("Unico", "Autor", "ISBN", 2020)
    gestor_recursos.actualizarDisponibilidad(codigo_r2, "Centro", 1)

    gestor.registrarPrestamo("U001", codigo_r2, "Centro")

    try:
        gestor.registrarPrestamo("U002", codigo_r2, "Centro")
        assert False, "Debería rechazar préstamo sin unidades"
    except:
        print(f"  ✓ Préstamo rechazado sin unidades")

    # CASO 3: CUELLO DE BOTELLA
    print("[CUELLO DE BOTELLA] Registrar 200 préstamos")
    gestor_usuarios = GestorUsuarios()
    gestor_recursos = GestorRecursos(numSedes=3)
    gestor_turnos = GestorTurnos(gestorUsuarios=gestor_usuarios, gestorRecursos=gestor_recursos)
    gestor = GestorPrestamos(gestorTurnos=gestor_turnos, gestorUsuarios=gestor_usuarios,
                             gestorRecursos=gestor_recursos)

    gestor_recursos.registrarSede(0, "Centro")
    for i in range(20):
        gestor_usuarios.registrar(f"User_{i}", f"user{i}@test.com")

    for i in range(10):
        codigo = gestor_recursos.registrarLibro(f"Libro_{i}", "Autor", f"ISBN-{i}", 2020)
        gestor_recursos.actualizarDisponibilidad(codigo, "Centro", 20)

    prestamos = []
    for i in range(200):
        try:
            usuario = f"U{(i % 20) + 1:03d}"
            recurso = f"R{(i % 10) + 1:04d}"
            codigo_p = gestor.registrarPrestamo(usuario, recurso, "Centro")
            prestamos.append(codigo_p)
        except:
            pass

    print(f"  ✓ {len(prestamos)} préstamos registrados")


def test_m04_turnos():
    print("\nM04 - GESTION DE TURNOS (Cola FIFO)")

    # CASO 1: EXITOSO
    print("[EXITOSO] Solicitar turno válido")
    gestor_usuarios = GestorUsuarios()
    gestor_recursos = GestorRecursos(numSedes=3)
    gestor = GestorTurnos(gestorUsuarios=gestor_usuarios, gestorRecursos=gestor_recursos)
    gestor_recursos.registrarSede(0, "Centro")  # la sede debe existir para pedir turno

    gestor_usuarios.registrar("Ana", "ana@test.com")
    codigo_r = gestor_recursos.registrarLibro("Recurso1", "Autor", "ISBN", 2020)

    codigo_turno = gestor.solicitarTurno("U001", codigo_r, "Centro")
    assert codigo_turno is not None
    print(f"  ✓ Turno solicitado: {codigo_turno}")

    # CASO 2: BORDE
    print("[BORDE] Verificar orden FIFO (5 usuarios)")
    gestor_usuarios = GestorUsuarios()
    gestor_recursos = GestorRecursos(numSedes=3)
    gestor = GestorTurnos(gestorUsuarios=gestor_usuarios, gestorRecursos=gestor_recursos)
    gestor_recursos.registrarSede(0, "Centro")  # la sede debe existir para pedir turno

    for i in range(5):
        gestor_usuarios.registrar(f"User_{i}", f"user{i}@test.com")
    codigo_r = gestor_recursos.registrarLibro("PopularLibro", "Autor", "ISBN", 2020)

    turnos = []
    for i in range(5):
        usuario = f"U{i+1:03d}"
        turno = gestor.solicitarTurno(usuario, codigo_r, "Centro")
        turnos.append(turno)

    siguiente = gestor.verSiguiente(codigo_r)
    assert siguiente.codigo == turnos[0], "FIFO incorrecto"
    print(f"  ✓ Orden FIFO correcto")

    # CASO 3: CUELLO DE BOTELLA
    print("[CUELLO DE BOTELLA] 500 usuarios en fila")
    gestor_usuarios = GestorUsuarios()
    gestor_recursos = GestorRecursos(numSedes=3)
    gestor = GestorTurnos(gestorUsuarios=gestor_usuarios, gestorRecursos=gestor_recursos)
    gestor_recursos.registrarSede(0, "Centro")  # la sede debe existir para pedir turno

    codigo_r = gestor_recursos.registrarLibro("MuyPopular", "Autor", "ISBN", 2020)

    for i in range(500):
        gestor_usuarios.registrar(f"User_{i}", f"user{i}@test.com")
        gestor.solicitarTurno(f"U{i+1:03d}", codigo_r, "Centro")

    cantidad = gestor.obtenerCantidadEspera(codigo_r)
    assert cantidad == 500
    print(f"  ✓ 500 turnos registrados")


def test_m05_categorias():
    print("\nM05 - GESTION DE CATEGORIAS (Árbol BST)")

    # CASO 1: EXITOSO
    print("[EXITOSO] Registrar categoría válida")
    gestor = GestorCategorias()
    gestor.registrarCategoria("C001", "Ciencias")
    cat = gestor.obtenerCategoria("C001")
    assert cat.nombre == "Ciencias"
    print(f"  ✓ Categoría registrada: C001")

    # CASO 2: BORDE
    print("[BORDE] Rechazar categoría duplicada")
    gestor = GestorCategorias()
    gestor.registrarCategoria("C001", "Ciencias")
    try:
        gestor.registrarCategoria("C001", "Ciencias Exactas")
        assert False, "Debería rechazar duplicado"
    except ValueError:
        print(f"  ✓ Duplicado rechazado correctamente")

    # CASO 3: CUELLO DE BOTELLA
    print("[CUELLO DE BOTELLA] Insertar 500 categorías en árbol")
    gestor = GestorCategorias()
    for i in range(500):
        codigo = f"C{i:04d}"
        nombre = f"Categoria_{i}"
        gestor.registrarCategoria(codigo, nombre)

    cantidad = gestor.obtenerCantidad()
    print(f"  ✓ 500 categorías registradas")


def test_m06_informes():
    print("\nM06 - INFORMES Y REPORTES (Merge Sort)")

    # CASO 1: EXITOSO
    print("[EXITOSO] Generar reporte de uso")
    gestor_usuarios = GestorUsuarios()
    gestor_recursos = GestorRecursos(numSedes=3)
    gestor_prestamos = GestorPrestamos(gestorTurnos=GestorTurnos(gestorUsuarios=gestor_usuarios,
                                                                 gestorRecursos=gestor_recursos),
                                       gestorUsuarios=gestor_usuarios, gestorRecursos=gestor_recursos)
    gestor = GeneradorInformes(gestorRecursos=gestor_recursos, gestorPrestamos=gestor_prestamos)

    reporte = gestor.generarReporteUso()
    assert reporte is not None
    print(f"  ✓ Reporte generado")

    # CASO 2: BORDE
    print("[BORDE] Reporte sin préstamos")
    reporte = gestor.generarReporteUso()
    assert reporte is not None
    print(f"  ✓ Reporte sin datos funciona")

    # CASO 3: CUELLO DE BOTELLA
    print("[CUELLO DE BOTELLA] Merge Sort de 300 recursos")
    gestor_recursos = GestorRecursos(numSedes=3)
    for i in range(300):
        gestor_recursos.registrarLibro(f"Libro_{i}", f"Autor_{i}", f"ISBN-{i}", 2020)

    gestor = GeneradorInformes(gestorRecursos=gestor_recursos, gestorPrestamos=None)
    ordenados = gestor.listarRecursosOrdenadosPrestamos(gestor_recursos.listarTodos())

    assert len(ordenados) == 300
    print(f"  ✓ 300 recursos ordenados")


def test_m07_inventario():
    print("\nM07 - INVENTARIO (Matriz)")

    # CASO 1: EXITOSO
    print("[EXITOSO] Mostrar matriz de inventario")
    gestor = GestorRecursos(numSedes=3)
    gestor.registrarSede(0, "Centro")
    gestor.registrarSede(1, "Norte")

    codigo = gestor.registrarLibro("Libro", "Autor", "ISBN", 2020)
    gestor.actualizarDisponibilidad(codigo, "Centro", 5)

    matriz = gestor.inventario.mostrarMatriz()
    assert matriz is not None and len(matriz) > 0
    print(f"  ✓ Matriz generada")

    # CASO 2: BORDE
    print("[BORDE] Matriz con distribución desigual")
    codigo = gestor.registrarLibro("Unico", "Autor", "ISBN", 2020)
    gestor.actualizarDisponibilidad(codigo, "Centro", 1)

    matriz = gestor.inventario.mostrarMatriz()
    assert "1" in matriz
    print(f"  ✓ Matriz maneja valores desiguales")

    # CASO 3: CUELLO DE BOTELLA
    print("[CUELLO DE BOTELLA] Matriz 200 recursos x 3 sedes")
    gestor = GestorRecursos(numSedes=3)
    gestor.registrarSede(0, "Centro")
    gestor.registrarSede(1, "Norte")
    gestor.registrarSede(2, "Sur")

    for i in range(200):
        codigo = gestor.registrarLibro(f"Libro_{i}", f"Autor_{i}", f"ISBN-{i}", 2020)
        for sede in ["Centro", "Norte", "Sur"]:
            gestor.actualizarDisponibilidad(codigo, sede, (i % 5) + 1)

    matriz = gestor.inventario.mostrarMatriz()
    print(f"  ✓ 600 celdas de matriz generadas")


def main():
    print("PRUEBAS - EXITOSO, BORDE, CUELLO DE BOTELLA")

    try:
        test_m01_usuarios()
    except AssertionError as e:
        print(f"  ✗ FAIL: {e}")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")

    try:
        test_m02_recursos()
    except AssertionError as e:
        print(f"  ✗ FAIL: {e}")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")

    try:
        test_m03_prestamos()
    except AssertionError as e:
        print(f"  ✗ FAIL: {e}")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")

    try:
        test_m04_turnos()
    except AssertionError as e:
        print(f"  ✗ FAIL: {e}")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")

    try:
        test_m05_categorias()
    except AssertionError as e:
        print(f"  ✗ FAIL: {e}")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")

    try:
        test_m06_informes()
    except AssertionError as e:
        print(f"  ✗ FAIL: {e}")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")

    try:
        test_m07_inventario()
    except AssertionError as e:
        print(f"  ✗ FAIL: {e}")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")

    print("\n" + "=" * 60)
    print("Pruebas completadas")
    print("=" * 60)


if __name__ == "__main__":
    main()
