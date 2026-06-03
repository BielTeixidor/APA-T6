"""
Normalización de expresiones horarias mediante expresiones regulares.

Autor: Biel Teixidor Cladellas

Este fichero define la función 'normalizaHoras(ficText, ficNorm)', que lee el
fichero de texto 'ficText', busca en él expresiones horarias escritas en los
distintos formatos habituales del castellano y escribe en 'ficNorm' el mismo
texto con dichas expresiones normalizadas al formato estándar HH:MM. Las
expresiones horarias incorrectas se dejan tal cual.
"""

import re


# Para cada partícula del día se indica, mediante un diccionario, la hora del
# reloj de 24 h (0-23) que corresponde a cada hora hablada (reloj de 12 h, de
# 1 a 12). Si la hora hablada no figura en el diccionario, la expresión es
# incorrecta (p. ej. 'las 11 de la tarde').
_PERIODOS = {
    'madrugada': {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6},
    'mañana':    {4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12},
    'mediodía':  {12: 12, 1: 13, 2: 14, 3: 15},
    'tarde':     {3: 15, 4: 16, 5: 17, 6: 18, 7: 19, 8: 20},
    'noche':     {8: 20, 9: 21, 10: 22, 11: 23, 12: 0, 1: 1, 2: 2, 3: 3, 4: 4},
}

# Minutos asociados a cada partícula relativa ('en punto', 'y cuarto', ...).
_RELATIVOS = {
    'en punto': 0,
    'y cuarto': 15,
    'y media': 30,
    'menos cuarto': 45,
}


def _normaliza(encaje):
    """
    Recibe un objeto 'match' con una posible expresión horaria y devuelve su
    versión normalizada (HH:MM). Si la expresión es incorrecta, devuelve el
    texto original sin modificar.
    """
    original = encaje.group(0)

    # --- Formato estándar HH:MM ('8:27', '08:27') ---------------------------
    if encaje.group('h24') is not None:
        hora = int(encaje.group('h24'))
        minuto = int(encaje.group('m24'))
        if hora <= 23 and minuto <= 59:
            return f'{hora:02d}:{minuto:02d}'
        return original

    hora = int(encaje.group('hora'))
    hflag = encaje.group('hflag')
    minh = encaje.group('minh')
    rel = encaje.group('rel')
    per = encaje.group('per')

    # Un número suelto, sin 'h', sin partícula relativa ni de periodo, no es
    # una expresión horaria (p. ej. 'las 7 puertas').
    if hflag is None and rel is None and per is None:
        return original

    if hflag is not None:
        # Formato 'HhMm' / 'Hh'. La hora hablada y los minutos son directos.
        minuto = int(minh) if minh is not None else 0
    elif rel is not None:
        # Formato relativo: 'en punto', 'y cuarto', 'y media', 'menos cuarto'.
        rel = ' '.join(rel.split())
        minuto = _RELATIVOS[rel]
        if rel == 'menos cuarto':
            hora -= 1
    else:
        # Sólo partícula de periodo: 'las 12 de la noche'.
        minuto = 0

    if minuto > 59:
        return original

    if per is not None:
        # Reloj de 12 h ajustado a la franja del día indicada.
        hora24 = _PERIODOS[per].get(hora)
        if hora24 is None:
            return original
        return f'{hora24:02d}:{minuto:02d}'

    if rel is not None:
        # Relativo sin periodo: reloj de 12 h (1-12), resultado en 00:00-11:59.
        if not 1 <= int(encaje.group('hora')) <= 12:
            return original
        return f'{hora % 12:02d}:{minuto:02d}'

    # Formato 'HhMm' sin periodo: reloj de 24 h.
    if hora <= 23:
        return f'{hora:02d}:{minuto:02d}'
    return original


# Expresión regular que reúne todos los formatos admitidos. El orden de las
# alternativas importa: las más específicas van antes que las más generales.
_PATRON = r"""
    (?<!\d)
    (?:
        (?P<h24>\d{1,2}):(?P<m24>\d{2})                     # 8:27 / 08:27
      |
        (?P<hora>\d{1,2})
        (?:
            (?P<hflag>h)(?P<minh>\d{1,2})?m?               # 8h / 18h45m
          |
            \s+(?P<rel>en\s+punto|y\s+cuarto
                       |y\s+media|menos\s+cuarto)          # 8 y media
        )?
        (?:\s+de(?:\s+la|l)\s+
            (?P<per>mañana|mediodía|tarde|noche|madrugada))?  # de la tarde
    )
    (?!\d)
"""


def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero 'ficText', normaliza todas las expresiones horarias que
    encuentre y escribe el resultado en el fichero 'ficNorm'. Las expresiones
    horarias incorrectas se dejan sin modificar.
    """
    with open(ficText, 'rt', encoding='utf-8') as fEntrada, \
         open(ficNorm, 'wt', encoding='utf-8') as fSalida:
        for linea in fEntrada:
            fSalida.write(re.sub(_PATRON, _normaliza, linea, flags=re.VERBOSE))


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        normalizaHoras(sys.argv[1], sys.argv[2])
    else:
        normalizaHoras('horas.txt', 'horasNorm.txt')
