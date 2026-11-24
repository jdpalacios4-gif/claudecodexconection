"""Cálculo de días hábiles (lunes a viernes) entre dos fechas."""

from datetime import date, datetime

_DIAS_LABORABLES_POR_SEMANA = 5
_SABADO = 5  # lunes = 0 ... domingo = 6, igual que date.weekday()


def _a_ordinal(valor, nombre):
    """Valida que valor sea datetime.date y lo convierte a su ordinal.

    datetime.datetime se rechaza aunque sea subclase de date. La conversión usa
    date.toordinal de la clase base: así el resultado no depende de métodos que
    una subclase haya redefinido ni de que la instancia tenga hash. A partir de
    aquí la función trabaja solo con enteros.
    """
    if isinstance(valor, datetime) or not isinstance(valor, date):
        raise TypeError(
            f"{nombre} debe ser datetime.date, no {type(valor).__name__}"
        )
    return date.toordinal(valor)


def _dia_semana(ordinal):
    """Día de la semana de un ordinal. El ordinal 1 (0001-01-01) es lunes."""
    return (ordinal - 1) % 7


def _normalizar_feriados(feriados):
    """Consume el iterable una sola vez y devuelve los ordinales sin duplicados."""
    if feriados is None:
        return set()
    try:
        iterador = iter(feriados)
    except TypeError:
        raise TypeError(
            "feriados debe ser None o un iterable de datetime.date, "
            f"no {type(feriados).__name__}"
        ) from None
    return {_a_ordinal(feriado, "cada feriado") for feriado in iterador}


def dias_habiles(inicio, fin, feriados=None):
    """Cuenta los días de lunes a viernes entre inicio y fin, ambos incluidos.

    Los feriados que caen en día laborable dentro del intervalo se descuentan
    una sola vez. Los que caen en fin de semana o fuera del intervalo se ignoran.

    Lanza TypeError si algún argumento no es del tipo esperado y ValueError si
    inicio es posterior a fin.
    """
    ordinal_inicio = _a_ordinal(inicio, "inicio")
    ordinal_fin = _a_ordinal(fin, "fin")
    if ordinal_inicio > ordinal_fin:
        raise ValueError("inicio no puede ser posterior a fin")
    ordinales_feriados = _normalizar_feriados(feriados)

    # Siete días consecutivos siempre contienen cinco laborables, así que solo
    # hace falta revisar uno por uno los días que sobran (máximo seis).
    total_dias = ordinal_fin - ordinal_inicio + 1
    semanas, resto = divmod(total_dias, 7)
    habiles = semanas * _DIAS_LABORABLES_POR_SEMANA
    primer_dia = _dia_semana(ordinal_inicio)
    for desplazamiento in range(resto):
        if (primer_dia + desplazamiento) % 7 < _SABADO:
            habiles += 1

    for ordinal in ordinales_feriados:
        if ordinal_inicio <= ordinal <= ordinal_fin and _dia_semana(ordinal) < _SABADO:
            habiles -= 1
    return habiles
