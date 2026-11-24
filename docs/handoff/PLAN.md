# Plan para `dias_habiles`

## 1. Objetivo

Agregar la función pública `dias_habiles(inicio, fin, feriados=None)` en `src/dias_habiles.py`. Debe devolver el número de días de lunes a viernes del intervalo, excluyendo los feriados indicados. Usar solo la biblioteca estándar de Python 3.14 y agregar pruebas con `unittest` en `tests/test_dias_habiles.py`.

## 2. Decisiones de diseño

- Incluir ambos extremos del intervalo. Si `inicio > fin`, lanzar `ValueError`.
- Aceptar objetos `datetime.date` como extremos y como elementos de `feriados`. Rechazar `datetime.datetime`, cadenas y otros tipos con `TypeError`.
- Aceptar `None` o cualquier iterable de fechas como `feriados`, incluidos generadores. `None` equivale a un iterable vacío. Un valor no iterable o un elemento inválido produce `TypeError`.
- Contar cada feriado una sola vez. Los feriados fuera del intervalo o en fin de semana no afectan el resultado.

## 3. Casos borde y riesgos

- Un intervalo de un solo día devuelve `1` si es laborable y `0` si cae en fin de semana o es feriado.
- Contar cinco días por semana completa y revisar los días restantes. Esto evita recorrer cada fecha en intervalos largos.
- Consumir el iterable de feriados una sola vez y deduplicarlo. Evitar avanzar más allá de `date.max` al contar el último día.

## 4. Criterios de aceptación

En los ejemplos, las fechas ISO representan objetos `datetime.date`, salvo cuando se indica explícitamente otro tipo.

1. Del `2026-11-23` al `2026-11-27`, sin feriados, devuelve el entero `5`. Del `2026-11-27` al `2026-11-30` con `feriados=[]`, devuelve `2`.
2. Del `2026-11-23` al `2026-11-23`, devuelve `1` sin feriados y `0` si ese día es feriado. Del `2026-11-28` al `2026-11-28`, devuelve `0`.
3. Del `2026-11-23` al `2026-11-29`, con un generador que entrega `2026-11-23` dos veces, `2026-11-28` y `2026-11-30`, devuelve `4`.
4. Del `2026-11-24` al `2026-11-23`, lanza `ValueError`.
5. Con la cadena `"2026-11-23"` como `inicio`, un `datetime.datetime` como `fin`, `feriados=42` o `feriados=[None]`, lanza `TypeError` en cada caso.
6. Del `2024-02-28` al `2024-03-01`, devuelve `3`. El intervalo de un solo día `date.max` a `date.max` devuelve `1` sin desbordamiento.
7. La función se puede importar con `from src.dias_habiles import dias_habiles`, y `python -m unittest discover -s tests -v` descubre y ejecuta las pruebas sin fallos.