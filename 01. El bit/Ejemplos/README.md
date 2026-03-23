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

## Ejemplo 6: El Ruido del Universo (El Pin Flotante)

Como hemos visto, el ruido eléctrico no es una imperfección accidental; es inevitable y omnipresente. En computación solemos pensar que si no conectamos nada a un pin, su valor natural será "0". Esto es falso. El silencio eléctrico absoluto no existe por defecto, debe ser construido (forzando el voltaje a tierra).

Cuando dejas un pin desconectado (flotando en el aire), la pieza de metal actúa como una pequeña antena. El pin comienza a absorber el ruido electromagnético del ambiente: la radiodifusión, el parpadeo de las luces fluorescentes, o incluso la estática de tu ropa.

En este código, le pido a un pin analógico al que no hay nada conectado que me lea el mundo. Al aplicarle nuestro clásico umbral a esta señal fantasma, el resultado no es un cero constante, sino el caos: un bit que oscila impredeciblemente entre 0 y 1. Este ejemplo demuestra visualmente que, para la máquina, la "nada" física es en realidad una tormenta de energía, justificando por qué el bit y los umbrales son estrictamente necesarios para que la lógica sobreviva al mundo físico.

**Código:** 06_ruido_universo.py

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

ib = IdeaBoard()

# Usamos un pin analógico sin NADA conectado a él.
# Se convierte en una antena para el ruido electromagnético.
pin_flotante = ib.AnalogIn(board.IO33) 

# Un umbral arbitrario a la mitad de la capacidad del ADC (0-65535)
UMBRAL = 32000 

while True:
    # 1. Leemos el caos electromagnético del ambiente
    ruido_crudo = pin_flotante.value
    
    # 2. Obligamos al caos a tomar una forma binaria
    if ruido_crudo > UMBRAL:
        bit_aleatorio = 1
        ib.pixel = (50, 0, 50)  # Morado para evidenciar el 1
    else:
        bit_aleatorio = 0
        ib.pixel = (0, 0, 0)    # Apagado para el 0
        
    # Verás que el valor crudo fluctúa salvajemente y el bit salta sin control.
    print(f"Ruido absorbido: {ruido_crudo:<5} -> Bit caótico: {bit_aleatorio}")
    
    time.sleep(0.1)
```

## Ejemplo 7: El Tiempo Roto (El Rebote Mecánico)

Nosotros creemos que al presionar un botón ocurre una transición limpia e instantánea de 0 a 1. Es la ilusión del mundo digital. Pero la física es elástica y violenta.

A nivel microscópico, cuando dos placas de metal (como las de un botón o un cable) chocan, no se unen de inmediato. Rebotan, vibran y chocan varias veces durante un par de milisegundos. Para nosotros es un instante imperceptible, pero el reloj del microcontrolador divide el tiempo en fracciones minúsculas. Para él, ese único "clic" es una avalancha ensordecedora de ceros y unos alternándose a gran velocidad.

En este código capturamos ese choque. Al leer un botón de forma excesivamente rápida, documentamos el rebote físico antes de que la señal se estabilice en un bit definitivo. Este es el motivo por el cual, en proyectos más grandes, debemos programar técnicas de "antirrebote" (debounce) usando el tiempo para ignorar la vibración física y extraer de ella una sola decisión lógica limpia.

**Código:** 07_rebote_mecanico.py

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------

import board
import digitalio
from ideaboard import IdeaBoard

ib = IdeaBoard()

# Configuramos un pin digital puro.
# Puedes simular el botón tocando el pin IO27 con un cable conectado a GND.
boton = digitalio.DigitalInOut(board.IO27)
boton.switch_to_input(pull=digitalio.Pull.UP) # Estado natural en 1 (Alto)

print("Esperando colisión física (conecta el pin IO27 a GND)...")

while True:
    estado_anterior = boton.value
    
    # Bucle extremadamente rápido para atrapar la vibración del metal
    while boton.value == estado_anterior:
        pass # El reloj avanza, no hacemos nada hasta que ocurra un cambio
    
    # ¡Ocurrió un cambio! Atrapamos las siguientes 25 lecturas a máxima velocidad
    lecturas_rebote = []
    for _ in range(25):
        # Invertimos la lógica (si es False/GND lo llamamos 1 para leerlo mejor)
        bit = 1 if not boton.value else 0 
        lecturas_rebote.append(bit)
        
    # Imprimimos la radiografía del choque físico.
    # En lugar de un salto limpio de 0 a 1, verás el caos del metal: [0, 1, 0, 1, 1, 0, 1...]
    print(f"Avalancha del rebote: {lecturas_rebote}")
    
    # Pausa para poder leer la consola y prepararnos para el siguiente intento
    time.sleep(1)
```

## Ejemplo 8: La Autopsia del Toque (Capacitancia Cruda)
Este código es la disección de cómo el microcontrolador muestrea el mundo. Nada en la naturaleza es mágicamente binario, ni siquiera el sofisticado campo electromagnético de los pines táctiles capacitivos.

A menudo, las librerías de programación ocultan la verdad entregándonos directamente un True o un False al tocar un pin. Aquí rompemos esa caja negra. En lugar de pedirle a la máquina la decisión final, le exigimos ver la magnitud física continua que está midiendo: la capacitancia cruda.

Verás cómo, a medida que acercas tu dedo sin llegar a tocar el metal, el número comienza a crecer gradualmente. Al mismo tiempo, imprimimos el umbral interno de la placa, esa frontera arbitraria que impone el límite. Demostramos así en tiempo real cómo la presencia física de un humano empuja una variable analógica hasta obligarla a cruzar la línea imaginaria donde la máquina, finalmente, declara el nacimiento del bit.

**Código:** 08_autopsia_toque.py

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------

import board
import touchio
import time
from ideaboard import IdeaBoard

ib = IdeaBoard()

# Configuramos nuestro sensor capacitivo en el pin IO4
toque = touchio.TouchIn(board.IO4)

print("--- Disección del Campo Capacitivo ---")
print("Acerca tu dedo al pin IO4 lentamente, sin llegar a tocarlo.")
time.sleep(2)

while True:
    # 1. LA MAGNITUD FÍSICA: Leemos la alteración del campo eléctrico
    # Es un número que sube conforme te acercas.
    valor_crudo = toque.raw_value
    
    # 2. EL CRITERIO DE LA MÁQUINA: El umbral interno calculado por la placa
    frontera = toque.threshold
    
    # 3. EL JUICIO DIGITAL: Lo que la librería hace en secreto
    if valor_crudo > frontera:
        bit = 1
        ib.pixel = (0, 0, 255) # Azul (Tocado / Umbral superado)
    else:
        bit = 0
        ib.pixel = (0, 0, 0)   # Apagado (En calma / Por debajo del umbral)
        
    # Comparamos la física (el número que sube), la barrera y el nacimiento del bit
    print(f"Física: {valor_crudo:<4} | Frontera: {frontera} | Bit: {bit}")
    
    time.sleep(0.1)
```
