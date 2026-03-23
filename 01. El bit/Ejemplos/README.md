# Ejemplos del capítulo: El Bit

He escrito estos scripts como complemento práctico de la lectura.  
Mi objetivo es materializar los conceptos filosóficos del capítulo: analizar cómo nace una decisión (un bit) a partir del ruido y cómo la manipulación del tiempo permite crear matices en el comportamiento del sistema.

Para mí, el código no es más que una herramienta que hace visibles fenómenos físicos, permitiéndonos observar, experimentar y razonar sobre ellos.

## Ejemplo 1: El nacimiento del bit (Histéresis)

En este código busco demostrar cómo una señal ruidosa e inestable (analógica) puede transformarse en una decisión firme y estable (digital).

En el mundo físico, el voltaje nunca es perfecto. Si utilizo un único punto de corte para decidir si algo es “1” o “0”, el ruido hará que el sistema dude y oscile.  
Para resolver este problema implemento **histéresis**: doto al sistema de una forma mínima de memoria. Una vez que se toma una decisión, el sistema se resiste a cambiarla hasta que la señal varía de manera significativa, creando así una **zona de seguridad** frente al ruido.

**Código:** `01_histeresis.py`

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

# Inicialización
ib = IdeaBoard()

# Potenciómetro en IO33 simulando una señal ruidosa
pot = ib.AnalogIn(board.IO33)

# Configuración de umbrales (zona de seguridad)
UMBRAL_ALTO = 45000
UMBRAL_BAJO = 20000

estado_activo = False

while True:
    lectura_cruda = pot.value

    # Lógica con memoria (histéresis)
    if estado_activo:
        # Si la decisión actual es 1, resistimos apagar.
        # Solo cambiamos si la señal cae por debajo del umbral establecido.
        if lectura_cruda < UMBRAL_BAJO:
            estado_activo = False
            print("Decisión: 0 (Apagado)")
    else:
        # Si la decisión actual es 0, resistimos encender.
        # Solo cambiamos si la señal supera el umbral establecido.
        if lectura_cruda > UMBRAL_ALTO:
            estado_activo = True
            print("Decisión: 1 (Encendido)")

    # Visualización
    # El LED muestra la DECISIÓN limpia, no el voltaje ruidoso.
    if estado_activo:
        ib.pixel = (0, 255, 0)  # Verde
    else:
        ib.pixel = (50, 0, 0)   # Rojo

    time.sleep(0.01)
```



## Ejemplo 2: La Manivela del Tiempo (PWM Manual)

Con este código ilustro la "ilusión de continuidad". El microcontrolador no sabe generar "medio voltaje" o "media luz"; solo sabe encender o apagar.

Aquí alterno manualmente esos dos estados tan rápido que tu ojo percibe un cambio de brillo suave. Con este ejemplo te demuestro que, en computación, la intensidad es, en realidad, una gestión del tiempo.


**Código:** `02_pwm_manual.py`
 ```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------

import time
import math
from ideaboard import IdeaBoard

# Inicialización
ib = IdeaBoard()

COLOR_ENCENDIDO = (0, 0, 255) # Azul
COLOR_APAGADO   = (0, 0, 0)   # Negro

DURACION_CICLO  = 0.02 

while True:
    # Efecto de respiración
    now = time.monotonic()
    intensidad = (1 + math.sin(now * 3)) / 2 

    #Calculo el reparto del tiempo (PWM)
    tiempo_on  = DURACION_CICLO * intensidad
    tiempo_off = DURACION_CICLO - tiempo_on
    
    # Pasos discretos:
    
    # Paso A: Encendido
    ib.pixel = COLOR_ENCENDIDO
    time.sleep(tiempo_on)
    
    # Paso B: Apagado
    ib.pixel = COLOR_APAGADO
    time.sleep(tiempo_off)
    
    # Al repetirlo 50 veces por segundo, tu ojo integra la luz.
```

## Ejemplo 3: Fabricando un Bit (Del Espacio a la Lógica)

Aquí utilizo uns sensor ultrasónico para ilustrar cómo se fabrica un bit.

El universo físico es continuo: una distancia puede ser 10 cm, 10.1 cm o 10.001 cm. Pero a la lógica binaria no le sirven los matices infinitos, necesita certezas absolutas.

En este código, obligo a esa realidad continua a dividirse en dos únicos estados. Al trazar una línea imaginaria (el umbral), decido que todo lo que está de un lado es "0" y todo lo que está del otro es "1". Así es como la computación proyecta su orden binario sobre el espacio físico.


**Código:** 03_bit_Ultrasónico.py

 ```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------

import board
import time
from ideaboard import IdeaBoard
from hcsr04 import HCSR04

ib = IdeaBoard()
sonar = HCSR04(board.IO26, board.IO25)

# Umbrales (histéresis)
UMBRAL_ON  = 15.0  # cm → pasa a 1
UMBRAL_OFF = 18.0  # cm → vuelve a 0

# Estado lógico inicial
bit_presencia = 0  # 0 o 1 (bit explícito)


