# Auditoría de `dias_habiles`

**Veredicto — Requiere cambios.** Los siete criterios de aceptación se cumplen en los casos especificados. Queda un bloqueante en el manejo de feriados que son instancias válidas de `datetime.date`.

Ejecuté `python3.14 -B -m unittest discover -s tests -v` desde la raíz del repositorio. Las 11 pruebas pasaron en Python 3.14.2. Usé `python3.14` porque el alias `python` falló al iniciarse, y `-B` evitó que se escribieran archivos de bytecode.

## Hallazgos bloqueantes

### Un feriado válido sin hash provoca `TypeError` en `src/dias_habiles.py:30`

El plan acepta objetos `datetime.date` como feriados. `_validar_fecha` acepta una subclase de `date` sin hash, pero `conjunto.add(feriado)` falla al deduplicarla. Esto impone un requisito adicional sobre los feriados válidos. Deduplicar por el ordinal de la fecha evitaría depender del hash de la instancia.

Reproducción desde la raíz del repositorio:

```python
from datetime import date
from src.dias_habiles import dias_habiles

class FechaSinHash(date):
    __hash__ = None

lunes = date(2026, 11, 23)
dias_habiles(lunes, lunes, [FechaSinHash(2026, 11, 23)])
```

El resultado esperado es `0` porque el lunes es feriado. En Python 3.14.2, la llamada lanza `TypeError` al insertar el feriado en el conjunto.

## Sugerencias

- `tests/test_dias_habiles.py:48` — Agregar un `datetime.datetime` como elemento de `feriados` a `test_tipos_invalidos`. El `None` ya cubre un elemento inválido, mientras que este caso protegería el rechazo explícito de una subclase de `date` en los feriados.

## Criterios de aceptación

| Criterio | Estado | Prueba que lo cubre |
| --- | --- | --- |
| 1. Devuelve el entero `5` de lunes a viernes y `2` de viernes a lunes con `feriados=[]`. | Cumplido | `test_semana_completa_sin_feriados`, `test_intervalo_que_cruza_fin_de_semana` |
| 2. Para un solo día, devuelve `1` si es laborable y `0` si es feriado o sábado. | Cumplido | `test_un_solo_dia_laborable`, `test_un_solo_dia_feriado`, `test_un_solo_dia_en_fin_de_semana` |
| 3. Devuelve `4` con el generador que incluye un duplicado, un sábado y una fecha fuera del intervalo. | Cumplido | `test_generador_con_duplicados_fin_de_semana_y_fuera_de_rango` |
| 4. Lanza `ValueError` si el inicio es posterior al fin. | Cumplido | `test_inicio_posterior_a_fin` |
| 5. Lanza `TypeError` para un inicio de tipo cadena, un fin de tipo `datetime`, `feriados=42` y `feriados=[None]`. | Cumplido | `test_tipos_invalidos`, con un subcaso por entrada |
| 6. Devuelve `3` para el intervalo que cruza el 29 de febrero y `1` para `date.max` sin desbordarse. | Cumplido | `test_febrero_bisiesto`, `test_date_max_sin_desbordamiento` |
| 7. La función se importa desde `src.dias_habiles` y `unittest discover` ejecuta la suite sin fallos. | Cumplido | Importación al cargar `tests/test_dias_habiles.py` y ejecución de las 11 pruebas |

La comprobación cruzada `test_coincide_con_recorrido_dia_a_dia` compara el conteo con un recorrido de referencia para los siete días posibles de inicio y 30 duraciones. La implementación revisa como máximo seis días sobrantes y su coste crece con la cantidad de feriados, independientemente de la duración del intervalo.

## Respuestas a las dudas del Ejecutor

1. **Validación de todos los feriados.** Sí. El plan exige `TypeError` ante cualquier elemento inválido. El filtro por intervalo se aplica a los elementos que ya se validaron como fechas.
2. **Validación de tipos antes del orden.** Es correcto. Primero se comprueba que ambos extremos sean fechas válidas. `ValueError` corresponde a dos fechas válidas en orden inverso.
3. **Importación sin `src/__init__.py`.** `src` funciona como paquete de espacio de nombres cuando la raíz del repositorio está en `sys.path`. La ejecución desde la raíz cumple esa condición y verifiqué que descubre las 11 pruebas.
4. **Cadena como `feriados`.** Para una cadena no vacía, `TypeError` y el mensaje sobre «cada feriado» identifican correctamente el carácter inválido. Verifiqué que `feriados=""` se acepta como iterable vacío, conforme a la regla del plan que admite cualquier iterable cuyos elementos sean fechas.