#El sistema inteligente permite:
#1. Recomendaciones inteligentes (Motor IA basico)
#2. Calificaciones y reviews de los recursos
#3. Predicciones de disponibilidad de recursos
#4. Gamificacion (Badges, puntos, leaderboards)

from estructuras import VectorDinamico
from datetime import datetime, timedelta

class sistemaInteligente:

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
        """Registra préstamo para análisis de recomendaciones."""
        self.historialPrestamos.agregar((usuarioCodigo, recursoCodigo, datetime.now()))
        if usuarioCodigo in self.recomendacionesCache:
            del self.recomendacionesCache[usuarioCodigo]

