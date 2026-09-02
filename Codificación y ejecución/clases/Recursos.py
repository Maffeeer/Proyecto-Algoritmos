# ==========================================
# 1. CLASE BASE
# ==========================================

class Recurso:
    # Se define la clase base Recurso, que representa un recurso genérico de la biblioteca.
    # Incluye atributos comunes como ID, nombre, cantidad total, cantidad disponible, categoría y sede asociada.
    def __init__(self, id_recurso: int, nombre: str, cantidad: int, categoria: str, sede: str):
        self.id_recurso = id_recurso
        self.nombre = nombre
        self.cantidad = cantidad
        self.cantidad_disponible = cantidad
        self.categoria = categoria
        self.sede = sede
        # Indica si el recurso está disponible para préstamo o no, basado en la cantidad disponible.
        self.estado = "disponible" if cantidad > 0 else "no disponible"
        # Contador de cuántas veces se ha prestado este recurso.
        self.contador_prestamos = 0

    # Registra la cantidad de unidades ocupadas del recurso.
    # Inicia en 1 por defecto ya que se asume que se está prestando al menos una unidad.
    # Usa booleano para indicar si la operación fue exitosa o no.
    def registrar_ocupacion(self, cantidad: int = 1) -> bool:
        # Si hay suficientes unidades disponibles, frente a la cantidad solicitada, se procede a registrar la ocupación.
        if self.cantidad_disponible >= cantidad:
            # Disminuye la cantidad disponible del recurso.
            self.cantidad_disponible -= cantidad
            # Actualiza el contador de préstamos del recurso.
            self.contador_prestamos += cantidad
            # Si la cantidad disponible es 0, se actualiza el estado del recurso a "no disponible".
            return True
        return False
        self.estado = "no disponible"

    # Registra la devolución de unidades prestadas.
    # Usa booleano para indicar si la operación fue exitosa o no.
    def registrar_devolucion(self, cantidad: int = 1) -> bool:
        # Si la cantidad disponible más la cantidad a devolver no excede la cantidad total del recurso, se procede a registrar la devolución.
        if self.cantidad_disponible + cantidad <= self.cantidad:
            # Aumenta la cantidad disponible del recurso.
            self.cantidad_disponible += cantidad
            # El estado del recurso se actualiza a "disponible".
            self.estado = "disponible"
            return True
        # Si la devolución excede la cantidad total del recurso, no se realiza la operación y se retorna False.
        return False

    # Se agrega un método para actualizar la cantidad total del recurso y disponibilidad.
    def actualizar_cantidad(self, nueva_unidad: int) -> bool:
        # Si la nueva cantidad es negativo, se vende o se descarta unidades.
        # Si la nueva cantidad es postivio, hubo compra y se incrementa la cantidad total y la cantidad disponible.
        if nueva_unidad != 0:
            # Evitar que la cantidad disponible sea negativa después de la actualización.
            if nueva_unidad < 0 and self.cantidad_disponible + nueva_unidad < 0:
                return False  # No se puede reducir más de lo disponible
            # Si la validación pasa, se actualiza la cantidad total y la cantidad disponible del recurso.
            self.cantidad += nueva_unidad
            self.cantidad_disponible += nueva_unidad
            # Actualiza el estado del recurso según la nueva cantidad disponible.
            self.estado = "disponible" if self.cantidad_disponible > 0 else "no disponible"
            return True
        # Si la nueva cantidad es cero, no se realiza ninguna operación y se retorna False.
        return False

    # Se define el método __str__ para proporcionar una representación legible del objeto Recurso al imprimirlo.
    def __str__(self):
        return (f"[{self.__class__.__name__}] ID: {self.id_recurso} | Nombre: {self.nombre} | "
                f"Disp: {self.cantidad_disponible}/{self.cantidad} | Sede: {self.sede} | Estado: {self.estado}")

# ==========================================
# 2. HERENCIA DE RECURSOS
# ==========================================
class Libro(Recurso):
    def __init__(self, id_recurso: int, nombre: str, cantidad: int, categoria: str, sede: str, autor: str):
        super().__init__(id_recurso, nombre, cantidad, categoria, sede)
        self.autor = autor


class Equipo(Recurso):
    def __init__(self, id_recurso: int, nombre: str, cantidad: int, categoria: str, sede: str, marca: str, tipo: str):
        super().__init__(id_recurso, nombre, cantidad, categoria, sede)
        self.marca = marca
        self.tipo = tipo


