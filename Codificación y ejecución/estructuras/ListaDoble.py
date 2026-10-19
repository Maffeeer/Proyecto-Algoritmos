class NodoDoble:

    def _init_(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

    def _str_(self):
        return f"NodoDoble({self.dato})"


class ListaDoble:

    def _init_(self):
        """Inicializa lista vacía."""
        self.cabeza = None
        self.cola = None
        self.tamaño = 0

    # Agrega un elemento al inicio de la lista
    def agregarAlInicio(self, dato):
        nuevoNodo = NodoDoble(dato)

        if self.cabeza is None:
            self.cabeza = self.cola = nuevoNodo
        else:
            nuevoNodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevoNodo
            self.cabeza = nuevoNodo

        self.tamaño += 1

    #   Agrega un elemento al final de la lista
    def agregarAlFinal(self, dato):
        nuevoNodo = NodoDoble(dato)

        if self.cola is None:
            self.cabeza = self.cola = nuevoNodo         
        else:
            nuevoNodo.anterior = self.cola
            self.cola.siguiente = nuevoNodo
            self.cola = nuevoNodo

        self.tamaño += 1

    # Elimina el primer nodo de la lista y devuelve su dato
    def eliminarInicio(self):
        if self.cabeza is None:
            return None

        dato = self.cabeza.dato

        if self.cabeza == self.cola:
            self.cabeza = self.cola = None
        else:
            self.cabeza = self.cabeza.siguiente
            self.cabeza.anterior = None

        self.tamaño -= 1
        return dato

    # Elimina el último nodo de la lista y devuelve su dato
    def eliminarFinal(self):
        if self.cola is None:
            return None

        dato = self.cola.dato

        if self.cabeza == self.cola:
            self.cabeza = self.cola = None
        else:
            self.cola = self.cola.anterior
            self.cola.siguiente = None

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

    # Recorre todos los elementos de la lista hacia adelante y devuelve una lista con ellos
    def recorrerAdelante(self):
        resultado = []
        actual = self.cabeza
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    #  Recorre todos los elementos de la lista hacia atrás y devuelve una lista con ellos
    def recorrerAtras(self):
        resultado = []
        actual = self.cola
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.anterior
        return resultado

    def obtenerTamaño(self):
        return self.tamaño

    def estaVacia(self):
        return self.tamaño == 0

    def limpiar(self):
        self.cabeza = None
        self.cola = None
        self.tamaño = 0

    def _str_(self):
        return f"ListaDoble({self.recorrerAdelante()})"

    def _repr_(self):
        return self._str_()
