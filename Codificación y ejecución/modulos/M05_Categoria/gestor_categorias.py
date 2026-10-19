#----------------------------------------
# Clase categoria
#----------------------------------------

from estructuras import ArbolBinario, TablaHash


class Categoria:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

    def __str__(self):
        return f"Categoria({self.codigo}: {self.nombre})"

    def __repr__(self):
        return self.__str__()


class GestorCategorias:
    def __init__(self):
        self.arbol = ArbolBinario()
        self.categorias = TablaHash(211)  # código -> Categoria

    def registrarCategoria(self, codigo, nombre):
        if self.categorias.contiene(codigo): # comprueba que eñ codigo ya exista, en ese caso da error
            raise ValueError(f"La categoria {codigo} ya existe")
        cat = Categoria(codigo, nombre)
        self.categorias.insertar(codigo, cat)
        self.arbol.insertar(codigo, lambda nuevo, existente: -1 if nuevo < existente else (1 if nuevo > existente else 0))
        return codigo

    def obtenerCategoria(self, codigo):
        return self.categorias.buscar(codigo)

    def obtenerCantidad(self):
        return self.categorias.obtener_cantidad()
