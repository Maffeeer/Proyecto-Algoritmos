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

    def esta_en_espera(self, usuario_codigo, recurso_codigo):
        cola = self.colas.buscar(recurso_codigo)
        if cola is None:
            return False
        for sol in cola.recorrer():
            if sol.usuario_codigo == usuario_codigo:
                return True
        return False

    def solicitar_turno(self, usuario_codigo, recurso_codigo, sede):
        if self.gestor_usuarios:
            usuario = self.gestor_usuarios.buscar_por_codigo(usuario_codigo)
            if usuario is None:
                raise ValueError(f"Usuario {usuario_codigo} no existe")
            if not usuario.es_activo():
                raise ValueError(f"El usuario {usuario_codigo} esta inactivo")
 
        if self.gestor_recursos:
            recurso = self.gestor_recursos.buscar_por_codigo(recurso_codigo)
            if recurso is None:
                raise ValueError(f"Recurso {recurso_codigo} no existe")
            if recurso.obtener_estado() == "Dado de baja":
                raise ValueError(f"El recurso {recurso_codigo} esta dado de baja")
            sede_existe = any(s.nombre == sede for s in self.gestor_recursos.listar_sedes())
            if not sede_existe:
                raise ValueError(f"Sede '{sede}' no existe")
            if self.gestor_recursos.obtener_disponibilidad(recurso_codigo, sede) > 0:
                raise ValueError("Hay unidades disponibles: registre el préstamo")
 
        if self.esta_en_espera(usuario_codigo, recurso_codigo):
            raise ValueError(f"El usuario {usuario_codigo} ya esta en la fila de {recurso_codigo}")
 
        return self.encolar(usuario_codigo, recurso_codigo)



    

    