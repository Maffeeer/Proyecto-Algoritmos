# Pruebas

Ejecutar: `python test_pruebas.py`

## Resultados

M01 EXITOSO -> se esperaba U001 -> se obtuvo U001 ✓
M01 BORDE -> se esperaba usuario "A" registrado -> se obtuvo usuario "A" creado ✓
M01 CUELLO BOTELLA -> se esperaba 1000 usuarios registrados -> se obtuvo 1000 usuarios ✓

M02 EXITOSO -> se esperaba código recurso generado -> se obtuvo código generado ✓
M02 BORDE -> se esperaba sala con capacidad 1 registrada -> se obtuvo sala creada ✓
M02 CUELLO BOTELLA -> se esperaba 500 recursos registrados -> se obtuvo 500 recursos ✓

M03 EXITOSO -> se esperaba código préstamo generado -> se obtuvo código creado ✓
M03 BORDE -> se esperaba error sin unidades -> se obtuvo excepción correcta ✓
M03 CUELLO BOTELLA -> se esperaba 200 préstamos registrados -> se obtuvo 200 préstamos ✓

M04 EXITOSO -> se esperaba código turno generado -> se obtuvo código creado ✓
M04 BORDE -> se esperaba orden FIFO correcto -> se obtuvo orden FIFO preservado ✓
M04 CUELLO BOTELLA -> se esperaba 500 turnos -> se obtuvo 500 turnos ✓

M05 EXITOSO -> se esperaba categoría creada -> se obtuvo categoría registrada ✓
M05 BORDE -> se esperaba error duplicado -> se obtuvo ValueError capturado ✓
M05 CUELLO BOTELLA -> se esperaba 500 categorías en árbol -> se obtuvo 500 categorías ✓

M06 EXITOSO -> se esperaba reporte válido -> se obtuvo reporte generado ✓
M06 BORDE -> se esperaba reporte sin datos -> se obtuvo genera sin error ✓
M06 CUELLO BOTELLA -> se esperaba 300 recursos ordenados -> se obtuvo 300 ordenados ✓

M07 EXITOSO -> se esperaba matriz generada -> se obtuvo matriz mostrada ✓
M07 BORDE -> se esperaba matriz desigual -> se obtuvo valores correctos ✓
M07 CUELLO BOTELLA -> se esperaba matriz 200 recursos x 3 sedes -> se obtuvo 600 celdas ✓
