#!/usr/bin/env python3
"""
PRUEBAS DE LAS CORRECCIONES DEL MENÚ (E1 a E11)

Ejecutar desde la carpeta del proyecto:
    python -m pruebas.test_correcciones_menu

Cada caso se reporta como:
    ENTRADA -> OPERACIÓN -> RESULTADO ESPERADO -> RESULTADO OBTENIDO

Tipos de caso: [normal] operación válida, [error] operación inválida que
debe rechazarse, [límite] última unidad, cola vacía, recurso 101, etc.
Los casos [menú] ejecutan main.py con la entrada indicada y revisan su salida.
"""

import os
import subprocess
import sys

# Agregar la carpeta raíz al path para importaciones
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from estructuras import VectorDinamico, TablaHash
from modulos import (GestorUsuarios, GestorRecursos, GestorPrestamos, GestorTurnos,
                     GestorCategorias, GeneradorInformes)
from modulos.M03_Prestamos import SinUnidadesError


# UTILIDADES

def caso(tipo, entrada, operacion, esperado, obtenido):
    """Imprime el caso en el formato pedido y verifica que esperado == obtenido."""
    ok = esperado == obtenido
    print(f"  [{tipo}] {'CORRECTO' if ok else 'ERROR'}")
    print(f"    ENTRADA:            {entrada}")
    print(f"    OPERACIÓN:          {operacion}")
    print(f"    RESULTADO ESPERADO: {esperado}")
    print(f"    RESULTADO OBTENIDO: {obtenido}")
    assert ok, f"{operacion}: se esperaba {esperado!r} y se obtuvo {obtenido!r}"


def error_de(funcion, *args):
    """Ejecuta la función y devuelve 'Tipo: mensaje' del ValueError, o 'sin error'."""
    try:
        funcion(*args)
    except ValueError as e:
        return f"{type(e).__name__}: {e}"
    return "sin error"


def sistema(unidades=5):
    """
    Sistema como el de main.py: usuarios U001-U003, sedes Centro/Norte/Sur
    y R0001 con `unidades` ejemplares en Centro.
    """
    gu = GestorUsuarios()
    gr = GestorRecursos(numSedes=3)
    for i, nombre in enumerate(("Centro", "Norte", "Sur")):
        gr.registrarSede(i, nombre)
    gt = GestorTurnos(gestorUsuarios=gu, gestorRecursos=gr)
    gp = GestorPrestamos(gestorTurnos=gt, gestorUsuarios=gu, gestorRecursos=gr)
    for nombre in ("Carlos", "Ana", "Luis"):
        gu.registrar(nombre, nombre.lower() + "@uni.edu")
    r = gr.registrarLibro("Python 101", "Guido", "978-123", 2020)
    gr.actualizarDisponibilidad(r, "Centro", unidades)
    return gu, gr, gt, gp


def disp(gr, recurso="R0001", sede="Centro"):
    """Unidades disponibles en la matriz de inventario."""
    return gr.obtenerDisponibilidad(recurso, sede)


def fila(gt, recurso="R0001"):
    """Usuarios en la fila de espera, en orden."""
    return [s.usuario_codigo for s in gt.obtenerFila(recurso)]


def ejecutar_menu(entrada):
    """Ejecuta main.py con la entrada dada y devuelve (salida, código de salida)."""
    entorno = os.environ.copy()
    entorno["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run([sys.executable, "-W", "ignore", "main.py"], input=entrada,
                       capture_output=True, text=True, encoding="utf-8",
                       cwd=RAIZ, env=entorno)
    return r.stdout + r.stderr, r.returncode


def menu_ok(salida, codigo):
    """El programa terminó normalmente y sin Traceback."""
    return codigo == 0 and "Traceback" not in salida


# PRUEBAS

