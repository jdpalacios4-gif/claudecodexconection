import unittest
from datetime import date, datetime

from src.dias_habiles import dias_habiles


class DiasHabilesTest(unittest.TestCase):
    # Criterio 1
    def test_semana_completa_sin_feriados(self):
        resultado = dias_habiles(date(2026, 11, 23), date(2026, 11, 27))
        self.assertEqual(resultado, 5)
        self.assertIs(type(resultado), int)

    def test_intervalo_que_cruza_fin_de_semana(self):
        self.assertEqual(
            dias_habiles(date(2026, 11, 27), date(2026, 11, 30), feriados=[]), 2
        )

    # Criterio 2
    def test_un_solo_dia_laborable(self):
        lunes = date(2026, 11, 23)
        self.assertEqual(dias_habiles(lunes, lunes), 1)

    def test_un_solo_dia_feriado(self):
        lunes = date(2026, 11, 23)
        self.assertEqual(dias_habiles(lunes, lunes, feriados=[lunes]), 0)

    def test_un_solo_dia_en_fin_de_semana(self):
        sabado = date(2026, 11, 28)
        self.assertEqual(dias_habiles(sabado, sabado), 0)

    # Criterio 3
    def test_generador_con_duplicados_fin_de_semana_y_fuera_de_rango(self):
        def feriados():
            yield date(2026, 11, 23)
            yield date(2026, 11, 23)
            yield date(2026, 11, 28)
            yield date(2026, 11, 30)

        self.assertEqual(
            dias_habiles(date(2026, 11, 23), date(2026, 11, 29), feriados()), 4
        )

    # Criterio 4
    def test_inicio_posterior_a_fin(self):
        with self.assertRaises(ValueError):
            dias_habiles(date(2026, 11, 24), date(2026, 11, 23))

    # Criterio 5
    def test_tipos_invalidos(self):
        lunes = date(2026, 11, 23)
        viernes = date(2026, 11, 27)
        casos = {
            "inicio como cadena": lambda: dias_habiles("2026-11-23", viernes),
            "fin como datetime": lambda: dias_habiles(
                lunes, datetime(2026, 11, 27, 12, 0)
            ),
            "feriados no iterable": lambda: dias_habiles(lunes, viernes, feriados=42),
            "feriado None": lambda: dias_habiles(lunes, viernes, feriados=[None]),
            "feriado datetime": lambda: dias_habiles(
                lunes, viernes, feriados=[datetime(2026, 11, 24, 9, 0)]
            ),
        }
        for nombre, llamada in casos.items():
            with self.subTest(nombre):
                with self.assertRaises(TypeError):
                    llamada()

    # Criterio 6
    def test_febrero_bisiesto(self):
        self.assertEqual(dias_habiles(date(2024, 2, 28), date(2024, 3, 1)), 3)

    def test_date_max_sin_desbordamiento(self):
        self.assertEqual(dias_habiles(date.max, date.max), 1)

    # AUDIT.md ronda 1: una subclase de date sin hash es un feriado válido
    def test_feriado_de_subclase_sin_hash(self):
        class FechaSinHash(date):
            __hash__ = None

        lunes = date(2026, 11, 23)
        feriados = [FechaSinHash(2026, 11, 23), FechaSinHash(2026, 11, 23)]
        self.assertEqual(dias_habiles(lunes, lunes, feriados), 0)
        self.assertEqual(dias_habiles(lunes, date(2026, 11, 27), feriados), 4)

    # Comprobación cruzada del conteo aritmético contra un recorrido día por día
    def test_coincide_con_recorrido_dia_a_dia(self):
        inicio_base = date(2026, 1, 1).toordinal()
        for desplazamiento in range(7):
            for largo in range(0, 30):
                inicio = date.fromordinal(inicio_base + desplazamiento)
                fin = date.fromordinal(inicio_base + desplazamiento + largo)
                esperado = sum(
                    1
                    for ordinal in range(inicio.toordinal(), fin.toordinal() + 1)
                    if date.fromordinal(ordinal).weekday() < 5
                )
                with self.subTest(inicio=inicio, fin=fin):
                    self.assertEqual(dias_habiles(inicio, fin), esperado)


if __name__ == "__main__":
    unittest.main()
