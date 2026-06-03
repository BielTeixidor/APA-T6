# Expresiones Regulares

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Fulano Mengano Zutano

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es aprender a usar las expresiones regulares. En concreto, su
> implementación en Python. A los profesores de la asignatura les importa un pimiento si
> usted conoce alguna biblioteca que hace el mismo trabajo de manera más sencilla y/o
> eficiente; su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.
 
## Fecha de entrega: 7 de junio a medianoche

## Tratamiento de ficheros de notas

Con el final de curso llega la ardua tarea de evaluar las tareas realizadas por los alumnos durante el
mismo. Para facilitar esta tarea, se dispone de la clase `Alumno` que proporciona los datos
fundamentales de cada alumno: su número de identificación (`numIden`), su nombre completo 
(`nombre`) y la lista de notas obtenidas a lo largo del curso (`notas`). La clase también
proporciona métodos para añadir una nota al expediente del alumno (`__add__()`), para obtener
la representación *oficial* del mismo (`__repr__()`) y para obtener la representación
*bonita* (`__str__()`).

La definición de la clase `Alumno`, disponible en `alumno.py`, es:

```python
class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'
```

A menudo, las notas de los alumnos se almacenan en ficheros de texto en los que los datos de cada alumno
ocupan una línea con los distintos valores separados por espacios y/o tabuladores.

El ejemplo siguiente muestra un fichero típico con las notas de tres alumnos:

```text
171 Blanca Agirrebarrenetse 10  	9 	  9.5
23  Carles Balcell de Lara  5 	    5 	  4.5  	5.2
68  David Garcia Fuster 	7.75    5.25  8   
```

Añada al fichero `alumno.py` la función `leeAlumnos(ficAlum)` que lea un fichero de texto con los datos de 
todos los alumnos y devuelva un diccionario en el que la clave sea el nombre de cada alumno y su contenido 
el objeto `Alumno` correspondiente.

La función deberá cumplir los requisitos siguientes:

- Sólo debe realizar lo que se indica; es decir, debe leer el fichero de texto que se le pasa como único
  argumento y devolver un diccionario con los datos de los alumnos.
- El análisis de cada línea de texto se realizará usando expresiones regulares.
- La función `leeAlumnos()` debe incluir, en su cadena de documentación, la prueba unitaria siguiente según
  el formato de la biblioteca `doctest`, donde el fichero `'alumnos.txt'` es el fichero mostrado como ejemplo
  al principio de este enunciado:

  ```python
  >>> alumnos = leeAlumnos('alumnos.txt')
  >>> for alumno in alumnos:
  ...     print(alumnos[alumno])
  ...
  171     Blanca Agirrebarrenetse 9.5
  23      Carles Balcells de Lara 4.9
  68      David Garcia Fuster     7.0
  ```

  - Evidentemente, es responsabilidad del autor comprobar que la prueba unitaria se pasa satisfactoriamente
    antes de la entrega de la tarea.

  - Para evitar que diferencias debidas a espacios en blanco o tabuladores den lugar a error, se recomienda
    efectuar las pruebas unitarias con la opción `doctest.NORMALIZE_WHITESPACE`. Por ejemplo,
    `doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)`.


## Análisis de expresiones horarias

En casi todos los idiomas más habituales, cualquier hora puede reducirse al formato estándar HH:MM, donde HH es 
un número de dos dígitos, que representa la hora y está comprendido entre 00 y 23, y MM es otro número de dos 
dígitos, que representa el minuto y está comprendido entre 00 y 59.

No obstante, en el lenguaje hablado, es raro usar este formato estándar. En el caso del castellano, existe una
gran variedad de formatos. La lista siguiente alguna de las posibilidades más frecuentes, aunque existen bastantes
más:

- **08:27**

  Es el formato estándar. Cuando la hora es menor que 10, es posible representarla con
  dos dígitos (08:27), o sólo uno (8:27). Los minutos se representan siempre con dos (8:05).

- **8h27m**

  Las horas o minutos menores que 10 pueden representarse usando uno o dos dígitos. Las horas
  *en punto* pueden indicarse sin minutos (8h).

- **8 en punto**

  Las horas exactas suelen indicarse con la partícula *'en punto'*. En ese caso, es
  habitual omitir la letra *h* después de la cifra.

  Otras alternativas semejantes son las *'8 y cuarto'*, las *'8 y media'* o las *'8 menos cuarto'*.

  En todos estos casos, el reloj empleado será de 12 horas y empezando en 1 (de 1 a 12). El
  resultado será ambiguo, ya que no sabremos si una cierta hora es AM o PM, pero así es cómo
  se suele hablar (la gente queda a *'las 11 en punto'* para ir a una fiesta, no a las
  *'las 23 en punto'*). El resultado se devolverá siempre en el rango de 00:00 a 11:59.

- **... de la mañana**

  Las expresiones horarias entre las 4 y las 12 pueden ir seguidas de la partícula *'de la mañana'*.

  Análogamente, las horas entre las 12 y las 3 pueden ir seguidas de *'del mediodía'*, las horas entre
  las 3 y las 8 pueden serlo de *'de la tarde'*, entre 8 y 4 de *'de la noche'* y entre 1 y
  6 de *'de la madrugada'*.

  En estos casos, el reloj empleado es siempre de 12 horas (nunca se dice *'las 18 de la tarde'*, sino
  *'las 6 de la tarde'*). Además la hora no puede ser cero, sino que, en ese caso, se usaría 12.

### Tarea: normalización de las expresiones horarias de un texto

Escriba el fichero `horas.py` con la función `normalizaHoras(ficText, ficNorm)`, que lee el fichero de
texto `ficText`, lo analiza en busca de expresiones horarias y escribe el fichero `ficNorm` en el que
éstas se expresan según el formato normalizado, con las horas y los minutos indicados por dos dígitos
y separados por dos puntos (08:27).

