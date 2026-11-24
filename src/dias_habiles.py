"""Cálculo de días hábiles (lunes a viernes) entre dos fechas."""

from datetime import date, datetime

_DIAS_LABORABLES_POR_SEMANA = 5
_SABADO = 5  # date.weekday(): lunes = 0 ... domingo = 6


def _validar_fecha(valor, nombre):
    """Acepta solo datetime.date; datetime.datetime se rechaza aunque sea subclase."""
    if isinstance(valor, datetime) or not isinstance(valor, date):
        raise TypeError(
            f"{nombre} debe ser datetime.date, no {type(valor).__name__}"
        )


def _normalizar_feriados(feriados):
    """Consume el iterable una sola vez y devuelve los ordinales sin duplicados.

    Se guardan ordinales y no las fechas para no depender de que cada instancia
    tenga hash (una subclase de date puede no tenerlo).
    """
    if feriados is None:
        return set()
    try:
        iterador = iter(feriados)
    except TypeError:
        raise TypeError(
            "feriados debe ser None o un iterable de datetime.date, "
            f"no {type(feriados).__name__}"
        ) from None
    ordinales = set()
    for feriado in iterador:
        _validar_fecha(feriado, "cada feriado")
        ordinales.add(feriado.toordinal())
    return ordinales


def dias_habiles(inicio, fin, feriados=None):
    """Cuenta los días de lunes a viernes entre inicio y fin, ambos incluidos.

    Los feriados que caen en día laborable dentro del intervalo se descuentan
    una sola vez. Los que caen en fin de semana o fuera del intervalo se ignoran.

    Lanza TypeError si algún argumento no es del tipo esperado y ValueError si
    inicio es posterior a fin.
    """
    _validar_fecha(inicio, "inicio")
    _validar_fecha(fin, "fin")
    if inicio > fin:
        raise ValueError("inicio no puede ser posterior a fin")
    ordinales_feriados = _normalizar_feriados(feriados)

    # Siete días consecutivos siempre contienen cinco laborables, así que solo
    # hace falta revisar uno por uno los días que sobran. No se suma a ninguna
    # fecha, por lo que no hay desbordamiento cerca de date.max.
    total_dias = (fin - inicio).days + 1
    semanas, resto = divmod(total_dias, 7)
    habiles = semanas * _DIAS_LABORABLES_POR_SEMANA
    primer_dia = inicio.weekday()
    for desplazamiento in range(resto):
        if (primer_dia + desplazamiento) % 7 < _SABADO:
            habiles += 1

    ordinal_inicio = inicio.toordinal()
    ordinal_fin = fin.toordinal()
    for ordinal in ordinales_feriados:
        if (
            ordinal_inicio <= ordinal <= ordinal_fin
            and date.fromordinal(ordinal).weekday() < _SABADO
        ):
            habiles -= 1
    return habiles
