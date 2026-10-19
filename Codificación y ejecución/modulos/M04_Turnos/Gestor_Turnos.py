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