def test_e1_listarActivos():
    """E1: GestorPrestamos.listarActivos()."""
    print("\nE1: Listar préstamos activos")
    print("-" * 50)
    gu, gr, gt, gp = sistema(5)

    caso("límite", "sin préstamos", "listarActivos().obtenerTamaño()", 0,
         gp.listarActivos().obtenerTamaño())

    gp.registrarPrestamo("U001", "R0001", "Centro")
    gp.registrarPrestamo("U002", "R0001", "Centro")
    activos = gp.listarActivos()
    caso("normal", "P0001 y P0002 activos", "listarActivos() devuelve VectorDinamico",
         True, isinstance(activos, VectorDinamico))
    caso("normal", "P0001 y P0002 activos", "códigos en listarActivos()",
         "P0001,P0002", ",".join(activos.obtener(i).codigo for i in range(activos.obtenerTamaño())))

    gp.registrarDevolucion("P0001")
    activos = gp.listarActivos()
    caso("normal", "P0001 devuelto, P0002 activo", "listarActivos() solo trae 'Activo'",
         "P0002", ",".join(activos.obtener(i).codigo for i in range(activos.obtenerTamaño())))

    salida, codigo = ejecutar_menu("4\n1\nU001\nR0001\nCentro\n\n3\n\n0\n0\n")
    caso("menú", "Préstamos -> 1 (U001, R0001, Centro) -> 3", "salida de main.py",
         "sin Traceback, 'Total prestamos activos: 1'",
         "sin Traceback, 'Total prestamos activos: 1'"
         if menu_ok(salida, codigo) and "Total prestamos activos: 1" in salida else salida[-300:])

    salida, codigo = ejecutar_menu("4\n3\n\n0\n0\n")
    caso("menú", "Préstamos -> 3 sin préstamos", "salida de main.py",
         "sin Traceback, 'Total prestamos activos: 0'",
         "sin Traceback, 'Total prestamos activos: 0'"
         if menu_ok(salida, codigo) and "Total prestamos activos: 0" in salida else salida[-300:])

    print("E1: CORRECTO")
    return True


def test_e2_errores_capturados():
    """E2: el menú captura los ValueError de los gestores."""
    print("\nE2: ValueError capturados en el menú")
    print("-" * 50)
    gu = GestorUsuarios()

    caso("error", "nombre='', email='x@u'", "GestorUsuarios.registrar",
         "ValueError: El nombre del usuario no puede estar vacío",
         error_de(gu.registrar, "", "x@u"))
    caso("error", "nombre='Ana', email='   '", "GestorUsuarios.registrar",
         "ValueError: El email del usuario no puede estar vacío",
         error_de(gu.registrar, "Ana", "   "))

    salida, codigo = ejecutar_menu("1\n1\n\n\n\n0\n0\n")
    caso("menú", "Usuarios -> 1 con nombre y email vacíos", "salida de main.py",
         "sin Traceback, 'Error: El nombre del usuario no puede estar vacío'",
         "sin Traceback, 'Error: El nombre del usuario no puede estar vacío'"
         if menu_ok(salida, codigo) and "Error: El nombre del usuario no puede estar vacío" in salida
         else salida[-300:])

    salida, codigo = ejecutar_menu("1\n1\nLuis\nluis@uni.edu\n\n0\n0\n")
    caso("menú", "Usuarios -> 1 con 'Luis', 'luis@uni.edu'", "salida de main.py",
         "sin Traceback, 'Usuario registrado: U003'",
         "sin Traceback, 'Usuario registrado: U003'"
         if menu_ok(salida, codigo) and "Usuario registrado: U003" in salida else salida[-300:])

    salida, codigo = ejecutar_menu("4\n1\nU999\nR0001\nCentro\n\n1\nU001\nR0001\nMarte\n\n8\n\n0\n0\n")
    caso("menú", "Préstamos -> usuario U999, sede 'Marte', deshacer sin operaciones",
         "salida de main.py",
         "sin Traceback, 3 mensajes",
         "sin Traceback, 3 mensajes"
         if menu_ok(salida, codigo) and "Error: Usuario U999 no existe" in salida
         and "Error: Sede 'Marte' no existe" in salida
         and "No hay operaciones para deshacer" in salida else salida[-300:])

    print("E2: CORRECTO")
    return True


