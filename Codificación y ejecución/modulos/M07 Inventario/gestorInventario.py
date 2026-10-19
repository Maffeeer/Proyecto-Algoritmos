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

    #Duplicar el número de columnas de la matriz
    def _redimensionarColumnas(self):
        nuevaCapacidad = max (1, self.numRecursos * 2)
        #Arreglo de tamaño fijo por fila
        nuevaMatriz = [[0] * nuevaCapacidad for _ in range(self.numSedes)]
        for i in range(self.numSedes):
            for j in range(self.contadorRecursos):
                nuevaMatriz[i][j] = self.matriz[i][j]
        self.matriz = nuevaMatriz
        self.numRecursos = nuevaCapacidad

    #Registra un recurso en el mapeo si no existe, y redimensiona la matriz si es necesario
    def _registrarRecurso(self, codigoRecurso, nombreRecurso):
        if codigoRecurso not in self.mapeoRecursos:
            if self.contadorRecursos >= self.numRecursos:
                self._redimensionarColumnas()
            idx = self.contadorRecursos
            self.mapeoRecursos[codigoRecurso] = idx
            self.contadorRecursos += 1
            return idx
        return self.mapeoRecursos[codigoRecurso]

    #Registra una sede en el mapeo si no existe
    def registrarSede(self, indiceFila, nombreSede):
        if indiceFila >= self.numSedes:
            raise ValueError("Índice de sede fuera de rango")

        self.mapeoSedes[nombreSede] = indiceFila

    def obtenerDisponibilidad(self, codigoRecurso, sede):
        if codigoRecurso not in self.mapeoRecursos or sede not in self.mapeoSedes:
            return 0

        i = self.mapeoSedes[sede]
        j = self.mapeoRecursos[codigoRecurso]
        return self.matriz[i][j]

    def decrementar(self, codigoRecurso, sede):
        if codigoRecurso not in self.mapeoRecursos or sede not in self.mapeoSedes:
            return False

        i = self.mapeoSedes[sede]
        j = self.mapeoRecursos[codigoRecurso]

        if self.matriz[i][j] > 0:
            self.matriz[i][j] -= 1
            return True
        return False

    def incrementar(self, codigoRecurso, sede):
        if codigoRecurso not in self.mapeoRecursos or sede not in self.mapeoSedes:
            return False

        i = self.mapeoSedes[sede]
        j = self.mapeoRecursos[codigoRecurso]

        self.matriz[i][j] += 1
        return True

    def actualizar(self, codigoRecurso, sede, cantidad):
        if codigoRecurso not in self.mapeoRecursos or sede not in self.mapeoSedes:
            return False

        i = self.mapeoSedes[sede]
        j = self.mapeoRecursos[codigoRecurso]

        self.matriz[i][j] = max(0, cantidad)
        return True

    def obtenerFila(self, sede):
        if sede not in self.mapeoSedes:
            return []

        i = self.mapeoSedes[sede]
        return self.matriz[i][:self.contadorRecursos]

    
    
    