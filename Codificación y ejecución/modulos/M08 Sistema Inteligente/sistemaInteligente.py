#El sistema inteligente permite:
#1. Recomendaciones inteligentes (Motor IA basico)
#2. Calificaciones y reviews de los recursos
#3. Predicciones de disponibilidad de recursos
#4. Gamificacion (Badges, puntos, leaderboards)

from estructuras import VectorDinamico
from datetime import datetime, timedelta

class SistemaInteligente:

    def __init__(self):

        # Historial de préstamos
        self.historialPrestamos = VectorDinamico()
        self.recomendacionesCache = {}  # Cache para recomendaciones

        # Calificaciones y reviews
        self.calificaciones = VectorDinamico()  # Vector para almacenar calificaciones y reviews

        # Predicciones de disponibilidad
        self.duracionPromedio = {}
        self.demandaxHora = {}

        # Gamificación
        self.usuariosGamificados = {}  # Diccionario para almacenar puntos y badges de usuarios

    # Registra un préstamo en el historial y actualiza la cache de recomendaciones
    def registrarPrestamoHist(self, codigoUsuario, codigoRecurso):
        self.historialPrestamos.agregar((codigoUsuario, codigoRecurso, datetime.now()))
        if codigoUsuario in self.recomendacionesCache:
            del self.recomendacionesCache[codigoUsuario]  # Invalidar cache de recomendaciones para este usuario

    # Recomendaciones inteligentes basadas en usuarios similares
    def recomendarRecursos(self, codigoUsuario, top_n=5):
        # Si ya hay recomendaciones en cache, devolverlas
        recursosUsuario = set()
        for i in range(self.historialPrestamos.obtenerTamaño()):
            user, recurso, _ = self.historialPrestamos.obtener(i)
            if user == codigoUsuario:
                recursosUsuario.add(recurso)

        usuariosUnicos = set()
        for i in range(self.historialPrestamos.obtenerTamaño()):
            user, _, _ = self.historialPrestamos.obtener(i)
            usuariosUnicos.add(user)

        recursosSugeridos = {}
        for otroUsuario in usuariosUnicos:
            if otroUsuario == codigoUsuario:
                continue

            recursosOtro = set()
            for i in range(self.historialPrestamos.obtenerTamaño()):
                user, recurso, _ = self.historialPrestamos.obtener(i)
                if user == otroUsuario:
                    recursosOtro.add(recurso)

            interseccion = len(recursosUsuario & recursosOtro)
            union = len(recursosUsuario | recursosOtro)
            similitud = interseccion / union if union > 0 else 0.0

            for recurso in recursosOtro:
                if recurso not in recursosUsuario:
                    if recurso not in recursosSugeridos:
                        recursosSugeridos[recurso] = 0
                    recursosSugeridos[recurso] += similitud

        recomendaciones = [(r, s, "Usuarios similares lo pidieron")
                          for r, s in recursosSugeridos.items()]
        recomendaciones.sort(key=lambda x: x[1], reverse=True)
        return recomendaciones[:top_n]

    # Registra una calificación (1-5 estrellas) para un recurso por un usuario
    def registrarCalificacion(self, codigoUsuario, codigoRecurso, estrellas, comentario=""):
        """Registra una calificación (1-5 estrellas)."""
        if not 1 <= estrellas <= 5:
            raise ValueError("Estrellas deben estar entre 1 y 5")

        self.calificaciones.agregar({
            'usuario': codigoUsuario,
            'recurso': codigoRecurso,
            'estrellas': estrellas,
            'comentario': comentario,
            'fecha': datetime.now()
        })

    # Obtiene el promedio de calificaciones para un recurso específico
    def registrarCalificacion(self, codigoUsuario, codigoRecurso, estrellas, comentario=""):
        if not 1 <= estrellas <= 5:
            raise ValueError("Estrellas deben estar entre 1 y 5")

        self.calificaciones.agregar({
            'usuario': codigoUsuario,
            'recurso': codigoRecurso,
            'estrellas': estrellas,
            'comentario': comentario,
            'fecha': datetime.now()
        })

    # Obtiene el promedio de calificaciones para un recurso específico
    def obtenerPromedioxRecurso(self, codigoRecurso):
        suma = 0
        cantidad = 0

        for i in range(self.calificaciones.obtenerTamaño()):
            cal = self.calificaciones.obtener(i)
            if cal['recurso'] == codigoRecurso:
                suma += cal['estrellas']
                cantidad += 1

        return suma / cantidad if cantidad > 0 else 0.0