def test_e3_disponibilidad_por_sede():
    """E3: se presta mientras haya unidades en la sede (sin regla 'exclusivo')."""
    print("\nE3: Préstamo según unidades de la sede")
    print("-" * 50)
    gu, gr, gt, gp = sistema(5)

    codigos = ",".join(gp.registrarPrestamo(u, "R0001", "Centro")
                       for u in ("U001", "U002", "U003", "U001", "U002"))
    caso("normal", "R0001 con 5 en Centro", "prestar 5 veces", "P0001,P0002,P0003,P0004,P0005", codigos)
    caso("límite", "se prestó la última unidad", "disponibilidad R0001/Centro", 0, disp(gr))
    caso("error", "R0001 con 0 en Centro", "sexto préstamo",
         "SinUnidadesError: Sin unidades disponibles de R0001 en Centro",
         error_de(gp.registrarPrestamo, "U003", "R0001", "Centro"))
    caso("error", "SinUnidadesError", "¿es un ValueError?", True, issubclass(SinUnidadesError, ValueError))
    caso("error", "R0001 con 0 en Norte", "prestar en Norte",
         "SinUnidadesError: Sin unidades disponibles de R0001 en Norte",
         error_de(gp.registrarPrestamo, "U001", "R0001", "Norte"))
    caso("normal", "GestorPrestamos", "¿todavía tiene el atributo 'exclusivo'?",
         False, hasattr(gp, "exclusivo"))

    salida, codigo = ejecutar_menu("4\n1\nU001\nR0001\nCentro\n\n1\nU002\nR0001\nCentro\n\n0\n3\n\n0\n")
    caso("menú", "dos préstamos de R0001 en Centro y ver la matriz", "salida de main.py",
         "P0002 registrado, nunca 'None', Centro R0001 = 3",
         "P0002 registrado, nunca 'None', Centro R0001 = 3"
         if menu_ok(salida, codigo) and "Prestamo registrado: P0002" in salida
         and "registrado: None" not in salida and "Centro          | 3" in salida else salida[-400:])

    # R0003 tiene 1 unidad: U001 la toma y U002 pide turno desde el menú de préstamos
    salida, codigo = ejecutar_menu("4\n1\nU001\nR0003\nCentro\n\n1\nU002\nR0003\nCentro\ns\n\n0\n0\n")
    caso("menú", "R0003 (1 unidad): U001 presta, U002 intenta y responde 's'", "salida de main.py",
         "sin unidades + 'Turno S0001 asignado, posicion 1 en la fila'",
         "sin unidades + 'Turno S0001 asignado, posicion 1 en la fila'"
         if menu_ok(salida, codigo) and "Error: Sin unidades disponibles de R0003 en Centro" in salida
         and "Turno S0001 asignado, posicion 1 en la fila" in salida else salida[-400:])

    print("E3: CORRECTO")
    return True


def test_e4_inventario():
    """E4: prestar/devolver/deshacer actualizan la matriz de inventario."""
    print("\nE4: Inventario en préstamo, devolución y deshacer")
    print("-" * 50)
    gu, gr, gt, gp = sistema(5)

    gp.registrarPrestamo("U001", "R0001", "Centro")
    caso("normal", "R0001 con 5 en Centro", "prestar 1", 4, disp(gr))
    for u in ("U002", "U003", "U001", "U002"):
        gp.registrarPrestamo(u, "R0001", "Centro")
    caso("límite", "4 préstamos más", "disponibilidad", 0, disp(gr))

    gp.registrarDevolucion("P0001")
    caso("normal", "disponibilidad 0", "devolver P0001", 1, disp(gr))
    gp.deshacer()
    caso("normal", "disponibilidad 1 tras devolver", "deshacer esa devolución", 0, disp(gr))
    caso("normal", "deshacer devolución", "estado de P0001", "Activo", gp.buscarPrestamo("P0001").estado)
    gp.deshacer()
    caso("normal", "disponibilidad 0", "deshacer el préstamo P0005", 1, disp(gr))
    caso("normal", "deshacer préstamo", "¿P0005 sigue existiendo?", None, gp.buscarPrestamo("P0005"))
    caso("normal", "Norte no participó", "disponibilidad R0001/Norte", 0, disp(gr, sede="Norte"))

    # Caso límite: el inventario se cambió a mano y ya no hay unidad para revertir la devolución
    gp.registrarDevolucion("P0004")
    gr.actualizar_disponibilidad("R0001", "Centro", 0)
    caso("límite", "devolución de P0004 y luego inventario puesto en 0 a mano", "deshacer",
         "ValueError: No se puede deshacer la devolucion de P0004: no quedan unidades de R0001 en Centro",
         error_de(gp.deshacer))
    tope = gp.pilaDeshacer.peek()
    caso("límite", "deshacer rechazado", "tope de la pila (la operación no se perdió)",
         "registrarDevolucion P0004", f"{tope['operacion']} {tope['prestamo'].codigo}")
    caso("límite", "deshacer rechazado", "estado de P0004 (sin cambios)", "Devuelto",
         gp.buscarPrestamo("P0004").estado)

    print("E4: CORRECTO")
    return True


