# Estado: `dias_habiles`

Rama: `feat/prueba-flujo`. Ronda 2: bloqueante de `AUDIT.md` corregido, pendiente de re-auditoría.

## Resumen de cambios

Se implementó `dias_habiles(inicio, fin, feriados=None)` siguiendo `PLAN.md`:

- Ambos extremos incluidos; `inicio > fin` lanza `ValueError`.
- Solo se aceptan `datetime.date`; `datetime.datetime`, cadenas y otros tipos lanzan `TypeError`.
- `feriados` puede ser `None` o cualquier iterable; se consume una vez y se deduplica.
- El conteo es aritmético: cinco laborables por semana completa más una revisión de los días
  sobrantes (máximo seis). No se suma a ninguna fecha, así que no hay desbordamiento en `date.max`.

## Respuesta a la auditoría (ronda 1)

| Hallazgo | Tipo | Resolución |
| --- | --- | --- |
| Un feriado de una subclase de `date` sin hash lanza `TypeError` (`src/dias_habiles.py`) | Bloqueante | **Corregido.** Reproducido con una prueba nueva antes de tocar el código. Los feriados ahora se deduplican por ordinal (`toordinal()`), sin depender del hash de la instancia. |
| Agregar un `datetime.datetime` como elemento de `feriados` a `test_tipos_invalidos` | Sugerencia | **Aplicada.** Nuevo subcaso "feriado datetime". |

## Archivos modificados

- `src/dias_habiles.py`
- `tests/test_dias_habiles.py`
- `.gitignore` (ignora `__pycache__/`)

## Pruebas

`python -m unittest discover -s tests -v` → `Ran 12 tests in 0.001s — OK`

Antes de la corrección, la prueba nueva `test_feriado_de_subclase_sin_hash` fallaba con el mismo
`TypeError` que describe la auditoría; después de la corrección pasa.

## Dudas y riesgos para el Auditor

Las cuatro dudas de la ronda 1 quedaron respondidas en `AUDIT.md` sin cambios requeridos. Sin dudas
nuevas.
