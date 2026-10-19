#----------------------------------------
# Clase sala, herencia de clase recurso
#----------------------------------------

from .recurso import Recurso


class Sala(Recurso):
    def __init__(self, codigo, nombre, capacidad, recursosDisponibles=None):
        super().__init__(codigo, nombre)
        self.capacidad = capacidad
        self.recursosDisponibles = recursosDisponibles if recursosDisponibles else []

    def obtenerTipo(self):
        return "Sala"

    def obtenerInfo(self):

        return {
            'codigo': self.codigo,
            'tipo': self.obtenerTipo(),
            'nombre': self.nombre,
            'capacidad': self.capacidad,
            'recursos': self.recursosDisponibles.copy(),
            'estado': self.estado,
            'cantidadReservas': self.cantidadPrestamos,  # "Préstamos" = reservas en salas
            'fechaRegistro': self.fechaRegistro.strftime("%Y-%m-%d"),
            'disponible': self.esDisponible(),
        }

    def obtenerCapacidad(self):
        return self.capacidad

    def obtenerRecursos(self): # retorna la lista de salas disponibles
        return self.recursosDisponibles.copy()

    def agregarRecurso(self, recurso): # agrega un recurso a la sala
        if recurso not in self.recursosDisponibles:
            self.recursosDisponibles.append(recurso)

    def removerRecurso(self, recurso): # devuelve el recurso de la sala
        if recurso in self.recursosDisponibles:
            self.recursosDisponibles.remove(recurso)

    def tieneRecurso(self, recurso): # verifica que la sala esté vacia
        return recurso in self.recursosDisponibles

    def __str__(self):
        return f"Sala({self.codigo}: {self.nombre}, capacidad={self.capacidad}, recursos={len(self.recursosDisponibles)}, {self.estado})"

    def __repr__(self):
        return f"Sala(codigo='{self.codigo}', nombre='{self.nombre}', capacidad={self.capacidad})"