def test_e5_devolucion_inexistente():
    """E5: devolver un préstamo inexistente o ya devuelto."""
    print("\nE5: Devolución inexistente")
    print("-" * 50)
    gu, gr, gt, gp = sistema(5)
    gp.registrarPrestamo("U001", "R0001", "Centro")

    caso("error", "P9999 no existe", "registrarDevolucion('P9999')", False, gp.registrarDevolucion("P9999"))
    caso("normal", "P0001 activo", "registrarDevolucion('P0001')", True, gp.registrarDevolucion("P0001"))
    caso("límite", "P0001 ya devuelto", "registrarDevolucion('P0001') otra vez", False,
         gp.registrarDevolucion("P0001"))
    caso("límite", "segunda devolución rechazada", "disponibilidad (no suma dos veces)", 5, disp(gr))

    salida, codigo = ejecutar_menu("4\n2\nP9999\n\n0\n0\n")
    caso("menú", "Préstamos -> 2 con P9999", "salida de main.py",
         "'Error: El prestamo P9999 no existe o ya fue devuelto', sin 'Devolucion registrada'",
         "'Error: El prestamo P9999 no existe o ya fue devuelto', sin 'Devolucion registrada'"
         if menu_ok(salida, codigo) and "Error: El prestamo P9999 no existe o ya fue devuelto" in salida
         and "Devolucion registrada" not in salida else salida[-300:])

    print("E5: CORRECTO")
    return True


def test_e6a_solicitarTurno():
    """E6a: GestorTurnos.solicitarTurno valida antes de encolar."""
    print("\nE6a: Solicitar turno")
    print("-" * 50)
    gu, gr, gt, gp = sistema(1)

    caso("error", "R0001 con 1 en Centro", "solicitarTurno(U002, R0001, Centro)",
         "ValueError: Hay unidades disponibles: registre el préstamo",
         error_de(gt.solicitarTurno, "U002", "R0001", "Centro"))

    gp.registrarPrestamo("U001", "R0001", "Centro")
    caso("normal", "R0001 con 0 en Centro", "solicitarTurno(U002, R0001, Centro)",
         "S0001", gt.solicitarTurno("U002", "R0001", "Centro"))
    caso("normal", "R0001 con 0 en Centro", "solicitarTurno(U003, R0001, Centro)",
         "S0002", gt.solicitarTurno("U003", "R0001", "Centro"))
    caso("normal", "dos turnos", "posición de U003 = obtenerCantidadEspera", 2,
         gt.obtenerCantidadEspera("R0001"))
    caso("error", "U002 ya está en la fila", "solicitarTurno(U002, R0001, Centro)",
         "ValueError: El usuario U002 ya esta en la fila de R0001",
         error_de(gt.solicitarTurno, "U002", "R0001", "Centro"))
    caso("error", "U999 no existe", "solicitarTurno(U999, R0001, Centro)",
         "ValueError: Usuario U999 no existe", error_de(gt.solicitarTurno, "U999", "R0001", "Centro"))
    caso("error", "R0099 no existe", "solicitarTurno(U001, R0099, Centro)",
         "ValueError: Recurso R0099 no existe", error_de(gt.solicitarTurno, "U001", "R0099", "Centro"))
    caso("error", "sede 'Marte' no existe", "solicitarTurno(U001, R0001, Marte)",
         "ValueError: Sede 'Marte' no existe", error_de(gt.solicitarTurno, "U001", "R0001", "Marte"))
    u4 = gu.registrar("Inactivo", "in@uni.edu")
    gu.darDeBaja(u4)
    caso("error", f"{u4} dado de baja", f"solicitarTurno({u4}, R0001, Centro)",
         f"ValueError: El usuario {u4} esta inactivo", error_de(gt.solicitarTurno, u4, "R0001", "Centro"))
    caso("error", "solicitudes rechazadas", "la fila no cambió", ["U002", "U003"], fila(gt))

    # Menú: R0003 tiene 1 unidad; U001 la presta y U002 pide turno desde Turnos -> 4
    salida, codigo = ejecutar_menu("4\n1\nU001\nR0003\nCentro\n\n0\n5\n4\nU002\nR0003\nCentro\n\n"
                                   "4\nU002\nR0003\nCentro\n\n4\nU001\nR0001\nCentro\n\n0\n0\n")
    caso("menú", "Turnos -> 4: U002/R0003 dos veces y U001/R0001 (con unidades)", "salida de main.py",
         "turno asignado, duplicado rechazado, 'Hay unidades disponibles'",
         "turno asignado, duplicado rechazado, 'Hay unidades disponibles'"
         if menu_ok(salida, codigo) and "Turno S0001 asignado, posicion 1 en la fila" in salida
         and "Error: El usuario U002 ya esta en la fila de R0003" in salida
         and "Error: Hay unidades disponibles: registre el préstamo" in salida else salida[-400:])

    print("E6a: CORRECTO")
    return True


