class VectorDinamico:

    # inicializa el vector con capacidad inicial
    def __init__(self, capacidadInicial=10):
        self.datos = [None] * capacidadInicial
        self.tamaño = 0
        self.capacidad = capacidadInicial

    # Agrega un elemento al final del vector
    def agregar(self, elemento):
        if self.tamaño == self.capacidad:
            self._redimensionar()

        self.datos[self.tamaño] = elemento
        self.tamaño += 1

    # Redimensiona el vector cuando se llena
    def _redimensionar(self):
        nuevaCapacidad = self.capacidad * 2
        nuevosDatos = [None] * nuevaCapacidad

        for i in range(self.tamaño):
            nuevosDatos[i] = self.datos[i]

        self.datos = nuevosDatos
        self.capacidad = nuevaCapacidad

    # Obtiene un elemento por su índice
    def obtener(self, indice):
        if 0 <= indice < self.tamaño:
            return self.datos[indice]
        return None

    # Elimina un elemento por su índice
    def eliminarxIndice(self, indice):
        if not (0 <= indice < self.tamaño):
            return False

        for i in range(indice, self.tamaño - 1):
            self.datos[i] = self.datos[i + 1]

        self.datos[self.tamaño - 1] = None
        self.tamaño -= 1
        return True

    # Elimina un elemento por su valor
    def eliminarxValor(self, elemento):
        indice = self.buscar(elemento)
        if indice != -1:
            self.eliminarxIndice(indice)
            return True
        return False

    # Busca un elemento en el vector y devuelve su índice
    def buscar(self, elemento):
        for i in range(self.tamaño):
            if self.datos[i] == elemento:
                return i
        return -1

    # Recorre todos los elementos del vector y devuelve una lista con ellos
    def recorrer(self):
        resultado = []
        for i in range(self.tamaño):
            resultado.append(self.datos[i])
        return resultado

    # Verifica si el vector está vacío
    def estaVacio(self):
        return self.tamaño == 0

    # Obtiene el tamaño actual del vector
    def obtenerTamaño(self):
        return self.tamaño

    # Obtiene la capacidad actual del vector
    def obtenerCapacidad(self):
        return self.capacidad

    # Limpia el vector, eliminando todos los elementos
    def limpiar(self):
        self.datos = [None] * 10
        self.tamaño = 0
        self.capacidad = 10

    def __str__(self):
        return f"VectorDinamico({self.recorrer()}, tamaño={self.tamaño}, capacidad={self.capacidad})"

    def __repr__(self):
        return self.__str__()
