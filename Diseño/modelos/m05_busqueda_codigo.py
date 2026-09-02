"""M05 - Busqueda por codigo.

Capa transversal de indexacion (sin clase propia en el UML).
Estructura de datos: tabla hash propia con colisiones por encadenamiento.
Dos instancias: una para usuarios (M01) y otra para recursos (M02), sincronizadas.
"""


class TablaHash:
    def __init__(self, capacidad=16):
        self.buckets = [None] * capacidad   # cada bucket es una lista enlazada
        self.n = 0

    def _hash(self, clave):
        pass  # TODO: implementar en fase de desarrollo

    def insertar(self, clave, valor):
        pass  # TODO

    def obtener(self, clave):
        pass  # TODO

    def eliminar(self, clave):
        pass  # TODO


class IndiceBusqueda:
    def __init__(self):
        self.usuarios = TablaHash()   # id_usuario -> posicion en M01
        self.recursos = TablaHash()   # id_recurso -> posicion en M02

    def buscar_usuario(self, id_usuario):
        pass  # TODO

    def buscar_recurso(self, id_recurso):
        pass  # TODO
