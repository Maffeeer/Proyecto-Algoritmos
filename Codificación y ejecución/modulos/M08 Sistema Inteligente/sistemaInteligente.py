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

    def registrarPrestamoHist(self, usuarioCodigo, recursoCodigo):
        self.historialPrestamos.agregar((usuarioCodigo, recursoCodigo, datetime.now()))
        if usuarioCodigo in self.recomendacionesCache:
            del self.recomendacionesCache[usuarioCodigo]

    def recomendarRecursos(self, usuarioCodigo, top_n=5):
        recursosUsuario = set()
        for i in range(self.historialPrestamos.obtenerTamaño()):
            user, recurso, _ = self.historialPrestamos.obtener(i)
            if user == usuarioCodigo:
                recursosUsuario.add(recurso)

        usuariosUnicos = set()
        for i in range(self.historialPrestamos.obtenerTamaño()):
            user, _, _ = self.historialPrestamos.obtener(i)
            usuariosUnicos.add(user)

        recursosSugeridos = {}
        for otroUsuario in usuariosUnicos:
            if otroUsuario == usuarioCodigo:
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


