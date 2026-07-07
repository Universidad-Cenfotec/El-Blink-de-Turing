# Ejemplos del capítulo 4: Sensar es computar

Hasta ahora he visto que un sensor no es simplemente un dispositivo que entrega datos del mundo físico. Una lectura aislada de luz, distancia, movimiento o contacto solamente representa un valor, pero no contiene una interpretación. Es mediante la computación que puedo transformar esas señales en información con significado.

Cuando programo un sistema embebido, no me limito a leer datos; construyo una forma de percepción. Mi código compara valores, recuerda estados anteriores, identifica cambios, filtra errores y decide cuándo una situación es suficientemente importante como para generar una respuesta. Entre lo que ocurre en el mundo físico y la acción de la máquina existe un proceso de interpretación donde los datos comienzan a tener contexto.

En este capítulo exploro diferentes maneras en las que un sistema puede construir una percepción más estable del entorno. A través de estos ejemplos muestro cómo una señal continua puede convertirse en un evento, cómo una memoria mínima permite reconocer tendencias, cómo la repetición puede generar confianza y cómo una interacción humana puede validarse mediante la acumulación de evidencia en el tiempo.

Estos ejemplos me permiten entender una idea fundamental: **un sensor no comprende el mundo; soy yo quien, mediante la programación, construyo esa comprensión**. El hardware únicamente captura señales, pero es el algoritmo el que decide qué significan y cómo debe responder el sistema.

A lo largo de los siguientes ejemplos desarrollo cuatro formas de darle significado a una lectura:

- **Histéresis y memoria:** utilizo fronteras dobles para transformar una señal cambiante en una decisión estable, evitando que el ruido provoque respuestas erráticas.
- **Tendencia y variación:** comparo el presente con el pasado inmediato para crear una noción de dirección, permitiendo que el sistema identifique si algo está aumentando o disminuyendo.
- **Validación sensorial:** incorporo tiempo y repetición para diferenciar entre una lectura accidental y un evento real, creando un sistema capaz de esperar antes de actuar.
- **Memoria táctil:** convierto una interacción física momentánea en una decisión basada en evidencia acumulada, demostrando cómo una máquina puede construir confianza.

Estos ejercicios muestran que sensar no es un acto instantáneo, sino un proceso donde la información adquiere valor a través del tiempo. La percepción de una máquina surge de la capacidad de recordar, comparar y decidir. En este sentido, **computar es darle memoria al presente para poder interpretar lo que está ocurriendo y responder de manera inteligente**.


## Ejemplo 1: La Emergencia del Evento (Histéresis y Memoria)

En este ejemplo transformo una lectura analógica continua en una decisión discreta utilizando **fronteras dobles**. Mi objetivo es evitar que el ruido natural del sensor provoque cambios erráticos cuando la señal se encuentra cerca de un límite.

Para lograrlo, implemento dos umbrales diferentes: uno para activar el sistema y otro para desactivarlo. Esta separación crea una zona de estabilidad donde la máquina mantiene su estado anterior en lugar de reaccionar inmediatamente ante pequeñas variaciones.

Aquí puedo observar cómo aparece la memoria dentro de un sistema aparentemente simple. El microcontrolador no solo pregunta "¿cuál es el valor actual?", sino que también recuerda "¿qué estaba ocurriendo antes?". Esa pequeña memoria permite construir comportamientos más confiables y es una de las bases fundamentales de los sistemas de control.


### Código: 01_histeresis.py

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez López
# Aylin Salazar Delgado
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

En este ejemplo exploro cómo una máquina puede obtener información nueva al comparar el presente con el pasado inmediato. Un sensor solamente entrega valores, pero al almacenar una lectura anterior puedo calcular una diferencia y construir una idea que originalmente no existía en el dato: la dirección del cambio.

El microcontrolador no sabe naturalmente qué significa subir o bajar. Soy yo, mediante la lógica del programa, quien creo esa interpretación al comparar dos momentos diferentes. Una simple resta entre el valor actual y el valor anterior se convierte en una forma básica de percepción temporal.

Este ejemplo muestra que incluso una memoria mínima puede cambiar completamente el comportamiento de un sistema. Conservar solamente una lectura anterior es suficiente para que la máquina pueda reconocer tendencias y responder a la dinámica del entorno.


### Código: 02_memoria_tendencia.py

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salazar Delgado
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

## Reflexiones para el lector:

- **La construcción de la dirección:** Un sensor únicamente entrega valores; no sabe si algo está subiendo o bajando. Al comparar la lectura actual con la lectura anterior, el sistema construye una interpretación del cambio y transforma una simple diferencia numérica en una noción de tendencia.

