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



## Ejemplo 2: La Manivela del Tiempo (PWM Manual)

Con este código ilustro la "ilusión de continuidad". El microcontrolador no sabe generar "medio voltaje" o "media luz"; solo sabe encender o apagar.

Aquí alterno manualmente esos dos estados tan rápido que tu ojo percibe un cambio de brillo suave. Con este ejemplo te demuestro que, en computación, la intensidad es, en realidad, una gestión del tiempo.


**Código:** `02_pwm_manual.py`
 ```python
import time
import math
from ideaboard import IdeaBoard

# Inicialización
ib = IdeaBoard()

COLOR_ENCENDIDO = (0, 0, 255) # Azul
COLOR_APAGADO   = (0, 0, 0)   # Negro

# Velocidad de "manivela" temporal (Ciclo completo)
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
