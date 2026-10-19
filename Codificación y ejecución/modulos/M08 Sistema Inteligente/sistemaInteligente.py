#El sistema inteligente permite:
#1. Recomendaciones inteligentes (Motor IA basico)
#2. Calificaciones y reviews de los recursos
#3. Predicciones de disponibilidad de recursos
#4. Gamificacion (Badges, puntos, leaderboards)

from estructuras import VectorDinamico
from datetime import datetime, timedelta

class sistemaInteligente:

    def __init__(self):

        self.historialPrestamos = VectorDinamico()
        self.recomendacionesCache = {}  # Cache para recomendaciones

        self.calificaciones = vectorDinamico()  # Vector para almacenar calificaciones y reviews

        self.duracionPromedio = {}
        self.demandaxHora = {}

        self.usuariosGamificados = {}  # Diccionario para almacenar puntos y badges de usuarios