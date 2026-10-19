class _Nodo:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None


class TablaHash:

    # Constructor de la tabla hash
    def __init__(self, tamaño=100):
        self.tamaño = tamaño
        self.tabla = [None] * tamaño  # Arreglo de cabeceras
        self.cantidad = 0

    # Función hash simple para cadenas y números
    def _hash(self, clave):
        if isinstance(clave, str):
            # Suma ASCII de caracteres módulo tamaño
            h = 0
            for c in clave:
                h += ord(c)
            return h % self.tamaño
        else:
            # Para números, usar módulo directo
            return abs(hash(clave)) % self.tamaño

    # Inserta o actualiza un par clave-valor    
    def insertar(self, clave, valor):
        """
        Inserta o actualiza un par clave-valor.

        Complejidad: O(1) promedio, O(n) peor caso
        """
        idx = self._hash(clave)

        # Buscar si ya existe en la cadena
        nodo = self.tabla[idx]
        while nodo is not None:
            if nodo.clave == clave:
                nodo.valor = valor  # Actualizar
                return
            nodo = nodo.siguiente

        # No existe, agregar al inicio de la cadena
        nuevoNodo = _Nodo(clave, valor)
        nuevoNodo.siguiente = self.tabla[idx]
        self.tabla[idx] = nuevoNodo
        self.cantidad += 1

    # Busca un valor por su clave
    def buscar(self, clave):
        idx = self._hash(clave)

        nodo = self.tabla[idx]
        while nodo is not None:
            if nodo.clave == clave:
                return nodo.valor
            nodo = nodo.siguiente

        return None

    # Elimina un par clave-valor de la tabla
    def eliminar(self, clave):
        idx = self._hash(clave)

        # Caso 1: Eliminar del inicio de la cadena
        if self.tabla[idx] is not None and self.tabla[idx].clave == clave:
            self.tabla[idx] = self.tabla[idx].siguiente
            self.cantidad -= 1
            return True

        # Caso 2: Buscar en el resto de la cadena
        nodo = self.tabla[idx]
        while nodo is not None and nodo.siguiente is not None:
            if nodo.siguiente.clave == clave:
                nodo.siguiente = nodo.siguiente.siguiente
                self.cantidad -= 1
                return True
            nodo = nodo.siguiente

        return False

    # Verifica si la tabla contiene una clave
    def contiene(self, clave):
        return self.buscar(clave) is not None

    # Obtiene la cantidad de elementos en la tabla
    def obtenerCantidad(self):
        return self.cantidad

    # Obtiene el tamaño de la tabla
    def obtenerTamaño(self):
        return self.tamaño

    # Obtiene el factor de carga de la tabla
    def obtenerTodasLasClaves(self):
        claves = []
        for celda in self.tabla:
            nodo = celda
            while nodo is not None:
                claves.append(nodo.clave)
                nodo = nodo.siguiente
        return claves

    # Obtiene el factor de carga de la tabla
    def obtenerFactorCarga(self):
        return self.cantidad / self.tamaño if self.tamaño > 0 else 0

    # Obtiene el factor de carga de la tabla
    def limpiar(self):
        self.tabla = [None] * self.tamaño
        self.cantidad = 0

    def __str__(self):
        return f"TablaHash(cantidad={self.cantidad}, tamaño={self.tamaño}, factor_carga={self.obtener_factor_carga():.2f})"

    def __repr__(self):
        return self.__str__()
