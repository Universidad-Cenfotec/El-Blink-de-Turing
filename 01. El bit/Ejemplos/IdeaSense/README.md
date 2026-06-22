# Computación discreta en el IdeaSense

Todo lo que hemos discutido sobre la construcción del bit y la discretización del mundo físico cobra una nueva dimensión con la tarjeta **IdeaSense**. Mientras que con interruptores y potenciómetros extraíamos decisiones del voltaje, esta tarjeta nos permite interactuar con fuerzas físicas más complejas. Sin embargo, el principio fundamental sigue siendo el mismo:

> El mundo físico no nos entrega bits por defecto; los bits son fronteras lógicas que nosotros debemos construir.

---

# Ejemplo 1: El Bit Gravitacional (El peso de una decisión)

El universo no es binario. La gravedad actúa sobre el IdeaSense de forma continua y con infinitos matices, y el acelerómetro registra esa fuerza como un flujo constante de números con decimales. Pero la computación digital no puede operar sobre esa inmensidad inestable; necesita certezas absolutas. Necesita bits.

En este ejemplo, vamos a fabricar un bit a partir de la fuerza de gravedad. El sensor nos entregará la realidad continua (aceleración en el eje X), pero nosotros trazaremos una línea estricta en el código: **el umbral**.

Al obligar a esa fuerza física a cruzar la línea para ser reconocida, estamos colapsando el espacio continuo en un estado discreto. Para la máquina, a partir de ese umbral, la gravedad deja de ser una fuerza infinita y se convierte simplemente en un **0** o un **1**.

## Código: `01_bit_gravitacional.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideasense import IdeaSense 

# Inicialización
sense = IdeaSense()

# La gravedad es continua. Definimos el umbral donde nacerá nuestro bit.
# Si la fuerza supera este número, declaramos un 1 lógico (inclinado).
UMBRAL_INCLINACION = 3.0 

print("--- La Fabricación del Bit Gravitacional ---")
time.sleep(2)

while True:
    # 1. LA MATERIA PRIMA (Mundo Analógico):
    # Leemos la fuerza de gravedad continua.
    aceleracion_x, aceleracion_y, aceleracion_z = sense.accel
    
    # Limpiamos la matriz 5x5 en cada ciclo
    sense.matrix.fill(0)
    
    # 2. LA EXTRACCIÓN DEL BIT (El Juicio Lógico)
    if aceleracion_x > UMBRAL_INCLINACION:
        # La fuerza superó la frontera. Nace el bit (1 lógico positivo).
        bit = 1
        
        # Materializamos el bit encendiendo un píxel a la derecha
        sense.matrix[4, 2] = 1
        estado = "1 (Inclinado Der)"
        
    elif aceleracion_x < -UMBRAL_INCLINACION:
        # La fuerza cruzó la frontera negativa.
        # Sigue siendo un estado activo (1 lógico).
        bit = 1
        
        # Materializamos el bit encendiendo un píxel a la izquierda
        sense.matrix[0, 2] = 1
        estado = "1 (Inclinado Izq)"
        
    else:
        # El valor físico no alcanza el umbral.
        # La máquina ignora las pequeñas fluctuaciones y declara un cero absoluto.
        bit = 0
        
        # Representamos el cero absoluto en el centro
        sense.matrix[2, 2] = 1
        estado = "0 (Plano / Ruido)"

    # 3. AUTOPSIA DEL DATO:
    # Comparamos el caos físico con el orden digital
    print(
        f"Magnitud Física (X): {aceleracion_x:>6.2f}  |  "
        f"Decisión Lógica (Bit): {estado}"
    )
    
    # Mostramos el estado del bit en la matriz
    sense.matrix.show()
    
    time.sleep(0.2)