- **El tiempo como parte de la percepción:** La velocidad con la que realizo las lecturas modifica la forma en que interpreto el entorno. Si cambio el intervalo del `time.sleep()`, también cambia la magnitud de la diferencia entre mediciones. La percepción del movimiento depende del ritmo con el que observo y proceso los datos.

- **La memoria mínima como origen del comportamiento:** Guardar solamente un valor anterior parece una acción sencilla, pero representa una de las formas más básicas de memoria computacional. Al conservar información del pasado inmediato, el sistema puede comparar, interpretar cambios y construir una percepción temporal que no existe en una lectura aislada.
- 
## Ejemplo 3: Validación Sensorial (Construyendo Certeza)

En este ejemplo aplico una idea fundamental: **una sola lectura no representa necesariamente la realidad**. Los sensores pueden producir errores, interferencias o lecturas inesperadas, por lo que una reacción inmediata puede generar decisiones equivocadas.

Para solucionar esto utilizo una Máquina de Estados que funciona como un proceso de evaluación. El sistema no toma una decisión definitiva después de una única medición, sino que espera acumular suficiente evidencia antes de actuar.

De esta manera, incorporo una forma de paciencia dentro del programa. El tiempo y la repetición se convierten en herramientas para separar el ruido de un evento verdadero. La máquina no obtiene certeza porque "comprenda" el entorno, sino porque verifica que la información se mantiene consistente.

### Código: 03_validacion_sensorial.py

```python

# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salazar Delgado
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

- **La paciencia algorítmica:** Sensar no es un acto instantáneo, sino un proceso de acumulación de evidencia. Al exigir varias lecturas consecutivas antes de actuar, el sistema transforma una señal momentánea en una decisión más confiable.

- **La estabilidad ante el ruido:** El código funciona como un filtro que evita respuestas impulsivas frente a lecturas incorrectas o interferencias del entorno. La computación permite darle estabilidad al mundo físico al establecer condiciones antes de tomar una acción.

- **La construcción de la certeza:** La máquina no "sabe" que un objeto está presente; simplemente aumenta su nivel de confianza al observar que la información se mantiene constante durante cierto tiempo. La certeza aparece como resultado de la repetición y persistencia de los datos.


# Ejemplo 4: Memoria táctil
En este ejemplo, el sistema no solo mira si hay contacto o no, sino que compara la intensidad de la carga capacitiva actual con la del pasado inmediato. Aquí, el microcontrolador computa una "intención" de acercamiento: ¿el usuario está presionando más fuerte o está retirando su mano? Este código transforma una lectura eléctrica en una tendencia de proximidad física.

### Código 04: memoria_tactil.py 
```python
# ----------------------------------------
# Universidad Cenfotec - Capítulo 4: Sensar
# Proyecto: Validación de Presencia Humana (Capacitancia)
# Autores: Ph. Tomás de Camino Beck, Fiorella Perez, 
# Aylin Salazar Delgado, Gabriela Urbina Hernández
# ----------------------------------------

import board
import time
import touchio
from ideaboard import IdeaBoard

ib = IdeaBoard()

# 1. Usamos el pin IO27 como sensor de tacto al poner un cable ahí
sensor_tacto = touchio.TouchIn(board.IO27)

contador = 0
META = 5 

print("--- Sistema de Validación por Contacto Humano ---")
print("Toca el cable en IO27 para iniciar la validación...")

while True:
    # Lógica de validación
    if sensor_tacto.value:
        contador += 1
        ib.pixel = (0, 0, 150) # Azul: Verificando identidad...
        print(f"[PROCESANDO] Evidencia de contacto: {contador}/{META}")
        
        if contador >= META:
            ib.pixel = (0, 150, 0) # Verde: ¡USUARIO VALIDADO!
            print(">>> ACCESO CONFIRMADO: Ser Humano Detectado <<<")
    else:
        # Si soltamos el cable, la confianza se pierde (Seguridad)
        if contador > 0:
            print("Contacto perdido - Reiniciando protocolos...")
            contador = 0
            ib.pixel = (0, 0, 0)

    time.sleep(0.15)
```
# Reflexiones para el lector:

- **La paciencia algorítmica:** Sensar no es un acto instantáneo, sino un proceso de acumulación. Al exigir varias lecturas consecutivas antes de actuar, el sistema transforma un impulso eléctrico efímero en una decisión sólida.

- **Estabilidad ante el caos:** El código actúa como un filtro de ruido. La computación permite darle estabilidad al mundo físico, evitando que la máquina reaccione ante interferencias o "falsos positivos" del entorno.

- **La construcción de la certeza:** La máquina no "sabe" que hay un humano presente; simplemente deja de dudar después de acumular suficiente evidencia. La certeza aparece como resultado de la persistencia del dato en el tiempo, convirtiendo el caos sensorial en una decisión lógica.