def test_e6b_verSiguiente():
    """E6b: verSiguiente consulta sin desencolar."""
    print("\nE6b: Ver siguiente turno sin sacarlo")
    print("-" * 50)
    gu, gr, gt, gp = sistema(0)

    caso("límite", "fila vacía", "verSiguiente(R0001)", None, gt.verSiguiente("R0001"))
    gt.solicitarTurno("U002", "R0001", "Centro")
    caso("límite", "un solo elemento [U002]", "verSiguiente(R0001).usuario_codigo", "U002",
         gt.verSiguiente("R0001").usuario_codigo)
    gt.solicitarTurno("U003", "R0001", "Centro")
    gt.verSiguiente("R0001")
    gt.verSiguiente("R0001")
    caso("normal", "fila [U002, U003]", "verSiguiente dos veces -> tamaño de la fila", 2,
         gt.obtenerCantidadEspera("R0001"))
    caso("normal", "fila [U002, U003]", "estado de S0001 tras consultar", "En espera",
         gt.buscarSolicitud("S0001").estado)

    # Menú: dejar a U002 en fila de R0003 y consultar "Ver siguiente" dos veces
    salida, codigo = ejecutar_menu("4\n1\nU001\nR0003\nCentro\n\n0\n5\n4\nU002\nR0003\nCentro\n\n"
                                   "1\nR0003\n\n1\nR0003\n\n3\nR0003\n\n0\n0\n")
    caso("menú", "Turnos -> 1 dos veces y luego 3", "salida de main.py",
         "U002 aparece 2 veces como siguiente y sigue '1 personas esperando'",
         "U002 aparece 2 veces como siguiente y sigue '1 personas esperando'"
         if menu_ok(salida, codigo) and salida.count("Siguiente en fila: U002") == 2
         and "1 personas esperando por R0003" in salida else salida[-400:])

    print("E6b: CORRECTO")
    return True


def test_e6c_atender_al_devolver():
    """E6c: al devolver se asigna automáticamente al siguiente de la fila."""
    print("\nE6c: Atender la fila al devolver")
    print("-" * 50)
    gu, gr, gt, gp = sistema(1)

    gp.registrarPrestamo("U001", "R0001", "Centro")
    caso("límite", "R0001 sin fila", "registrarDevolucion('P0001')", True, gp.registrarDevolucion("P0001"))

    gp.registrarPrestamo("U001", "R0001", "Centro")  # P0002, queda 0
    gt.solicitarTurno("U002", "R0001", "Centro")
    gt.solicitarTurno("U003", "R0001", "Centro")
    resultado = gp.registrarDevolucion("P0002")
    caso("normal", "fila [U002, U003]", "registrarDevolucion('P0002') devuelve", "P0003", resultado)
    caso("normal", "asignación automática", "usuario del préstamo P0003", "U002",
         gp.buscarPrestamo("P0003").usuario_codigo)
    caso("normal", "asignación automática", "fila después", ["U003"], fila(gt))
    caso("normal", "asignación automática", "disponibilidad (devuelta y vuelta a prestar)", 0, disp(gr))
    caso("normal", "asignación automática", "estado de S0001", "Otorgado", gt.buscarSolicitud("S0001").estado)

    # Usuario de la fila que ya no está activo: se salta
    gu2, gr2, gt2, gp2 = sistema(1)
    gp2.registrarPrestamo("U001", "R0001", "Centro")
    gt2.solicitarTurno("U002", "R0001", "Centro")
    gt2.solicitarTurno("U003", "R0001", "Centro")
    gu2.darDeBaja("U002")
    resultado = gp2.registrarDevolucion("P0001")
    caso("normal", "fila [U002 (inactivo), U003]", "devolver P0001 -> usuario asignado",
         "U003", gp2.buscarPrestamo(resultado).usuario_codigo)
    caso("normal", "U002 inactivo saltado", "estado de su solicitud S0001", "Cancelado",
         gt2.buscarSolicitud("S0001").estado)

    # Fila solo con usuarios inactivos: la unidad queda libre
    gu3, gr3, gt3, gp3 = sistema(1)
    gp3.registrarPrestamo("U001", "R0001", "Centro")
    gt3.solicitarTurno("U002", "R0001", "Centro")
    gu3.darDeBaja("U002")
    caso("límite", "fila [U002 (inactivo)]", "registrarDevolucion('P0001')", True,
         gp3.registrarDevolucion("P0001"))
    caso("límite", "nadie activo en la fila", "disponibilidad", 1, disp(gr3))
    caso("límite", "nadie activo en la fila", "fila después", [], fila(gt3))

    # Menú: devolver con alguien en la fila
    salida, codigo = ejecutar_menu("4\n1\nU001\nR0003\nCentro\n\n0\n5\n4\nU002\nR0003\nCentro\n\n0\n"
                                   "4\n2\nP0001\n\n0\n0\n")
    caso("menú", "U001 presta R0003, U002 en fila, devolver P0001", "salida de main.py",
         "'Asignado automaticamente a U002 (siguiente en la fila): P0002'",
         "'Asignado automaticamente a U002 (siguiente en la fila): P0002'"
         if menu_ok(salida, codigo)
         and "Asignado automaticamente a U002 (siguiente en la fila): P0002" in salida else salida[-400:])

    print("E6c: CORRECTO")
    return True


