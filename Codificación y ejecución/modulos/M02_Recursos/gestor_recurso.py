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
from modulos.M07_Inventario import GestorInventario


class GestorRecursos:
    def __init__(self, numSedes=10):
        self.recursos = VectorDinamico(capacidadInicial=20) # 20 recursos iniciales
        self.indice = TablaHash(tamaño=100)  # Búsqueda O(1) por código
        self.contadorCodigos = 0
        self.codigosUsados = set()
        self.sedes = TablaHash(tamaño=50)
        self.contadorSedes = 0
        self.inventario = GestorInventario(numSedes=numSedes, numRecursos=100)

    def _generarCodigo(self): # Genera un codigo unico para cada recurso
        self.contadorCodigos += 1
        codigo = f"R{self.contadorCodigos:04d}"
        self.codigosUsados.add(codigo)
        return codigo

    def registrarLibro(self, nombre, autor, isbn, añoPublicacion): # Registra un nuevo libro, herencia de recurso
        codigo = self._generarCodigo()
        libro = Libro(codigo, nombre, autor, isbn, añoPublicacion) 
        self.recursos.agregar(libro)
        self.indice.insertar(codigo, libro)  # Indexar para búsqueda O(1)
        return codigo

    def registrarEquipo(self, nombre, tipoEquipo, modelo, ubicacion): # Registra un nuevo equipo, herencia de recurso
        codigo = self._generarCodigo()
        equipo = Equipo(codigo, nombre, tipoEquipo, modelo, ubicacion)
        self.recursos.agregar(equipo)
        self.indice.insertar(codigo, equipo)  
        return codigo

    def registrarSala(self, nombre, capacidad, recursosDisponibles=None): # Registra una nueva sala, herencia de recurso
        codigo = self._generarCodigo()
        sala = Sala(codigo, nombre, capacidad, recursosDisponibles)
        self.recursos.agregar(sala)
        self.indice.insertar(codigo, sala)  
        return codigo

    def buscarxCodigo(self, codigo): # Busca el recurso por su codigo
        return self.indice.buscar(codigo)

    def darDeBaja(self, codigo): # Desactiva un recurso
        recurso = self.buscarxCodigo(codigo)
        if recurso:
            recurso.darDeBaja()
            return True
        return False

    def listarTodos(self): # Lista de todos los recursos
        return self.recursos.recorrer()

    def listarxTipo(self, tipo): # Obtiene recursos de un tipo especifico, como equipo
        todos = self.recursos.recorrer()
        return [r for r in todos if r.obtenerTipo() == tipo]

    def obtenerCantidad(self): # Da la cantidad total 
        return self.recursos.obtenerTamaño()

    # ─── GESTIÓN DE SEDES ───

    def registrarSede(self, indiceFila, nombre):
        
        codigo = f"S{indiceFila:03d}"
        sede = Sede(codigo, nombre)
        self.sedes.insertar(codigo, sede)
        self.contadorSedes += 1
        # Registrar sede en inventario
        self.inventario.registrarSede(indiceFila, nombre)
        return nombre

    def obtenerSede(self, codigo): # Busca la sede por su codigo

        return self.sedes.buscar(codigo)

    def obtenerCantidadSedes(self): # Conocer la cantidad de sedes

        return self.contadorSedes

    def listarSedes(self): # Muestra todas las sedes registradas

        sedes = []
        for codigo in self.sedes.obtenerTodasLasClaves():
            sede = self.sedes.buscar(codigo)
            if sede is not None:
                sedes.append(sede)
        return sedes

    # ─── GESTIÓN DE DISPONIBILIDAD  ───

    def registrarRecursoEnInventario(self, codigoRecurso): # Registra un recurso en el modulo inventarios
        recurso = self.buscarxCodigo(codigoRecurso)
        if recurso:
            self.inventario.registrarRecurso(codigoRecurso, recurso.nombre)
            return True
        return False

    def actualizarDisponibilidad(self, codigoRecurso, sede, cantidad): # Actualzia la cantidad del recurso por sede
        self.registrarRecursoEnInventario(codigoRecurso)
        return self.inventario.actualizar(codigoRecurso, sede, cantidad)

    def obtenerDisponibilidad(self, codigoRecurso, sede): # Obtiene la disponibilidad del recurso por sede
        return self.inventario.obtenerDisponibilidad(codigoRecurso, sede)

    def decrementarDisponibilidad(self, codigoRecurso, sede): # Actualiza la disponibilidad despues de un prestamo
        return self.inventario.decrementar(codigoRecurso, sede)

    def incrementarDisponibilidad(self, codigoRecurso, sede): # Actualzia la disponibilidad despues de una devolución
        return self.inventario.incrementar(codigoRecurso, sede)

    def __str__(self):
        libros = len(self.listarxTipo("Libro"))
        equipos = len(self.listarxTipo("Equipo"))
        salas = len(self.listarxTipo("Sala"))
        return f"GestorRecursos(libros={libros}, equipos={equipos}, salas={salas})"
