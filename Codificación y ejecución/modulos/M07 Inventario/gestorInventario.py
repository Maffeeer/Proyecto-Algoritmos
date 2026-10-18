#La clase gestorInventario gestiona la disponibilidad de los
#recursos por sede, usando matriz [i][j]

class gestorInventario:

    #Inicializador 
    def __init__(self, numSedes = 5, numRecursos = 50):
        self.numSedes = numSedes
        self.numRecursos = numRecursos

        #Matriz inicializada en 0
        self.matriz = [[0 for _ in range(numRecursos)] for _ in range(numSedes)]

        #Mapeo de codigos a indices de la matriz
        self.mapeoRecursos = {}   # {código: índice_columna}  
        self.mapeoSedes = {}   # {nombre_sede: índice_fila}
        self.contadorRecursos = 0
        self.contadorSedes = 0

    #Duplicar ek número de columnas de la matriz
    def _redimensionarColumnas(self):
        nuevaCapacidad = max (1, self.numRecursos * 2)
        #Arreglo de tamaño fijo por fila
        nuevaMatriz = [[0] * nuevaCapacidad for _ in range(self.numSedes)]
        for i in range(self.numSedes):
            for j in range(self.contadorRecursos):
                nuevaMatriz[i][j] = self.matriz[i][j]
        self.matriz = nuevaMatriz
        self.numRecursos = nuevaCapacidad

    