def test_e7_categoria_repetida():
    """E7: no se repiten códigos de categoría."""
    print("\nE7: Categoría repetida")
    print("-" * 50)
    gc = GestorCategorias()

    caso("normal", "C1 'Ingenieria'", "registrarCategoria", "C1", gc.registrarCategoria("C1", "Ingenieria"))
    caso("error", "C1 ya existe", "registrarCategoria('C1', 'Repetida')",
         "ValueError: La categoria C1 ya existe", error_de(gc.registrarCategoria, "C1", "Repetida"))
    caso("error", "C1 rechazada", "nombre de C1", "Ingenieria", gc.obtenerCategoria("C1").nombre)
    caso("error", "C1 rechazada", "obtener_cantidad()", 1, gc.obtener_cantidad())
    caso("normal", "GestorCategorias", "estructura de 'categorias'", "TablaHash",
         type(gc.categorias).__name__)
    caso("límite", "C9 no existe", "obtenerCategoria('C9')", None, gc.obtenerCategoria("C9"))

    salida, codigo = ejecutar_menu("6\n1\nC1\nIngenieria\n\n1\nC1\nRepetida\n\n2\nC1\n\n0\n0\n")
    caso("menú", "Categorías -> C1 dos veces y buscar C1", "salida de main.py",
         "'Error: La categoria C1 ya existe' y 'C1: Ingenieria'",
         "'Error: La categoria C1 ya existe' y 'C1: Ingenieria'"
         if menu_ok(salida, codigo) and "Error: La categoria C1 ya existe" in salida
         and "C1: Ingenieria" in salida and "C1: Repetida" not in salida else salida[-300:])

    print("E7: CORRECTO")
    return True


def test_e8_informes():
    """E8: GeneradorInformes recibe recursos y préstamos."""
    print("\nE8: Informes")
    print("-" * 50)
    gu, gr, gt, gp = sistema(5)
    gr.registrarEquipo("Proyector", "Proyector", "Epson", "Sala A")
    gr.registrarSala("Sala", 30)
    gp.registrarPrestamo("U001", "R0001", "Centro")
    gi = GeneradorInformes(gestor_recursos=gr, gestor_prestamos=gp)

    caso("normal", "3 recursos y 1 préstamo", "generarReporteUso()",
         "Total de préstamos registrados: 1", gi.generarReporteUso())
    caso("normal", "3 recursos y 1 préstamo", "generarReporteInventario()",
         "GestorRecursos(libros=1, equipos=1, salas=1)", gi.generarReporteInventario())
    caso("límite", "sin gestores", "GeneradorInformes().generarReporteUso()", "Sin datos",
         GeneradorInformes().generarReporteUso())

    salida, codigo = ejecutar_menu("4\n1\nU001\nR0001\nCentro\n\n0\n7\n1\n\n2\n\n0\n0\n")
    caso("menú", "1 préstamo y luego Informes -> 1 y 2", "salida de main.py",
         "'Total de préstamos registrados: 1' y 'GestorRecursos(...)'",
         "'Total de préstamos registrados: 1' y 'GestorRecursos(...)'"
         if menu_ok(salida, codigo) and "Total de préstamos registrados: 1" in salida
         and "GestorRecursos(libros=1, equipos=1, salas=1)" in salida
         and "GestorUsuarios(" not in salida else salida[-300:])

    print("E8: CORRECTO")
    return True


