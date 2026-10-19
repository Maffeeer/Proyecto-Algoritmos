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

    def ver_siguiente(self, recurso_codigo):
        cola = self.colas.buscar(recurso_codigo)
        if cola is None:
            return None
        return cola.frente()

    def obtener_siguiente(self, recurso_codigo):
        cola = self.colas.buscar(recurso_codigo)
        if cola is None or cola.esta_vacia():
            return None

        solicitud = cola.desecolar()
        if solicitud is not None:
            solicitud.otorgar()
        return solicitud

    def obtener_fila(self, recurso_codigo):
        cola = self.colas.buscar(recurso_codigo)
        if cola is None:
            return []
        return cola.recorrer()
 
    def obtener_cantidad_espera(self, recurso_codigo):
        cola = self.colas.buscar(recurso_codigo)
        if cola is None:
            return 0
        return cola.obtener_tamaño()

    def cancelar_solicitud(self, codigo_solicitud):
        solicitud = self.solicitudes.buscar(codigo_solicitud)
        if solicitud is None or solicitud.estado != "En espera":
            return False
 
        cola = self.colas.buscar(solicitud.recurso_codigo)
        if cola is not None:
            nueva_cola = ColaFIFO()
            for sol in cola.recorrer():
                if sol.codigo != codigo_solicitud:
                    nueva_cola.encolar(sol)
            self.colas.insertar(solicitud.recurso_codigo, nueva_cola)
 
        solicitud.cancelar()
        return True

    def reinsertar_al_frente(self, solicitud):
        cola = self.colas.buscar(solicitud.recurso_codigo)
        if cola is None:
            cola = ColaFIFO()
 
        nueva_cola = ColaFIFO()
        nueva_cola.encolar(solicitud)
        for sol in (cola.recorrer() if cola is not None else []):
            if sol.codigo != solicitud.codigo:
                nueva_cola.encolar(sol)
 
        self.colas.insertar(solicitud.recurso_codigo, nueva_cola)
        solicitud.reiniciar()

    def obtener_cantidad(self):
        total = 0
        for recurso_codigo in self.colas.obtener_todas_las_claves():
            cola = self.colas.buscar(recurso_codigo)
            if cola is not None:
                total += cola.obtener_tamaño()
        return total

    def buscar_solicitud(self, codigo):
        return self.solicitudes.buscar(codigo)
 
    def __str__(self):
        cantidad = self.obtener_cantidad()
        return f"GestorTurnos(colas={len(self.colas.obtener_todas_las_claves())}, en_espera={cantidad})"


    

    