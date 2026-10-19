from datetime import datetime

class Usuario:
    def __init__(self, codigo, nombre, email):
        self.codigo = codigo
        self.nombre = nombre
        self.email = email
        self.fecha_registro = datetime.now()
        self.estado = "Activo"
        self.cantidad_prestamos = 0
        self.historial_prestamos = []

    def registrar_prestamo(self, codigo_prestamo):
        if codigo_prestamo not in self.historial_prestamos:
            self.historial_prestamos.append(codigo_prestamo)
            self.cantidad_prestamos += 1

    def devolver_prestamo(self, codigo_prestamo):
        if codigo_prestamo in self.historial_prestamos:
            self.historial_prestamos.remove(codigo_prestamo)
            self.cantidad_prestamos = max(0, self.cantidad_prestamos - 1)
            return True
        return False

    def actualizar_email(self, nuevo_email):
        self.email = nuevo_email

    def dar_de_baja(self):
        self.estado = "Inactivo"

    def reactivar(self):
        self.estado = "Activo"

    def es_activo(self):
        return self.estado == "Activo"

    def obtener_informacion(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "email": self.email,
            "fecha_registro": self.fecha_registro,
            "estado": self.estado,
            "cantidad_prestamos": self.cantidad_prestamos,
            "historial_prestamos": self.historial_prestamos
        }

    def __str__(self):
        return f"Usuario({self.codigo}: {self.nombre}, {self.email}, {self.estado})"

    def __repr__(self):
        return f"Usuario(codigo='{self.codigo}', nombre='{self.nombre}', email='{self.email}', estado='{self.estado}', prestamos={self.cantidad_prestamos})"

    def __eq__(self, otro):
        if isinstance(otro, Usuario):
            return self.codigo == otro.codigo
        return False

    