def test_e9_usuario_inactivo_recurso_baja():
    """E9: no se presta a usuarios inactivos ni recursos dados de baja."""
    print("\nE9: Usuario inactivo / recurso dado de baja")
    print("-" * 50)
    gu, gr, gt, gp = sistema(5)

    gu.darDeBaja("U001")
    caso("error", "U001 inactivo", "registrarPrestamo(U001, R0001, Centro)",
         "ValueError: El usuario U001 esta inactivo",
         error_de(gp.registrarPrestamo, "U001", "R0001", "Centro"))
    caso("error", "préstamo rechazado", "disponibilidad (no se descontó)", 5, disp(gr))
    caso("normal", "U002 activo", "registrarPrestamo(U002, R0001, Centro)", "P0001",
         gp.registrarPrestamo("U002", "R0001", "Centro"))

    r2 = gr.registrar_libro("Viejo", "a", "i", 1990)
    gr.actualizar_disponibilidad(r2, "Centro", 2)
    gr.darDeBaja(r2)
    caso("error", f"{r2} dado de baja", f"registrarPrestamo(U002, {r2}, Centro)",
         f"ValueError: El recurso {r2} esta dado de baja",
         error_de(gp.registrarPrestamo, "U002", r2, "Centro"))
    caso("error", "préstamo rechazado", f"disponibilidad de {r2}", 2, disp(gr, r2))

    print("E9: CORRECTO")
    return True


def test_e10_inventario_500():
    """E10: la matriz crece y acepta 500+ recursos."""
    print("\nE10: 500 recursos con existencias")
    print("-" * 50)
    gr = GestorRecursos(num_sedes=3)
    gr.registrar_sede(0, "Centro")
    for i in range(500):
        c = gr.registrar_libro(f"L{i}", "a", "i", 2000)
        gr.actualizar_disponibilidad(c, "Centro", 3)

    caso("normal", "500 libros con 3 en Centro", "cantidad de recursos", 500, gr.obtener_cantidad())
    caso("normal", "500 libros con 3 en Centro", "disponibilidad R0500", 3, disp(gr, "R0500"))
    caso("normal", "tras crecer varias veces", "disponibilidad R0001 (se copió)", 3, disp(gr, "R0001"))
    caso("límite", "recurso 101 (antes fallaba)", "disponibilidad R0101", 3, disp(gr, "R0101"))
    caso("límite", "500 columnas usadas", "capacidad de columnas >= 500", True, gr.inventario.num_recursos >= 500)

    columnas = gr.inventario.num_recursos
    caso("límite", "R0001 ya registrado", "registrar_recurso('R0001') otra vez -> columna", 0,
         gr.inventario.registrar_recurso("R0001", "L0"))
    caso("límite", "R0001 ya registrado", "las columnas no crecieron", columnas, gr.inventario.num_recursos)

    gu = GestorUsuarios()
    gu.registrar("Ana", "a@u")
    gp = GestorPrestamos(gestor_usuarios=gu, gestor_recursos=gr)
    gp.registrarPrestamo("U001", "R0101", "Centro")
    caso("normal", "R0101 con 3", "prestar R0101 -> disponibilidad", 2, disp(gr, "R0101"))

    print("E10: CORRECTO")
    return True


