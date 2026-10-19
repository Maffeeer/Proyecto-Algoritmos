from estructuras import VectorDinamico, ListaSimple, ListaDoble, Pila, TablaHash
from .prestamo import Prestamo


def _num(codigo):
    return int(str(codigo)[1:])

class SinUnidadesError(ValueError):
    pass


class GestorPrestamos:
 
    def __init__(self, gestor_turnos=None, gestor_usuarios=None, gestor_recursos=None):
        self.prestamos = VectorDinamico(capacidad_inicial=50)
        self.historial_simple = ListaSimple()
        self.historial_doble = ListaDoble()
        self.pila_deshacer = Pila()
        self.contador_codigos = 0
        self.gestor_turnos = gestor_turnos
        self.gestor_usuarios = gestor_usuarios
        self.gestor_recursos = gestor_recursos
        self.indice_codigo = TablaHash(211)
        self.recursos_activos = TablaHash(211)
 
    def _indexar_activo(self, p):
        n = self.recursos_activos.buscar(p.recurso_codigo)
        if n is None:
            n = 0
        self.recursos_activos.insertar(p.recurso_codigo, n + 1)
 
    def _desindexar_activo(self, p):
        n = self.recursos_activos.buscar(p.recurso_codigo)
        if n is None:
            n = 0
        if n <= 1:
            self.recursos_activos.eliminar(p.recurso_codigo)
        else:
            self.recursos_activos.insertar(p.recurso_codigo, n - 1)
 
    def recurso_prestado(self, recurso_codigo):
        return self.recursos_activos.buscar(recurso_codigo) is not None
 
    def registrar_prestamo(self, usuario_codigo, recurso_codigo, sede,
                           fecha_prestamo=None, dias_limite=14, _solicitud=None):
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
 
            sedes = self.gestor_recursos.listar_sedes()
            sede_existe = any(s.nombre == sede for s in sedes)
            if not sede_existe:
                raise ValueError(f"Sede '{sede}' no existe")
 
            if not self.gestor_recursos.decrementar_disponibilidad(recurso_codigo, sede):
                raise SinUnidadesError(f"Sin unidades disponibles de {recurso_codigo} en {sede}")
            
        self.contador_codigos += 1
        codigo = f"P{self.contador_codigos:04d}"
        prestamo = Prestamo(codigo, usuario_codigo, recurso_codigo, sede,
                            fecha_prestamo, dias_limite)
 
        self.prestamos.agregar(prestamo)
        self.historial_simple.agregar_al_final(prestamo)
        self.historial_doble.agregar_al_final(prestamo)
        self.indice_codigo.insertar(codigo, prestamo)
        self._indexar_activo(prestamo)
 
        if self.gestor_usuarios:
            usuario = self.gestor_usuarios.buscar_por_codigo(usuario_codigo)
            if usuario:
                usuario.registrar_prestamo(codigo)
 
        self.pila_deshacer.push({
            'operacion': 'registrar_prestamo',
            'prestamo': prestamo,
            'solicitud': _solicitud,
        })
        return codigo

    def registrar_devolucion(self, codigo_prestamo):
        p = self.indice_codigo.buscar(codigo_prestamo)
        if p is None or p.estado != "Activo":
            return False
        p.devolver()
        self._desindexar_activo(p)
 
        if self.gestor_recursos:
            self.gestor_recursos.incrementar_disponibilidad(p.recurso_codigo, p.sede)
 
        if self.gestor_usuarios:
            usuario = self.gestor_usuarios.buscar_por_codigo(p.usuario_codigo)
            if usuario:
                usuario.devolver_prestamo(codigo_prestamo)
 
        self.pila_deshacer.push({'operacion': 'registrar_devolucion', 'prestamo': p})
 
        if self.gestor_turnos and self.gestor_turnos.obtener_cantidad_espera(p.recurso_codigo) > 0:
            try:
                asignado = self.atender_siguiente_turno(p.recurso_codigo, p.sede)
            except ValueError:
                asignado = None
            if asignado:
                return asignado
        return True