#----------------------------------------
# Clase gestorRecursos
#----------------------------------------
# Gestiona los recursos, su busqueda rapida e inventarios. 


from estructuras import VectorDinamico, TablaHash
from .recurso import Recurso
from .libro import Libro
from .equipo import Equipo
from .sala import Sala
from .sede import Sede
from modulos.M07_inventario import GestorInventario


class GestorRecursos:
    def __init__(self, num_sedes=10):
        self.recursos = VectorDinamico(capacidad_inicial=20) # 20 recursos iniciales
        self.indice = TablaHash(tamaño=100)  # Búsqueda O(1) por código
        self.contador_codigos = 0
        self.codigos_usados = set()
        self.sedes = TablaHash(tamaño=50)
        self.contador_sedes = 0
        self.inventario = GestorInventario(num_sedes=num_sedes, num_recursos=100)

    def _generar_codigo(self): # Genera un codigo unico para cada recurso
        self.contador_codigos += 1
        codigo = f"R{self.contador_codigos:04d}"
        self.codigos_usados.add(codigo)
        return codigo

    def registrar_libro(self, nombre, autor, isbn, año_publicacion): # Registra un nuevo libro, herencia de recurso
        codigo = self._generar_codigo()
        libro = Libro(codigo, nombre, autor, isbn, año_publicacion) 
        self.recursos.agregar(libro)
        self.indice.insertar(codigo, libro)  # Indexar para búsqueda O(1)
        return codigo

    def registrar_equipo(self, nombre, tipo_equipo, modelo, ubicacion): # Registra un nuevo equipo, herencia de recurso
        codigo = self._generar_codigo()
        equipo = Equipo(codigo, nombre, tipo_equipo, modelo, ubicacion)
        self.recursos.agregar(equipo)
        self.indice.insertar(codigo, equipo)  
        return codigo

    def registrar_sala(self, nombre, capacidad, recursos_disponibles=None): # Registra una nueva sala, herencia de recurso
        codigo = self._generar_codigo()
        sala = Sala(codigo, nombre, capacidad, recursos_disponibles)
        self.recursos.agregar(sala)
        self.indice.insertar(codigo, sala)  
        return codigo

    def buscar_por_codigo(self, codigo): # Busca el recurso por su codigo
        return self.indice.buscar(codigo)

    def dar_de_baja(self, codigo): # Desactiva un recurso
        recurso = self.buscar_por_codigo(codigo)
        if recurso:
            recurso.dar_de_baja()
            return True
        return False

    def listar_todos(self): # Lista de todos los recursos
        return self.recursos.recorrer()

    def listar_por_tipo(self, tipo): # Obtiene recursos de un tipo especifico, como equipo
        todos = self.recursos.recorrer()
        return [r for r in todos if r.obtener_tipo() == tipo]

    def obtener_cantidad(self): # Da la cantidad total 
        return self.recursos.obtener_tamaño()

    # ─── GESTIÓN DE SEDES ───

    def registrar_sede(self, indice_fila, nombre):
        
        codigo = f"S{indice_fila:03d}"
        sede = Sede(codigo, nombre)
        self.sedes.insertar(codigo, sede)
        self.contador_sedes += 1
        # Registrar sede en inventario
        self.inventario.registrar_sede(indice_fila, nombre)
        return nombre

    def obtener_sede(self, codigo): # Busca la sede por su codigo

        return self.sedes.buscar(codigo)

    def obtener_cantidad_sedes(self): # Conocer la cantidad de sedes

        return self.contador_sedes

    def listar_sedes(self): # Muestra todas las sedes registradas

        sedes = []
        for codigo in self.sedes.obtener_todas_las_claves():
            sede = self.sedes.buscar(codigo)
            if sede is not None:
                sedes.append(sede)
        return sedes

    # ─── GESTIÓN DE DISPONIBILIDAD  ───

    def registrar_recurso_en_inventario(self, codigo_recurso): # Registra un recurso en el modulo inventarios
        recurso = self.buscar_por_codigo(codigo_recurso)
        if recurso:
            self.inventario.registrar_recurso(codigo_recurso, recurso.nombre)
            return True
        return False

    def actualizar_disponibilidad(self, codigo_recurso, sede, cantidad): # Actualzia la cantidad del recurso por sede
        self.registrar_recurso_en_inventario(codigo_recurso)
        return self.inventario.actualizar(codigo_recurso, sede, cantidad)

    def obtener_disponibilidad(self, codigo_recurso, sede): # Obtiene la disponibilidad del recurso por sede
        return self.inventario.obtener_disponibilidad(codigo_recurso, sede)

    def decrementar_disponibilidad(self, codigo_recurso, sede): # Actualiza la disponibilidad despues de un prestamo
        return self.inventario.decrementar(codigo_recurso, sede)

    def incrementar_disponibilidad(self, codigo_recurso, sede): # Actualzia la disponibilidad despues de una devolución
        return self.inventario.incrementar(codigo_recurso, sede)

    def __str__(self):
        libros = len(self.listar_por_tipo("Libro"))
        equipos = len(self.listar_por_tipo("Equipo"))
        salas = len(self.listar_por_tipo("Sala"))
        return f"GestorRecursos(libros={libros}, equipos={equipos}, salas={salas})"
