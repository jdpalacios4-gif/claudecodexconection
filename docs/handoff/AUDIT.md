# Auditoría de `dias_habiles` · Ronda 3

**Veredicto — Aprobado.** El bloqueante de la ronda 2 quedó resuelto y se cumplen los siete criterios de aceptación del plan. No encontré bloqueantes nuevos.

## Estado de los hallazgos de la ronda 2

| Hallazgo | Estado | Verificación |
| --- | --- | --- |
| **Bloqueante.** Una subclase de `date` que redefine `toordinal()` puede impedir que se descuente un feriado válido. | **Resuelto** | Repetí las dos llamadas de la ronda 2, usando la subclase primero como feriado y luego como ambos extremos. Las dos devolvieron `0`. La conversión usa `date.toordinal(valor)` para todos los argumentos de fecha en `src/dias_habiles.py:19`. Pasó la prueba de regresión en `tests/test_dias_habiles.py:87`, que también verifica una redefinición de `weekday()`. |

La ronda 2 no registró sugerencias nuevas. Volví a verificar que los feriados sin hash se deduplican y que un `datetime.datetime` se rechaza como feriado.

## Hallazgos bloqueantes nuevos

Ninguno.

## Sugerencias nuevas

- **`tests/test_dias_habiles.py:87`** — Ampliar la prueba de subclases para cubrir el orden y la resta de los extremos. El último commit también trasladó esas operaciones a los ordinales. Verifiqué que una subclase cuyos métodos `__gt__` y `__sub__` lanzan una excepción devuelve `4` de lunes a viernes con el lunes feriado, y que al invertir los extremos la función lanza `ValueError`. La suite actual no protege ese comportamiento frente a una regresión.

## Verificación

Revisé `git diff main...HEAD` y `git show HEAD` para el commit `015127b`. Las 13 pruebas pasaron en Python 3.14.2 con `python3.14 -B -m unittest discover -s tests -v`. También pasaron 502 comparaciones con un conteo día a día, con casos en `date.min` y `date.max` y feriados duplicados en los extremos. El conteo aritmético revisa como máximo seis días sobrantes, independientemente de la duración del intervalo. La auditoría se realizó en solo lectura.