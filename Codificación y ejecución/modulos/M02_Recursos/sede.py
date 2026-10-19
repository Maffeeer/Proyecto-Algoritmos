# Sede para conocer la ubicación de recursos

class Sede:

    def __init__(self, codigo, nombre):

        self.codigo = codigo
        self.nombre = nombre
        self.conectada = True

    def __str__(self):
        return f"Sede({self.codigo}: {self.nombre})"

    def __repr__(self):
        return self.__str__()
