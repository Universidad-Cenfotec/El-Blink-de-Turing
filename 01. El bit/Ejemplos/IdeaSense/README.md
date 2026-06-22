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
