"""M09 - Informes de uso.

Capa de agregacion sin datos propios. Recorre M02 (stock), M03 (historial) y
M07 (categorias) para calcular indicadores. Reutiliza las estructuras de esos
modulos.
"""


class GeneradorInformes:
    def __init__(self, gestor_inventario=None, gestor_prestamos=None,
                 gestor_categorias=None, gestor_turnos=None):
        self.inventario = gestor_inventario     # M02
        self.prestamos = gestor_prestamos       # M03
        self.categorias = gestor_categorias     # M07
        self.turnos = gestor_turnos             # M04 (opcional)

    def recursos_mas_prestados(self, top=10, desde=None, hasta=None):
        pass  # TODO: implementar en fase de desarrollo

    def recursos_nunca_prestados(self):
        pass  # TODO

    def tasa_ocupacion_por_recurso(self):
        pass  # TODO

    def prestamos_por_categoria(self, desde=None, hasta=None):
        pass  # TODO

    def demanda_insatisfecha(self):
        pass  # TODO

    def prestamos_vencidos(self, referencia=None):
        pass  # TODO

    def resumen_general(self):
        pass  # TODO
