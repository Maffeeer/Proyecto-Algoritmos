#----------------------------------------
# Clase libro, herencia de clase recurso
#----------------------------------------

from .recurso import Recurso

class Libro(Recurso):

    def __init__(self, codigo, nombre, autor, isbn, año_publicacion): # Atributos de clase libro

        # Llamar al constructor de la clase padre
        super().__init__(codigo, nombre)

        # Atributos específicos del libro
        self.autor = autor
        self.isbn = isbn
        self.año_publicacion = año_publicacion

    def obtener_tipo(self): # Retorna el tipo de recurso, en este caso libro
        return "Libro"

    def obtener_info(self): # Retorna la informacion del recurso
        return {
            'codigo': self.codigo,
            'tipo': self.obtener_tipo(),
            'nombre': self.nombre,
            'autor': self.autor,
            'isbn': self.isbn,
            'año_publicacion': self.año_publicacion,
            'estado': self.estado,
            'cantidad_prestamos': self.cantidad_prestamos,
            'fecha_registro': self.fecha_registro.strftime("%Y-%m-%d"),
            'disponible': self.es_disponible(),
        }

    def obtener_autor(self): # retorna el autor
        return self.autor

    def obtener_isbn(self): # retorna el ISBN
        return self.isbn

    def obtener_año(self): # retorna el año de publicacion
        return self.año_publicacion

    def __str__(self): # Ordena toda la informacion del recurso
        return f"Libro({self.codigo}: '{self.nombre}' by {self.autor}, ISBN {self.isbn}, {self.estado})"

    def __repr__(self):
        return f"Libro(codigo='{self.codigo}', nombre='{self.nombre}', autor='{self.autor}', isbn='{self.isbn}', año={self.año_publicacion})"
