
def _esPrimo(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def primoSiguiente(n):
    c = max(2, n)
    while not _esPrimo(c):
        c += 1
    return c


class _Nodo:
    __slots__ = ("clave", "valor", "sig")

    def __init__(self, clave, valor, sig=None):
        self.clave = clave
        self.valor = valor
        self.sig = sig


class TablaHash:

    FACTOR_MAX = 0.75

    def __init__(self, capacidad=211, tamaño=None):
        # 'tamaño' se acepta para ser compatible con TablaHash(tamaño=100) de la Entrega 1
        if tamaño is not None:
            capacidad = tamaño
        self.capacidad = primoSiguiente(capacidad)
        self.cubetas = [None] * self.capacidad
        self.tamaño = 0

    @staticmethod
    def funcionHash(clave):
        h = 5381
        for ch in str(clave):
            h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
        return h

    def _indice(self, clave):
        return self.funcionHash(clave) % self.capacidad

    def _nodo(self, clave):
        n = self.cubetas[self._indice(clave)]
        while n is not None:
            if n.clave == clave:
                return n
            n = n.sig
        return None

    # ---- operaciones ----
    def insertar(self, clave, valor):
        n = self._nodo(clave)
        if n is not None:
            n.valor = valor
            return False
        i = self._indice(clave)
        self.cubetas[i] = _Nodo(clave, valor, self.cubetas[i])
        self.tamaño += 1
        if self.tamaño / self.capacidad > self.FACTOR_MAX:
            self._redimensionar()
        return True

    def buscar(self, clave, defecto=None):
        n = self._nodo(clave)
        return n.valor if n is not None else defecto

    def contiene(self, clave):
        return self._nodo(clave) is not None

    def eliminar(self, clave):
        i = self._indice(clave)
        previo, n = None, self.cubetas[i]
        while n is not None:
            if n.clave == clave:
                if previo is None:
                    self.cubetas[i] = n.sig
                else:
                    previo.sig = n.sig
                self.tamaño -= 1
                return True
            previo, n = n, n.sig
        return False

    def _redimensionar(self):
        viejas = self.cubetas
        self.capacidad = primoSiguiente(self.capacidad * 2)
        self.cubetas = [None] * self.capacidad
        for n in viejas:
            while n is not None:
                sig = n.sig
                i = self._indice(n.clave)
                n.sig = self.cubetas[i]
                self.cubetas[i] = n
                n = sig

    # ---- recorridos ----
    def items(self):
        for n in self.cubetas:
            while n is not None:
                yield n.clave, n.valor
                n = n.sig

    def claves(self):
        for k, _ in self.items():
            yield k

    def valores(self):
        for _, v in self.items():
            yield v

    def __len__(self):
        return self.tamaño

    def __contains__(self, clave):
        return self.contiene(clave)

    # ---- mismos nombres que la TablaHash de la Entrega 1 (compatibilidad) ----
    def obtenerCantidad(self):
        return self.tamaño

    def obtenerTamaño(self):
        return self.capacidad

    def obtenerTodasLasClaves(self):
        return list(self.claves())

    def obtenerFactorCarga(self):
        return self.tamaño / self.capacidad

    # ---- análisis de colisiones (para el informe) ----
    def estadisticas(self):
        ocupadas = 0
        maxima = 0
        for n in self.cubetas:
            largo = 0
            while n is not None:
                largo += 1
                n = n.sig
            if largo:
                ocupadas += 1
                maxima = max(maxima, largo)
        return {
            "capacidad": self.capacidad,
            "elementos": self.tamaño,
            "factorCarga": round(self.tamaño / self.capacidad, 3),
            "cubetasOcupadas": ocupadas,
            "colisiones": self.tamaño - ocupadas,
            "cadenaMaxima": maxima,
            "cadenaPromedio": round(self.tamaño / ocupadas, 3) if ocupadas else 0,
        }

    def __str__(self):
        return f"TablaHash({self.estadisticas()})"


class ConjuntoHash:

    def __init__(self, capacidad=211):
        self._t = TablaHash(capacidad)

    def agregar(self, elemento):
        return self._t.insertar(elemento, True)

    def contiene(self, elemento):
        return self._t.contiene(elemento)

    def eliminar(self, elemento):
        return self._t.eliminar(elemento)

    def elementos(self):
        return list(self._t.claves())

    def __len__(self):
        return len(self._t)

    def __contains__(self, elemento):
        return self.contiene(elemento)
