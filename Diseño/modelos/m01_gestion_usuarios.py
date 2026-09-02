"""M01 - Gestion de usuarios.

Estructura de datos: vector dinamico propio + tabla hash (M05) para buscar por id.
Operaciones: alta, baja, actualizacion, consulta.
Consumido por M03 (prestamos) y M04 (turnos).
"""


class Usuario:
    def __init__(self, id_usuario, nombre, email, tipo="estudiante"):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.tipo = tipo
        self.estado = "activo"


class GestorUsuarios:
    def __init__(self):
        self.usuarios = []   # vector dinamico
        self.indice = None   # tabla hash de M05: id_usuario -> posicion

    def alta(self, usuario):
        pass  # TODO: implementar en fase de desarrollo

    def baja(self, id_usuario):
        pass  # TODO

    def actualizar(self, id_usuario, **campos):
        pass  # TODO

    def consultar(self, id_usuario):
        pass  # TODO
