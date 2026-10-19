#----------------------------------------
# Clase equipo, herencia de clase recurso
#----------------------------------------

from .recurso import Recurso


class Equipo(Recurso):
    def __init__(self, codigo, nombre, tipo_equipo, modelo, ubicacion):
        super().__init__(codigo, nombre) 
        self.tipo_equipo = tipo_equipo
        self.modelo = modelo
        self.ubicacion = ubicacion

    def obtener_tipo(self): # Retorna el tipo de recurso 
        return "Equipo"

    def obtener_info(self): # Retorna toda la información del equipo
        return {
            'codigo': self.codigo,
            'tipo': self.obtener_tipo(),
            'nombre': self.nombre,
            'tipo_equipo': self.tipo_equipo,
            'modelo': self.modelo,
            'ubicacion': self.ubicacion,
            'estado': self.estado,
            'cantidad_prestamos': self.cantidad_prestamos,
            'fecha_registro': self.fecha_registro.strftime("%Y-%m-%d"),
            'disponible': self.es_disponible(),
        }

    def obtener_tipo_equipo(self): # Retorna el tipo de equipo
        return self.tipo_equipo

    def obtener_modelo(self):
        return self.modelo

    def obtener_ubicacion(self):
        return self.ubicacion

    def cambiar_ubicacion(self, nueva_ubicacion):
        self.ubicacion = nueva_ubicacion

    def __str__(self):
        return f"Equipo({self.codigo}: {self.nombre} ({self.tipo_equipo} {self.modelo}), {self.estado}, en {self.ubicacion})"

    def __repr__(self):
        return f"Equipo(codigo='{self.codigo}', nombre='{self.nombre}', tipo='{self.tipo_equipo}', modelo='{self.modelo}')"
