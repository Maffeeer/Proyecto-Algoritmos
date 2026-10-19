
import os
import sys
from modulos import (GestorUsuarios, GestorRecursos, GestorPrestamos, GestorTurnos,
                     GestorCategorias, GeneradorInformes, GestorInventario, SistemaInteligente)
from modulos.M03_Prestamos import SinUnidadesError
from estructuras import (VectorDinamico, ListaSimple, ListaDoble, Pila, ColaFIFO,
                         TablaHash, ArbolBinario)
from evidencia import ejecutarEvidencia
from datetime import datetime, timedelta


def limpiarPantalla():
    """Limpia la pantalla de consola."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pausa():
    """Pausa y espera que el usuario presione Enter."""
    try:
        input("\nPresione Enter para continuar...")
    except EOFError:
        pass


def menuPrincipal():
    """Muestra el menu principal."""
    limpiarPantalla()
    print("  SISTEMA DE GESTION DE RECURSOS COMUNITARIOS")
    print("  Red de Bibliotecas Universitarias")
    print()
    print("  1. Gestion de Usuarios (M01)")
    print("     Registrar, listar, consultar usuarios")
    print()
    print("  2. Gestion de Recursos (M02)")
    print("     Registrar libros, equipos, salas con herencia")
    print()
    print("  3. Gestion de Inventario (M07)")
    print("     Ver matriz de disponibilidad por sede y recurso")
    print()
    print("  4. Gestion de Prestamos (M03)")
    print("     Registrar, devolver, deshacer, historial")
    print()
    print("  5. Gestion de Turnos (M04)")
    print("     Solicitar turno, ver turnos y fila de espera")
    print()
    print("  6. Gestion de Categorias (M05)")
    print("     Registrar y buscar categorías")
    print()
    print("  7. Informes y Reportes (M06)")
    print("     Reportes de uso e inventario")
    print()
    print("  8. Pruebas de Estructuras")
    print("     Vector, Listas, Pila, Cola, Tabla Hash y Arbol BST")
    print()
    print("  9. Funciones Inteligentes (M08)")
    print("     Recomendaciones, calificaciones, prediccion y gamificacion")
    print()
    print(" 10. Evidencia de eficiencia (Entrega 1 vs Entrega 2)")
    print("     Mide en vivo: busqueda, funcion hash y ordenamientos")
    print()
    print("  0. Salir")
    print()


def menuFuncionesInteligentes(sistema, gestorRecursos, gestorUsuarios):
    """Submenu M08. Todo se calcula con los prestamos reales registrados en el sistema."""
    while True:
        limpiarPantalla()
        print("  FUNCIONES INTELIGENTES (M08)")
        print("  Se alimentan de los prestamos y devoluciones reales del sistema")
        print()
        print("  1. Recomendaciones (usuarios con prestamos similares)")
        print("  2. Calificaciones y ranking de recursos")
        print("  3. Prediccion de disponibilidad")
        print("  4. Gamificacion (puntos, niveles, insignias, tabla de lideres)")
        print("  0. Volver al menu principal")
        print()
        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break
        if opcion == "0":
            break
        elif opcion == "1":
            demoRecomendaciones(sistema, gestorRecursos, gestorUsuarios)
        elif opcion == "2":
            demoCalificaciones(sistema, gestorRecursos)
        elif opcion == "3":
            demoPrediccion(sistema, gestorRecursos)
        elif opcion == "4":
            demoGamificacion(sistema, gestorUsuarios)
        else:
            print("\nOpcion invalida")
        pausa()


def _nombreRecurso(gestorRecursos, codigo):
    r = gestorRecursos.buscarxCodigo(codigo)
    return r.nombre if r else codigo


def demoRecomendaciones(sistema, gestorRecursos, gestorUsuarios):
    print("\n  RECOMENDACIONES")
    print("  Similitud de Jaccard = recursos en comun / recursos en total entre dos usuarios")
    codigo = input("\nCodigo usuario (ej. U001): ").strip()
    usuario = gestorUsuarios.buscarUsuario(codigo)
    if usuario is None:
        print(f"\nUsuario {codigo} no encontrado")
        return
    recs = sistema.recomendarRecursos(codigo, top_n=5)
    if not recs:
        print(f"\n{usuario.nombre} aun no tiene prestamos parecidos a los de otros usuarios.")
        print("Registre un prestamo para este usuario (menu 4) y vuelva a consultar.")
        return
    print(f"\nRecomendado para {usuario.nombre}:")
    for cod, puntaje, motivo in recs:
        print(f"  {cod}  {_nombreRecurso(gestorRecursos, cod):<25} puntaje {puntaje:.2f}  ({motivo})")


def demoCalificaciones(sistema, gestorRecursos):
    print("\n  RANKING DE RECURSOS (promedio de estrellas, desempata el numero de reseñas)")
    for i, (cod, prom, n) in enumerate(sistema.rankingRecursos(top_n=10), 1):
        estrellas = "*" * round(prom)
        print(f"  {i}. {cod} {_nombreRecurso(gestorRecursos, cod):<25} {prom:.1f}/5 {estrellas:<5} ({n} reseñas)")


def demoPrediccion(sistema, gestorRecursos):
    print("\n  PREDICCION DE DISPONIBILIDAD (promedio de dias de los prestamos ya devueltos)")
    codigo = input("\nCodigo recurso (ej. R0001): ").strip()
    if gestorRecursos.buscarxCodigo(codigo) is None:
        print(f"\nRecurso {codigo} no encontrado")
        return
    pred = sistema.predecirDisponibilidad(codigo)
    datos = sistema.duracionesPromedio.get(codigo, [])
    print(f"\n{codigo} {_nombreRecurso(gestorRecursos, codigo)}")
    print(f"  Prestamos devueltos analizados: {len(datos)}  {datos}")
    print(f"  {pred['mensaje']}")
    print(f"  Fecha estimada: {pred['fechaEstimada'].strftime('%Y-%m-%d')}")
    print("  (la confianza sube 10% por cada prestamo historico, hasta 100%)")


def demoGamificacion(sistema, gestorUsuarios):
    print("\n  TABLA DE LIDERES")
    print("  +10 por prestamo, +20 por devolucion a tiempo. Insignias: LEAL (10 prestamos),")
    print("  DEVOLVEDOR (5 devoluciones a tiempo).")
    print()
    for i, (cod, puntos, nivel) in enumerate(sistema.leaderboard(top_n=10), 1):
        u = gestorUsuarios.buscarUsuario(cod)
        insignias = ", ".join(sorted(sistema.obtenerUsuarioGami(cod)['badges'])) or "-"
        print(f"  {i}. {cod} {u.nombre if u else '':<15} {puntos:4d} pts  nivel {nivel}  insignias: {insignias}")


def gestionUsuarios(gestor):
    """Submenu para gestion de usuarios."""
    limpiarPantalla()
    print("  GESTION DE USUARIOS (M01)")
    print()

    while True:
        print("\n1. Registrar usuario")
        print("2. Listar usuarios")
        print("3. Consultar usuario")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break

        elif opcion == "1":
            nombre = input("\nNombre: ")
            email = input("Email: ")
            # registrar() lanza ValueError si nombre o email están vacíos;
            # sin el try el programa se cerraba con un Traceback.
            try:
                codigo = gestor.registrar(nombre, email)
                print(f"\nUsuario registrado: {codigo}")
            except ValueError as e:
                print(f"\nError: {e}")

        elif opcion == "2":
            usuarios = gestor.listarTodos()
            print(f"\nTotal usuarios: {len(usuarios)}\n")
            for u in usuarios:
                estado = "Activo" if u.estado == "Activo" else "Inactivo"
                print(f"  {u.codigo}: {u.nombre} ({u.email}) [{estado}]")

        elif opcion == "3":
            codigo = input("\nCodigo usuario: ")
            usuario = gestor.buscarUsuario(codigo)
            if usuario:
                print(f"\n{usuario.codigo}: {usuario.nombre}")
                print(f"Email: {usuario.email}")
                print(f"Estado: {usuario.estado}")
                print(f"Prestamos: {usuario.cantidadPrestamos}")
            else:
                print(f"\nUsuario {codigo} no encontrado")

        pausa()


def gestionRecursos(gestor):
    """Submenu para gestion de recursos."""
    limpiarPantalla()
    print("  GESTION DE RECURSOS (M02 - Con HERENCIA)")
    print()

    while True:
        print("\n1. Registrar Libro")
        print("2. Registrar Equipo")
        print("3. Registrar Sala")
        print("4. Listar recursos")
        print("5. Consultar recurso")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break

        elif opcion == "1":
            nombre = input("\nNombre del libro: ")
            autor = input("Autor: ")
            isbn = input("ISBN: ")
            ano = input("Ano publicacion: ")
            try:
                codigo = gestor.registrarLibro(nombre, autor, isbn, int(ano))
                print(f"\nLibro registrado: {codigo}")
            except ValueError:
                print(f"\nError: El año debe ser un número válido")

        elif opcion == "2":
            nombre = input("\nNombre equipo: ")
            tipo = input("Tipo de equipo: ")
            modelo = input("Modelo: ")
            ubicacion = input("Ubicacion: ")
            codigo = gestor.registrarEquipo(nombre, tipo, modelo, ubicacion)
            print(f"\nEquipo registrado: {codigo}")

        elif opcion == "3":
            nombre = input("\nNombre sala: ")
            capacidad = input("Capacidad: ")
            try:
                codigo = gestor.registrarSala(nombre, int(capacidad))
                print(f"\nSala registrada: {codigo}")
            except ValueError:
                print(f"\nError: La capacidad debe ser un número válido")

        elif opcion == "4":
            recursos = gestor.listarTodos()
            print(f"\nTotal recursos: {len(recursos)}\n")
            for r in recursos:
                print(f"  {r.codigo}: {r.nombre} ({r.obtenerTipo()})")

        elif opcion == "5":
            codigo = input("\nCodigo recurso: ")
            recurso = gestor.buscarxCodigo(codigo)
            if recurso:
                print(f"\n{recurso.codigo}: {recurso.nombre}")
                print(f"Tipo: {recurso.obtenerTipo()}")
                print(f"Disponible: {recurso.esDisponible()}")
            else:
                print(f"\nRecurso {codigo} no encontrado")

        pausa()


def solicitarTurnoMenu(gestorTurnos, usuarioCod, recursoCod, sede):
    """Pide turno y muestra la posición. Lo usan los menús de Turnos y de Préstamos."""
    try:
        codigo = gestorTurnos.solicitarTurno(usuarioCod, recursoCod, sede)
        # La solicitud entra al final, así que su posición es el tamaño de la fila
        posicion = gestorTurnos.obtenerCantidadEspera(recursoCod)
        print(f"\n Turno {codigo} asignado, posicion {posicion} en la fila")
    except ValueError as e:
        print(f"\n Error: {e}")


def gestionPrestamos(gestorPrestamos, gestorUsuarios, gestorRecursos):
    """Submenu para gestion de prestamos."""
    limpiarPantalla()
    print("  GESTION DE PRESTAMOS (M03)")
    print()

    while True:
        print("\n1. Registrar prestamo")
        print("2. Registrar devolucion")
        print("3. Listar prestamos activos")
        print("4. Listar prestamos atrasados")
        print("5. Listar prestamos por usuario")
        print("6. Listar prestamos por sede")
        print("7. Consultar prestamo")
        print("8. Deshacer ultima operacion (Pila)")
        print("9. Ver historial completo (Lista doble: adelante y atras)")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break

        elif opcion == "1":
            usuarioCod = input("\nCodigo usuario: ")
            recursoCod = input("Codigo recurso: ")
            sede = input("Sede (Centro/Norte/Sur): ")
            try:
                codigoPrestamo = gestorPrestamos.registrarPrestamo(usuarioCod, recursoCod, sede)
                print(f"\nPrestamo registrado: {codigoPrestamo}")
            except SinUnidadesError as e:
                # Sin unidades en esa sede: se ofrece entrar a la fila de espera (RF3).
                # Va antes de "except ValueError" porque SinUnidadesError es un ValueError.
                print(f"\nError: {e}")
                if gestorPrestamos.gestorTurnos is not None:
                    try:
                        respuesta = input("¿Desea pedir turno en la fila de espera? (s/n): ")
                    except EOFError:
                        respuesta = "n"
                    if respuesta.strip().lower() == "s":
                        solicitarTurnoMenu(gestorPrestamos.gestorTurnos,
                                             usuarioCod, recursoCod, sede)
            except ValueError as e:
                print(f"\nError: {e}")

        elif opcion == "2":
            codigoPrestamo = input("\nCodigo prestamo: ")
            try:
                resultado = gestorPrestamos.registrarDevolucion(codigoPrestamo)
                # registrar_devolucion indica el fallo devolviendo False (no lanza
                # error); antes no se revisaba y siempre decía "registrada".
                if not resultado:
                    print(f"\nError: El prestamo {codigoPrestamo} no existe o ya fue devuelto")
                else:
                    print(f"\nDevolucion registrada")
                    # Si devuelve un código, la unidad pasó al siguiente de la fila
                    if isinstance(resultado, str):
                        asignado = gestorPrestamos.buscarPrestamo(resultado)
                        print(f"Asignado automaticamente a {asignado.codigoUsuario} "
                              f"(siguiente en la fila): {resultado}")
            except ValueError as e:
                print(f"\nError: {e}")

        elif opcion == "3":
            # listarActivos devuelve un VectorDinamico (no una list)
            activos = gestorPrestamos.listarActivos()
            print(f"\nTotal prestamos activos: {activos.obtenerTamaño()}\n")
            for i in range(activos.obtenerTamaño()):
                p = activos.obtener(i)
                print(f"  {p.codigo}: {p.codigoUsuario} -> {p.codigoRecurso} [{p.sede}]")

        elif opcion == "4":
            prestamos = gestorPrestamos.obtenerPrestamosAtrasados()
            print(f"\nTotal prestamos ATRASADOS: {len(prestamos)}\n")
            for p in prestamos:
                dias_atraso = p.diasAtraso()
                print(f"  {p.codigo}: {p.codigoUsuario} -> {p.codigoRecurso} [{dias_atraso} días atraso]")

        elif opcion == "5":
            usuarioCod = input("\nCodigo usuario: ")
            prestamos = gestorPrestamos.obtenerPrestamosUsuario(usuarioCod)
            print(f"\nPrestamos de {usuarioCod}: {len(prestamos)}\n")
            for p in prestamos:
                print(f"  {p.codigo}: {p.codigoRecurso} [{p.estado}]")

        elif opcion == "6":
            sede = input("\nSede (Centro/Norte/Sur): ")
            prestamos = gestorPrestamos.obtenerPrestamosSede(sede)
            print(f"\nPrestamos en {sede}: {len(prestamos)}\n")
            for p in prestamos:
                print(f"  {p.codigo}: {p.codigoUsuario} -> {p.codigoRecurso}")

        elif opcion == "7":
            codigo = input("\nCodigo prestamo: ")
            prestamo = gestorPrestamos.buscarPrestamo(codigo)
            if prestamo:
                print(f"\n{prestamo.codigo}: {prestamo.codigoUsuario} -> {prestamo.codigoRecurso}")
                print(f"Sede: {prestamo.sede}")
                print(f"Fecha: {prestamo.fechaPrestamo.strftime('%Y-%m-%d %H:%M')}")
                print(f"Estado: {prestamo.estado}")
                if prestamo.estaAtrasado():
                    print(f"ATRASADO: {prestamo.diasAtraso()} días")
            else:
                print(f"\nPrestamo {codigo} no encontrado")

        elif opcion == "8":
            # deshacer() puede lanzar ValueError si ya no hay unidad para revertir una devolución
            try:
                if gestorPrestamos.deshacer():
                    print(f"\nOperacion deshecha (Pila LIFO)")
                else:
                    print(f"\nNo hay operaciones para deshacer")
            except ValueError as e:
                print(f"\nError: {e}")

        elif opcion == "9":
            print("\nHistorial del mas antiguo al mas reciente (recorrido con 'siguiente'):")
            for p in gestorPrestamos.historialAdelante():
                print(f"  {p.codigo}: {p.codigoUsuario} -> {p.codigoRecurso} [{p.estado}]")
            print("\nHistorial del mas reciente al mas antiguo (recorrido con 'anterior'):")
            for p in gestorPrestamos.historialAtras():
                print(f"  {p.codigo}: {p.codigoUsuario} -> {p.codigoRecurso} [{p.estado}]")

        pausa()


def gestionInventario(gestor):
    """Muestra la matriz de inventario."""
    limpiarPantalla()
    print("  MATRIZ DE INVENTARIO (M07)")
    print()
    print("Disponibilidad por sede y recurso:")
    print()
    print(gestor.inventario.mostrarMatriz())
    pausa()


def gestionTurnos(gestorTurnos):
    """Submenu para gestion de turnos (M04)."""
    limpiarPantalla()
    print("  GESTION DE TURNOS (M04 - Cola FIFO)")
    print()

    while True:
        print("\n1. Ver siguiente turno")
        print("2. Ver fila de espera (por recurso)")
        print("3. Ver cantidad en espera")
        print("4. Solicitar turno")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break
        elif opcion == "1":
            recurso = input("\nCodigo recurso: ")
            # ver_siguiente solo consulta; obtener_siguiente sacaba al usuario de la fila
            siguiente = gestorTurnos.verSiguiente(recurso)
            if siguiente:
                print(f"\nSiguiente en fila: {siguiente.codigoUsuario} (turno {siguiente.codigo})")
            else:
                print(f"\nNo hay nadie en fila para {recurso}")
        elif opcion == "2":
            recurso = input("\nCodigo recurso: ")
            fila = gestorTurnos.obtenerFila(recurso)
            print(f"\nFila para {recurso}: {len(fila)} personas\n")
            for i, sol in enumerate(fila, 1):
                print(f"  {i}. {sol.codigoUsuario}")
        elif opcion == "3":
            recurso = input("\nCodigo recurso: ")
            cantidad = gestorTurnos.obtenerCantidadEspera(recurso)
            print(f"\n{cantidad} personas esperando por {recurso}")
        elif opcion == "4":
            # Antes no había forma de entrar a la fila desde el programa (RF3)
            usuarioCod = input("\nCodigo usuario: ")
            recursoCod = input("Codigo recurso: ")
            sede = input("Sede (Centro/Norte/Sur): ")
            solicitarTurnoMenu(gestorTurnos, usuarioCod, recursoCod, sede)

        pausa()


def gestionCategorias(gestorCategorias):
    """Submenu para gestion de categorias (M05 - Árbol)."""
    limpiarPantalla()
    print("  GESTION DE CATEGORIAS (M05 - Árbol Binario)")
    print()

    while True:
        print("\n1. Registrar categoria")
        print("2. Buscar categoria")
        print("3. Listar todas las categorias")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break
        elif opcion == "1":
            codigo = input("\nCodigo categoria: ")
            nombre = input("Nombre categoria: ")
            # registrar_categoria lanza ValueError si el código ya existe (RF7)
            try:
                gestorCategorias.registrarCategoria(codigo, nombre)
                print(f"\nCategoria registrada: {codigo}")
            except ValueError as e:
                print(f"\nError: {e}")
        elif opcion == "2":
            codigo = input("\nCodigo categoria: ")
            cat = gestorCategorias.obtenerCategoria(codigo)
            if cat:
                print(f"\n{cat.codigo}: {cat.nombre}")
            else:
                print(f"\nCategoria {codigo} no encontrada")
        elif opcion == "3":
            cantidad = gestorCategorias.obtenerCantidad()
            print(f"\nTotal categorias: {cantidad}  (recorrido inorden del arbol = orden por codigo)")
            for codigo in gestorCategorias.arbol.recorridoInorden():
                cat = gestorCategorias.obtenerCategoria(codigo)
                print(f"  {cat.codigo}: {cat.nombre}")
            print(f"Altura del arbol: {gestorCategorias.arbol.obtenerAltura()}")

        pausa()


def gestionInformes(generador, gestorRecursos, gestorUsuarios):
    """Submenu para informes y reportes (M06)."""
    limpiarPantalla()
    print("  INFORMES Y REPORTES (M06)")
    print()

    while True:
        print("\n1. Reporte de uso (prestamos)")
        print("2. Reporte de inventario")
        print("3. Recursos mas prestados (merge sort)")
        print("4. Usuarios por nombre (merge sort)")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break
        elif opcion == "1":
            print("\n REPORTE DE USO:")
            print(generador.generarReporteUso())
        elif opcion == "2":
            print("\n REPORTE DE INVENTARIO:")
            print(generador.generarReporteInventario())
        elif opcion == "3":
            print("\n RECURSOS MAS PRESTADOS (merge sort, estable, O(n log n)):")
            ordenados = generador.listarRecursosOrdenadosPrestamos(gestorRecursos.listarTodos())
            for i, r in enumerate(ordenados, 1):
                print(f"  {i}. {r.codigo} {r.nombre:<25} {r.cantidadPrestamos} prestamos")
        elif opcion == "4":
            print("\n USUARIOS POR NOMBRE (merge sort):")
            for u in generador.listarUsuariosOrdenadosNombre(gestorUsuarios.listarTodos()):
                print(f"  {u.codigo}: {u.nombre}")

        pausa()


def pruebasEstructuras():
    """Demostracion de estructuras de datos."""
    limpiarPantalla()
    print("  PRUEBAS DE ESTRUCTURAS DE DATOS (propias)")
    print()

    print("1. VECTOR DINAMICO (O(1) amortizado):")
    v = VectorDinamico(capacidadInicial=2)
    v.agregar("A")
    v.agregar("B")
    print(f"   Despues agregar A, B: tamaño={v.obtenerTamaño()}, capacidad={v.obtenerCapacidad()}")
    v.agregar("C")
    print(f"   Despues agregar C: tamaño={v.obtenerTamaño()}, capacidad={v.obtenerCapacidad()}")
    print(f"   Contenido: {[v.obtener(i) for i in range(v.obtenerTamaño())]}")
    print()

    print("2. LISTA SIMPLE (O(n) busqueda, O(1) insercion):")
    ls = ListaSimple()
    ls.agregarAlFinal("X")
    ls.agregarAlFinal("Y")
    ls.agregarAlFinal("Z")
    print(f"   Contenido: {ls.recorrer()}")
    print()

    print("3. LISTA DOBLE (Bidireccional):")
    ld = ListaDoble()
    ld.agregarAlFinal(1)
    ld.agregarAlFinal(2)
    ld.agregarAlFinal(3)
    print(f"   Adelante: {ld.recorrerAdelante()}")
    print(f"   Atras:    {ld.recorrerAtras()}")
    print()

    print("4. PILA - LIFO (O(1) push/pop):")
    p = Pila()
    p.push("Op1")
    p.push("Op2")
    p.push("Op3")
    print(f"   Tope: {p.peek()}")
    print(f"   Pop: {p.pop()}, nuevo tope: {p.peek()}")
    print()

    print("5. COLA - FIFO (O(1) encolar/desencolar):")
    c = ColaFIFO()
    c.encolar("User1")
    c.encolar("User2")
    c.encolar("User3")
    print(f"   Frente: {c.frente()}")
    print(f"   Desencolar: {c.desencolar()}, nuevo frente: {c.frente()}")
    print()

    print("6. TABLA HASH djb2 (O(1) promedio insertar/buscar):")
    t = TablaHash(7)
    for i in range(1, 11):
        t.insertar(f"R{i:04d}", f"Recurso {i}")
    e = t.estadisticas()
    print(f"   10 claves en tabla inicial de 7 -> crecio a {e['capacidad']} (primo, factor 0.75)")
    print(f"   buscar('R0007') = {t.buscar('R0007')}   factor de carga = {e['factorCarga']}")
    print()

    print("7. ARBOL BINARIO DE BUSQUEDA (O(log n) promedio):")
    a = ArbolBinario()
    comparar = lambda x, y: -1 if x < y else (1 if x > y else 0)
    for c in ["C05", "C02", "C08", "C01", "C03", "C07", "C09"]:
        a.insertar(c, comparar)
    print(f"   Insertados: C05 C02 C08 C01 C03 C07 C09")
    print(f"   Inorden (sale ordenado): {a.recorridoInorden()}")
    print(f"   Altura: {a.obtenerAltura()} (balanceado por el orden de insercion)")
    print()

    print("Todas las estructuras funcionan correctamente")
    print()

    pausa()


def cargarHistorialEjemplo(gestorRecursos, gestorPrestamos, gestorCategorias,
                           sistemaInteligente, r1, r2):
    """Datos de ejemplo para la exposicion: mas recursos, categorias, prestamos de
    dias anteriores (algunos devueltos, uno atrasado) y calificaciones."""
    r4 = gestorRecursos.registrarLibro("Estructuras de Datos", "Cormen", "978-456", 2009)
    r5 = gestorRecursos.registrarEquipo("Portatil Dell", "Portatil", "Latitude", "Centro")
    for cod, sede, unidades in ((r4, "Centro", 3), (r4, "Norte", 1), (r5, "Centro", 2)):
        gestorRecursos.actualizarDisponibilidad(cod, sede, unidades)

    for cod, nombre in (("C001", "Ciencias"), ("C002", "Ingenieria"), ("C003", "Literatura")):
        gestorCategorias.registrarCategoria(cod, nombre)

    # Historial: prestamos de dias anteriores (algunos ya devueltos) para que
    # informes, atrasados y M08 trabajen con datos reales del sistema.
    hoy = datetime.now()
    historial = (("U002", r1, 10, True), ("U002", r4, 5, True),
                 ("U003", r1, 4, True), ("U003", r4, 2, False), ("U003", r5, 1, False),
                 ("U004", r2, 2, True), ("U004", r1, 3, True),
                 ("U005", r1, 20, False))          # U005 tiene un prestamo atrasado
    for usuario, recurso, diasAtras, devuelto in historial:
        cod = gestorPrestamos.registrarPrestamo(usuario, recurso, "Centro",
                                                fechaPrestamo=hoy - timedelta(days=diasAtras))
        if devuelto:
            gestorPrestamos.registrarDevolucion(cod)
    gestorPrestamos.pilaDeshacer = Pila()  # la precarga no se puede deshacer

    for usuario, recurso, estrellas in (("U002", r1, 5), ("U003", r1, 4), ("U004", r1, 4),
                                        ("U002", r4, 5), ("U003", r4, 5),
                                        ("U004", r2, 3), ("U003", r5, 4)):
        sistemaInteligente.registrarCalificacion(usuario, recurso, estrellas)



def main():
    """Funcion principal."""
    print("Cargando sistema...")

    # Crear gestores (M01-M08)
    gestorUsuarios = GestorUsuarios()
    gestorRecursos = GestorRecursos(numSedes=3)
    # GestorTurnos recibe usuarios y recursos para validar "Solicitar turno"
    gestorTurnos = GestorTurnos(
        gestorUsuarios=gestorUsuarios,
        gestorRecursos=gestorRecursos
    )
    sistemaInteligente = SistemaInteligente()
    gestorPrestamos = GestorPrestamos(
        gestorTurnos=gestorTurnos,
        gestorUsuarios=gestorUsuarios,
        gestorRecursos=gestorRecursos,
        sistemaInteligente=sistemaInteligente  # M08 aprende de cada prestamo real
    )
    gestorCategorias = GestorCategorias()
    generadorInformes = GeneradorInformes(
        gestorRecursos=gestorRecursos,
        gestorPrestamos=gestorPrestamos
    )

    # Pre-cargar datos de ejemplo
    print("Cargando datos de ejemplo...")

    # PRECARGA_MINIMA la usan las pruebas automaticas (solo U001, U002 y R0001-R0003)
    completa = not os.environ.get("PRECARGA_MINIMA")

    usuariosEjemplo = [("Carlos Lopez", "carlos@uni.edu"), ("Ana Garcia", "ana@uni.edu")]
    if completa:
        usuariosEjemplo += [("Luis Perez", "luis@uni.edu"), ("Maria Rojas", "maria@uni.edu"),
                            ("Pedro Diaz", "pedro@uni.edu")]
    for nombre, correo in usuariosEjemplo:
        gestorUsuarios.registrar(nombre, correo)          # U001 .. U005

    gestorRecursos.registrarSede(0, "Centro")
    gestorRecursos.registrarSede(1, "Norte")
    gestorRecursos.registrarSede(2, "Sur")

    r1 = gestorRecursos.registrarLibro("Python 101", "Guido van Rossum", "978-123", 2020)
    r2 = gestorRecursos.registrarEquipo("Proyector 1", "Proyector", "Epson", "Sala A")
    r3 = gestorRecursos.registrarSala("Sala de Estudio", 30)
    for cod, sede, unidades in ((r1, "Centro", 5), (r2, "Centro", 2), (r3, "Centro", 1)):
        gestorRecursos.actualizarDisponibilidad(cod, sede, unidades)

    if completa:
        cargarHistorialEjemplo(gestorRecursos, gestorPrestamos, gestorCategorias,
                               sistemaInteligente, r1, r2)

    print("Sistema listo\n")


    # Menu interactivo
    while True:
        menuPrincipal()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            print("\n¡Hasta luego!\n")
            break

        elif opcion == "1":
            gestionUsuarios(gestorUsuarios)

        elif opcion == "2":
            gestionRecursos(gestorRecursos)

        elif opcion == "3":
            gestionInventario(gestorRecursos)

        elif opcion == "4":
            gestionPrestamos(gestorPrestamos, gestorUsuarios, gestorRecursos)

        elif opcion == "5":
            gestionTurnos(gestorTurnos)

        elif opcion == "6":
            gestionCategorias(gestorCategorias)

        elif opcion == "7":
            gestionInformes(generadorInformes, gestorRecursos, gestorUsuarios)

        elif opcion == "8":
            pruebasEstructuras()

        elif opcion == "9":
            menuFuncionesInteligentes(sistemaInteligente, gestorRecursos, gestorUsuarios)

        elif opcion == "10":
            limpiarPantalla()
            ejecutarEvidencia()
            pausa()

        else:
            print("\nOpcion invalida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Programa interrumpido! \n")
        sys.exit(0)
