# Cuando el comportamiento tiene memoria

Hasta ahora he utilizado las Máquinas de Estados para organizar la ejecución de mis programas. Sin embargo, su verdadero potencial aparece cuando las entiendo como un mecanismo para construir comportamientos que evolucionan con el tiempo.

Gracias a ellas, puedo hacer que un sistema recuerde información, espere el momento adecuado para actuar y tome decisiones según su estado interno, en lugar de responder únicamente a la entrada que recibe en un instante determinado.

La tarjeta **IdeaSense** resulta especialmente adecuada para explorar esta idea. Sus botones, la matriz de LEDs y sus sensores permiten desarrollar sistemas que no solo reaccionan a los estímulos del entorno, sino que también conservan información y representan visualmente su estado interno.

En los siguientes ejemplos aplicaré este principio de tres maneras diferentes. Primero construiré un sistema capaz de recordar una selección realizada por el usuario. Después utilizaré una Máquina de Estados para convertir un sensor táctil en un interruptor confiable, evitando múltiples activaciones accidentales. Finalmente, emplearé el acelerómetro para distinguir entre movimiento y reposo, filtrando las variaciones propias del mundo físico.

En todos los casos aparece la misma idea fundamental: el comportamiento del sistema ya no depende únicamente de la entrada actual, sino también del estado en el que se encuentra. Esta pequeña diferencia transforma un programa puramente reactivo en un sistema capaz de tomar decisiones de una manera mucho más organizada.

# Ejemplo 1: Memoria Visual y Eventos

Al conectar la placa **IdeaSense** a mi **IdeaBoard**, aumento las posibilidades de interacción con el mundo físico. Ahora cuento con tres botones dedicados y una matriz de LEDs de 5×5.

Mi primer impulso al programar podría ser crear un sistema puramente reactivo:

> Si mantengo presionado el botón A, se dibuja la letra A; si lo suelto, se borra.

Sin embargo, mediante el pensamiento computacional puedo ir más allá de estos reflejos básicos. Me planteo una pregunta diferente:

**¿Qué ocurre si quiero que el sistema recuerde mi selección y la muestre durante un tiempo específico sin necesidad de mantener el botón presionado?**

En este escenario, interpreto las pulsaciones de los botones como eventos que provocan transiciones entre distintos estados. Cuando ocurre una transición, la placa cambia su comportamiento: dibuja la letra correspondiente en la matriz y controla el tiempo necesario antes de regresar al estado inicial.

Mientras permanece dentro de un estado determinado, el programa mantiene ese comportamiento independientemente de que el botón continúe presionado. La acción deja de depender únicamente de la entrada física inmediata y pasa a depender de la información almacenada dentro de la Máquina de Estados.

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

> **Importante:** Al observar este código, puedo notar que la carga cognitiva se reduce considerablemente. La función `dibujar_en_matriz()` encapsula la lógica necesaria para representar una imagen en la matriz de LEDs.

> De esta forma, las funciones de estado pueden concentrarse en responder preguntas más importantes: **cuándo debe ocurrir una acción y por qué debe ocurrir**. Cada estado evalúa las condiciones necesarias, decide si debe permanecer activo o realizar una transición, mientras que la función de dibujo únicamente ejecuta la representación visual solicitada.

> Este diseño refuerza una idea central del capítulo: separar la intención lógica de la implementación física permite crear programas más claros, mantenibles y fáciles de ampliar.

# Ejemplo 2: El Interruptor Capacitivo Visual

En el ejemplo anterior utilicé la Máquina de Estados para recordar una selección durante un tiempo determinado. Ahora aplicaré el mismo concepto con un propósito diferente: garantizar que una única interacción física produzca una sola activación lógica.

La **IdeaBoard** dispone de pines táctiles capacitivos capaces de detectar la presencia de un dedo mediante cambios en la capacitancia eléctrica. Sin embargo, si leo continuamente este sensor sin una estrategia de control, una misma pulsación puede generar múltiples activaciones mientras el usuario mantiene el dedo colocado.

Para solucionar este problema, dividiré la interacción en dos fases claramente diferenciadas:

1. **Detección del toque:** el sistema espera hasta identificar una nueva interacción.
2. **Espera de liberación:** el sistema permanece bloqueado hasta que el usuario retire el dedo, permitiendo una nueva activación únicamente después de liberar el sensor.

