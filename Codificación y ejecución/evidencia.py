"""
Evidencia de eficiencia: Entrega 1 vs Entrega 2 (opción 10 del menú).

Mide en vivo, con las estructuras y algoritmos del propio proyecto:
  1. Búsqueda de usuario por código: vector (lineal, E1) vs tabla hash (E2).
  2. Función hash: suma ASCII (E1) vs djb2 + tamaño primo + redimensionamiento (E2).
  3. Ordenamiento para listados: bubble sort (E1) vs merge sort y quick sort (E2).
  4. Búsqueda en listado ordenado: secuencial vs binaria.

Los tiempos se toman con time.perf_counter() y se reporta la mediana de varias
repeticiones, para que una interrupción del sistema operativo no distorsione el dato.
"""

import random
import time

from estructuras import TablaHash, TablaHashASCII
from estructuras.Algoritmos import (bubbleSort, mergeSort, quickSort,
                                    busquedaSecuencial, busquedaBinaria)
from modulos import GestorUsuarios


def _mediana(valores):
    v = sorted(valores)
    return v[len(v) // 2]


def _medir(funcion, repeticiones=5):
    tiempos = []
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        funcion()
        tiempos.append(time.perf_counter() - t0)
    return _mediana(tiempos)


def _estadisticasASCII(tabla):
    """Mismas métricas que TablaHash.estadisticas(), calculadas sobre la tabla de la E1."""
    ocupadas, maxima, comparaciones = 0, 0, 0
    for cabeza in tabla.tabla:
        largo = 0
        nodo = cabeza
        while nodo is not None:
            largo += 1
            comparaciones += largo  # buscar el k-ésimo nodo cuesta k comparaciones
            nodo = nodo.siguiente
        if largo:
            ocupadas += 1
            maxima = max(maxima, largo)
    n = tabla.obtenerCantidad()
    return {"capacidad": tabla.obtenerTamaño(), "ocupadas": ocupadas,
            "colisiones": n - ocupadas, "cadenaMaxima": maxima,
            "comparacionesProm": comparaciones / n if n else 0}


def _estadisticasDjb2(tabla):
    comparaciones = 0
    for cabeza in tabla.cubetas:
        largo = 0
        nodo = cabeza
        while nodo is not None:
            largo += 1
            comparaciones += largo
            nodo = nodo.sig
    e = tabla.estadisticas()
    n = e["elementos"]
    return {"capacidad": e["capacidad"], "ocupadas": e["cubetasOcupadas"],
            "colisiones": e["colisiones"], "cadenaMaxima": e["cadenaMaxima"],
            "comparacionesProm": comparaciones / n if n else 0}


def pruebaBusquedaUsuarios(n=2000):
    print(f"1) BUSCAR USUARIO POR CODIGO  ({n} usuarios, {n} busquedas)")
    gu = GestorUsuarios()
    for i in range(n):
        gu.registrar(f"Usuario {i}", f"u{i}@uni.edu")
    codigos = [f"U{i:03d}" for i in range(1, n + 1)]
    random.shuffle(codigos)

    def lineal():
        for c in codigos:
            gu.buscarUsuarioLineal(c)

    def hashing():
        for c in codigos:
            gu.buscarUsuario(c)

    tLineal = _medir(lineal, 3) / n * 1e6
    tHash = _medir(hashing, 3) / n * 1e6
    print(f"   Entrega 1 - vector, recorrido lineal  O(n)  : {tLineal:8.2f} us por busqueda")
    print(f"   Entrega 2 - tabla hash djb2           O(1)  : {tHash:8.2f} us por busqueda")
    print(f"   -> La tabla hash es {tLineal / tHash:.0f} veces mas rapida")
    print()


def pruebaFuncionHash(n=2000):
    print(f"2) FUNCION HASH  (codigos reales P0001..P{n:04d})")
    claves = [f"P{i:04d}" for i in range(1, n + 1)]
    ascii_ = TablaHashASCII(211)
    djb2 = TablaHash(211)
    for c in claves:
        ascii_.insertar(c, c)
        djb2.insertar(c, c)
    ea = _estadisticasASCII(ascii_)
    ed = _estadisticasDjb2(djb2)
    print("                             cubetas  usadas  colisiones  cadena max  comparaciones")
    print(f"   E1 suma ASCII (fija 211)  {ea['capacidad']:6d}  {ea['ocupadas']:6d}  {ea['colisiones']:10d}"
          f"  {ea['cadenaMaxima']:10d}  {ea['comparacionesProm']:13.2f}")
    print(f"   E2 djb2 + primo + resize  {ed['capacidad']:6d}  {ed['ocupadas']:6d}  {ed['colisiones']:10d}"
          f"  {ed['cadenaMaxima']:10d}  {ed['comparacionesProm']:13.2f}")
    print("   Por que: con suma ASCII 'P0019' y 'P0091' suman lo mismo (el orden no importa)")
    print(f"   djb2('P0019') % 211 = {TablaHash.funcionHash('P0019') % 211}   "
          f"djb2('P0091') % 211 = {TablaHash.funcionHash('P0091') % 211}")
    print()


def pruebaOrdenamientos(n=2000):
    print(f"3) ORDENAR RECURSOS POR CANTIDAD DE PRESTAMOS  (n = {n}, datos aleatorios)")
    datos = [random.randint(0, 500) for _ in range(n)]
    esperado = sorted(datos)
    for nombre, f in (("bubble", bubbleSort), ("merge", mergeSort), ("quick", quickSort)):
        assert f(datos) == esperado, nombre  # los tres dan el mismo resultado
    tB = _medir(lambda: bubbleSort(datos), 3) * 1000
    tM = _medir(lambda: mergeSort(datos), 5) * 1000
    tQ = _medir(lambda: quickSort(datos), 5) * 1000
    print(f"   Entrega 1 - bubble sort   O(n^2)     : {tB:8.2f} ms")
    print(f"   Entrega 2 - merge sort    O(n log n) : {tM:8.2f} ms   (estable, el que usan los informes)")
    print(f"   Entrega 2 - quick sort    O(n log n) : {tQ:8.2f} ms")
    print(f"   -> merge sort es {tB / tM:.0f} veces mas rapido que bubble sort")
    print("   (los tres algoritmos se verificaron contra sorted(): mismo resultado)")
    print()


def pruebaBusquedas(n=10000, consultas=2000):
    print(f"4) BUSCAR EN UN LISTADO ORDENADO  (n = {n}, {consultas} consultas)")
    codigos = [f"R{i:05d}" for i in range(1, n + 1)]  # los códigos se generan en orden
    objetivos = random.sample(codigos, consultas)
    tS = _medir(lambda: [busquedaSecuencial(codigos, o) for o in objetivos], 3) / consultas * 1e6
    tB = _medir(lambda: [busquedaBinaria(codigos, o) for o in objetivos], 3) / consultas * 1e6
    print(f"   Secuencial  O(n)     : {tS:8.2f} us por busqueda")
    print(f"   Binaria     O(log n) : {tB:8.2f} us por busqueda  (maximo 14 comparaciones con 10.000)")
    print()


def ejecutarEvidencia():
    random.seed(42)  # resultados reproducibles
    print("  EVIDENCIA DE EFICIENCIA: ENTREGA 1 vs ENTREGA 2")
    print("  (medido ahora mismo en este computador; mediana de varias repeticiones)")
    print()
    pruebaBusquedaUsuarios()
    pruebaFuncionHash()
    pruebaOrdenamientos()
    pruebaBusquedas()
