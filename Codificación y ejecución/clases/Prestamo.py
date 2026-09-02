##NODO
from datetime import date
class NodosPrestamo:
    def __init__(self, id_prestamo, id_usuario, id_recurso, fecha_prestamo):
        self.id_prestamo = id_prestamo
        self.id_usuario = id_usuario
        self.id_recurso = id_recurso
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = None
        self.siguiente = None


##LISTA ENSLAZADA SIMPLE DE PRESTAMOS
class ListaPrestamos:
    def __init__(self):
        self.cabeza = None
        self.contador_id = 1  # Para generar IDs automatico

    def registrar_prestamo(self, id_usuario, id_recurso, fecha_prestamo=None):
        if fecha_prestamo is None:
            fecha_prestamo = date.today()

        nuevo_prestamo = NodosPrestamo(self.contador_id, id_usuario, id_recurso, fecha_prestamo)
        nuevo_prestamo.siguiente = self.cabeza
        self.cabeza = nuevo_prestamo
        self.contador_id += 1
        return nuevo_prestamo.id_prestamo  # Retorna el ID del préstamo registrado

    def registrar_devolucion (self, id_prestamo):
        actual = self.cabeza
        anterior = None

        while actual is not None:
            if actual.id_prestamo == id_prestamo:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                return True  # Devolución registrada exitosamente
            anterior = actual
            actual = actual.siguiente
        return False  # No se encontró el préstamo con el ID proporcionado

    def buscar_prestamo(self, id_prestamo):
        actual = self.cabeza
        while actual is not None:
            if actual.id_prestamo == id_prestamo:
                return actual  # Retorna el nodo del préstamo encontrado
            actual = actual.siguiente
        return None  # No se encontró el préstamo con el ID proporcionado
    def prestamos_por_usuario(self, id_usuario):
        prestamos_usuario = []
        actual = self.cabeza
        while actual is not None:
            if actual.id_usuario == id_usuario:
                prestamos_usuario.append(actual)
            actual = actual.siguiente
        return prestamos_usuario  # Retorna una lista de préstamos del usuario

    def actualizar_fecha(self, id_prestamo, nueva_fecha):
        nodo_prestamo = self.buscar_prestamo(id_prestamo)
        if nodo_prestamo is not None:
            nodo_prestamo.fecha_prestamo = nueva_fecha
            return True  # Fecha actualizada exitosamente
        return False  # No se encontró el préstamo con el ID proporcionado

    def listar_prestamos(self):
        prestamos = []
        actual = self.cabeza
        while actual is not None:
            prestamos.append(actual)
            actual = actual.siguiente
        return prestamos  # Retorna una lista de todos los préstamos registrados

    def mostrar_prestamos(self):
        if self.cabeza is None:
            print("No hay préstamos registrados.")
            return
        actual = self.cabeza
        while actual is not None:
            print(f"ID: {actual.id_prestamo}, Usuario: {actual.id_usuario}, Recurso: {actual.id_recurso}, Fecha: {actual.fecha_prestamo}")
            actual = actual.siguiente