La **IdeaSense** funcionará como un elemento visual que representa el estado actual del sistema. Cada vez que se detecte un toque válido, la matriz de LEDs cambiará su dibujo mostrando la nueva condición lógica.

De esta manera, la Máquina de Estados funciona como un filtro de eventos físicos. En lugar de reaccionar repetidamente ante una señal mantenida, interpreta una interacción completa: presionar → procesar → liberar.

## Código: `02_ideasense_touch_sm.py`

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

> **Importante:** El estado `ESPERANDO_LIBERACION` funciona como un mecanismo de protección. Su función es evitar que una misma pulsación física sea interpretada como múltiples eventos lógicos.

> Sin esta Máquina de Estados, mientras el usuario mantuviera el dedo sobre el sensor, el programa podría ejecutar repetidamente la acción de cambio, provocando comportamientos inestables como cambios rápidos entre el **Check** y la **X**.

> Este ejemplo muestra cómo una Máquina de Estados puede transformar una señal física continua en un evento digital limpio y controlado. La interacción humana deja de depender únicamente de la lectura instantánea del sensor y pasa a tener una secuencia definida de comportamiento.

# Ejemplo 3: El Detector de Actividad (Movimiento vs. Reposo)

Para una persona resulta sencillo distinguir entre una placa inmóvil y otra que está siendo agitada. Sin embargo, un acelerómetro no entrega directamente información como "la placa se está moviendo" o "la placa está quieta". El sensor únicamente proporciona valores de aceleración en diferentes ejes, y es el programa quien debe interpretar esos datos.

Cuando la placa permanece en reposo, el acelerómetro continúa midiendo la aceleración producida por la gravedad terrestre. Por esta razón, una lectura constante no necesariamente representa movimiento. Para detectar actividad real debo observar los cambios que ocurren entre mediciones consecutivas.

Para resolver este problema utilizaré dos estrategias complementarias:

1. **Cálculo del Delta:** comparo la lectura actual con la lectura anterior para identificar cambios significativos en la aceleración.
2. **Temporizador de estabilidad:** después de detectar movimiento, el sistema exige permanecer durante dos segundos sin cambios importantes antes de regresar al estado **QUIETO**.

De esta manera, pequeñas variaciones del sensor o vibraciones momentáneas no provocan cambios constantes entre estados. El sistema obtiene un comportamiento más estable y cercano a una interpretación humana de movimiento y reposo.

## Código: `03_ideasense_actividad_sm.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Proyecto: Detector de Actividad IdeaSense
# Autores: Ph. Tomás de Camino Beck, Fiorella Perez, 
#          Aylin Salazar Delgado, Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideaboard import IdeaBoard
from ideasense import IdeaSense
from StateMachine import StateMachine

# 1. Inicialización
ib = IdeaBoard()
idea = IdeaSense()

# 2. Abstracción visual para la matriz
DIBUJO_REPOSO = [(2,2)]  # Un simple punto central (Durmiendo)
DIBUJO_ACTIVO_A = [(1,1), (2,1), (3,1), (1,3), (2,3), (3,3), (1,2), (3,2)]  # Cuadro
DIBUJO_ACTIVO_B = [(0,0), (4,0), (0,4), (4,4), (2,2)]  # Puntos en las esquinas

# 3. Estados y Variables
QUIETO = "quieto"
MOVIENDOSE = "moviendose"

# Ajusta este valor (ej. 0.5 a 1.5) para hacerlo más o menos sensible.
UMBRAL_MOVIMIENTO = 1.5
ultimo_movimiento_detectado = 0.0

# Guardamos la primera lectura para tener un punto de comparación
last_ax, last_ay, last_az = idea.accel

def dibujar_en_matriz(coordenadas):
    idea.matrix.fill(0)
    for x, y in coordenadas:
        idea.matrix[x, y] = 1
    idea.matrix.show()

