"""M03 - Prestamos, devoluciones y deshacer.

Estructura de datos: lista enlazada simple para prestamos activos,
lista doblemente enlazada/circular para el historial y una pila para deshacer.
Depende de M02 (disponibilidad) y M01 (usuario). Dispara M04 al devolver.
"""


class Prestamo:
    def __init__(self, usuario, recurso, fecha_prestamo):
        self.usuario = usuario
        self.recurso = recurso
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = None
        self.estado = "activo"


class GestorPrestamos:
    def __init__(self, gestor_usuarios=None, gestor_inventario=None, gestor_turnos=None):
        self.activos = None      # lista enlazada simple
        self.historial = None    # lista doblemente enlazada / circular
        self.deshacer_pila = []  # pila de operaciones
        self.usuarios = gestor_usuarios
        self.inventario = gestor_inventario
        self.turnos = gestor_turnos

    def registrar(self, id_usuario, id_recurso, id_sede):
        pass  # TODO: implementar en fase de desarrollo

    def devolver(self, id_prestamo):
        pass  # TODO

    def deshacer(self):
        pass  # TODO

    def consultar(self, id_prestamo):
        pass  # TODO
