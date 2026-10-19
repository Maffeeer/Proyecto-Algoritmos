#Mafe Morales

#La clase gestorInventario gestiona la disponibilidad de los
#recursos por sede, usando matriz [i][j]

class GestorInventario:

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

    def registrarRecurso(self, codigoRecurso, nombreRecurso):
        return self._registrarRecurso(codigoRecurso, nombreRecurso)

    #Registra una sede en el mapeo si no existe
    def registrarSede(self, indiceFila, nombreSede):
        if indiceFila >= self.numSedes:
            raise ValueError("Índice de sede fuera de rango")

        self.mapeoSedes[nombreSede] = indiceFila

    # Obtiene la disponibilidad de un recurso en una sede específica
    def obtenerDisponibilidad(self, codigoRecurso, sede):
        if codigoRecurso not in self.mapeoRecursos or sede not in self.mapeoSedes:
            return 0

        i = self.mapeoSedes[sede]
        j = self.mapeoRecursos[codigoRecurso]
        return self.matriz[i][j]

    # Incrementa o decrementa la disponibilidad de un recurso en una sede específica
    def decrementar(self, codigoRecurso, sede):
        if codigoRecurso not in self.mapeoRecursos or sede not in self.mapeoSedes:
            return False

        i = self.mapeoSedes[sede]
        j = self.mapeoRecursos[codigoRecurso]

        if self.matriz[i][j] > 0:
            self.matriz[i][j] -= 1
            return True
        return False

    # Incrementa la disponibilidad de un recurso en una sede específica
    def incrementar(self, codigoRecurso, sede):
        if codigoRecurso not in self.mapeoRecursos or sede not in self.mapeoSedes:
            return False

        i = self.mapeoSedes[sede]
        j = self.mapeoRecursos[codigoRecurso]

        self.matriz[i][j] += 1
        return True

    # Actualiza la disponibilidad de un recurso en una sede específica
    def actualizar(self, codigoRecurso, sede, cantidad):
        if codigoRecurso not in self.mapeoRecursos or sede not in self.mapeoSedes:
            return False

        i = self.mapeoSedes[sede]
        j = self.mapeoRecursos[codigoRecurso]

        self.matriz[i][j] = max(0, cantidad)
        return True

    # Obtiene la disponibilidad total de un recurso en todas las sedes
    def obtenerFila(self, sede):
        if sede not in self.mapeoSedes:
            return []

        i = self.mapeoSedes[sede]
        return self.matriz[i][:self.contadorRecursos]

    # Obtiene la disponibilidad de un recurso específico en todas las sedes
    def obtenerColumna(self, codigoRecurso):
        if codigoRecurso not in self.mapeoRecursos:
            return []

        j = self.mapeoRecursos[codigoRecurso]
        return [self.matriz[i][j] for i in range(self.numSedes)]

    # Obtiene la disponibilidad total de todos los recursos en todas las sedes
    def mostrarMatriz(self):
        sedesOrdenadas = sorted(self.mapeoSedes.items(), key=lambda x: x[1])
        recursosOrdenados = sorted(self.mapeoRecursos.items(), key=lambda x: x[1])

        #Encabezado
        linea = "sede \\ recurso".ljust(15)
        for codigo, idx in recursosOrdenados:
            linea += f"{codigo}".ljust(8)
        resultado = linea + "\n"
        resultado += "-" * len(linea) + "\n"

        #Filas
        for nombreSede, idxSede in sedesOrdenadas:
            linea = f"{nombreSede}".ljust(15)
            for codigo, idxRecurso in recursosOrdenados:
                linea += f"{self.matriz[idxSede][idxRecurso]}".ljust(8)
            resultado += linea + "\n"
        return resultado

    def _str__(self):
        return f"gestorInventario({self.numSedes} sedes x {self.contadorRecursos} recursos)" 
    