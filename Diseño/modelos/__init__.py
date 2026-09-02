"""Diseno / modelos - stubs de los modulos M01-M09.

Cada archivo define las clases con sus atributos y los metodos como stubs
(cuerpo 'pass  # TODO'). La implementacion real ira en 'Codificacion y ejecucion/'.

M01 gestion_usuarios     vector dinamico + hash (M05)
M02 recursos_inventario  vector (catalogo) + matriz sede x recurso
M03 prestamos            lista simple (activos) + lista doble (historial) + pila (deshacer)
M04 turnos               una cola FIFO por recurso agotado
M05 busqueda_codigo      tablas hash con encadenamiento (usuarios y recursos)
M06 ordenamientos        insercion, quicksort, mergesort + busqueda binaria
M07 categorias           arbol AVL de categorias
M08 red_sedes            grafo (lista de adyacencia) + BFS/DFS
M09 informes_uso         agregacion sobre M02, M03, M07

Dependencias: M01,M02,M05 -> M03 -> M04 ; M02 -> M06,M07 ; M02,M03,M07 -> M09.
"""
