"""M02 - Recursos e inventario.

Estructura de datos: vector dinamico para el catalogo + matriz sede x recurso
para la disponibilidad.
Fuente de verdad de stock: la consultan M03, M06 y M09.
"""


class Recurso:
    def __init__(self, id_recurso, titulo, categoria=""):
        self.id_recurso = id_recurso
        self.titulo = titulo
        self.categoria = categoria
        self.subcategoria = ""


class Libro(Recurso):
    def __init__(self, id_recurso, titulo, autor, isbn, categoria=""):
        super().__init__(id_recurso, titulo, categoria)
        self.autor = autor
        self.isbn = isbn


class Equipo(Recurso):
    def __init__(self, id_recurso, titulo, numero_serie, categoria=""):
        super().__init__(id_recurso, titulo, categoria)
        self.numero_serie = numero_serie


class Sala(Recurso):
    def __init__(self, id_recurso, titulo, capacidad, categoria=""):
        super().__init__(id_recurso, titulo, categoria)
        self.capacidad = capacidad


class Inventario:
    def __init__(self, id_recurso, id_sede, cantidad_total):
        self.id_recurso = id_recurso
        self.id_sede = id_sede
        self.cantidad_total = cantidad_total
        self.cantidad_disponible = cantidad_total


class GestorInventario:
    def __init__(self):
        self.catalogo = []   # vector dinamico de recursos
        self.matriz = []     # matriz sede x recurso -> Inventario
        self.indice = None   # tabla hash de M05: id_recurso -> posicion

    def crear_recurso(self, recurso):
        pass  # TODO: implementar en fase de desarrollo

    def obtener_recurso(self, id_recurso):
        pass  # TODO

    def actualizar_recurso(self, id_recurso, **campos):
        pass  # TODO

    def eliminar_recurso(self, id_recurso):
        pass  # TODO

    def consultar_stock(self, id_recurso, id_sede=None):
        pass  # TODO

    def hay_disponibilidad(self, id_recurso, id_sede=None):
        pass  # TODO

    def reservar(self, id_recurso, id_sede):
        pass  # TODO: llamado por M03 al prestar

    def liberar(self, id_recurso, id_sede):
        pass  # TODO: llamado por M03 al devolver
