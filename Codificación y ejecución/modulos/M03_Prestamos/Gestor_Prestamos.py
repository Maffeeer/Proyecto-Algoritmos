from estructuras import VectorDinamico, ListaSimple, ListaDoble, Pila, TablaHash
from .Prestamo import Prestamo


def _num(codigo):
    return int(str(codigo)[1:])

class SinUnidadesError(ValueError):
    pass


class GestorPrestamos:
 
    def __init__(self, gestorTurnos=None, gestorUsuarios=None, gestorRecursos=None):
        self.prestamos = VectorDinamico(capacidadInicial=50)
        self.historialSimple = ListaSimple()
        self.historialDoble = ListaDoble()
        self.pilaDeshacer = Pila()
        self.contadorCodigos = 0
        self.gestorTurnos = gestorTurnos
        self.gestorUsuarios = gestorUsuarios
        self.gestorRecursos = gestorRecursos
        self.indiceCodigo = TablaHash(211)
        self.recursosActivos = TablaHash(211)
 
    def _indexarActivo(self, p):
        n = self.recursosActivos.buscar(p.recurso_codigo)
        if n is None:
            n = 0
        self.recursosActivos.insertar(p.recurso_codigo, n + 1)

    def _desindexarActivo(self, p):
        n = self.recursosActivos.buscar(p.recurso_codigo)
        if n is None:
            n = 0
        if n <= 1:
            self.recursosActivos.eliminar(p.recurso_codigo)
        else:
            self.recursosActivos.insertar(p.recurso_codigo, n - 1)
 
    def recursoPrestado(self, codigoRecurso):
        return self.recursosActivos.buscar(codigoRecurso) is not None
 
    def registrarPrestamo(self, codigoUsuario, codigoRecurso, sede,
                           fechaPrestamo=None, diasLimite=14, _solicitud=None):
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
 
            sedes = self.gestorRecursos.listarSedes()
            sedeExiste = any(s.nombre == sede for s in sedes)
            if not sedeExiste:
                raise ValueError(f"Sede '{sede}' no existe")
 
            if not self.gestorRecursos.decrementarDisponibilidad(codigoRecurso, sede):
                raise SinUnidadesError(f"Sin unidades disponibles de {codigoRecurso} en {sede}")
            
        self.contadorCodigos += 1
        codigo = f"P{self.contadorCodigos:04d}"
        prestamo = Prestamo(codigo, codigoUsuario, codigoRecurso, sede,
                            fechaPrestamo, diasLimite)
 
        self.prestamos.agregar(prestamo)
        self.historialSimple.agregarAlFinal(prestamo)
        self.historialDoble.agregarAlFinal(prestamo)
        self.indiceCodigo.insertar(codigo, prestamo)
        self._indexarActivo(prestamo)
 
        if self.gestorUsuarios:
            usuario = self.gestorUsuarios.buscarUsuario(codigoUsuario)
            if usuario:
                usuario.registrarPrestamo(codigo)

        self.pilaDeshacer.push({
            'operacion': 'registrar_prestamo',
            'prestamo': prestamo,
            'solicitud': _solicitud,
        })
        return codigo

    def registrarDevolucion(self, codigoPrestamo):
        p = self.indiceCodigo.buscar(codigoPrestamo)
        if p is None or p.estado != "Activo":
            return False
        p.devolver()
        self._desindexarActivo(p)
 
        if self.gestorRecursos:
            self.gestorRecursos.incrementarDisponibilidad(p.recurso_codigo, p.sede)
 
        if self.gestorUsuarios:
            usuario = self.gestorUsuarios.buscarUsuario(p.usuario_codigo)
            if usuario:
                usuario.devolverPrestamo(codigoPrestamo)

        self.pilaDeshacer.push({'operacion': 'registrarDevolucion', 'prestamo': p})
 
        if self.gestorTurnos and self.gestorTurnos.obtenerCantidadEspera(p.recurso_codigo) > 0:
            try:
                asignado = self.atenderSiguienteTurno(p.recurso_codigo, p.sede)
            except ValueError:
                asignado = None
            if asignado:
                return asignado
        return True

    def deshacer(self):
        op = self.pilaDeshacer.pop()
        if op is None:
            return False
 
        p = op['prestamo']
        if op['operacion'] == 'registrarPrestamo':
            if p.estado == "Activo":
                self._desindexarActivo(p)
                if self.gestorRecursos:
                    self.gestorRecursos.incrementarDisponibilidad(p.recurso_codigo, p.sede)
            self.indiceCodigo.eliminar(p.codigo)
 
            if self.gestorUsuarios:
                usuario = self.gestorUsuarios.buscarUsuario(p.usuario_codigo)
                if usuario:
                    usuario.devolverPrestamo(p.codigo)
 
            restantes = [x for x in self.prestamos.recorrer() if x is not p]
            self.prestamos = VectorDinamico(capacidadInicial=50)
            self.historialSimple = ListaSimple()
            self.historialDoble = ListaDoble()
            for x in restantes:
                self.prestamos.agregar(x)
                self.historialSimple.agregarAlFinal(x)
                self.historialDoble.agregarAlFinal(x)
            if _num(p.codigo) == self.contadorCodigos:
                self.contadorCodigos -= 1
 
            solicitud = op.get('solicitud')
            if solicitud is not None and self.gestorTurnos:
                self.gestorTurnos.reinsertarAlFrente(solicitud)
        elif op['operacion'] == 'registrarDevolucion':
            if self.gestorRecursos and not self.gestorRecursos.decrementarDisponibilidad(p.recurso_codigo, p.sede):
                self.pilaDeshacer.push(op)
                raise ValueError(f"No se puede deshacer la devolucion de {p.codigo}: "
                                 f"no quedan unidades de {p.recurso_codigo} en {p.sede}")
            p.reactivar()
            self._indexarActivo(p)
 
            if self.gestorUsuarios:
                usuario = self.gestorUsuarios.buscarUsuario(p.usuario_codigo)
                if usuario:
                    usuario.registrarPrestamo(p.codigo)
        return True

    def atenderSiguienteTurno(self, codigoRecurso, sede):
        if self.gestorTurnos is None:
            raise ValueError("GestorPrestamos no tiene GestorTurnos asociado")
        while True:
            sol = self.gestorTurnos.obtenerSiguiente(codigoRecurso)
            if sol is None:
                return None
            if self.gestorUsuarios:
                usuario = self.gestorUsuarios.buscarUsuario(sol.codigoUsuario)
                if usuario is None or not usuario.esActivo():
                    sol.cancelar()
                    continue
            try:
                return self.registrarPrestamo(sol.codigoUsuario, codigoRecurso, sede,
                                               _solicitud=sol)
            except ValueError:
                self.gestorTurnos.reinsertarAlFrente(sol)
                raise

    def listarActivos(self):
        activos = VectorDinamico(capacidadInicial=10)
        for i in range(self.prestamos.obtenerTamaño()):
            p = self.prestamos.obtener(i)
            if p.estado == "Activo":
                activos.agregar(p)
        return activos
 
    def buscarPrestamo(self, codigo):
        return self.indiceCodigo.buscar(codigo)
 
    def obtenerPrestamosUsuario(self, codigoUsuario):
        return [p for p in self.prestamos.recorrer()
                if p.usuario_codigo == codigoUsuario and p.estado == "Activo"]
 
    def obtenerPrestamosAtrasados(self, ahora=None):
        return [p for p in self.prestamos.recorrer() if p.esta_atrasado(ahora)]
 
    def obtenerPrestamosSede(self, sede):
        return [p for p in self.prestamos.recorrer() if p.sede == sede and p.estado == "Activo"]
 
    def listarTodos(self):
        return self.prestamos.recorrer()
 
    def obtenerCantidad(self):
        return self.prestamos.obtenerTamaño()
 
    def __str__(self):
        activos = len([p for p in self.prestamos.recorrer() if p.estado == "Activo"])
        return f"GestorPrestamos(total={self.obtenerCantidad()}, activos={activos})"
 
