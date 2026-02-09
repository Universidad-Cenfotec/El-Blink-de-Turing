
# Ejemplos del capítulo 4: Sensar

## Ejemplo 1: La Emergencia del Evento (Umbrales y Memoria)
En este script, transformamos una lectura analógica continua en una decisión discreta. El sistema no reacciona a cada pequeña fluctuación del 
sensor (ruido); en su lugar, utiliza una memoria mínima (el estado anterior) y un umbral para determinar si el mundo ha cambiado de estado o si 
simplemente está vibrando.

### Código: 01 
```python
import time
from ideaboard import IdeaBoard
ib = IdeaBoard()

# El sistema recuerda el pasado para entender el presente

estado_previo = False
umbral_activacion = 1.5 # Voltios o valor de referencia

while True:
    # 1. Muestreo: Captura de un instante del mundo
    lectura_actual = ib.potentiometer.value
    
    # 2. Discretización: El mundo continuo se vuelve binario
    estado_actual = lectura_actual > umbral_activacion
    
    # 3. Detección de Transición: Comparación entre historia y presente
    if estado_actual != estado_previo:
        if estado_actual:
            print(f"Evento: Umbral superado ({lectura_actual:.2f}) - Ascenso")
            ib.pixel = (10, 0, 0) # Rojo: Activado
        else:
            print(f"Evento: Por debajo del umbral ({lectura_actual:.2f}) - Descenso")
            ib.pixel = (0, 0, 10) # Azul: Reposo
            
    # 4. Actualización de la memoria
    estado_previo = estado_actual
    
    # El ritmo de muestreo define la resolución de la historia
    time.sleep(0.05)
```

## Ejemplo 2:La construcción de la memoria (Tendencia y Variación
En este ejemplo, el sistema no solo mira el valor actual, sino que lo compara con el pasado inmediato para entender la dirección del cambio. 
Aquí, el microcontrolador no solo mide una magnitud física; computa una intención del entorno (¿está subiendo o está bajando?).

En el mundo físico, los fenómenos tienen inercia. Un microcontrolador puede capturar esa inercia comparando dos puntos en el tiempo. 
Este código transforma una lectura aislada en una tendencia, permitiendo que el sistema anticipe o reaccione al movimiento antes de que
este alcance un valor crítico.


### Código: 02 memoria_tendencia.py
```python
import time
from ideaboard import IdeaBoard

ib = IdeaBoard()

# Variables que actúan como la memoria histórica del sistema
valor_anterior = ib.potentiometer.value
umbral_movimiento = 0.05

while True:
    # Captura del presente
    valor_actual = ib.potentiometer.value
    
    # Computación de la diferencia (La derivada simple)
    diferencia = valor_actual - valor_anterior
    
    # Determinación de la tendencia
    if abs(diferencia) > umbral_movimiento:
        if diferencia > 0:
            print(f"Tendencia: Ascendente (+) | Variación: {diferencia:.3f}")
            ib.pixel = (0, 10, 0) # Verde: Creciendo
        else:
            print(f"Tendencia: Descendente (-) | Variación: {diferencia:.3f}")
            ib.pixel = (10, 0, 0) # Rojo: Decreciendo
    else:
        # El sistema percibe estabilidad
        ib.pixel = (0, 0, 0)
    
    # El presente se convierte en pasado para el próximo ciclo
    valor_anterior = valor_actual
    
    # La frecuencia de este sleep define la 'sensibilidad' a la velocidad
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

#Fio-Perez
#Universidad Cenfotec

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