```

---

# Para reflexionar sobre este código

## El ruido no es información

Cuando la tarjeta está plana sobre la mesa, si observas la consola, notarás que la **Magnitud Física** no es un cero perfecto. Podrías observar valores como:

```text
0.15
-0.05
0.22
```

Estos pequeños cambios son consecuencia del ruido del sensor y de las microvibraciones del entorno.

Si no existiera nuestro umbral, la máquina intentaría reaccionar a cada uno de esos decimales. El bit **0** que fabricamos en el código no representa la ausencia de gravedad; representa una decisión matemática para ignorar pequeñas variaciones y declarar estabilidad.

---

## La compresión del universo

Cuando inclinas la tarjeta y la aceleración alcanza **3.1**, el bit cambia a **1**.

Si continúas inclinándola y la aceleración alcanza **8.5**, el bit sigue siendo **1**.

Para la lógica digital, ambas situaciones son equivalentes. No importa cuánto más inclinado esté el dispositivo. Toda la riqueza del mundo analógico se reduce a una sola pregunta:

> ¿Superó el umbral?

- Sí → `1`
- No → `0`

La discretización consiste precisamente en esta compresión de información.

---

## El píxel como evidencia

La matriz LED de **5×5** del IdeaSense no está mostrando una animación abstracta.

Cada LED se enciende porque existe una decisión lógica almacenada en la memoria del microcontrolador. El píxel iluminado es la evidencia física de que un bit ha sido creado a partir de una magnitud continua del mundo real.

Así, una fuerza gravitacional continua termina representada por:

- Un valor lógico (`0` o `1`)
- Una posición en la matriz LED
- Una decisión computacional discreta

---

# Concepto clave

> La computación digital no observa el mundo tal como es.  
> Construye fronteras, establece umbrales y transforma fenómenos continuos en estados discretos que puedan ser procesados por bits.


# Ejemplo 2: El nacimiento del bit con Luz (Histéresis)

En este código busco demostrar cómo una señal ruidosa e inestable (analógica) puede transformarse en una decisión firme y estable (digital).

En el mundo físico, la intensidad de la luz nunca es perfecta ni estática. Las sombras, el parpadeo de las lámparas y los reflejos generan un flujo constante de pequeñas variaciones. Si utilizáramos un único punto de corte para decidir si la luz representa un **1** o un **0**, el ruido provocaría que el sistema cambiara rápidamente entre ambos estados cuando la medición se encuentre cerca del umbral.

Para resolver este problema implementamos **histéresis**, una técnica que dota al sistema de una forma mínima de memoria. Una vez que se toma una decisión, el sistema se resiste a cambiarla hasta que la señal varía de manera significativa. Esto crea una zona de seguridad que protege al sistema contra las fluctuaciones del entorno.

Utilizaremos la matriz LED de **5×5** de la IdeaSense para visualizar el bit de manera clara y estable.

## Código: `02_histeresis_luz.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez López
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideasense import IdeaSense 

# Inicialización
sense = IdeaSense()

# Configuración de umbrales (zona de seguridad)
# Valores aproximados para el sensor de luz LTR303
UMBRAL_ALTO = 300  # Frontera para declarar "1" (Luz directa)
UMBRAL_BAJO = 100  # Frontera para declarar "0" (Sombra profunda)

estado_activo = False

def dibujar_cero():
    """Dibuja un '0' claro y centrado en la matriz de 5x5"""
    sense.matrix.fill(0)

    # Techo y base
    sense.matrix[1, 0] = 1
    sense.matrix[2, 0] = 1
    sense.matrix[3, 0] = 1

    sense.matrix[1, 4] = 1
    sense.matrix[2, 4] = 1
    sense.matrix[3, 4] = 1

    # Paredes laterales
    sense.matrix[0, 1] = 1
    sense.matrix[0, 2] = 1
    sense.matrix[0, 3] = 1

    sense.matrix[4, 1] = 1
    sense.matrix[4, 2] = 1
    sense.matrix[4, 3] = 1

    sense.matrix.show()

