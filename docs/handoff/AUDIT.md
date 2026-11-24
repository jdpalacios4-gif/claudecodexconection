# Auditoría de `dias_habiles` · Ronda 2

**Veredicto — Requiere cambios.** Se corrigió el bloqueante de la ronda 1. La corrección introdujo una regresión que puede dejar sin descontar feriados válidos cuando una subclase de `date` redefine `toordinal()`.

## Estado de los hallazgos de la ronda 1

| Hallazgo | Estado | Verificación |
| --- | --- | --- |
| **Bloqueante.** Un feriado de una subclase de `date` sin hash provocaba `TypeError`. | Resuelto | Repetí la reproducción original y devolvió `0`. También pasó `test_feriado_de_subclase_sin_hash`, que comprueba que dos instancias de la misma fecha se descuentan una sola vez. `tests/test_dias_habiles.py:77`. |
| **Sugerencia.** Probar un `datetime.datetime` como elemento de `feriados`. | Resuelta | Pasó el nuevo subcaso `feriado datetime`. Una llamada directa también confirmó que la validación del elemento lanza `TypeError`. `tests/test_dias_habiles.py:60`. |

## Bloqueantes nuevos

### Una redefinición de `toordinal()` puede cambiar qué feriados se descuentan

**Archivo y líneas:** `src/dias_habiles.py:35` y `src/dias_habiles.py:65–66`.

La función acepta subclases de `date` tanto para los feriados como para los extremos. El último commit llama a `toordinal()` en cada instancia, por lo que una subclase que devuelve ordinales con base cero desplaza la fecha que se usa para filtrar los feriados. En ambos casos de la reproducción, el feriado corresponde al único día del intervalo. Verifiqué que `HEAD^` devuelve `0` en ambos casos y que `HEAD` devuelve `1`.

```python
from datetime import date

from src.dias_habiles import dias_habiles


class FechaOrdinalCero(date):
    def toordinal(self):
        return super().toordinal() - 1


lunes = date(2026, 11, 23)
lunes_subclase = FechaOrdinalCero(2026, 11, 23)

print(dias_habiles(lunes, lunes, [lunes_subclase]))
print(dias_habiles(lunes_subclase, lunes_subclase, [lunes]))
```

La deduplicación por ordinal puede conservarse usando `date.toordinal(fecha)` tanto para los feriados como para los extremos. Una prueba de regresión con las dos llamadas cubriría el fallo.

## Sugerencias nuevas

Ninguna.

## Pruebas ejecutadas

Las 12 pruebas pasaron en Python 3.14.2 con `python3.14 -B -m unittest discover -s tests -v`. También pasaron 16 comparaciones con un conteo día a día cerca de `date.min` y `date.max`, con feriados duplicados en los extremos. Ejecuté las comprobaciones sin escribir archivos.