class NodoArbol:

    def _init_(self, dato):
        self.dato = dato
        self.izquierda = None
        self.derecha = None


class ArbolBinario:

    def _init_(self):
        """Inicializa árbol vacío."""
        self.raiz = None
        self.tamaño = 0

    def insertar(self, dato, criterioComparar):
        if self.raiz is None:
            self.raiz = NodoArbol(dato)
            self.tamaño = 1
        else:
            self._insertarRecursivo(self.raiz, dato, criterioComparar)

    def _insertarRecursivo(self, nodo, dato, criterio):
        resultado = criterio(dato, nodo.dato)

        if resultado < 0:
            if nodo.izquierda is None:
                nodo.izquierda = NodoArbol(dato)
                self.tamaño += 1
            else:
                self._insertarRecursivo(nodo.izquierda, dato, criterio)
        elif resultado > 0:
            if nodo.derecha is None:
                nodo.derecha = NodoArbol(dato)
                self.tamaño += 1
            else:
                self._insertarRecursivo(nodo.derecha, dato, criterio)

    def buscar(self, criterioBuscar):
        return self._buscarRecursivo(self.raiz, criterioBuscar)

    def _buscarRecursivo(self, nodo, criterio):
        if nodo is None:
            return None

        if criterio(nodo.dato):
            return nodo.dato

        resultado = self._buscarRecursivo(nodo.izquierda, criterio)
        if resultado is not None:
            return resultado

        return self._buscarRecursivo(nodo.derecha, criterio)

    def recorridoInorden(self):
        resultado = []
        self._inordenRecursivo(self.raiz, resultado)
        return resultado

    def _inordenRecursivo(self, nodo, resultado):
        if nodo is None:
            return
        self._inordenRecursivo(nodo.izquierda, resultado)
        resultado.append(nodo.dato)
        self._inordenRecursivo(nodo.derecha, resultado)

    def recorridoPreorden(self):
        resultado = []
        self._preordenRecursivo(self.raiz, resultado)
        return resultado

    def _preordenRecursivo(self, nodo, resultado):
        if nodo is None:
            return
        resultado.append(nodo.dato)
        self._preordenRecursivo(nodo.izquierda, resultado)
        self._preordenRecursivo(nodo.derecha, resultado)

    def recorridoPostorden(self):
        resultado = []
        self._postordenRecursivo(self.raiz, resultado)
        return resultado

    def _postordenRecursivo(self, nodo, resultado):
        if nodo is None:
            return
        self._postordenRecursivo(nodo.izquierda, resultado)
        self._postordenRecursivo(nodo.derecha, resultado)
        resultado.append(nodo.dato)

    def obtenerAltura(self):
        return self._alturaRecursiva(self.raiz)

    def _alturaRecursiva(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._alturaRecursiva(nodo.izquierda),
                       self._alturaRecursiva(nodo.derecha))

    def obtenerCantidad(self):
        return self.tamaño

    def estaVacio(self):
        return self.raiz is None

    def limpiar(self):
        self.raiz = None
        self.tamaño = 0
