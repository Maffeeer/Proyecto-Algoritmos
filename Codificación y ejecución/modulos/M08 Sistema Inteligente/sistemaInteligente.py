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

    # Obtiene el ranking de recursos basado en calificaciones y número de reviews
    def rankingRecursos(self, top_n=10):
        recursos = {}

        for i in range(self.calificaciones.obtenerTamaño()):
            cal = self.calificaciones.obtener(i)
            recurso = cal['recurso']
            if recurso not in recursos:
                recursos[recurso] = []
            recursos[recurso].append(cal['estrellas'])

        ranking = []
        for recurso, estrellasList in recursos.items():
            promedio = sum(estrellasList) / len(estrellasList)
            ranking.append((recurso, promedio, len(estrellasList)))

        ranking.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return ranking[:top_n]

    # Registra un préstamo finalizado para predicción de disponibilidad
    def registrarPrestamoFinalizado(self, codigoRecurso, fechaInicio, fechaFin):
        duracion = (fechaFin - fechaInicio).days
        if duracion < 0:
            duracion = 0

        if codigoRecurso not in self.duracionesPromedio:
            self.duracionesPromedio[codigoRecurso] = []
        self.duracionesPromedio[codigoRecurso].append(duracion)

        hora = fechaInicio.hour
        self.demandaxHora[hora] = self.demandaxHora.get(hora, 0) + 1

    # Predice la disponibilidad de un recurso basado en historial de préstamos
    def predecirDisponibilidad(self, codigoRecurso):
        if codigoRecurso not in self.duracionesPromedio:
            duracionProm = 3.0
            confianza = 0.0
        else:
            duraciones = self.duracionesPromedio[codigoRecurso]
            duracionProm = sum(duraciones) / len(duraciones)
            confianza = min(len(duraciones) / 10.0, 1.0)

        fechaEstimada = datetime.now() + timedelta(days=duracionProm)

        return {
            'fechaEstimada': fechaEstimada,
            'diasEstimados': int(duracionProm),
            'confianza': confianza,
            'mensaje': f"Disponible en ~{int(duracionProm)} días ({int(confianza*100)}% confianza)"
        }

    # Gamificación: Inicializa un usuario con sistema de gamificación
    def crearUsuarioGamificado(self, codigoUsuario):
        self.usuariosGamificados[codigoUsuario] = {
            'puntos': 0,
            'nivel': 1,
            'badges': set(),
            'prestamos': 0,
            'devolucionesTiempo': 0
        }

    # Gamificación: Agrega puntos a un usuario y actualiza su nivel
    def agregar_puntos(self, codigoUsuario, cantidad):
        """Agrega puntos a usuario y actualiza nivel."""
        if codigoUsuario not in self.usuariosGamificados:
            self.crearUsuarioGamificado(codigoUsuario)

        usuario = self.usuariosGamificados[codigoUsuario]
        usuario['puntos'] += cantidad

        puntosNivel = {1: 0, 2: 100, 3: 250, 4: 500, 5: 1000,
                       6: 1500, 7: 2000, 8: 3000, 9: 4000, 10: 5000}
        for nivel in range(10, 0, -1):
            if usuario['puntos'] >= puntosNivel[nivel]:
                usuario['nivel'] = nivel
                break

    # Gamificación: Registra un préstamo y otorga puntos y badges según la actividad
    def registrarPrestamoGami(self, codigoUsuario):
        if codigoUsuario not in self.usuariosGamificados:
            self.crearUsuarioGamificado(codigoUsuario)

        usuario = self.usuariosGamificados[codigoUsuario]
        usuario['prestamos'] += 1
        self.agregarPuntos(codigoUsuario, 10)

        if usuario['prestamos'] >= 10:
            usuario['badges'].add('LEAL')

    # Gamificación: Registra devolución a tiempo y otorga puntos y badges según la actividad
    def registrarDevolucionTiempo(self, codigoUsuario):
        if codigoUsuario not in self.usuariosGamificados:
            self.crearUsuarioGamificado(codigoUsuario)

        usuario = self.usuariosGamificados[codigoUsuario]
        usuario['devolucionesTiempo'] += 1
        self.agregar_puntos(codigoUsuario, 20)

        if usuario['devolucionesTiempo'] >= 5:
            usuario['badges'].add('DEVOLVEDOR')

    # Gamificación: Retorna top N usuarios por puntos
    def leaderboard(self, top_n=10):
        ranking = []
        for codigoUser, data in self.usuariosGamificados.items():
            ranking.append((codigoUser, data['puntos'], data['nivel']))

        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking[:top_n]



