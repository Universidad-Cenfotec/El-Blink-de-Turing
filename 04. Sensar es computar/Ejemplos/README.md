
# Ejemplos del capítulo 4: Sensar

## Ejemplo 1: La Emergencia del Evento (Histéresis y Memoria)
En este script, transformamos una lectura analógica continua en una decisión discreta utilizando **fronteras dobles**. El sistema utiliza dos umbrales para evitar que el ruido del sensor provoque cambios erráticos (parpadeos) cuando la señal está cerca del límite. Es la base de la estabilidad en sistemas de control.

### Código: 01_histeresis.py

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
import analogio
import digitalio

# 1. Configuración de Hardware al estilo CircuitPython
# Usamos el pin IO34 para el sensor y el LED interno de la placa
sensor = analogio.AnalogIn(board.IO34)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# 2. Fronteras (Histéresis) - Escala 0-65535
# Convertimos los valores de MicroPython (0-4095) a 16 bits
# 3000 -> aprox 48000 | 1000 -> aprox 16000
THRESHOLD_HIGH = 48000  
THRESHOLD_LOW  = 16000  

# Memoria del sistema
estado_previo = False

print("Sistema de Histéresis Iniciado...")

while True:
    # A. Muestreo: Lectura en rango 0-65535
    lectura_actual = sensor.value
    
    # B. Lógica de Histéresis (Discretización con memoria)
    estado_actual = estado_previo  # Mantener estado por defecto
    
    if estado_previo:
        # Si estaba encendido, solo se apaga si baja del umbral inferior
        if lectura_actual < THRESHOLD_LOW:
            estado_actual = False
    else:
        # Si estaba apagado, solo se enciende si supera el umbral superior
        if lectura_actual > THRESHOLD_HIGH:
            estado_actual = True
    
    # C. Detección de Transición (Eventos)
    if estado_actual != estado_previo:
        if estado_actual:
            print(f"Evento: Umbral superado ({lectura_actual}) - Ascenso")
        else:
            print(f"Evento: Por debajo del umbral ({lectura_actual}) - Descenso")
    
    # D. Actualización de salida y memoria
    led.value = estado_actual
    estado_previo = estado_actual
    
    # Pequeña pausa para estabilidad
    time.sleep(0.01)
```
## Ejemplo 2: La construcción de la memoria (Tendencia y Variación)

En este ejemplo, el sistema no solo mira el valor actual, sino que lo compara con el pasado inmediato para entender la dirección del cambio. Aquí, el microcontrolador computa una intención del entorno: ¿está subiendo o está bajando? Este código transforma una lectura aislada en una tendencia (una derivada simple).

### Código: 02_memoria_tendencia.py

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------

import machine
import time

# Configuración de hardware nativo
sensor = machine.ADC(machine.Pin(34))
sensor.atten(machine.ADC.ATTN_11DB)
led = machine.Pin(2, machine.Pin.OUT)

# Variables que actúan como la memoria histórica del sistema
valor_anterior = sensor.read()

# Umbral de movimiento (sensibilidad a la variación)
umbral_movimiento = 200

while True:
    # Captura del presente
    valor_actual = sensor.read()
    
    # Computación de la diferencia (La derivada simple)
    diferencia = valor_actual - valor_anterior
    
    # Determinación de la tendencia basada en la memoria
    if abs(diferencia) > umbral_movimiento:
        if diferencia > 0:
            print(f"Tendencia: Ascendente (+) | Variación: {diferencia}")
            led.value(1) # Feedback visual de crecimiento
        else:
            print(f"Tendencia: Descendente (-) | Variación: {diferencia}")
            led.value(0) # Feedback visual de decrecimiento
    else:
        # El sistema percibe estabilidad
        pass
    
    # El presente se convierte en pasado para el próximo ciclo
    valor_anterior = valor_actual
    
    # La frecuencia define la 'sensibilidad' a la velocidad
    time.sleep(0.1)
```


## Reflexiones para el lector
- La invención de la dirección: Un sensor de luz o un potenciómetro no saben qué es "subir". Es el microcontrolador el que, al retener el valor_anterior, inventa la noción de dirección. La computación aquí es el acto de comparar dos instantes para generar un concepto nuevo: la tendencia.

- El sensor como cronómetro: Nota que si reduces el time.sleep(), la diferencia se vuelve más pequeña porque el mundo cambia menos entre lecturas. La percepción de la velocidad del entorno depende directamente de la velocidad de nuestro ciclo de lectura.

- La historia mínima: Este sistema tiene una memoria de exactamente un paso. Es el nivel más básico de conciencia temporal: saber qué acaba de pasar para entender qué está pasando ahora.

# Ejemplo 3: Validación Sensorial (Construyendo Certeza)
En este ejemplo, aplico la idea de que "una sola lectura no es la realidad". Los sensores a veces mienten o detectan ecos falsos. Por eso, mi código no reacciona impulsivamente.

Utilizo una Máquina de Estados (concepto anteriormente desarrollado) para comportarme como un juez: no dicto sentencia (encender la luz) hasta no haber acumulado suficiente evidencia. El tiempo y la repetición son mis herramientas para distinguir entre el "ruido" y un "evento real".

### Código: 03_validacion_sensorial.py

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
from hcsr04 import HCSR04
from ideaboard import IdeaBoard
from StateMachine import StateMachine   

# --- Configuración ---
ib = IdeaBoard()
sonar = HCSR04(board.IO26, board.IO25)

# --- Memoria ---
contador = 0
META = 5   # Necesito 5 lecturas seguidas para "creer"

# --- Estados ---

def estado_vacio():
    global contador
    contador = 0  # Reinicio la cuenta, no hay nadie
    
    try:
        dist = sonar.dist_cm()
    except RuntimeError:
        return "vacio"

    print(f"[VACIO] Lectura: {dist:.1f}")

    # Si veo algo cerca, paso a verificar si es real
    if 0 < dist < 30:
        return "verificando"
        
    return "vacio"


def estado_verificando():
    global contador
    
    try:
        dist = sonar.dist_cm()
    except RuntimeError:
        return "vacio" # Si falla el sensor, vuelvo a empezar

    # Si el objeto desaparece, fue una falsa alarma
    if dist > 30:
        return "vacio"

    # Si sigue ahí, sumo un punto de confianza
    contador += 1
    print(f"[VERIFICANDO] Confianza: {contador}/{META}")

    # Si llego a la meta, es un objeto real
    if contador >= META:
        return "confirmado"

    return "verificando"


def estado_confirmado():
    # Ya estoy seguro, así que actúo
    ib.pixel = (255, 0, 0)
    
    try:
        dist = sonar.dist_cm()
    except RuntimeError:
        dist = 0

    print(f"[CONFIRMADO] Objeto presente")

    # Margen de seguridad: solo apago si se aleja claramente (>35)
    if dist > 35:
        ib.pixel = (0, 0, 0)
        return "vacio"

    return "confirmado"

# --- Ejecución ---

sm = StateMachine(initial_state="vacio")
sm.add_state("vacio", estado_vacio)
sm.add_state("verificando", estado_verificando)
sm.add_state("confirmado", estado_confirmado)

print("--- Validación Iniciada ---")

while True:
    sm.step()
    sleep(0.1) # Cada ciclo es un paso en el tiempo
```

## Reflexiones para el lector:
Con esto logro ver que sensar no es un acto instantáneo, sino un proceso. Al obligarme a verificar 5 veces antes de actuar, he creado un sistema que tiene "paciencia". He transformado una serie de lecturas ruidosas en una decisión sólida. Computar, en este caso, significa darle estabilidad al caos del mundo físico.
