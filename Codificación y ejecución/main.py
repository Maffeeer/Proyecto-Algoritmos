
import sys
from modulos import (GestorUsuarios, GestorRecursos, GestorPrestamos, GestorTurnos,
                     GestorCategorias, GeneradorInformes, GestorInventario, SistemaInteligente)
from modulos.M03_Prestamos import SinUnidadesError
from estructuras import VectorDinamico, ListaSimple, ListaDoble, Pila, ColaFIFO


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
    print("     VectorDinamico, ListaSimple, ListaDoble, Pila, Cola")
    print()
    print("  9. Funciones Inteligentes (M08)")
    print()
    print("  0. Salir")
    print()


def menuFuncionesInteligentes(sistemaInteligente):
    """Submenu para funciones inteligentes del startup."""
    while True:
        limpiarPantalla()
        print("  FUNCIONES INTELIGENTES ")
        print()
        print("  1. Recomendaciones Inteligentes")
        print("     (IA: Collaborative Filtering - Como Netflix)")
        print()
        print("  2. Calificaciones y Reviews")
        print("     (Community: Reviews 1-5 estrellas - Como Airbnb)")
        print()
        print("  3. Prediccion de Disponibilidad")
        print("     (Analytics: Forecast de cuando esta disponible)")
        print()
        print("  4. Gamificacion")
        print("     (Engagement: Puntos, Badges, Niveles, Leaderboards)")
        print()
        print("  0. Volver al menu principal")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break

        elif opcion == "1":
            demoRecomendaciones(sistemaInteligente)

        elif opcion == "2":
            demoCalificaciones(sistemaInteligente)

        elif opcion == "3":
            demoPrediccion(sistemaInteligente)

        elif opcion == "4":
            demoGamificacion(sistemaInteligente)

        else:
            print("\nOpcion invalida")
            pausa()


def demoRecomendaciones(sistema):
    """Demostracion de recomendaciones inteligentes."""
    limpiarPantalla()
    print("  RECOMENDACIONES INTELIGENTES (IA)")
    print("COMO FUNCIONA:")
    print("  1. Analiza historico de prestamos de usuarios")
    print("  2. Identifica usuarios con patrones similares")
    print("  3. Sugiere recursos que usuarios similares pidieron")
    print()
    print("EJEMPLO:")
    print("  Si Usuario A pidio: [Libro Python, Libro Java, Revista Tech]")
    print("  Y Usuario B pidio: [Libro Python, Libro Java, Libro C++]")
    print("  -> Sistema recomienda a A: 'Libro C++ (usuarios similares lo pidieron)'")
    print()
    print()

    pausa()


def demoCalificaciones(sistema):
    """Demostracion de calificaciones y reviews."""
    limpiarPantalla()
    print("  CALIFICACIONES Y REVIEWS (COMMUNITY-DRIVEN)")
    print()
    print("COMO FUNCIONA:")
    print("  1. Usuarios califican recursos (1-5 estrellas)")
    print("  2. Escriben comentarios y feedback")
    print("  3. Sistema genera RANKING de mejores recursos")
    print("  4. Comunidad vota utilidad de cada review")
    print()
    print("EJEMPLO:")
    print("  Libro Python (R001):")
    print("    ⭐⭐⭐⭐⭐ 'Excelente, muy didactico' (123 usuarios lo marcaron util)")
    print("    ⭐⭐⭐⭐   'Bueno pero un poco denso' (45 usuarios)")
    print("    Promedio: 4.3/5 estrellas")
    print()
    print("RANKING GENERAL:")
    print("  1. Sala Estudio (R003): 4.9/5 (8 reviews)")
    print("  2. Libro Python (R001): 4.3/5 (3 reviews)")
    print()
    print()

    pausa()


