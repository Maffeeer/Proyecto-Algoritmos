from datetime import datetime

class Usuario:
    def __init__(self, codigo, nombre, email):
        self.codigo = codigo
        self.nombre = nombre
        self.email = email
        self.fechaRegistro = datetime.now()
        self.estado = "Activo"
        self.cantidadPrestamos = 0
        self.historialPrestamos = []

    def registrar_prestamo(self, codigoPrestamo):
        if codigoPrestamo not in self.historialPrestamos:
            self.historialPrestamos.append(codigoPrestamo)
            self.cantidadPrestamos += 1

    def devolver_prestamo(self, codigoPrestamo):
        if codigoPrestamo in self.historialPrestamos:
            self.historialPrestamos.remove(codigoPrestamo)
            self.cantidadPrestamos = max(0, self.cantidadPrestamos - 1)
            return True
        return False

    def actualizar_email(self, nuevoEmail):
        self.email = nuevoEmail

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
            "fecha_registro": self.fechaRegistro,
            "estado": self.estado,
            "cantidad_prestamos": self.cantidadPrestamos,
            "historial_prestamos": self.historialPrestamos
        }

    def __str__(self):
        return f"Usuario({self.codigo}: {self.nombre}, {self.email}, {self.estado})"

    def __repr__(self):
        return f"Usuario(codigo='{self.codigo}', nombre='{self.nombre}', email='{self.email}', estado='{self.estado}', prestamos={self.cantidadPrestamos})"

    def __eq__(self, otro):
        if isinstance(otro, Usuario):
            return self.codigo == otro.codigo
        return False

    