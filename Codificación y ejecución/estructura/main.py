""" Se paso el diagrama de flujo directamente a este archivo para poder generar la estructura basica del codigo"""

"""Sistema Biblioteca - estructura basica  ======================================Traduccion directa del diagrama de flujo (Algoritmo SistemaBiblioteca) a Python.Se conserva el enfoque del diagrama:- Arreglos paralelos de tamano fijo (MAX = 100) en lugar de objetos.- Contadores nUsuarios, nRecursos, ... para el numero de elementos usados.  - Un menu que se repite hasta que la opcion sea 0.Mas adelante estos arreglos paralelos se reemplazan por las clases yestructuras de datos disenadas en "Diseno/modelos/".""" 
MAX = 100

# --- Arreglos paralelos (Dimensionar ...(100)) ---------------------------
usuarios = [""] * MAX             # nombre de cada usuario, indice = id
recursos = [""] * MAX             # nombre de cada recurso, indice = id
sedes = [""] * MAX               # nombre de cada sede, indice = id

inventario_recurso = [0] * MAX   # id de recurso de cada registro de inventario
inventario_sede = [0] * MAX      # id de sede de cada registro de inventario
cantidad = [0] * MAX             # cantidad disponible de cada registro

prestamos_usuario = [0] * MAX    # id de usuario de cada prestamo
prestamos_recurso = [0] * MAX    # id de recurso de cada prestamo

solicitudes_usuario = [0] * MAX  # id de usuario de cada solicitud
solicitudes_recurso = [0] * MAX  # id de recurso de cada solicitud

# --- Contadores (nUsuarios = 0, nRecursos = 0, ...) ---------------------
nUsuarios = 0
nRecursos = 0
nSedes = 0
nInventarios = 0
nPrestamos = 0
nSolicitudes = 0


# =======================================================================
# Opciones del menu
# =======================================================================
def registrar_usuario():
    """Opcion 1."""
    global nUsuarios
    nombre = input("Nombre del usuario: ")
    usuarios[nUsuarios] = nombre
    nUsuarios += 1
    print("Usuario registrado.")


def registrar_recurso():
    """Opcion 2."""
    global nRecursos
    nombre = input("Nombre del recurso: ")
    recursos[nRecursos] = nombre
    nRecursos += 1
    print("Recurso registrado.")


def registrar_sede():
    """Opcion 3."""
    global nSedes
    nombre = input("Nombre de la sede: ")
    sedes[nSedes] = nombre
    nSedes += 1
    print("Sede registrada.")


def registrar_inventario():
    """Opcion 4."""
    global nInventarios
    id_recurso = int(input("Numero del recurso: "))
    id_sede = int(input("Numero de la sede: "))
    cant = int(input("Cantidad disponible: "))
    inventario_recurso[nInventarios] = id_recurso
    inventario_sede[nInventarios] = id_sede
    cantidad[nInventarios] = cant
    nInventarios += 1
    print("Inventario registrado.")


def consultar_disponibilidad():
    """Opcion 5."""
    id_recurso = int(input("Numero del recurso: "))
    for i in range(nInventarios):
        if inventario_recurso[i] == id_recurso:
            print("Sede:", inventario_sede[i])
            print("Cantidad disponible:", cantidad[i])


def realizar_prestamo():
    """Opcion 6."""
    global nPrestamos
    usuario_prestamo = int(input("Numero del usuario: "))
    recurso_prestamo = int(input("Numero del recurso: "))
    prestamos_usuario[nPrestamos] = usuario_prestamo
    prestamos_recurso[nPrestamos] = recurso_prestamo
    nPrestamos += 1
    for i in range(nInventarios):
        if inventario_recurso[i] == recurso_prestamo:
            if cantidad[i] > 0:
                cantidad[i] = cantidad[i] - 1
    print("Prestamo realizado.")


def registrar_devolucion():
    """Opcion 7."""
    usuario_prestamo = int(input("Numero del usuario: "))
    recurso_prestamo = int(input("Numero del recurso: "))
    for i in range(nInventarios):
        if inventario_recurso[i] == recurso_prestamo:
            cantidad[i] = cantidad[i] + 1
    print("Devolucion registrada.")


def registrar_solicitud():
    """Opcion 8."""
    global nSolicitudes
    solicitudes_usuario[nSolicitudes] = int(input("Numero del usuario: "))
    solicitudes_recurso[nSolicitudes] = int(input("Numero del recurso: "))
    nSolicitudes += 1
    print("Solicitud registrada.")


def consultar_prestamos():
    """Opcion 9."""
    print("PRESTAMOS REGISTRADOS")
    for i in range(nPrestamos):
        print("Usuario:", prestamos_usuario[i], "- Recurso:", prestamos_recurso[i])


# =======================================================================
# Programa principal (Repetir ... Hasta Que opcion = 0)
# =======================================================================
def mostrar_menu():
    print("***********************")
    print("    SISTEMA BIBLIOTECA")
    print("***********************")
    print("1. Registrar usuario")
    print("2. Registrar recurso")
    print("3. Registrar sede")
    print("4. Registrar inventario")
    print("5. Consultar disponibilidad")
    print("6. Realizar prestamo")
    print("7. Registrar devolucion")
    print("8. Registrar solicitud")
    print("9. Consultar prestamos")
    print("0. Salir")


def main():
    opcion = -1
    while opcion != 0:
        mostrar_menu()
        opcion = int(input("Seleccione una opcion: "))

        if opcion == 1:
            registrar_usuario()
        elif opcion == 2:
            registrar_recurso()
        elif opcion == 3:
            registrar_sede()
        elif opcion == 4:
            registrar_inventario()
        elif opcion == 5:
            consultar_disponibilidad()
        elif opcion == 6:
            realizar_prestamo()
        elif opcion == 7:
            registrar_devolucion()
        elif opcion == 8:
            registrar_solicitud()
        elif opcion == 9:
            consultar_prestamos()
        elif opcion == 0:
            print("Saliendo del sistema.")
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()