class Espacio(Recurso):
    def __init__(self, id_recurso: int, nombre: str, cantidad: int, categoria: str, sede: str, capacidad: int):
        super().__init__(id_recurso, nombre, cantidad, categoria, sede)
        self.capacidad = capacidad


# ==========================================
# 3. VECTOR DINÁMICO PROPIO DE RECURSOS
# ==========================================

# La clase VectorDinamicoRecursos implementa un vector dinámico para almacenar objetos de tipo Recurso.
class VectorDinamicoRecursos:

     # Se define la capacidad inicial del vector y se inicializa el tamaño actual y la lista de datos.
    def __init__(self, capacidad_inicial: int = 4):
        # self.capacidad se define como un parametro de entrad.
        self.capacidad = capacidad_inicial
        # self.tamano se define como un atributo de la clase, que representa el número actual de elementos en el vector.
        self.tamano = 0
        # Se inicializa la lista de datos con None para reservar espacio para los recursos.
        self.datos = [None] * self.capacidad

    # Se define un método privado para redimensionar el vector dinámico cuando se alcanza su capacidad máxima.
    def _redimensionar(self, nueva_capacidad: int):
        # Se crea un nuevo arreglo con la nueva capacidad.
        nuevo_arreglo = [None] * nueva_capacidad
        # Se copian los elementos existentes al nuevo arreglo.
        for i in range(self.tamano):
            nuevo_arreglo[i] = self.datos[i]
        # Se actualizan los atributos de la clase para reflejar la nueva capacidad y el nuevo arreglo de datos.
        self.datos = nuevo_arreglo
        self.capacidad = nueva_capacidad

    # Se define un método para buscar un recurso por su ID. Si se encuentra, se devuelve el objeto Recurso; de lo contrario, se devuelve None.
    def buscar_por_id(self, id_recurso: int) -> Recurso:
        # Recorre el verctor comprobando si el id_recurso coincide con el id de algún recurso almacenado. Si se encuentra, retorna el recurso; si no, retorna None.
        for i in range(self.tamano):
            # Si el id del recurso en la posición i coincide con el id_recurso buscado, se retorna el recurso correspondiente.
            if self.datos[i].id_recurso == id_recurso:
                return self.datos[i]
        return None

    # Se define un método para agregar un recurso al vector dinámico. Si el recurso ya existe (basado en su ID), se incrementa su cantidad; de lo contrario, se agrega como un nuevo recurso.
    def agregar_recurso(self, recurso: Recurso) -> bool:
        # Se busca si el recurso ya existe en el vector dinámico por su ID.
        existente = self.buscar_por_id(recurso.id_recurso)
        # Si el recurso no pertenece a la clase Recurso, se imprime un mensaje de error y se retorna False.
        if not isinstance(recurso, Recurso):
            print("Error: No se proporcionó un recurso válido.")
            return False
        if existente:
            # Se actualiza la cantidad del recurso existente sumando la cantidad del nuevo recurso.
            existente.actualizar_cantidad(existente.cantidad + recurso.cantidad)
            return True
        # Se comprueba si el vector dinámico ha alcanzado su capacidad máxima.
        if self.tamano == self.capacidad:
            # Como alcanza la capacidad máxima, se redimensiona el vector dinámico duplicando su capacidad.
            self._redimensionar(self.capacidad * 2)
        # Se agrega el nuevo recurso al vector dinámico y se incrementa el tamaño actual del vector.
        self.datos[self.tamano] = recurso
        self.tamano += 1
        return True

    # Se define un método para obtener la disponibilidad de un recurso por su ID. 
    def obtener_disponibilidad(self, id_recurso: int) -> int:
        # Se busca el recurso en el vector dinámico por su ID.
        recurso = self.buscar_por_id(id_recurso)
        # Si se encuentra el recurso, se devuelve su cantidad disponible; de lo contrario, se devuelve 0.
        return recurso.cantidad_disponible if recurso else 0

    # Se define un método para eliminar un recurso por su ID. Si se encuentra, se actualiza su estado y cantidad disponible; de lo contrario, se devuelve False.
    def eliminar(self, id_recurso: int) -> bool:
        for i in range(self.tamano):
            if self.datos[i].id_recurso == id_recurso:
                self.datos[i].estado = "dado de baja"
                self.datos[i].cantidad_disponible = 0
                return True
        return False

    def recorrer(self):
        if self.tamano == 0:
            print("No hay recursos registrados.")
            return
        for i in range(self.tamano):
            print(f"[{i}] {self.datos[i]}")