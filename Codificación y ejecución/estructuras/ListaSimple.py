class NodoSimple:

    def _init_(self, dato):
        self.dato = dato
        self.siguiente = None

    def _str_(self):
        return f"NodoSimple({self.dato})"


class ListaSimple:

    def _init_(self):
        """Inicializa lista vacía."""
        self.cabeza = None
        self.tamaño = 0

    # Agrega un elemento al inicio de la lista
    def agregarAlInicio(self, dato):
        nuevoNodo = NodoSimple(dato)
        nuevoNodo.siguiente = self.cabeza
        self.cabeza = nuevoNodo
        self.tamaño += 1

    # Agrega un elemento al final de la lista
    def agregarAlFinal(self, dato):
        nuevoNodo = NodoSimple(dato)

        if self.cabeza is None:
            self.cabeza = nuevoNodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevoNodo

        self.tamaño += 1

    # Elimina el primer nodo de la lista y devuelve su dato
    def eliminarInicio(self):
        if self.cabeza is None:
            return None

        dato = self.cabeza.dato
        self.cabeza = self.cabeza.siguiente
        self.tamaño -= 1
        return dato

    # Elimina el último nodo de la lista y devuelve su dato
    def eliminarFinal(self):
        if self.cabeza is None:
            return None

        if self.cabeza.siguiente is None:
            dato = self.cabeza.dato
            self.cabeza = None
            self.tamaño -= 1
            return dato

        actual = self.cabeza
        while actual.siguiente.siguiente is not None:
            actual = actual.siguiente

        dato = actual.siguiente.dato
        actual.siguiente = None
        self.tamaño -= 1
        return dato

    # Busca un elemento en la lista y devuelve su dato
    def buscar(self, criterioFn):
        actual = self.cabeza
        while actual is not None:
            if criterioFn(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

    #   Recorre todos los elementos de la lista y devuelve una lista con ellos
    def recorrer(self):
        resultado = []
        actual = self.cabeza
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    # Obtiene el tamaño de la lista
    def obtenerTamaño(self):
        return self.tamaño

    # Verifica si la lista está vacía
    def estaVacia(self):
        return self.tamaño == 0

    # Limpia la lista, eliminando todos los elementos
    def limpiar(self):
        self.cabeza = None
        self.tamaño = 0

    def _str_(self):
        return f"ListaSimple({self.recorrer()})"

    def _repr_(self):
        return self._str_()
