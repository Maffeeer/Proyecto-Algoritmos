from estructuras import VectorDinamico
from .usuario import Usuario

class GestorUsuarios:
    def __init__(self):
        self.usuarios = VectorDinamico(capacidad_inicial=10)
        self.contadorCodigos = 0
        self.codigosUsados = set()

    def refistrar(self, nombre, email):
        #validar entrada
        if not nombre or (isinstance(nombre, str) and nombre.strip()):
            raise ValueError("El nombre no puede estar vacío.")
        if not email or (isinstance(email, str) and email.strip()):
            raise ValueError("El email no puede estar vacío.")

        #generar un código único para el usuario
        self.contadorCodigos += 1
        codigo = f"U{self.contadorCodigos:03d}"  # Formato: U0001, U0002, etc.

        #crear un nuevo usuario
        usuario = Usuario(codigo, nombre, email)

        #almacenar el usuario en el vector dinámico
        self.usuarios.agregar(usuario)
        self.codigosUsados.add(codigo)

        return codigo  # Devolver el código del usuario registrado

    def buscar_usuario(self, codigo):
        #busqueda lineal en el vector dinámico
        usuariosLista = self.usuarios.recorrer()
        for usuario in usuariosLista:
            if usuario.codigo == codigo:
                return usuario
        return None  # Devolver None si no se encuentra el usuario

    def actualizar(self, codigo, nuevoEmail):
        usuario = self.buscar_usuario(codigo)
        if usuario:
            usuario.email = nuevoEmail
            return True  # Actualización exitosa
        return False  # Usuario no encontrado

    def dar_de_baja(self, codigo):
        usuario = self.buscar_usuario(codigo)
        if usuario:
            if usuario.cantidadPrestamos > 0:
                raise ValueError(f"No se puede dar de baja al usuario {codigo}: tiene {usuario.cantidadPrestamos} préstamos activos.")
            usuario.dar_de_baja()
            return True  # Baja exitosa
        return False  # Usuario no encontrado

    def reactivar(self, codigo):
        usuario = self.buscar_usuario(codigo)
        if usuario and not usuario.es_activo():
            usuario.reactivar()
            return True  # Reactivación exitosa
        return False  # Usuario no encontrado o ya activo

    def listar_todos(self):
        return self.usuarios.recorrer()  # Devolver la lista de todos los usuarios

    def listar_activos(self):
        todos = self.usuarios.recorrer()
        return [u for u in todos if u.es_activo()]  # Devolver solo los usuarios activos

    def codigo_existe(self, codigo):
        return codigo in self.codigosUsados  

    def obtener_cantidad(self):
        return self.usuarios.obtener_tamaño()

    def obtener_cantidad_activos(self):
        return len(self.listar_activos())

    def limpiar(self):
        self.usuarios.limpiar()
        self.contadorCodigos = 0
        self.codigosUsados.clear()

    def __str__(self):
        activos = self.obtener_cantidad_activos()
        total = self.obtener_cantidad()
        return f"GestorUsuarios(total={total}, activos={activos})"
           
    