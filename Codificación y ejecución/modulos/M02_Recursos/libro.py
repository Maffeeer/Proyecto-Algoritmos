#----------------------------------------
# Clase libro, herencia de clase recurso
#----------------------------------------

from .recurso import Recurso

class Libro(Recurso):

    def __init__(self, codigo, nombre, autor, isbn, añoPublicacion): # Atributos de clase libro

        # Llamar al constructor de la clase padre
        super().__init__(codigo, nombre)

        # Atributos específicos del libro
        self.autor = autor
        self.isbn = isbn
        self.añoPublicacion = añoPublicacion

    def obtenerTipo(self): # Retorna el tipo de recurso, en este caso libro
        return "Libro"

    def obtenerInfo(self): # Retorna la informacion del recurso
        return {
            'codigo': self.codigo,
            'tipo': self.obtenerTipo(),
            'nombre': self.nombre,
            'autor': self.autor,
            'isbn': self.isbn,
            'añoPublicacion': self.añoPublicacion,
            'estado': self.estado,
            'cantidadPrestamos': self.cantidadPrestamos,
            'fechaRegistro': self.fechaRegistro.strftime("%Y-%m-%d"),
            'disponible': self.esDisponible(),
        }

    def obtenerAutor(self): # retorna el autor
        return self.autor

    def obtenerIsbn(self): # retorna el ISBN
        return self.isbn

    def obtenerAño(self): # retorna el año de publicacion
        return self.añoPublicacion

    def __str__(self): # Ordena toda la informacion del recurso
        return f"Libro({self.codigo}: '{self.nombre}' by {self.autor}, ISBN {self.isbn}, {self.estado})"

    def __repr__(self):
        return f"Libro(codigo='{self.codigo}', nombre='{self.nombre}', autor='{self.autor}', isbn='{self.isbn}', año={self.añoPublicacion})"
