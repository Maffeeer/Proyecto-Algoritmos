## Hecho por claude puesto que no hemos visto grafos

"""
GRAFO BÁSICO — Estructura de datos propia

Descripción:
    Grafo no dirigido simple con lista de adyacencia.
    Implementado sin usar dict o list nativos de Python.
    Usado en M07 para conectar sedes en red.

Implementación:
    - Arreglo de nodos vértice
    - Cada vértice contiene lista enlazada de vecinos

Complejidad:
    - BFS/DFS: O(V + E) donde V=vértices, E=aristas
"""


class _NodoVecino:
    """Nodo para lista enlazada de vecinos."""
    def __init__(self, id_vecino):
        self.id = id_vecino
        self.siguiente = None


class _NodoVertice:
    """Nodo para almacenar un vértice y sus vecinos."""
    def __init__(self, id_vertice):
        self.id = id_vertice
        self.vecinos = None  # Cabecera de lista enlazada de vecinos
        self.siguiente = None  # Para lista de vértices


class Grafo:
    """
    Grafo no dirigido con lista de adyacencia.

    Atributos:
        vertices (NodoVertice): Lista enlazada de vértices
        cantidad_vertices (int): Cantidad de vértices
        cantidad_aristas (int): Cantidad de aristas
    """

    def __init__(self):
        """Inicializa grafo vacío."""
        self.vertices = None  # Cabecera de lista de vértices
        self.cantidad_vertices = 0
        self.cantidad_aristas = 0

    def agregar_vertice(self, id_vertice):
        """Agrega un vértice. O(1) si no existe."""
        # Verificar si ya existe
        nodo = self.vertices
        while nodo is not None:
            if nodo.id == id_vertice:
                return  # Ya existe
            nodo = nodo.siguiente

        # No existe, agregar al inicio
        nuevo = _NodoVertice(id_vertice)
        nuevo.siguiente = self.vertices
        self.vertices = nuevo
        self.cantidad_vertices += 1

    def agregar_arista(self, origen, destino):
        """Agrega arista entre dos vértices. O(V)."""
        # Ambos vértices deben existir
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)

        # Agregar destino a lista de vecinos de origen
        nodo_origen = self._buscar_vertice(origen)
        if nodo_origen is not None:
            if not self._tiene_vecino(nodo_origen, destino):
                nuevo_vecino = _NodoVecino(destino)
                nuevo_vecino.siguiente = nodo_origen.vecinos
                nodo_origen.vecinos = nuevo_vecino

        # Grafo no dirigido: agregar origen a lista de vecinos de destino
        nodo_destino = self._buscar_vertice(destino)
        if nodo_destino is not None:
            if not self._tiene_vecino(nodo_destino, origen):
                nuevo_vecino = _NodoVecino(origen)
                nuevo_vecino.siguiente = nodo_destino.vecinos
                nodo_destino.vecinos = nuevo_vecino

        self.cantidad_aristas += 1

    def _buscar_vertice(self, id_vertice):
        """Busca un vértice por ID. O(V)."""
        nodo = self.vertices
        while nodo is not None:
            if nodo.id == id_vertice:
                return nodo
            nodo = nodo.siguiente
        return None

    def _tiene_vecino(self, nodo_vertice, id_vecino):
        """Verifica si un vértice ya tiene un vecino. O(grado)."""
        vecino = nodo_vertice.vecinos
        while vecino is not None:
            if vecino.id == id_vecino:
                return True
            vecino = vecino.siguiente
        return False

    def obtener_vecinos(self, id_vertice):
        """Obtiene lista de vecinos de un vértice. O(grado)."""
        nodo = self._buscar_vertice(id_vertice)
        if nodo is None:
            return []

        vecinos = []
        vecino_nodo = nodo.vecinos
        while vecino_nodo is not None:
            vecinos.append(vecino_nodo.id)
            vecino_nodo = vecino_nodo.siguiente
        return vecinos

    def obtener_vertices(self):
        """Obtiene lista de todos los vértices. O(V)."""
        vertices = []
        nodo = self.vertices
        while nodo is not None:
            vertices.append(nodo.id)
            nodo = nodo.siguiente
        return vertices

    def obtener_cantidad_vertices(self):
        """Obtiene cantidad de vértices. O(1)."""
        return self.cantidad_vertices

    def obtener_cantidad_aristas(self):
        """Obtiene cantidad de aristas. O(1)."""
        return self.cantidad_aristas

    def recorrido_amplitud(self, id_inicio):
        """
        BFS (Breadth-First Search).

        Returns:
            Lista de vértices en orden BFS

        Complejidad: O(V + E)
        """
        if self._buscar_vertice(id_inicio) is None:
            return []

        # Usar arreglo para visitados y cola manual
        visitados = []
        cola = []
        resultado = []

        cola.append(id_inicio)
        visitados.append(id_inicio)

        while len(cola) > 0:
            actual = cola.pop(0)
            resultado.append(actual)

            # Agregar vecinos no visitados a la cola
            for vecino in self.obtener_vecinos(actual):
                if vecino not in visitados:
                    cola.append(vecino)
                    visitados.append(vecino)

        return resultado

    def recorrido_profundidad(self, id_inicio):
        """
        DFS (Depth-First Search).

        Returns:
            Lista de vértices en orden DFS

        Complejidad: O(V + E)
        """
        visitados = []
        resultado = []
        self._dfs_recursivo(id_inicio, visitados, resultado)
        return resultado

    def _dfs_recursivo(self, id_vertice, visitados, resultado):
        """DFS recursivo."""
        if id_vertice in visitados:
            return

        visitados.append(id_vertice)
        resultado.append(id_vertice)

        for vecino in self.obtener_vecinos(id_vertice):
            if vecino not in visitados:
                self._dfs_recursivo(vecino, visitados, resultado)

    def __str__(self):
        """Representación en string."""
        return f"Grafo(V={self.cantidad_vertices}, E={self.cantidad_aristas})"

    def __repr__(self):
        """Representación para debug."""
        return self.__str__()
