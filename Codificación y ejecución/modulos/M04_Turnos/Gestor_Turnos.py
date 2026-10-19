from estructuras import ColaFIFO, TablaHash
from .Solicitud import Solicitud
 
 
class GestorTurnos:
 
    def __init__(self, gestorUsuarios=None, gestorRecursos=None):
        self.colas = TablaHash(211)
        self.solicitudes = TablaHash(211)
        self.contador = 0
        self.gestorUsuarios = gestorUsuarios
        self.gestorRecursos = gestorRecursos
 
    @staticmethod
    def _par(codigoUsuario, codigoRecurso):
        return f"{codigoUsuario}|{codigoRecurso}"

    def encolar(self, codigoUsuario, codigoRecurso):
        cola = self.colas.buscar(codigoRecurso)
        if cola is None:
            cola = ColaFIFO()
            self.colas.insertar(codigoRecurso, cola)

        self.contador += 1
        codigo = f"S{self.contador:04d}"
        solicitud = Solicitud(codigo, codigoUsuario, codigoRecurso)
        cola.encolar(solicitud)
        self.solicitudes.insertar(codigo, solicitud)
        return codigo

    def estaEnEspera(self, codigoUsuario, codigoRecurso):
        cola = self.colas.buscar(codigoRecurso)
        if cola is None:
            return False
        for sol in cola.recorrer():
            if sol.usuario_codigo == codigoUsuario:
                return True
        return False

    def solicitarTurno(self, codigoUsuario, codigoRecurso, sede):
        if self.gestorUsuarios:
            usuario = self.gestorUsuarios.buscarUsuario(codigoUsuario)
            if usuario is None:
                raise ValueError(f"Usuario {codigoUsuario} no existe")
            if not usuario.esActivo():
                raise ValueError(f"El usuario {codigoUsuario} esta inactivo")

        if self.gestorRecursos:
            recurso = self.gestorRecursos.buscarxCodigo(codigoRecurso)
            if recurso is None:
                raise ValueError(f"Recurso {codigoRecurso} no existe")
            if recurso.obtenerEstado() == "Dado de baja":
                raise ValueError(f"El recurso {codigoRecurso} esta dado de baja")
            sede_existe = any(s.nombre == sede for s in self.gestorRecursos.listarSedes())
            if not sede_existe:
                raise ValueError(f"Sede '{sede}' no existe")
            if self.gestorRecursos.obtenerDisponibilidad(codigoRecurso, sede) > 0:
                raise ValueError("Hay unidades disponibles: registre el préstamo")
 
        if self.estaEnEspera(codigoUsuario, codigoRecurso):
            raise ValueError(f"El usuario {codigoUsuario} ya esta en la fila de {codigoRecurso}")
 
        return self.encolar(codigoUsuario, codigoRecurso)

    def verSiguiente(self, codigoRecurso):
        cola = self.colas.buscar(codigoRecurso)
        if cola is None:
            return None
        return cola.frente()

    def obtenerSiguiente(self, codigoRecurso):
        cola = self.colas.buscar(codigoRecurso)
        if cola is None or cola.estaVacia():
            return None

        solicitud = cola.desecolar()
        if solicitud is not None:
            solicitud.otorgar()
        return solicitud

    def obtenerFila(self, codigoRecurso):
        cola = self.colas.buscar(codigoRecurso)
        if cola is None:
            return []
        return cola.recorrer()
 
    def obtenerCantidadEspera(self, codigoRecurso):
        cola = self.colas.buscar(codigoRecurso)
        if cola is None:
            return 0
        return cola.obtenerTamaño()

    def cancelarSolicitud(self, codigoSolicitud):
        solicitud = self.solicitudes.buscar(codigoSolicitud)
        if solicitud is None or solicitud.estado != "En espera":
            return False
 
        cola = self.colas.buscar(solicitud.codigoRecurso)
        if cola is not None:
            nuevaCola = ColaFIFO()
            for sol in cola.recorrer():
                if sol.codigo != codigoSolicitud:
                    nuevaCola.encolar(sol)
            self.colas.insertar(solicitud.codigoRecurso, nuevaCola)
 
        solicitud.cancelar()
        return True

    def reinsertarAlFrente(self, solicitud):
        cola = self.colas.buscar(solicitud.codigoRecurso)
        if cola is None:
            cola = ColaFIFO()
 
        nuevaCola = ColaFIFO()
        nuevaCola.encolar(solicitud)
        for sol in (cola.recorrer() if cola is not None else []):
            if sol.codigo != solicitud.codigo:
                nuevaCola.encolar(sol)
 
        self.colas.insertar(solicitud.codigoRecurso, nuevaCola)
        solicitud.reiniciar()

    def obtenerCantidad(self):
        total = 0
        for codigoRecurso in self.colas.obtenerTodasLasClaves():
            cola = self.colas.buscar(codigoRecurso)
            if cola is not None:
                total += cola.obtenerTamaño()
        return total

    def buscarSolicitud(self, codigo):
        return self.solicitudes.buscar(codigo)
 
    def __str__(self):
        cantidad = self.obtenerCantidad()
        return f"GestorTurnos(colas={len(self.colas.obtenerTodasLasClaves())}, en_espera={cantidad})"


    

    