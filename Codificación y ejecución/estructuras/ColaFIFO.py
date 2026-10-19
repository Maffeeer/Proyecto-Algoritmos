class ColaFIFO:

    def __init__(self, capacidadInicial=10):
        self.capacidad = capacidadInicial
        self.datos = [None] * capacidadInicial  # Arreglo preallocado
        self.inicio = 0
        self.fin = 0
        self.tamaño = 0

    def _redimensionar(self):
        nuevaCapacidad = self.capacidad * 2
        nuevoArreglo = [None] * nuevaCapacidad

        # Copiar elementos en orden
        for i in range(self.tamaño):
            idxOriginal = (self.inicio + i) % self.capacidad
            nuevoArreglo[i] = self.datos[idxOriginal]

        self.datos = nuevoArreglo
        self.inicio = 0
        self.fin = self.tamaño
        self.capacidad = nuevaCapacidad

    def encolar(self, dato):
        if self.tamaño >= self.capacidad:
            self._redimensionar()

        self.datos[self.fin] = dato
        self.fin = (self.fin + 1) % self.capacidad
        self.tamaño += 1

    def desencolar(self):
        if self.tamaño == 0:
            return None

        resultado = self.datos[self.inicio]
        self.datos[self.inicio] = None  # Limpiar referencia
        self.inicio = (self.inicio + 1) % self.capacidad
        self.tamaño -= 1
        return resultado

    def frente(self):
        if self.tamaño == 0:
            return None
        return self.datos[self.inicio]

    def estaVacia(self):
        return self.tamaño == 0

    def obtenerTamaño(self):
        return self.tamaño

    def limpiar(self):
        self.inicio = 0
        self.fin = 0
        self.tamaño = 0

    def recorrer(self):
        resultado = []
        for i in range(self.tamaño):
            idx = (self.inicio + i) % self.capacidad
            resultado.append(self.datos[idx])
        return resultado

    def __str__(self):
        return f"ColaFIFO(tamaño={self.tamaño}, capacidad={self.capacidad})"

    def __repr__(self):
        return self.__str__()