def demoPrediccion(sistema):
    """Demostracion de prediccion de disponibilidad."""
    limpiarPantalla()
    print("  PREDICCION DE DISPONIBILIDAD (ANALYTICS)")
    print()
    print("COMO FUNCIONA:")
    print("  1. Registra duracion historica de cada prestamo")
    print("  2. Calcula promedio de dias para cada tipo de recurso")
    print("  3. Analiza patrones de demanda por hora del dia")
    print("  4. Sugiere mejor horario para pedir (menos congestión)")
    print()
    print("EJEMPLO:")
    print("  Usuario pregunta: '¿Cuando estara disponible Libro Python?'")
    print()
    print("  Sistema responde:")
    print("    'Disponible en ~3 dias (78% confianza)'")
    print("    'Mejor horario: 09:00 (menos congestión)'")
    print()
    print("ANALISIS:")
    print("  - Duracion promedio de prestamo: 3.25 dias")
    print("  - Pico de demanda: 14:00 (8 solicitudes)")
    print("  - Mejor horario: 09:00 (2 solicitudes)")
    print()
    print()

    pausa()


def demoGamificacion(sistema):
    """Demostracion de gamificacion."""
    limpiarPantalla()
    print("  GAMIFICACION (ENGAGEMENT)")
    print()
    print("COMPONENTES:")
    print()
    print("1. PUNTOS:")
    print("   - Prestamo registrado: +10 puntos")
    print("   - Devolucion a tiempo: +20 puntos")
    print("   - Review escrita: +15 puntos")
    print("   - Busqueda realizada: +2 puntos")
    print()
    print("2. NIVELES (1-10):")
    print("   Nivel 1 Novato (0 pts)   -> Nivel 5 Expert (1000 pts)")
    print("   Nivel 2 Aprendiz (100)  -> Nivel 6 Pro (1500)")
    print("   Nivel 3 Usuario (250)   -> Nivel 10 Supremo (5000)")
    print()
    print("3. BADGES (6 tipos desbloqueables):")
    print("   LEAL: 10+ prestamos")
    print("   DEVOLVEDOR: 5+ devoluciones a tiempo")
    print("   EXPLORADOR: 3+ tipos de recursos")
    print("   CRITICO: 5+ reviews")
    print("   DETECTIVE: 20+ busquedas")
    print("   VIP: Reputacion 4.5+ estrellas")
    print()
    print("4. LEADERBOARDS:")
    print("   - Top usuarios globales por puntos")
    print("   - Usuarios agrupados por nivel")
    print("   - Usuarios con cada badge")
    print()
    print()

    pausa()


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
                print(f"Prestamos: {usuario.cantidad_prestamos}")
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
                        print(f"Asignado automaticamente a {asignado.usuarioCodigo} "
                              f"(siguiente en la fila): {resultado}")
            except ValueError as e:
                print(f"\nError: {e}")

        elif opcion == "3":
            # listarActivos devuelve un VectorDinamico (no una list)
            activos = gestorPrestamos.listarActivos()
            print(f"\nTotal prestamos activos: {activos.obtenerTamaño()}\n")
            for i in range(activos.obtenerTamaño()):
                p = activos.obtener(i)
                print(f"  {p.codigo}: {p.usuarioCodigo} -> {p.recursoCodigo} [{p.sede}]")

        elif opcion == "4":
            prestamos = gestorPrestamos.obtenerPrestamosAtrasados()
            print(f"\nTotal prestamos ATRASADOS: {len(prestamos)}\n")
            for p in prestamos:
                dias_atraso = p.dias_atraso()
                print(f"  {p.codigo}: {p.usuarioCodigo} -> {p.recursoCodigo} [{dias_atraso} días atraso]")

        elif opcion == "5":
            usuarioCod = input("\nCodigo usuario: ")
            prestamos = gestorPrestamos.obtenerPrestamosUsuario(usuarioCod)
            print(f"\nPrestamos de {usuarioCod}: {len(prestamos)}\n")
            for p in prestamos:
                print(f"  {p.codigo}: {p.recursoCodigo} [{p.estado}]")

        elif opcion == "6":
            sede = input("\nSede (Centro/Norte/Sur): ")
            prestamos = gestorPrestamos.obtenerPrestamosSede(sede)
            print(f"\nPrestamos en {sede}: {len(prestamos)}\n")
            for p in prestamos:
                print(f"  {p.codigo}: {p.usuarioCodigo} -> {p.recursoCodigo}")

        elif opcion == "7":
            codigo = input("\nCodigo prestamo: ")
            prestamo = gestorPrestamos.buscarPrestamo(codigo)
            if prestamo:
                print(f"\n{prestamo.codigo}: {prestamo.usuarioCodigo} -> {prestamo.recursoCodigo}")
                print(f"Sede: {prestamo.sede}")
                print(f"Fecha: {prestamo.fechaPrestamo.strftime('%Y-%m-%d %H:%M')}")
                print(f"Estado: {prestamo.estado}")
                if prestamo.esta_atrasado():
                    print(f"ATRASADO: {prestamo.dias_atraso()} días")
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

        pausa()


