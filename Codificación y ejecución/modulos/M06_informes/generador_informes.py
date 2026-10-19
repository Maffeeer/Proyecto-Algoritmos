class Ordenamientos:
    @staticmethod
    def bubbleSort(arr, clave=lambda x: x):
        arrCopia = arr.copy()
        for i in range(len(arrCopia)):
            for j in range(len(arrCopia)-1-i):
                if clave(arrCopia[j]) > clave(arrCopia[j+1]):
                    arrCopia[j], arrCopia[j+1] = arrCopia[j+1], arrCopia[j]
        return arrCopia

    @staticmethod
    def quickSort(arr, clave=lambda x: x, izq=0, der=None):
        if der is None:
            der = len(arr) - 1

        if izq < der:
            p = Ordenamientos._particionar(arr, clave, izq, der)
            Ordenamientos.quickSort(arr, clave, izq, p - 1)
            Ordenamientos.quickSort(arr, clave, p + 1, der)
        return arr

    @staticmethod
    def _particionar(arr, clave, izq, der):
        pivote = clave(arr[der])
        i = izq - 1
        for j in range(izq, der):
            if clave(arr[j]) < pivote:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[der] = arr[der], arr[i + 1]
        return i + 1

class GeneradorInformes:
    def __init__(self, gestorRecursos=None, gestorPrestamos=None):
        self.gestorRecursos = gestorRecursos
        self.gestorPrestamos = gestorPrestamos

    # ______Reportes______

    def generarReporteUso(self):
        if not self.gestorPrestamos:
            return "sin datos"
        total = self.gestorPrestamos.obtenerCantidad()
        return f"total de préstamos registrados: {total}"

    def generarReporteInventario(self):
        if not self.gestorRecursos:
            return "sin datos"
        return str(self.gestorRecursos)

    # listados

    def listarRecursosOrdenadosNombre(self, recursos):
        return Ordenamientos.bubbleSort(recursos.copy(), lambda r: r.nombre)

    def listarRecursosOrdenadosPrestamos(self, recursos):
        return Ordenamientos.bubbleSort(recursos.copy(), lambda r: -r.cantidadPrestamos)

    def listarUsuariosOrdenadosNombre(self, usuarios):
        return Ordenamientos.bubbleSort(usuarios.copy(), lambda u: u.nombre)

    def obtenerOrdenamientos(self):
        return Ordenamientos

    