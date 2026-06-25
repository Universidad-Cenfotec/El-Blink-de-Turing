# Ejemplo 1: Memoria Visual y Eventos 
Al conectar la placa **IdeaSense** a nuestra **IdeaBoard**, multiplicamos nuestras formas de interactuar con el mundo físico. Ahora contamos con tres botones dedicados y una matriz de LEDs de 5x5. Nuestro primer impulso al programar podría ser crear un sistema puramente reactivo: *si mantenemos presionado el botón A, se dibuja la letra A; si lo soltamos, se borra*.

Sin embargo, mediante el pensamiento computacional podemos ir más allá de estos reflejos básicos. Nos preguntamos: ¿qué ocurre si queremos que el sistema *recuerde* nuestra selección y la muestre durante un tiempo específico sin necesidad de mantener el botón presionado? En este escenario, la Máquina de Estados actúa como intermediaria. Los botones de la IdeaSense funcionan como detonadores que modifican el "modo" del sistema. Una vez que entramos en un estado determinado, la placa dibuja la letra correspondiente en la matriz y controla el tiempo de manera autónoma, ignorando las entradas de otros botones hasta finalizar su tarea.

## Código: `01_buttons_sm.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Proyecto: Memoria Visual IdeaSense
# Autores: Ph. Tomás de Camino Beck, Fiorella Perez,
#          Aylin Salazar Delgado, Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideaboard import IdeaBoard
from ideasense import IdeaSense
from StateMachine import StateMachine

# 1. Inicialización de Hardware
ib = IdeaBoard()
idea = IdeaSense()

# 2. Abstracción visual (Coordenadas de la matriz)
LETRA_A = [(1,0),(2,0),(3,0), (0,1),(4,1),
           (0,2),(1,2),(2,2),(3,2),(4,2),
           (0,3),(4,3), (0,4),(4,4)]

LETRA_B = [(0,0),(1,0),(2,0),(3,0),
           (0,1),(4,1),
           (0,2),(1,2),(2,2),(3,2),
           (0,3),(4,3),
           (0,4),(1,4),(2,4),(3,4)]

LETRA_C = [(1,0),(2,0),(3,0),
           (0,1),(4,1),
           (0,2),
           (0,3),(4,3),
           (1,4),(2,4),(3,4)]

# 3. Definición de estados
REPOSO = "reposo"
MODO_A = "modo_a"
MODO_B = "modo_b"
MODO_C = "modo_c"

# Guarda el instante en que inicia cada estado
tiempo_inicio = 0.0

def dibujar_en_matriz(coordenadas):
    """Traduce coordenadas lógicas en LEDs encendidos."""
    idea.matrix.fill(0)
    for x, y in coordenadas:
        idea.matrix[x, y] = 1
    idea.matrix.show()

# 4. Funciones de Estado
def estado_reposo():
    global tiempo_inicio

    ib.pixel = (0, 0, 0)
    idea.matrix.fill(0)
    idea.matrix.show()

    # Detecta qué botón fue presionado
    if idea.held[0]:
        print(">>> Transición a MODO_A")
        tiempo_inicio = time.monotonic()
        return MODO_A

    elif idea.held[1]:
        print(">>> Transición a MODO_B")
        tiempo_inicio = time.monotonic()
        return MODO_B

    elif idea.held[2]:
        print(">>> Transición a MODO_C")
        tiempo_inicio = time.monotonic()
        return MODO_C

    return REPOSO

def estado_modo_a():
    ib.pixel = (0, 255, 0)  # Indicador visual del estado
    dibujar_en_matriz(LETRA_A)

    # Permanece 2 segundos antes de regresar
    if time.monotonic() - tiempo_inicio > 2.0:
        return REPOSO

    return MODO_A

def estado_modo_b():
    ib.pixel = (0, 0, 255)
    dibujar_en_matriz(LETRA_B)

    if time.monotonic() - tiempo_inicio > 2.0:
        return REPOSO

    return MODO_B

def estado_modo_c():
    ib.pixel = (255, 0, 0)
    dibujar_en_matriz(LETRA_C)

    if time.monotonic() - tiempo_inicio > 2.0:
        return REPOSO

    return MODO_C

# 5. Configuración de la máquina de estados
sm = StateMachine(initial_state=REPOSO)