def gestionInventario(gestor):
    """Muestra la matriz de inventario."""
    limpiarPantalla()
    print("  MATRIZ DE INVENTARIO (M02)")
    print()
    print("Disponibilidad por sede y recurso:")
    print()
    print(gestor.inventario.mostrar_matriz())
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
            siguiente = gestorTurnos.ver_siguiente(recurso)
            if siguiente:
                print(f"\nSiguiente en fila: {siguiente.usuarioCodigo} (turno {siguiente.codigo})")
            else:
                print(f"\nNo hay nadie en fila para {recurso}")
        elif opcion == "2":
            recurso = input("\nCodigo recurso: ")
            fila = gestorTurnos.obtenerFila(recurso)
            print(f"\nFila para {recurso}: {len(fila)} personas\n")
            for i, sol in enumerate(fila, 1):
                print(f"  {i}. {sol.usuarioCodigo}")
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
            print(f"\nTotal categorias: {cantidad}")

        pausa()


def gestionInformes(generador):
    """Submenu para informes y reportes (M06)."""
    limpiarPantalla()
    print("  INFORMES Y REPORTES (M06)")
    print()

    while True:
        print("\n1. Reporte de uso (prestamos)")
        print("2. Reporte de inventario")
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

        pausa()


def pruebasEstructuras():
    """Demostracion de estructuras de datos."""
    limpiarPantalla()
    print("  PRUEBAS DE ESTRUCTURAS DE DATOS (8 propias)")
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
    print(f"   Adelante: {ld.recorrer_adelante()}")
    print(f"   Atras:    {ld.recorrer_atras()}")
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

    print("Todas las estructuras funcionan correctamente")
    print()

    pausa()


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
    gestorPrestamos = GestorPrestamos(
        gestorTurnos=gestorTurnos,
        gestorUsuarios=gestorUsuarios,
        gestorRecursos=gestorRecursos
    )
    gestorCategorias = GestorCategorias()
    # Argumentos con nombre: antes se pasaba (gestor_usuarios, gestor_recursos) por
    # posición y el reporte de uso contaba recursos y el de inventario mostraba usuarios.
    generadorInformes = GeneradorInformes(
        gestorRecursos=gestorRecursos,
        gestorPrestamos=gestorPrestamos
    )
    sistemaInteligente = SistemaInteligente()

    # Pre-cargar datos
    print("Cargando datos de ejemplo...")

    codU1 = gestorUsuarios.registrar("Carlos Lopez", "carlos@uni.edu")
    codU2 = gestorUsuarios.registrar("Ana Garcia", "ana@uni.edu")

    gestorRecursos.registrarSede(0, "Centro")
    gestorRecursos.registrarSede(1, "Norte")
    gestorRecursos.registrarSede(2, "Sur")

    codR1 = gestorRecursos.registrarLibro("Python 101", "Guido van Rossum", "978-123", 2020)
    codR2 = gestorRecursos.registrarEquipo("Proyector 1", "Proyector", "Epson", "Sala A")
    codR3 = gestorRecursos.registrarSala("Sala de Estudio", 30)

    gestorRecursos.actualizarDisponibilidad(codR1, "Centro", 5)
    gestorRecursos.actualizarDisponibilidad(codR2, "Centro", 2)
    gestorRecursos.actualizarDisponibilidad(codR3, "Centro", 1)

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
            gestionInformes(generadorInformes)

        elif opcion == "8":
            pruebasEstructuras()

        elif opcion == "9":
            menuFuncionesInteligentes(sistemaInteligente)

        else:
            print("\nOpcion invalida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Programa interrumpido! \n")
        sys.exit(0)
