#----------------------------------------
# Clase equipo, herencia de clase recurso
#----------------------------------------

from .recurso import Recurso


class Equipo(Recurso):
    def __init__(self, codigo, nombre, tipoEquipo, modelo, ubicacion):
        super().__init__(codigo, nombre) 
        self.tipoEquipo = tipoEquipo
        self.modelo = modelo
        self.ubicacion = ubicacion

    def obtenerTipo(self): # Retorna el tipo de recurso 
        return "Equipo"

    def obtenerInfo(self): # Retorna toda la información del equipo
        return {
            'codigo': self.codigo,
            'tipo': self.obtenerTipo(),
            'nombre': self.nombre,
            'tipoEquipo': self.tipoEquipo,
            'modelo': self.modelo,
            'ubicacion': self.ubicacion,
            'estado': self.estado,
            'cantidadPrestamos': self.cantidadPrestamos,
            'fechaRegistro': self.fechaRegistro.strftime("%Y-%m-%d"),
            'disponible': self.esDisponible(),
        }

    def obtenerTipoEquipo(self): # Retorna el tipo de equipo
        return self.tipoEquipo

    def obtenerModelo(self):
        return self.modelo

    def obtenerUbicacion(self):
        return self.ubicacion

    def cambiarUbicacion(self, nuevaUbicacion):
        self.ubicacion = nuevaUbicacion

    def __str__(self):
        return f"Equipo({self.codigo}: {self.nombre} ({self.tipoEquipo} {self.modelo}), {self.estado}, en {self.ubicacion})"

    def __repr__(self):
        return f"Equipo(codigo='{self.codigo}', nombre='{self.nombre}', tipo='{self.tipoEquipo}', modelo='{self.modelo}')"