def test_e11_deshacer_turno():
    """E11: deshacer un préstamo asignado desde la fila devuelve al usuario al frente."""
    print("\nE11: Deshacer préstamo asignado desde la fila")
    print("-" * 50)
    gu, gr, gt, gp = sistema(1)

    gp.registrarPrestamo("U001", "R0001", "Centro")  # P0001, queda 0
    gt.solicitarTurno("U002", "R0001", "Centro")
    gt.solicitarTurno("U003", "R0001", "Centro")
    gp.registrarDevolucion("P0001")  # asigna P0002 a U002
    caso("normal", "devolución con fila [U002, U003]", "operaciones en la pila (préstamo, devolución, automático)",
         3, gp.pilaDeshacer.obtenerTamaño())

    gp.deshacer()
    caso("normal", "deshacer el préstamo automático P0002", "fila", ["U002", "U003"], fila(gt))
    caso("normal", "deshacer el préstamo automático P0002", "estado de S0001", "En espera",
         gt.buscarSolicitud("S0001").estado)
    caso("normal", "deshacer el préstamo automático P0002", "¿P0002 existe?", None, gp.buscarPrestamo("P0002"))
    caso("normal", "deshacer el préstamo automático P0002", "disponibilidad", 1, disp(gr))

    gp.deshacer()
    caso("normal", "deshacer otra vez", "estado de P0001 (devolución revertida)", "Activo",
         gp.buscarPrestamo("P0001").estado)
    caso("normal", "deshacer otra vez", "disponibilidad", 0, disp(gr))
    caso("normal", "deshacer otra vez", "fila (sin cambios)", ["U002", "U003"], fila(gt))

    # atenderSiguienteTurno directo, como en el script del prompt (sin recurso R0005 especial)
    gu2, gr2, gt2, gp2 = sistema(0)
    gt2.solicitarTurno("U002", "R0001", "Centro")
    gt2.solicitarTurno("U003", "R0001", "Centro")
    gr2.actualizar_disponibilidad("R0001", "Centro", 1)
    gp2.atenderSiguienteTurno("R0001", "Centro")
    caso("normal", "atenderSiguienteTurno con fila [U002, U003]", "fila", ["U003"], fila(gt2))
    gp2.deshacer()
    caso("normal", "deshacer ese préstamo", "fila (U002 vuelve al frente)", ["U002", "U003"], fila(gt2))

    # Un préstamo normal (sin solicitud) no toca la fila al deshacerse
    gu3, gr3, gt3, gp3 = sistema(1)
    gp3.registrarPrestamo("U001", "R0001", "Centro")
    gt3.solicitarTurno("U002", "R0001", "Centro")
    gp3.deshacer()
    caso("límite", "deshacer un préstamo que no vino de la fila", "fila", ["U002"], fila(gt3))
    caso("límite", "pila vacía", "deshacer()", False, gp3.deshacer())

    print("E11: CORRECTO")
    return True


def main():
    """Ejecuta todas las pruebas."""
    print("\n" + "=" * 70)
    print("PRUEBAS DE CORRECCIONES DEL MENÚ - E1 a E11")
    print("=" * 70)

    pruebas = [
        ("E1  Listar préstamos activos", test_e1_listarActivos),
        ("E2  ValueError capturados en el menú", test_e2_errores_capturados),
        ("E3  Préstamo según unidades de la sede", test_e3_disponibilidad_por_sede),
        ("E4  Inventario en préstamo/devolución/deshacer", test_e4_inventario),
        ("E5  Devolución inexistente", test_e5_devolucion_inexistente),
        ("E6a Solicitar turno", test_e6a_solicitarTurno),
        ("E6b Ver siguiente sin sacar", test_e6b_verSiguiente),
        ("E6c Atender la fila al devolver", test_e6c_atender_al_devolver),
        ("E7  Categoría repetida", test_e7_categoria_repetida),
        ("E8  Informes", test_e8_informes),
        ("E9  Usuario inactivo / recurso de baja", test_e9_usuario_inactivo_recurso_baja),
        ("E10 500 recursos en inventario", test_e10_inventario_500),
        ("E11 Deshacer préstamo desde la fila", test_e11_deshacer_turno),
    ]

    resultados = []
    for nombre, prueba in pruebas:
        try:
            resultado = prueba()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"{nombre}: ERROR")
            print(f"   {e}")
            resultados.append((nombre, False))

    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)

    aprobadas = sum(1 for _, r in resultados if r)
    total = len(resultados)

    for nombre, resultado in resultados:
        estado = "CORRECTO" if resultado else "ERROR"
        print(f"{estado}: {nombre}")

    print(f"\nTotal: {aprobadas}/{total} pruebas aprobadas")

    if aprobadas == total:
        print("\nTODAS LAS PRUEBAS PASARON")
        return 0
    else:
        print(f"\n{total - aprobadas} prueba(s) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
