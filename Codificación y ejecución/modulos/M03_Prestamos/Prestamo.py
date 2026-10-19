from datetime import datetime

class Prestamo:

    def __init__(self, codigo, codigoUsuario, codigoRecurso, sede, fechaPrestamo=None, diasLimite=14):
        self.codigo = codigo
        self.codigoUsuario = codigoUsuario
        self.codigoRecurso = codigoRecurso
        self.sede = sede
        self.fechaPrestamo = fechaPrestamo if fechaPrestamo else datetime.now()
        self.diasLimite = diasLimite
        self.fechaDevolucion = None
        self.estado = "Activo"

    def devolver(self):
        self.fechaDevolucion = datetime.now()
        self.estado = "Devuelto"

    def reactivar(self):
        self.fechaDevolucion = None
        self.estado = "Activo"

    def diasAtraso(self, ahora=None):
        if self.estado != "Activo":
            return 0
        ahora = ahora if ahora else datetime.now()
        return max(0, (ahora - self.fechaPrestamo).days - self.diasLimite)

    def estaAtrasado(self, ahora=None):
        return self.diasAtraso(ahora) > 0

    def obtenerInfo(self):
        return {
            'codigo': self.codigo,
            'usuario': self.codigoUsuario,
            'recurso': self.codigoRecurso,
            'sede': self.sede,
            'fechaPrestamo': self.fechaPrestamo.strftime("%Y-%m-%d %H:%M"),
            'estado': self.estado,
            'atrasado': self.estaAtrasado(),
        }

    def __str__(self):
        return f"Prestamo({self.codigo}: {self.codigoUsuario} ← {self.codigoRecurso}, {self.estado})" 