def hay_movimiento():
    """Evalúa si la placa cambió de velocidad, ignorando la gravedad estática"""
    global last_ax, last_ay, last_az
    
    ax, ay, az = idea.accel
    
    # Calculamos cuánto cambió la aceleración en cada eje
    cambio_x = abs(ax - last_ax)
    cambio_y = abs(ay - last_ay)
    cambio_z = abs(az - last_az)
    
    # Actualizamos la memoria para la siguiente vuelta
    last_ax, last_ay, last_az = ax, ay, az
    
    # Sumamos los cambios. Si la placa está quieta, el cambio será casi 0.
    cambio_total = cambio_x + cambio_y + cambio_z
    return cambio_total > UMBRAL_MOVIMIENTO

# 4. Funciones de Estado
def estado_quieto():
    global ultimo_movimiento_detectado
    
    ib.pixel = (0, 0, 255)  # Azul tenue: Reposo
    dibujar_en_matriz(DIBUJO_REPOSO)
    
    if hay_movimiento():
        print("¡Movimiento detectado! Despertando...")
        ultimo_movimiento_detectado = time.monotonic()
        return MOVIENDOSE
        
    return QUIETO

def estado_moviendose():
    global ultimo_movimiento_detectado
    
    ib.pixel = (255, 100, 0)  # Naranja: Activo/Alerta
    
    # Animación de actividad alternando dibujos
    if int(time.monotonic() * 8) % 2 == 0:
        dibujar_en_matriz(DIBUJO_ACTIVO_A)
    else:
        dibujar_en_matriz(DIBUJO_ACTIVO_B)
        
    if hay_movimiento():
        ultimo_movimiento_detectado = time.monotonic()
        
    # Condición de salida: ¿Han pasado 2 segundos sin picos de movimiento?
    tiempo_sin_moverse = time.monotonic() - ultimo_movimiento_detectado
    if tiempo_sin_moverse > 2.0:
        print("El sistema se ha calmado. Volviendo a reposo.")
        return QUIETO
        
    return MOVIENDOSE

# 5. Orquestación
sm = StateMachine(initial_state=QUIETO)
sm.add_state(QUIETO, estado_quieto)
sm.add_state(MOVIENDOSE, estado_moviendose)

print("--- Monitor de Actividad Iniciado ---")
while True:
    sm.step()
    time.sleep(0.05)
```

> **Importante:** Este patrón de diseño permite separar las lecturas del mundo físico de las decisiones del programa.

> Al calcular el cambio entre mediciones consecutivas (**Delta**) se obtiene una referencia más útil para detectar actividad, ya que se presta atención a las variaciones producidas por el movimiento y no únicamente al valor absoluto del acelerómetro.

> Además, el temporizador de estabilidad evita que el sistema cambie inmediatamente a reposo ante una pequeña pausa. Esto genera una respuesta más natural: la placa debe permanecer realmente tranquila durante un período definido antes de considerarse nuevamente inactiva.

# Reflexión final: De programas reactivos a sistemas con comportamiento

Los tres ejemplos muestran una misma idea aplicada en diferentes situaciones:

- En el primer ejemplo, la Máquina de Estados permitió que el sistema **recordara una decisión del usuario** y mantuviera una representación visual durante un tiempo determinado.
- En el segundo ejemplo, permitió transformar una señal física continua en un **evento digital controlado**, evitando activaciones repetidas.
- En el tercero, permitió interpretar información del entorno y construir una respuesta más inteligente frente a datos imperfectos provenientes de un sensor.

La importancia de las Máquinas de Estados no está únicamente en cambiar entre funciones. Su verdadero valor aparece cuando permiten representar la memoria interna de un sistema.

Un programa tradicional responde únicamente a la pregunta:

> ¿Qué está ocurriendo ahora?

Un sistema basado en estados también puede responder:

> ¿Qué ocurrió antes?  
> ¿Qué estoy esperando?  
> ¿Qué condición necesito cumplir para cambiar mi comportamiento?

Esta capacidad de conservar contexto es la base de muchos sistemas modernos: robots, dispositivos inteligentes, interfaces interactivas y sistemas embebidos.

La **IdeaSense** permite observar esta transición de una manera tangible. Los botones generan eventos, los sensores aportan información del mundo real y la matriz de LEDs permite visualizar el estado interno del sistema.

Cuando un programa comienza a tener memoria, deja de ser una simple colección de instrucciones y empieza a comportarse como un sistema capaz de percibir, decidir y actuar.
