def _id(x):
    return x


def _antes(a, b, reverso):
    """True si la clave a debe ir ESTRICTAMENTE antes que la clave b."""
    return a > b if reverso else a < b


# Ordenamientos

def bubbleSort(datos, clave=_id, reverso=False):
    a = list(datos)
    n = len(a)
    for i in range(n):
        intercambio = False
        for j in range(n - i - 1):
            if _antes(clave(a[j + 1]), clave(a[j]), reverso):
                a[j], a[j + 1] = a[j + 1], a[j]
                intercambio = True
        if not intercambio:
            break
    return a


def insercion(datos, clave=_id, reverso=False):
    a = list(datos)
    for i in range(1, len(a)):
        actual = a[i]
        k = clave(actual)
        j = i - 1
        while j >= 0 and _antes(k, clave(a[j]), reverso):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = actual
    return a


def mergeSort(datos, clave=_id, reverso=False):
    a = list(datos)
    if len(a) <= 1:
        return a
    medio = len(a) // 2
    izq = mergeSort(a[:medio], clave, reverso)
    der = mergeSort(a[medio:], clave, reverso)
    res = []
    i = j = 0
    while i < len(izq) and j < len(der):
        # solo toma de la derecha si va estrictamente antes -> estabilidad
        if _antes(clave(der[j]), clave(izq[i]), reverso):
            res.append(der[j])
            j += 1
        else:
            res.append(izq[i])
            i += 1
    res.extend(izq[i:])
    res.extend(der[j:])
    return res


def quickSort(datos, clave=_id, reverso=False):
    a = list(datos)
    _qs(a, 0, len(a) - 1, clave, reverso)
    return a


def _qs(a, lo, hi, clave, reverso):
    while lo < hi:
        piv = clave(a[(lo + hi) // 2])
        i, j = lo, hi
        while i <= j:
            while _antes(clave(a[i]), piv, reverso):
                i += 1
            while _antes(piv, clave(a[j]), reverso):
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
        if j - lo < hi - i:
            _qs(a, lo, j, clave, reverso)
            lo = i
        else:
            _qs(a, i, hi, clave, reverso)
            hi = j


# Búsquedas (devuelven el índice, o -1 si no existe)
def busquedaSecuencial(datos, objetivo, clave=_id):
    for i, x in enumerate(datos):
        if clave(x) == objetivo:
            return i
    return -1


def busquedaBinaria(datos, objetivo, clave=_id):
    lo, hi = 0, len(datos) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        k = clave(datos[mid])
        if k == objetivo:
            return mid
        if k < objetivo:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def busquedaBinariaRecursiva(datos, objetivo, clave=_id, lo=0, hi=None):
    if hi is None:
        hi = len(datos) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    k = clave(datos[mid])
    if k == objetivo:
        return mid
    if k < objetivo:
        return busquedaBinariaRecursiva(datos, objetivo, clave, mid + 1, hi)
    return busquedaBinariaRecursiva(datos, objetivo, clave, lo, mid - 1)
