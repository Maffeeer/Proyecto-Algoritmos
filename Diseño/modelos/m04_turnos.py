"""M04 - Turnos / lista de espera.

Estructura de datos: una cola FIFO por cada recurso agotado.
M03 dispara la asignacion del siguiente al liberarse una unidad.
Depende de M02 (disponibilidad) y M01 (identidad del solicitante).
"""


class Solicitud:
    def __init__(self, usuario, recurso, id_sede, fecha_solicitud):
        self.usuario = usuario
        self.recurso = recurso
        self.id_sede = id_sede
        self.fecha_solicitud = fecha_solicitud
        self.estado = "en_espera"


class GestorTurnos:
    def __init__(self, gestor_usuarios=None, gestor_inventario=None, gestor_prestamos=None):
        self.colas = {}   # (id_recurso, id_sede) -> cola FIFO
        self.usuarios = gestor_usuarios
        self.inventario = gestor_inventario
        self.prestamos = gestor_prestamos

    def solicitar(self, id_usuario, id_recurso, id_sede):
        pass  # TODO: implementar en fase de desarrollo

    def cancelar(self, id_solicitud, id_recurso, id_sede):
        pass  # TODO

    def asignar_siguiente(self, id_recurso, id_sede):
        pass  # TODO: invocado por M03 tras una devolucion

    def consultar_posicion(self, id_usuario, id_recurso, id_sede):
        pass  # TODO
