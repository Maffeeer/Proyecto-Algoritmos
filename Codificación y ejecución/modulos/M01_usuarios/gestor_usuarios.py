from estructuras import VectorDinamico
from .usuario import Usuario

class GestorUsuarios:
    def __init__(self):
        self.usuarios = VectorDinamico(capacidadInicial=10)
        self.contadorCodigos = 0
        self.codigosUsados = set()

    def registrar(self, nombre, email):
        #validar entrada
        if not nombre or (isinstance(nombre, str) and not nombre.strip()):
            raise ValueError("El nombre no puede estar vacío.")
        if not email or (isinstance(email, str) and not email.strip()):
            raise ValueError("El email no puede estar vacío.")

        #generar un código único para el usuario
        self.contadorCodigos += 1
        codigo = f"U{self.contadorCodigos:03d}"  # Formato: U001, U002, etc.

        #crear un nuevo usuario
        usuario = Usuario(codigo, nombre, email)

        #almacenar el usuario en el vector dinámico
        self.usuarios.agregar(usuario)
        self.codigosUsados.add(codigo)

        return codigo  # Devolver el código del usuario registrado

    def buscarUsuario(self, codigo):
        #busqueda lineal en el vector dinámico
        usuariosLista = self.usuarios.recorrer()
        for usuario in usuariosLista:
            if usuario.codigo == codigo:
                return usuario
        return None  # Devolver None si no se encuentra el usuario

    def actualizar(self, codigo, nuevoEmail):
        usuario = self.buscarUsuario(codigo)
        if usuario:
            usuario.email = nuevoEmail
            return True  # Actualización exitosa
        return False  # Usuario no encontrado

    def darDeBaja(self, codigo):
        usuario = self.buscarUsuario(codigo)
        if usuario:
            if usuario.cantidadPrestamos > 0:
                raise ValueError(f"No se puede dar de baja al usuario {codigo}: tiene {usuario.cantidadPrestamos} préstamos activos.")
            usuario.darDeBaja()
            return True  # Baja exitosa
        return False  # Usuario no encontrado

    def reactivar(self, codigo):
        usuario = self.buscarUsuario(codigo)
        if usuario and not usuario.esActivo():
            usuario.reactivar()
            return True  # Reactivación exitosa
        return False  # Usuario no encontrado o ya activo

    def listarTodos(self):
        return self.usuarios.recorrer()  # Devolver la lista de todos los usuarios

    def listarActivos(self):
        todos = self.usuarios.recorrer()
        return [u for u in todos if u.esActivo()]  # Devolver solo los usuarios activos

    def codigoExiste(self, codigo):
        return codigo in self.codigosUsados  

    def obtenerCantidad(self):
        return self.usuarios.obtenerTamaño()

    def obtenerCantidadActivos(self):
        return len(self.listarActivos())

    def limpiar(self):
        self.usuarios.limpiar()
        self.contadorCodigos = 0
        self.codigosUsados.clear()

    def __str__(self):
        activos = self.obtenerCantidadActivos()
        total = self.obtenerCantidad()
        return f"GestorUsuarios(total={total}, activos={activos})"
           
    