sm.add_state(REPOSO, estado_reposo)
sm.add_state(MODO_A, estado_modo_a)
sm.add_state(MODO_B, estado_modo_b)
sm.add_state(MODO_C, estado_modo_c)

print("--- Interfaz Visual IdeaSense Iniciada ---")

while True:
    sm.step()  # Ejecuta el estado actual
    time.sleep(0.01)
```




## Ejemplo 2: El Interruptor Capacitivo Visual 

La IdeaBoard tiene pines táctiles (touch capacitivo). Leer este tipo de pines continuamente puede generar disparos múltiples si el usuario deja el dedo puesto una fracción de segundo de más. En este ejemplo, la Máquina de Estados divide la interacción en dos fases estables: el toque activo y la liberación.

La diferencia aquí es que utilizaremos la placa **IdeaSense** como nuestro lienzo. Cada vez que el toque es válido y seguro, la matriz de 5x5 cambiará su dibujo, reflejando el estado lógico interno del sistema.

### Código: `02_ideasense_touch_sm.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
import board
import touchio
from ideaboard import IdeaBoard
from ideasense import IdeaSense
from StateMachine import StateMachine

# 1. Inicialización de Hardware
ib = IdeaBoard()
idea = IdeaSense()
touch_pin = touchio.TouchIn(board.IO32)

# 2. Abstracción visual para la matriz
DIBUJO_CHECK = [(0,3), (1,4), (2,3), (3,2), (4,1)]
DIBUJO_EQUIS = [(0,0), (1,1), (2,2), (3,3), (4,4),
                (0,4), (1,3), (3,1), (4,0)]

def dibujar_en_matriz(coordenadas):
    idea.matrix.fill(0)
    for x, y in coordenadas:
        idea.matrix[x, y] = 1
    idea.matrix.show()

# 3. Estados
ESPERANDO_TOQUE = "esperando"
ESPERANDO_LIBERACION = "liberando"

# Variable para alternar el estado lógico
estado_toggle = False

# Estado visual inicial
dibujar_en_matriz(DIBUJO_EQUIS)
ib.pixel = (255, 0, 255)  # Magenta

# 4. Funciones de Estado
def estado_esperando():
    global estado_toggle

    if touch_pin.value:
        # Alternamos el estado lógico solo en el instante inicial del toque
        estado_toggle = not estado_toggle

        # Reflejamos el cambio tanto en el LED como en la matriz
        if estado_toggle:
            ib.pixel = (0, 0, 255)  # Azul
            dibujar_en_matriz(DIBUJO_CHECK)
        else:
            ib.pixel = (255, 0, 255)  # Magenta
            dibujar_en_matriz(DIBUJO_EQUIS)

        print("¡Toque detectado! Matriz actualizada.")
        return ESPERANDO_LIBERACION

    return ESPERANDO_TOQUE

def estado_liberando():
    # Nos quedamos atascados aquí intencionalmente hasta que no haya toque
    if not touch_pin.value:
        print("Dedo liberado. Listo para otro toque.")
        return ESPERANDO_TOQUE

    return ESPERANDO_LIBERACION

# 5. Orquestación
sm = StateMachine(initial_state=ESPERANDO_TOQUE)
sm.add_state(ESPERANDO_TOQUE, estado_esperando)
sm.add_state(ESPERANDO_LIBERACION, estado_liberando)

print("--- Interruptor Táctil Seguro con Matriz IdeaSense ---")
while True:
    sm.step()
    time.sleep(0.05)
```

> **Importante:** Nota cómo el estado `ESPERANDO_LIBERACION` sigue actuando como nuestro candado de seguridad, protegiendo tanto la lógica matemática como la visualización. Si no tuviéramos esta máquina de estados, el dibujo en la matriz parpadearía frenéticamente entre el **"Check"** y la **"X"** mientras el dedo del usuario rozara el pin capacitivo.

> **Importante:** Al observar este código, podemos notar que la carga cognitiva se reduce drásticamente. Hemos encapsulado el *cómo se dibuja* dentro de la función `dibujar_en_matriz()`. Esto nos permite hacer que las funciones de estado se concentren exclusivamente en el *cuándo* y el *por qué*. Cada estado evalúa, decide y realiza transiciones, mientras que la función de dibujo simplemente ejecuta la acción solicitada. De esta manera, reforzamos la filosofía central del capítulo: desacoplar la intención lógica de la acción física.
