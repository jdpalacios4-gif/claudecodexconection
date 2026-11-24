# Estado: `dias_habiles`

Rama: `feat/prueba-flujo`. Ronda 1, listo para auditoría.

## Resumen de cambios

Se implementó `dias_habiles(inicio, fin, feriados=None)` siguiendo `PLAN.md`:

- Ambos extremos incluidos; `inicio > fin` lanza `ValueError`.
- Solo se aceptan `datetime.date`; `datetime.datetime`, cadenas y otros tipos lanzan `TypeError`.
- `feriados` puede ser `None` o cualquier iterable; se consume una vez y se deduplica con un `set`.
- El conteo es aritmético: cinco laborables por semana completa más una revisión de los días
  sobrantes (máximo seis). No se suma a ninguna fecha, así que no hay desbordamiento en `date.max`.

## Archivos modificados

- `src/dias_habiles.py` (nuevo)
- `tests/test_dias_habiles.py` (nuevo)
- `.gitignore` (nuevo, ignora `__pycache__/`)

## Pruebas

`python -m unittest discover -s tests -v` → `Ran 11 tests in 0.001s — OK`

Cubren los criterios de aceptación 1 a 7 y una comprobación cruzada del conteo aritmético contra un
recorrido día por día (7 días de inicio × 30 largos de intervalo).

## Dudas y riesgos para el Auditor

1. Los feriados se validan todos, incluso los que quedan fuera del intervalo. Un elemento inválido
   lejos del rango también lanza `TypeError`. ¿Es el comportamiento deseado?
2. La validación de tipos ocurre antes que la de orden: `dias_habiles("x", fecha)` lanza `TypeError`
   aunque el orden también fuera inválido.
3. No hay `src/__init__.py`; la importación `from src.dias_habiles import ...` depende de ejecutar
   las pruebas desde la raíz del repositorio.
4. Una cadena pasada como `feriados` es iterable; falla con `TypeError` por sus elementos, con un
   mensaje que habla de "cada feriado" y no del argumento completo.
