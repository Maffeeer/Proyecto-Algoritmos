"""M06 - Ordenamientos y listados.

Sin entidad propia. Opera sobre el vector dinamico de recursos de M02 (y M03).
Algoritmos: uno basico (insercion) y dos avanzados (quicksort, mergesort),
mas busqueda binaria sobre el resultado ordenado.
"""


class Ordenamientos:
    def ordenar_insercion(self, datos, key=None, descendente=False):
        pass  # TODO: implementar en fase de desarrollo

    def ordenar_quicksort(self, datos, key=None, descendente=False):
        pass  # TODO

    def ordenar_mergesort(self, datos, key=None, descendente=False):
        pass  # TODO

    def busqueda_binaria(self, datos_ordenados, objetivo, key=None):
        pass  # TODO


class ListadosRecursos:
    def __init__(self, gestor_inventario=None, gestor_prestamos=None):
        self.inventario = gestor_inventario
        self.prestamos = gestor_prestamos

    def por_titulo(self, descendente=False):
        pass  # TODO

    def por_disponibilidad(self, descendente=True):
        pass  # TODO

    def mas_prestados(self, top=10):
        pass  # TODO
