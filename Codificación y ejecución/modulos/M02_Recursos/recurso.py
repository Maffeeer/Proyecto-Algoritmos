#----------------------------------------
# Clase recurso
#----------------------------------------
# define los atributos en común para todos los recursos y sus metodos

from datetime import datetime
from abc import ABC, abstractmethod

class Recurso(ABC):
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre
        self.fechaRegistro = datetime.now()
        self.estado = "Disponible"
        self.cantidadPrestamos = 0

    @abstractmethod
    def obtenerTipo(self): # retorna el tipo de recurso
        pass

    @abstractmethod
    def obtenerInfo(self): # retorna toda la información de cada recurso
        pass

    def esDisponible(self): # verifica si el recurso está disponible
        return self.estado == "Disponible"

    def marcarNoDisponible(self): # en caso de no estar disponible, lo marca como no disponible en el estado
        self.estado = "No disponible"

    def marcarDisponible(self): # marca el estado del recruso como disponible
        self.estado = "Disponible"

    def registrarPrestamo(self): # registra el prestamo del recurso
        self.cantidadPrestamos += 1

    def darDeBaja(self): # En caso de eliminar un recurso, se da de baja
        self.estado = "Dado de baja"

    def reactivar(self): # Reactiva un recurso dado de baja
        self.estado = "Disponible"

    def obtenerEstado(self): # retorna el estado del recurso
        return self.estado

    def obtenerCantidadPrestamos(self): # retorna el numero de prestamos
        return self.cantidadPrestamos

    def __str__(self): # presenta la informacion del recurso
        return f"{self.obtenerTipo()}({self.codigo}: {self.nombre}, {self.estado})"

    def __repr__(self):
        return f"{self.__class__.__name__}(codigo='{self.codigo}', nombre='{self.nombre}', estado='{self.estado}', prestamos={self.cantidadPrestamos})"

    def __eq__(self, otro):
        if isinstance(otro, Recurso):
            return self.codigo == otro.codigo
        return False
