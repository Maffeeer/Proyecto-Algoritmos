class Ordenamientos:
    @staticmethod
    def bubble_sort(arr, clave=lambda x: x):
        arrCopia = arr.copy()
        for i in range(len(arrCopia)):
            for j in range(len(arrCopia)-1-i):
                if clave(arrCopia[j]) > clave(arrCopia[j+1]):
                    arrCopia[j], arrCopia[j+1] = arrCopia[j+1], arrCopia[j]
        return arrCopia

    @staticmethod
    def quick_sort(arr, clave=lambda x: x, izq=0, der=None):
        if der is None:
            der = len(arr) - 1

        if izq < der:
            p = Ordenamientos._particionar(arr, clave, izq, der)
            Ordenamientos.quick_sort(arr, clave, izq, p - 1)
            Ordenamientos.quick_sort(arr, clave, p + 1, der)
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

    def generar_reporte_uso(self):
        if not self.gestorPrestamos:
            return "sin datos"
        total = self.gestorPrestamos.obtener_cantidad()
        return f"total de préstamos registrados: {total}"

    def generar_reporte_inventario(self):
        if not self.gestorRecursos:
            return "sin datos"
        return str(self.gestorRecursos)

    #______listados_______

    def listar_recursos_ordenados_nombre(self, recursos):
        return Ordenamientos.bubble_sort(recursos.copy(), lambda r: r.nombre)

    def listar_recursos_ordenados_prestamos(self, recursos):
        return Ordenamientos.bubble_sort(recursos.copy(), lambda r: -r.cantidadPrestamos)

    def listar_usuarios_ordenados_nombre(self, usuarios):
        return Ordenamientos.bubble_sort(usuarios.copy(), lambda u: u.nombre)

    def obtener_ordenamientos(self):
        return Ordenamientos

    