def dibujar_uno():
    """Dibuja un '1' claro y centrado en la matriz de 5x5"""
    sense.matrix.fill(0)

    # Tronco central
    sense.matrix[2, 0] = 1
    sense.matrix[2, 1] = 1
    sense.matrix[2, 2] = 1
    sense.matrix[2, 3] = 1
    sense.matrix[2, 4] = 1

    # Gancho izquierdo
    sense.matrix[1, 1] = 1

    # Base
    sense.matrix[1, 4] = 1
    sense.matrix[3, 4] = 1

    sense.matrix.show()

print("--- El Nacimiento del Bit con Luz ---")

while True:
    # 1. Lectura del mundo físico (analógico y ruidoso)
    lectura_cruda = sense.light

    # 2. Lógica con memoria (histéresis)
    if estado_activo:
        if lectura_cruda < UMBRAL_BAJO:
            estado_activo = False
    else:
        if lectura_cruda > UMBRAL_ALTO:
            estado_activo = True

    # 3. Visualización: El estado digital limpio
    if estado_activo:
        dibujar_uno()
        print(f"Luz: {lectura_cruda:>6.1f} | Decisión: 1 (Estable)")
    else:
        dibujar_cero()
        print(f"Luz: {lectura_cruda:>6.1f} | Decisión: 0 (Estable)")

    time.sleep(0.1)
```

---

# Para reflexionar sobre este código

## La memoria como filtro contra el ruido

La histéresis introduce una característica fundamental: la memoria.

Una vez que el sistema declara un **1**, no volverá inmediatamente a **0** cuando la luz disminuya ligeramente. Del mismo modo, cuando declara un **0**, no cambiará instantáneamente a **1** ante una pequeña fluctuación positiva.

Esto evita que el sistema oscile constantemente cuando la señal se encuentra cerca de una frontera.

---

## Dos fronteras en lugar de una

En lugar de utilizar un único umbral, utilizamos dos:

| Umbral | Función |
|----------|----------|
| `UMBRAL_ALTO` | Permite pasar de 0 a 1 |
| `UMBRAL_BAJO` | Permite pasar de 1 a 0 |

Entre ambos valores existe una zona donde la decisión anterior se mantiene.

Esta región es la esencia de la histéresis.

---

## El nacimiento de un bit estable

La luz es una magnitud continua.

El sensor puede producir cientos o miles de valores distintos, pero la lógica digital no necesita conocerlos todos. El sistema reduce toda esa riqueza física a una única pregunta:

> ¿La luz ha cambiado lo suficiente como para justificar una nueva decisión?

Si la respuesta es no, el estado permanece igual.

Si la respuesta es sí, nace un nuevo bit.

---

## El LED como evidencia física

Cada vez que observamos un **0** o un **1** dibujado en la matriz LED, estamos viendo el resultado de una decisión lógica tomada a partir de una señal física continua.

Los LEDs muestran únicamente el estado discreto final; todo el ruido, las fluctuaciones y la complejidad del mundo físico han sido descartados durante el proceso de discretización.

---

# Concepto clave

> La histéresis convierte una frontera frágil en una decisión robusta. Al agregar memoria al sistema, evitamos que el ruido del mundo físico destruya la estabilidad de los bits.

---

# Ejemplo 3: El nacimiento del bit con Potenciómetro (Histéresis)

En este ejemplo aplicamos el mismo principio filosófico, pero utilizando una fuente distinta: el voltaje.

El potenciómetro conectado a la IdeaBoard genera una señal analógica continua. Aunque pueda parecer estable, el voltaje siempre contiene pequeñas variaciones producidas por el ruido eléctrico, las tolerancias de los componentes y las características del convertidor analógico-digital.

Si intentáramos decidir entre **0** y **1** utilizando una única frontera matemática, la matriz LED cambiaría constantemente de estado cuando el potenciómetro estuviera cerca de ese valor.

La histéresis resuelve este problema ignorando las pequeñas fluctuaciones eléctricas y transformando el voltaje continuo en una decisión digital estable.

## Código: `03_histeresis_potenciometro.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez López
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
import board
from ideaboard import IdeaBoard
from ideasense import IdeaSense