Cada línea del fichero puede contener, o no, una o más expresiones horarias, pero éstas nunca aparecerán
partidas en más de una línea.

Las horas con expresión incorrecta, por ejemplo, *'17:5'* (en la expresión normalizada deben usarse dos
dígitos para expresar los minutos) u *'11 de la tarde'* (la tarde nunca llega hasta esa hora), deben
dejarse tal cual.

Para la evaluación de la tarea se usará un texto con unas cien expresiones horarias, que incluirán tanto
expresiones correctas como incorrectas. Una parte de la nota dependerá de la precisión en su normalización.

Se recomienda empezar normalizando textos que sólo contengan expresiones correctas del tipo más sencillo;
es decir, con la forma *'18h45m'*. La consecución de este objetivo garantiza una nota mínima de notable
bajo (7). La extensión al resto de formatos indicados y la detección de expresiones incorrectas serán
necesarias para alcanzar la nota máxima (10).

La tabla siguiente muestra un ejemplo de texto antes y después de su normalización, incluyendo tanto
expresiones horarias **correctas** como <span style="color:red">**incorrectas**</span>.

### Ejemplo de normalización de las expresiones horarias de un texto

Las líneas siguientes muestran ejemplos de expresiones horarias, tanto correctas como incorrectas. Las
mismas expresiones se encuentran en el fichero `horas.txt`, que puede usar para comprobar el correcto
funcionamiento de su función.

#### Expresiones válidas

> - La llegada del tren está prevista a las **18:30**
> - La llegada del tren está prevista a las **18:30**

> - Tenía su clase entre las **8h** y las **10h30m**
> - Tenía su clase entre las **08:00** y las **10:30**

> - Se acaba a las **4 y media de la tarde**
> - Se acaba a las **16:30**

> - Empieza a trabajar a las **7h de la mañana**
> - Empieza a trabajar a las **07:00**

> - Es lo mismo **5 menos cuarto** que **4:45**
> - Es lo mismo **04:45** que **04:45**

> - Tenemos descanso hasta las **17h5m**
> - Tenemos descanso hasta las **17:05**

> - Las campanadas son a las **12 de la noche**
> - Las campanadas son a las **00:00**

#### Expresiones incorrectas

> - Son exactamente las $\textbf{\color{red}17:5}$
> - Son exactamente las $\textbf{\color{red}17:5}$

> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$
> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$

> - El examen es a las $\textbf{\color{red}17 de la tarde}$
> - El examen es a las $\textbf{\color{red}17 de la tarde}$

> - Cenamos en las $\textbf{\color{red}7}$ puertas
> - Cenamos en las $\textbf{\color{red}7}$ puertas

> - No llegará antes de las $\textbf{\color{red}1h78m}$
> - No llegará antes de las $\textbf{\color{red}1h78m}$

> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó
> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó

> - Quedamos a las $\textbf{\color{red}23 en punto}$
> - Quedamos a las $\textbf{\color{red}23 en punto}$


#### Entrega

##### Ficheros `alumno.py` y `horas.py`

- Ambos ficheros deben incluir una cadena de documentación con el nombre del alumno o alumnos
  y una descripción de su contenido.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el
  uso de los estándares marcados por PEP-ocho.

##### Ejecución de los tests unitarios de `alumno.py`

![doctest-alumno](doctest-alumno.png)

##### Código desarrollado

###### `alumno.py` 

```python
"""
Tratamiento de ficheros de notas de alumnos mediante expresiones regulares.

Autor: Biel Teixidor Cladellas

Este fichero define la clase 'Alumno', que almacena el número de
identificación, el nombre completo y la lista de notas de un alumno, y la
función 'leeAlumnos()', que lee un fichero de texto con los datos de varios
alumnos y devuelve un diccionario indexado por el nombre de cada uno.
"""

import re


class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlum):
    """
    Lee el fichero de texto 'ficAlum' con los datos de los alumnos y devuelve
    un diccionario en el que la clave es el nombre de cada alumno y el valor el
    objeto 'Alumno' correspondiente.

    Cada línea del fichero contiene el número de identificación, el nombre
    completo y la lista de notas, separados por espacios y/o tabuladores.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171 Blanca Agirrebarrenetse 9.5
    23 Carles Balcell de Lara 4.9
    68 David Garcia Fuster     7.0
    """
    patron = r'(\d+)\s+([^\d]+?)\s+([\d.]+(?:\s+[\d.]+)*)\s*$'

    alumnos = {}
    with open(ficAlum, 'rt', encoding='utf-8') as fichero:
        for linea in fichero:
            encaje = re.match(patron, linea)
            if encaje:
                numIden = int(encaje.group(1))
                nombre = encaje.group(2)
                notas = [float(nota) for nota in encaje.group(3).split()]
                alumnos[nombre] = Alumno(nombre, numIden, notas)

    return alumnos


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
```

###### `horas.py`

```python
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

```

##### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y
visualizarse correctamente en el repositorio, incluyendo la imagen con la ejecución de
los tests unitarios y el realce sintáctico del código fuente insertado.

##### Y NADA MÁS

Sólo se corregirá el contenido de este fichero `README.md` y los códigos fuente `alumno.py`
y `horas.py`. No incluya otros ficheros con código fuente, notebooks de Jupyter o explicaciones
adicionales; simplemente, no se tendrán en cuenta para la evaluación de la tarea. Evidentemente,
sí puede añadir ficheros con las imágenes solicitadas en el enunciado, pero éstas deberán ser
visualizadas correctamente desde este mismo fichero al acceder al repositorio de la tarea.
