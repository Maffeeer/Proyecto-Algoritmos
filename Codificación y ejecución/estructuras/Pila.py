class Pila:
    def __init__(self, capacidad_inicial=10):
        """Inicializa pila vacía con capacidad inicial."""
        self.capacidad = capacidad_inicial
        self.datos = [None] * capacidad_inicial  # Arreglo preallocado
        self.tope = 0  # Índice donde irá el próximo elemento

    # Redimensiona la pila cuando se llena
    def _redimensionar(self):
        nuevaCapacidad = self.capacidad * 2
        nuevoArreglo = [None] * nuevaCapacidad

        # Copiar elementos existentes
        for i in range(self.tope):
            nuevoArreglo[i] = self.datos[i]

        self.datos = nuevoArreglo
        self.capacidad = nuevaCapacidad

    # Agrega un elemento al tope de la pila
    def push(self, dato):
        if self.tope >= self.capacidad:
            self._redimensionar()

        self.datos[self.tope] = dato
        self.tope += 1

    # Quita y retorna el elemento del tope de la pila
    def pop(self):
        if self.tope == 0:
            return None

        self.tope -= 1
        resultado = self.datos[self.tope]
        self.datos[self.tope] = None  # Limpiar referencia
        return resultado

    # Retorna el elemento del tope sin quitarlo
    def peek(self):
        if self.tope == 0:
            return None
        return self.datos[self.tope - 1]

    # Verifica si la pila está vacía
    def esta_vacia(self):
        return self.tope == 0

    # Obtiene la cantidad de elementos en la pila
    def obtener_tamaño(self):
        return self.tope

    # Mismos nombres que el resto de estructuras (camelCase)
    def estaVacia(self):
        return self.tope == 0

    def obtenerTamaño(self):
        return self.tope

    # Limpia la pila, eliminando todos los elementos
    def limpiar(self):
        self.tope = 0

    # Recorre todos los elementos de la pila y devuelve una lista con ellos
    def recorrer(self):
        resultado = []
        for i in range(self.tope - 1, -1, -1):
            resultado.append(self.datos[i])
        return resultado

    def __str__(self):
        return f"Pila(tamaño={self.tope}, capacidad={self.capacidad})"

    def __repr__(self):
        return self.__str__()
