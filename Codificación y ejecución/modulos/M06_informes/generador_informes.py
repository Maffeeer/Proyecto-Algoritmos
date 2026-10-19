class Ordenamientos:
    @staticmethod
    def bubble_sort(arr, clave=lambda x: x):
        arr_copia = arr.copy()
        for i in range(len(arr_copia)):
            for j in range(len(arr_copia)-1-i):
                if clave(arr_copia[j]) > clave(arr_copia[j+1]):
                    arr_copia[j], arr_copia[j+1] = arr_copia[j+1], arr_copia[j]
        return arr_copia

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
    def __init__(self, gestor_recursos=None, gestor_prestamos=None):
        self.gestor_recursos = gestor_recursos
        self.gestor_prestamos = gestor_prestamos

    # ______Reportes______

    def generar_reporte_uso(self):
        if not self.gestor_prestamos:
            return "sin datos"
        total = self.gestor_prestamos.obtener_cantidad()
        return f"total de préstamos registrados: {total}"

    def generar_reporte_inventario(self):
        if not self.gestor_recursos:
            return "sin datos"
        return str(self.gestor_recursos)

    #______listados_______

    def listar_recursos_ordenados_nombre(self, recursos):
        return Ordenamientos.bubble_sort(recursos.copy(), lambda r: r.nombre)

    def listar_recursos_ordenados_prestamos(self, recursos):
        return Ordenamientos.bubble_sort(recursos.copy(), lambda r: -r.cantidad_prestamos)

    def listar_usuarios_ordenados_nombre(self, usuarios):
        return Ordenamientos.bubble_sort(usuarios.copy(), lambda u: u.nombre)

    def obtener_ordenamientos(self):
        return Ordenamientos

    