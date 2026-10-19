#----------------------------------------
# Clase sala, herencia de clase recurso
#----------------------------------------

from .recurso import Recurso


class Sala(Recurso):
    def __init__(self, codigo, nombre, capacidad, recursos_disponibles=None):
        super().__init__(codigo, nombre)
        self.capacidad = capacidad
        self.recursos_disponibles = recursos_disponibles if recursos_disponibles else []

    def obtener_tipo(self):
        return "Sala"

    def obtener_info(self):

        return {
            'codigo': self.codigo,
            'tipo': self.obtener_tipo(),
            'nombre': self.nombre,
            'capacidad': self.capacidad,
            'recursos': self.recursos_disponibles.copy(),
            'estado': self.estado,
            'cantidad_reservas': self.cantidad_prestamos,  # "Préstamos" = reservas en salas
            'fecha_registro': self.fecha_registro.strftime("%Y-%m-%d"),
            'disponible': self.es_disponible(),
        }

    def obtener_capacidad(self):
        return self.capacidad

    def obtener_recursos(self): # retorna la lista de salas disponibles
        return self.recursos_disponibles.copy()

    def agregar_recurso(self, recurso): # agrega un recurso a la sala
        if recurso not in self.recursos_disponibles:
            self.recursos_disponibles.append(recurso)

    def remover_recurso(self, recurso): # devuelve el recurso de la sala
        if recurso in self.recursos_disponibles:
            self.recursos_disponibles.remove(recurso)

    def tiene_recurso(self, recurso): # verifica que la sala esté vacia
        return recurso in self.recursos_disponibles

    def __str__(self):
        return f"Sala({self.codigo}: {self.nombre}, capacidad={self.capacidad}, recursos={len(self.recursos_disponibles)}, {self.estado})"

    def __repr__(self):
        return f"Sala(codigo='{self.codigo}', nombre='{self.nombre}', capacidad={self.capacidad})"