while True:
    try:
        distancia = sonar.dist_cm()

        # Ignorar lecturas inválidas
        if distancia < 0:
            continue

        # Fabricación del bit (con memoria)
        if bit_presencia == 0 and distancia < UMBRAL_ON:
            bit_presencia = 1
        elif bit_presencia == 1 and distancia > UMBRAL_OFF:
            bit_presencia = 0

        #Respuesta digital
        if bit_presencia == 1:
            ib.pixel = (255, 255, 255)  # Estado lógico 1
        else:
            ib.pixel = (0, 0, 0)        # Estado lógico 0

        print(f"Distancia: {distancia:5.1f} cm → Bit: {bit_presencia}")

    except RuntimeError:
        pass

    time.sleep(0.1)
```

## Ejemplo 4: Anatomía de una Decisión (ADC y Umbrales)

Como hemos visto, muchas veces se enseña la computación como si los sensores 'entregaran' ceros y unos. Esa es una simplificación peligrosa: la realidad física nunca es binaria. Usaremos los cuatro sensores infrarrojos no para distinguir si estamos sobre blanco o negro, sino para observar lo que realmente ven los sensores: voltajes.

El microcontrolador traduce estos voltajes mediante el ADC en un valor crudo (0-65535), describiendo el "cuánto" pero ignorando el "qué". El bit nace después, cuando impongo un criterio sobre esa medición. Al definir un umbral arbitrario (3500), transformo una medición física en un juicio lógico. Este código expone esa disección, mostrando lado a lado la realidad continua y la decisión digital.


**Código:** 04_bit_Infrarrojos.py

 ```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------

import board
from time import sleep
from ideaboard import IdeaBoard

ib = IdeaBoard()

# Configuración: Sensores Analógicos (Lectura del ADC)
sensores = [
    ib.AnalogIn(board.IO36), 
    ib.AnalogIn(board.IO39), 
    ib.AnalogIn(board.IO34), 
    ib.AnalogIn(board.IO35)  
]

UMBRAL = 3500

while True:
    print("--- Realidad (ADC) vs. Lógica (Bit) ---")
    
    for i, sen in enumerate(sensores, start=1):
 
        lectura_adc = sen.value
        
        # El bit nace de una decisión, no directamente del sensor.
        if lectura_adc > UMBRAL:
            bit = 1 
        else:
            bit = 0 
            
        # Comparativa visual
        print(f"Sensor {i}: {lectura_adc:<5}  |  Bit: {bit}")

    print("")
    sleep(0.5)
```


## Ejemplo 5: El Botón Fantasma (El Bit Capacitivo) 

Un botón mecánico es una imposición física: o los metales hacen contacto, o no lo hacen. El circuito se cierra a la fuerza obligando a la realidad a ser binaria. Pero con este ejemplo quiero mostrarte cómo podemos extraer un bit de un fenómeno completamente invisible: un campo eléctrico.

Los pines táctiles (capacitivos) generan un pequeño campo electromagnético a su alrededor. Cuando acercas tu dedo, tu cuerpo —compuesto de agua y sales, y por tanto, conductor— altera la capacitancia de ese campo. Esta alteración no es un interruptor de encendido y apagado; es una perturbación analógica que crece conforme te acercas.

En este código, la librería lee esa magnitud física continua y aplica un umbral interno de manera silenciosa para entregarnos una decisión limpia. Si la perturbación es suficiente, el sistema colapsa esa lectura y declara un 1 (¡Tocado!). Si el campo está en calma, nos entrega un 0. El cero aquí no es la "nada", es información activa: certifica la ausencia de perturbación. Sin partes móviles, tu propio cuerpo se convierte en la variable que altera la realidad digital.

**Código:** 05_bit_capacitivo.py

```python

# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez López
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import board
import touchio
from time import sleep
from ideaboard import IdeaBoard

# Inicialización
ib = IdeaBoard()

# Configuración de los "Botones Fantasma"
# Estos pines miden continuamente la alteración del campo eléctrico
toque_1 = touchio.TouchIn(board.IO4)
toque_2 = touchio.TouchIn(board.IO32)

while True:
    # 1. Lectura del estado capacitivo 
    # La librería lee el valor analógico, aplica su propio umbral 
    # y nos entrega la decisión binaria (True = 1, False = 0).
    estado_t1 = toque_1.value  
    estado_t2 = toque_2.value

    # 2. Visualización de los estados binarios
    if estado_t1:
        # Decisión 1: Perturbación detectada en el primer pin
        print("Campo alterado en IO4  -> Bit: 1")
        ib.pixel = (0, 0, 255)   # Azul
        
    elif estado_t2:
        # Decisión 1: Perturbación detectada en el segundo pin
        print("Campo alterado en IO32 -> Bit: 1")
        ib.pixel = (255, 255, 0) # Amarillo
        
    else:
        # Decisión 0: El cero también es información (ausencia confirmada)
        print("Campo en calma         -> Bit: 0")
        ib.pixel = (0, 0, 0)     # Apagado

    # Pausa para poder leer la consola sin que la información fluya demasiado rápido
    sleep(0.2)
```