# Inicialización
ib = IdeaBoard()
sense = IdeaSense()

# Potenciómetro en IO33
pot = ib.AnalogIn(board.IO33)

# Configuración de umbrales
UMBRAL_ALTO = 45000
UMBRAL_BAJO = 20000

estado_activo = False

def dibujar_cero():
    """Dibuja un '0' claro y centrado en la matriz de 5x5"""
    sense.matrix.fill(0)

    # Techo y base
    sense.matrix[1, 0] = 1
    sense.matrix[2, 0] = 1
    sense.matrix[3, 0] = 1

    sense.matrix[1, 4] = 1
    sense.matrix[2, 4] = 1
    sense.matrix[3, 4] = 1

    # Paredes laterales
    sense.matrix[0, 1] = 1
    sense.matrix[0, 2] = 1
    sense.matrix[0, 3] = 1

    sense.matrix[4, 1] = 1
    sense.matrix[4, 2] = 1
    sense.matrix[4, 3] = 1

    sense.matrix.show()

def dibujar_uno():
    """Dibuja un '1' claro y centrado en la matriz de 5x5"""
    sense.matrix.fill(0)

    # Tronco central
    sense.matrix[2, 0] = 1
    sense.matrix[2, 1] = 1
    sense.matrix[2, 2] = 1
    sense.matrix[2, 3] = 1
    sense.matrix[2, 4] = 1

    # Gancho izquierdo
    sense.matrix[1, 1] = 1

    # Base
    sense.matrix[1, 4] = 1
    sense.matrix[3, 4] = 1

    sense.matrix.show()

print("--- El Nacimiento del Bit con Voltaje ---")

while True:
    # 1. Lectura de la realidad analógica
    lectura_cruda = pot.value

    # 2. Lógica con memoria (histéresis)
    if estado_activo:
        if lectura_cruda < UMBRAL_BAJO:
            estado_activo = False
    else:
        if lectura_cruda > UMBRAL_ALTO:
            estado_activo = True

    # 3. Visualización: El estado digital limpio
    if estado_activo:
        dibujar_uno()
        print(f"Voltaje crudo: {lectura_cruda:>5} | Decisión: 1 (Estable)")
    else:
        dibujar_cero()
        print(f"Voltaje crudo: {lectura_cruda:>5} | Decisión: 0 (Estable)")

    time.sleep(0.1)
```

---

# Para reflexionar sobre este código

## El ruido eléctrico también existe

Aunque los circuitos electrónicos parezcan precisos, ninguna señal es perfectamente estable.

Incluso cuando el potenciómetro permanece inmóvil, las mediciones pueden variar ligeramente debido a:

- Ruido térmico.
- Interferencias electromagnéticas.
- Limitaciones del convertidor analógico-digital.
- Tolerancias de los componentes.

---

## La histéresis protege la decisión

La existencia de dos umbrales crea una zona de estabilidad.

Mientras la señal permanezca dentro de esa región, el sistema conserva la decisión previa.

Esto evita cambios innecesarios y transforma una señal analógica fluctuante en un estado lógico robusto.

---

## Del voltaje al bit

El potenciómetro puede generar decenas de miles de valores posibles entre `0` y `65535`.

Sin embargo, la lógica digital reduce toda esa complejidad a una sola variable:

```python
estado_activo
```

Toda la riqueza del mundo analógico queda comprimida en un único bit.

---

## El significado de la discretización

La discretización no consiste únicamente en convertir números continuos en números enteros.

Consiste en imponer reglas que permitan transformar fenómenos físicos ambiguos en decisiones inequívocas.

La histéresis demuestra que, para construir bits confiables, no basta con medir el mundo; también es necesario decidir cuándo ignorar sus pequeñas imperfecciones.

---

# Concepto clave

> Un bit estable no surge únicamente de una medición. Surge de una decisión lógica capaz de resistir el ruido inevitable del mundo físico.
