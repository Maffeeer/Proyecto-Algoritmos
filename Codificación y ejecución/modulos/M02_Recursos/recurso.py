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
        self.fecha_registro = datetime.now()
        self.estado = "Disponible"
        self.cantidad_prestamos = 0

    @abstractmethod
    def obtener_tipo(self): # retorna el tipo de recurso
        pass

    @abstractmethod
    def obtener_info(self): # retorna toda la información de cada recurso
        pass

    def es_disponible(self): # verifica si el recurso está disponible
        return self.estado == "Disponible"

    def marcar_no_disponible(self): # en caso de no estar disponible, lo marca como no disponible en el estado
        self.estado = "No disponible"

    def marcar_disponible(self): # marca el estado del recruso como disponible
        self.estado = "Disponible"

    def registrar_prestamo(self): # registra el prestamo del recurso
        self.cantidad_prestamos += 1

    def dar_de_baja(self): # En caso de eliminar un recurso, se da de baja
        self.estado = "Dado de baja"

    def reactivar(self): # Reactiva un recurso dado de baja
        self.estado = "Disponible"

    def obtener_estado(self): # retorna el estado del recurso
        return self.estado

    def obtener_cantidad_prestamos(self): # retorna el numero de prestamos
        return self.cantidad_prestamos

    def __str__(self): # presenta la informacion del recurso
        return f"{self.obtener_tipo()}({self.codigo}: {self.nombre}, {self.estado})"

    def __repr__(self):
        return f"{self.__class__.__name__}(codigo='{self.codigo}', nombre='{self.nombre}', estado='{self.estado}', prestamos={self.cantidad_prestamos})"

    def __eq__(self, otro):
        if isinstance(otro, Recurso):
            return self.codigo == otro.codigo
        return False
