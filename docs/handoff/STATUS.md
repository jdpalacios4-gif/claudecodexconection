# Estado: `dias_habiles`

Rama: `feat/prueba-flujo`. Bloqueante de la ronda 2 corregido. Se alcanzó el máximo de dos rondas
de auditoría (`AGENTS.md`), así que el cierre queda a decisión de la persona responsable.

## Resumen de cambios

Se implementó `dias_habiles(inicio, fin, feriados=None)` siguiendo `PLAN.md`:

- Ambos extremos incluidos; `inicio > fin` lanza `ValueError`.
- Solo se aceptan `datetime.date`; `datetime.datetime`, cadenas y otros tipos lanzan `TypeError`.
- `feriados` puede ser `None` o cualquier iterable; se consume una vez y se deduplica.
- Las fechas se convierten a ordinales enteros en la entrada con `date.toordinal` de la clase base,
  y todo el cálculo (orden, largo del intervalo, día de la semana, filtro de feriados) se hace con
  enteros. No se suma a ninguna fecha, así que no hay desbordamiento en `date.max`.

## Respuesta a las auditorías

| Ronda | Hallazgo | Tipo | Resolución |
| --- | --- | --- | --- |
| 1 | Un feriado de una subclase de `date` sin hash lanza `TypeError` | Bloqueante | **Corregido** y verificado como resuelto por el Auditor en la ronda 2. |
| 1 | Probar un `datetime.datetime` como elemento de `feriados` | Sugerencia | **Aplicada.** |
| 2 | Una subclase que redefine `toordinal()` cambia qué feriados se descuentan (regresión de la corrección anterior) | Bloqueante | **Corregido.** Reproducido con una prueba nueva (`1 != 0`) antes de tocar el código. Se usa `date.toordinal(valor)` como propuso el Auditor. |

Decisión del Ejecutor más allá de lo pedido: el día de la semana también se calcula desde el ordinal
(`_dia_semana`) en vez de llamar a `weekday()` de la instancia. Es la misma clase de problema que el
hallazgo de la ronda 2 y habría quedado abierta. La fórmula se comprobó contra `date.weekday()` en
20 000 ordinales aleatorios.

Opinión del Ejecutor: los dos bloqueantes dependen de subclases de `date` que rompen el contrato de
la clase base. Son reproducibles y la corrección es barata, pero en un proyecto real se podrían
clasificar como Sugerencia.

## Archivos modificados

- `src/dias_habiles.py`
- `tests/test_dias_habiles.py`
- `.gitignore` (ignora `__pycache__/`)

## Pruebas

`python -m unittest discover -s tests -v` → `Ran 13 tests in 0.001s — OK`

## Dudas y riesgos para el Auditor

Sin dudas nuevas. La corrección de la ronda 2 no ha sido auditada.
