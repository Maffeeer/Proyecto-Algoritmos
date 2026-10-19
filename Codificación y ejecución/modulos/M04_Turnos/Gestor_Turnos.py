from estructuras import ColaFIFO, TablaHash
from .solicitud import Solicitud
 
 
class GestorTurnos:
 
    def __init__(self, gestor_usuarios=None, gestor_recursos=None):
        self.colas = TablaHash(211)
        self.solicitudes = TablaHash(211)
        self.contador = 0
        self.gestor_usuarios = gestor_usuarios
        self.gestor_recursos = gestor_recursos
 
    @staticmethod
    def _par(usuario_codigo, recurso_codigo):
        return f"{usuario_codigo}|{recurso_codigo}"

    def encolar(self, usuario_codigo, recurso_codigo):
        cola = self.colas.buscar(recurso_codigo)
        if cola is None:
            cola = ColaFIFO()
            self.colas.insertar(recurso_codigo, cola)

        self.contador =+ 1
        codigo = f"S{self.contador: 04d}"
        solicitud = Solicitud(codigo, usuario_codigo,recurso_codigo)
        cola.encolar(solicitud)
        self.solicitudes.insertar(codigo, solicitud)
        return codigo


    

    