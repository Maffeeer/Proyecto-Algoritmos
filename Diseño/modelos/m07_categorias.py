"""M07 - Categorias del catalogo.

Convierte categoria/subcategoria de Recurso (M02) en una jerarquia real.
Estructura de datos: arbol binario de busqueda balanceado (AVL); cada nodo es
una categoria y puede tener recursos asociados.
"""


class Categoria:
    def __init__(self, nombre, ruta, padre=None):
        self.nombre = nombre
        self.ruta = ruta          # ej. "Tecnologia/Redes"
        self.padre = padre
        self.id_recursos = []     # recursos asociados (referencias a M02)
        self.subcategorias = []


class ArbolCategorias:
    def __init__(self):
        self.raiz = None   # arbol AVL indexado por ruta

    def insertar(self, categoria):
        pass  # TODO: implementar en fase de desarrollo

    def eliminar(self, ruta):
        pass  # TODO

    def buscar(self, ruta):
        pass  # TODO

    def recorrido_en_orden(self):
        pass  # TODO


class GestorCategorias:
    def __init__(self, gestor_inventario=None):
        self.arbol = ArbolCategorias()
        self.inventario = gestor_inventario

    def crear_categoria(self, nombre, ruta_padre=None):
        pass  # TODO

    def asociar_recurso(self, ruta, id_recurso):
        pass  # TODO

    def recursos_de_categoria(self, ruta, incluir_subcategorias=True):
        pass  # TODO
