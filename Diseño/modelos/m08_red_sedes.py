"""M08 - Red de sedes.

Administra Sede y sus relaciones de distancia/conexion.
Estructura de datos: grafo como lista de adyacencia.
Algoritmos BFS/DFS para camino mas corto y deteccion de sedes aisladas.
"""


class Sede:
    def __init__(self, id_sede, nombre, ciudad=""):
        self.id_sede = id_sede
        self.nombre = nombre
        self.ciudad = ciudad


class GrafoSedes:
    def __init__(self):
        self.sedes = {}        # id_sede -> Sede
        self.adyacencia = {}   # id_sede -> [(id_destino, peso)]

    def agregar_sede(self, sede):
        pass  # TODO: implementar en fase de desarrollo

    def conectar(self, id_a, id_b, peso=1.0):
        pass  # TODO

    def desconectar(self, id_a, id_b):
        pass  # TODO

    def bfs(self, id_origen):
        pass  # TODO

    def dfs(self, id_origen):
        pass  # TODO

    def camino_mas_corto(self, id_origen, id_destino):
        pass  # TODO

    def componentes_conexas(self):
        pass  # TODO

    def sedes_aisladas(self):
        pass  # TODO
