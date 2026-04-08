
# Ejemplos de capítulo 3: Máquinas de estado
A continuación, presento algunas implementaciones que construyen la realidad paso a paso. En cada ejemplo, mi objetivo no es solo encender luces o mover motores, sino demostrar cómo el concepto de "Máquina de Estados" actúa como el intermediario entre mi intención lógica y la realidad expresada mediante el microcontrolador.
## Ejemplo 1: El Semáforo (Intermediario entre Tiempo y Etapas)
Este es el ejemplo fundamental. El tiempo fluye de manera continua e imparable, pero mi lógica necesita pasos discretos y ordenados (Verde, Amarillo, Rojo).
Aquí, la Máquina de Estados actúa como un organizador temporal. Sin ella, tendría que paralizar el procesador con un comando sleep para generar una espera. Con ella, cambio la estrategia: puedo "vigilar" el tiempo activamente. El Estado es quien mira el reloj por mí y decide cuándo es el momento exacto de cerrar una etapa y abrir la siguiente.
### Código: 01_semaforo_temporal.py
```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez López
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideaboard import IdeaBoard
# Inicialización
ib = IdeaBoard()
# Estados
SIGA = 0
ATENCION = 1
PARE = 2
estado_actual = SIGA
ultimo_cambio = time.monotonic() # Marca de tiempo inicial
print("--- Semáforo Inteligente Iniciado ---")
while True:
    ahora = time.monotonic()
    
    # Lógica de Estados
    if estado_actual == SIGA:
        ib.pixel = (0, 255, 0) # Verde
        
        # El Estado decide cuándo cambiar
        if ahora - ultimo_cambio > 3.0:
            print("Tiempo cumplido: Cambiando a ATENCION")
            estado_actual = ATENCION
            ultimo_cambio = ahora
            
    elif estado_actual == ATENCION:
        ib.pixel = (255, 100, 0) # Amarillo/Naranja
        
        if ahora - ultimo_cambio > 1.0:
            print("Precaución finalizada: Cambiando a PARE")
            estado_actual = PARE
            ultimo_cambio = ahora
            
    elif estado_actual == PARE:
        ib.pixel = (255, 0, 0) # Rojo
        
        if ahora - ultimo_cambio > 3.0:
            print("Ciclo completado: Reiniciando a SIGA")
            estado_actual = SIGA
            ultimo_cambio = ahora
    # Pequeña pausa para no saturar al procesador
    time.sleep(0.01)
```
## Importante:
Este ejemplo nos deja que que: "esperar" no significa "dormir". La Máquina de Estados me permite traducir la espera en una condición lógica activa, manteniendo el control del sistema en todo momento.
##  Ejemplo 2: Modos de Operación (Intermediario entre Contexto y Comportamiento)
Este caso me ayuda a entender la versatilidad. Físicamente, solo tengo un botón y un LED, pero gracias a los estados, puedo simular que tengo tres dispositivos diferentes en la mano.
Aquí, la Máquina de Estados define qué "reglas" aplican en cada momento:
Si el estado es MODO_SEM_VERDE, la regla es temporal (esperar y cambiar).
Si el estado es MODO_ALARMA, la regla es matemática (parpadear rápido).
El botón funciona como un selector que me permite saltar de un reglamento a otro.
### Código: 02_selector_contexto.py
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
import keypad
from ideaboard import IdeaBoard
ib = IdeaBoard()
# Configuración del botón BOOT (IO0)
keys = keypad.Keys(
    (board.IO0,),
    value_when_pressed=False, 
    pull=True
)
# Estados del Sistema
MODO_OFF = 0
MODO_SEM_VERDE = 1
MODO_SEM_ROJO = 2
MODO_ALARMA = 3
estado_actual = MODO_OFF
ultimo_cambio_tiempo = time.monotonic()
print("--- Sistema Multimodal Iniciado ---")
print("Presiona el botón BOOT para cambiar de modo")
while True:
    ahora = time.monotonic()
    
    # Escuchar al Botón
    evento = keys.events.get()
    if evento and evento.pressed:
        # Avanzamos al siguiente estado en ciclo (0->1->2->3->0...)
        estado_actual = (estado_actual + 1) % 4
        ultimo_cambio_tiempo = ahora
        print(f"Botón presionado: Cambiando a Estado {estado_actual}")
    # Comportamiento según el Estado actual
    if estado_actual == MODO_OFF:
        ib.pixel = (0, 0, 0) # Todo apagado
        
    elif estado_actual == MODO_SEM_VERDE:
        ib.pixel = (0, 255, 0)
        # Aquí las reglas dicen: cambia por tiempo
        if ahora - ultimo_cambio_tiempo > 4.0:
            estado_actual = MODO_SEM_ROJO
            ultimo_cambio_tiempo = ahora
    elif estado_actual == MODO_SEM_ROJO:
        ib.pixel = (255, 0, 0)
        if ahora - ultimo_cambio_tiempo > 4.0:
            estado_actual = MODO_SEM_VERDE
            ultimo_cambio_tiempo = ahora
    elif estado_actual == MODO_ALARMA:
        # Aquí las reglas dicen: parpadea rápido
        if int(ahora * 5) % 2 == 0: 
            ib.pixel = (255, 255, 0) 
        else:
            ib.pixel = (0, 0, 0)
    time.sleep(0.01)
```
## Importante:
Aquí busco mostrar que el hardware no define el producto final. Es el Estado el que decide si mi placa actúa como una luz de tráfico tranquila o como una sirena de emergencia frenética. El código es el que otorga la personalidad al objeto.
## Ejemplo 3: Física e Inercia (Intermediario entre Decisión y Acción)
Este es mi favorito porque utiliza un robot (Cenfobot) y hace que se sienta real. En el mundo físico, las cosas no suceden instantáneamente; tienen masa e inercia.
Aquí, la Máquina de Estados es el intermediario entre lo que quiero (mi intención inmediata) y lo que sucede (el proceso físico).
Mi intención: "¡Frena!" (Cambio de estado instantáneo).
La realidad: El robot reduce la velocidad poco a poco (Proceso gradual).
El estado protege a la mecánica de mis decisiones bruscas.
### Código: 03_cinetica_motor.py
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
import keypad
from ideaboard import IdeaBoard
ib = IdeaBoard()
# Configuración del botón BOOT
keys = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)
# Estados del sistema
DETENIDO   = 0
ACELERANDO = 1
CONSTANTE  = 2
FRENANDO   = 3
# Variables iniciales
estado = DETENIDO
velocidad = 0.0
# Configuración del movimiento
meta = 1.0       # Velocidad máxima
tasa_acc = 0.05  # Qué tan rápido acelera
tasa_freno = 0.10 # Qué tan rápido frena
print("--- Robot con Inercia ---")
while True:
    # Leer entradas (¿Qué pasa afuera?)
    evento = keys.events.get()
    boton_presionado = evento and evento.pressed
    # Máquina de Estados (Mi Intención Lógica)
    # Cambiamos de intención instantáneamente al pulsar el botón
    if estado == DETENIDO:
        if boton_presionado:
            estado = ACELERANDO
            print(">>> Decisión: Empezar a Acelerar")
    elif estado == ACELERANDO:
        if boton_presionado:
            estado = FRENANDO
        elif velocidad >= meta:
            estado = CONSTANTE
            print(">>> Decisión: Mantener velocidad")
    elif estado == CONSTANTE:
        if boton_presionado:
            estado = FRENANDO
            print(">>> Decisión: Empezar a Frenar")
    elif estado == FRENANDO:
        if velocidad <= 0:
            estado = DETENIDO
            print(">>> Decisión: Detenerse por completo")
    # Física (La Reacción Real)
    # El movimiento ocurre gradualmente, obedeciendo al estado
    if estado == ACELERANDO:
        velocidad += tasa_acc
        if velocidad > meta: 
            velocidad = meta
    elif estado == FRENANDO:
        velocidad -= tasa_freno
        if velocidad < 0: 
            velocidad = 0.0
    # Actuación
    ib.motor_1.throttle = velocidad
    ib.motor_2.throttle = velocidad
    time.sleep(0.05)
```
## Importante:
Con este ejemplo he logrado desacoplar la decisión de la ejecución. La Máquina de Estados recibe mi orden instantánea, pero la administra para que el mundo físico la asimile a su propio ritmo. Es la diferencia entre ser un dictador que grita órdenes y un conductor que gestiona el movimiento.
# Implementación Formal: Uso de la Librería StateMachine
Hasta ahora, he construido mis máquinas de estado utilizando una larga cadena de bloques if y elif dentro de un ciclo infinito. Reconozco que esta técnica es válida y visual para empezar, pero noto que tiene un defecto fundamental: mezcla la gestión del sistema con la lógica del comportamiento.
A medida que mi sistema crece (imagino un robot con 10 o 20 estados distintos), ese bloque if/elif se convierte en una torre inestable. Si quiero cambiar algo en el estado 15, corro el riesgo de romper accidentalmente el estado 3. Mi código se vuelve difícil de leer, de mantener y propenso a errores.
Para solucionar esto, cambiaré mi estrategia hacia un diseño modular bajo la filosofía de "Divide y vencerás". En lugar de tener toda la lógica amontonada en el ciclo principal, aislaré cada estado en su propia función independiente.
### La Librería: StateMachine.py
Primero, definimos la pequeña librería que vamos a utilizar. Esta pieza de código nos permite registrar nuestros estados y ejecutarlos paso a paso sin ensuciar el código principal.
```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

class StateMachine:
    def __init__(self, initial_state):
        # 1. Estado interno actual
        self.current_state = initial_state
        
        # 2. Diccionario estado -> función
        self.state_actions = {}
    # 3. Método para agregar asociaciones estado-función
    def add_state(self, state, action):
        """
        state: cualquier objeto hashable (str, int, enum)
        action: función que implementa el comportamiento del estado
                y retorna el próximo estado
        """
        self.state_actions[state] = action
    def step(self):
        """
        Ejecuta la función asociada al estado actual
        y avanza al siguiente estado.
        """
        if self.current_state not in self.state_actions:
            return  # estado sin comportamiento definido
        next_state = self.state_actions[self.current_state]()
        self.current_state = next_state
```
## Ejemplo 1 Adaptado: El Semáforo Modular
En la versión anterior, verificába el tiempo dentro del bucle principal. Ahora, busco que cada función de estado es responsable de su propio cronómetro simplificando el código. Lo importante aquí es el valor de retorno: si el tiempo no ha pasado, la función retorna su mismo nombre (se queda ahí); si el tiempo pasó, retorna el nombre del siguiente estado.
 ### Código: 01_semaforo_sm.py
 
``` python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideaboard import IdeaBoard
from StateMachine import StateMachine
ib = IdeaBoard()
Estados
SIGA = "siga"
ATENCION = "atencion"
PARE = "pare"
# Variables globales para el manejo del tiempo
ultimo_cambio = time.monotonic()
# Funciones de cada Estado
def estado_siga():
    global ultimo_cambio
    ib.pixel = (0, 255, 0)  # Verde
    
    # Lógica de transición
    if time.monotonic() - ultimo_cambio > 3.0:
        print("Cambio a ATENCION")
        ultimo_cambio = time.monotonic()
        return ATENCION  # Transición
    return SIGA          # Mantener estado
def estado_atencion():
    global ultimo_cambio
    ib.pixel = (255, 100, 0) # Amarillo
    
    if time.monotonic() - ultimo_cambio > 1.0:
        print("Cambio a PARE")
        ultimo_cambio = time.monotonic()
        return PARE
    return ATENCION
def estado_pare():
    global ultimo_cambio
    ib.pixel = (255, 0, 0)   # Rojo
    
    if time.monotonic() - ultimo_cambio > 3.0:
        print("Reinicio a SIGA")
        ultimo_cambio = time.monotonic()
        return SIGA
    return PARE
# Configuración de la Máquina
sm = StateMachine(initial_state=SIGA)
sm.add_state(SIGA, estado_siga)
sm.add_state(ATENCION, estado_atencion)
sm.add_state(PARE, estado_pare)
# 4. Loop Principal
while True:
    sm.step()
    time.sleep(0.01)
```
## Ejemplo 2 Adaptado: Modos de Operación
Con este ejemplo demuestro se pueden cómo manejar entradas externas (el botón) dentro de las funciones de estado. Cada modo es tiene una lógica independiente. El estado estado_alarma contiene su propia lógica de parpadeo, totalmente aislada de la luz fija.
### Código: 02_contexto_sm.py
``` python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
import board
import keypad
from ideaboard import IdeaBoard
from StateMachine import StateMachine
ib = IdeaBoard()
keys = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)
# Nombres de Estados
OFF = "off"
LUZ_FIJA = "fija"
ALARMA = "alarma"
# Funciones de Estado
def estado_off():
    ib.pixel = (0, 0, 0)
    
    # Verificar si se presiona el botón para salir
    evento = keys.events.get()
    if evento and evento.pressed:
        return LUZ_FIJA
    return OFF
def estado_luz_fija():
    ib.pixel = (0, 255, 0)
    
    evento = keys.events.get()
    if evento and evento.pressed:
        return ALARMA
    return LUZ_FIJA
def estado_alarma():
    # Lógica interna del estado (parpadeo)
    if int(time.monotonic() * 5) % 2 == 0:
        ib.pixel = (255, 0, 0)
    else:
        ib.pixel = (0, 0, 0)
        
    evento = keys.events.get()
    if evento and evento.pressed:
        return OFF
    return ALARMA
# Configuración
sm = StateMachine(initial_state=OFF)
sm.add_state(OFF, estado_off)
sm.add_state(LUZ_FIJA, estado_luz_fija)
sm.add_state(ALARMA, estado_alarma)
while True:
    sm.step()
    time.sleep(0.01)
```
## Ejemplo 3 Adaptado: Física e Inercia
Con este es el ejemplo quiero demostrar la separación más potente de responsabilidades.
La Máquina de Estados (Cerebro): Decide qué queremos hacer (acelerar, frenar). Define la velocidad_objetivo.
El Loop Principal (Cuerpo): Ejecuta la física. Ajusta gradualmente la velocidad_actual para alcanzar el objetivo.
Al usar la librería, busco encapsular las decisiones. El loop principal no toma decisiones, solo obedece las leyes de la física.
## Código: 03_inercia_sm.py
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
import keypad
from ideaboard import IdeaBoard
from StateMachine import StateMachine
ib = IdeaBoard()
keys = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)
# Nombres de Estados
DETENIDO = "detenido"
ACELERANDO = "acelerando"
FRENANDO = "frenando"
# Variables de Estado (Intención vs Realidad)
velocidad_actual = 0.0
velocidad_objetivo = 0.0  # La máquina controla esto
# Constantes Físicas
TASA_ACC = 0.05
TASA_FRENO = 0.10
# Funciones de Estado (El Cerebro)
def cerebro_detenido():
    global velocidad_objetivo
    velocidad_objetivo = 0.0
    
    evento = keys.events.get()
    if evento and evento.pressed:
        return ACELERANDO
    return DETENIDO
def cerebro_acelerando():
    global velocidad_objetivo
    velocidad_objetivo = 1.0
    
    evento = keys.events.get()
    if evento and evento.pressed:
        return FRENANDO
    return ACELERANDO
def cerebro_frenando():
    global velocidad_objetivo
    velocidad_objetivo = 0.0
    
    # Transición automática: si ya paramos, cambiar estado
    if velocidad_actual <= 0.01:
        return DETENIDO
    return FRENANDO
# Configuración
sm = StateMachine(initial_state=DETENIDO)
sm.add_state(DETENIDO, cerebro_detenido)
sm.add_state(ACELERANDO, cerebro_acelerando)
sm.add_state(FRENANDO, cerebro_frenando)
print("--- Robot Modular Iniciado ---")
while True:
    # La máquina decide la intención (velocidad_objetivo)
    sm.step()
    
    # ACTUAR: Simulación física 
    if velocidad_actual < velocidad_objetivo:
        velocidad_actual += TASA_ACC
        if velocidad_actual > velocidad_objetivo: 
            velocidad_actual = velocidad_objetivo
            
    elif velocidad_actual > velocidad_objetivo:
        velocidad_actual -= TASA_FRENO
        if velocidad_actual < velocidad_objetivo: 
            velocidad_actual = velocidad_objetivo
    ib.motor_1.throttle = velocidad_actual
    ib.motor_2.throttle = velocidad_actual
    
    time.sleep(0.05)
```

# Ejemplo 4 Adaptado: Control Cinemático por Consigna y Rampa de Inercia
Este ejemplo demuestra el desacoplamiento entre la Intención Lógica (qué queremos que pase) y la Respuesta Física (cómo reacciona el hardware ante la inercia).
## Código: 04_control_cinematico_sm.py
```python
# ----------------------------------------
# Universidad Cenfotec
# Proyecto: Control Cinemático de Precisión
# Autores: Ph. Tomás de Camino Beck, Fiorella Perez, 
#          Aylin Salazar Delgado, Gabriela Urbina Hernández
# ----------------------------------------

import time
import board
import keypad
from ideaboard import IdeaBoard

# Asumimos que StateMachine ya está disponible

#Configuración de Actuadores
ib = IdeaBoard()
ib.motor_1.throttle = 0.0
ib.motor_2.throttle = 0.0
user_input = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)

#Capa Física: Consigna vs Realidad
v_actual = 0.0      # Estado real
v_consigna = 0.0    # Intención lógica (Setpoint)

RAMPA_ASCENSO = 0.02  
RAMPA_DESCENSO = 0.06 

# Capa Lógica: Estados
def modo_estacionario():
    global v_consigna
    v_consigna = 0.0
    evento = user_input.events.get()
    if evento and evento.pressed:
        return "PROPULSION"
    return "ESTACIONARIO"

def modo_propulsion():
    global v_consigna
    v_consigna = 0.85 
    evento = user_input.events.get()
    if evento and evento.pressed:
        return "INERCIA_RESIDUAL"
    return "PROPULSION"

def modo_inercia_residual():
    global v_consigna
    v_consigna = 0.0
    if v_actual <= 0.001:
        return "ESTACIONARIO"
    return "INERCIA_RESIDUAL"

# Orquestación
controlador = StateMachine(initial_state="ESTACIONARIO")
controlador.add_state("ESTACIONARIO", modo_estacionario)
controlador.add_state("PROPULSION", modo_propulsion)
controlador.add_state("INERCIA_RESIDUAL", modo_inercia_residual)

while True:
    controlador.step() # El cerebro decide el 'Deseo'
    
    # El cuerpo procesa la 'Realidad'
    if v_actual < v_consigna:
        v_actual += RAMPA_ASCENSO
    elif v_actual > v_consigna:
        v_actual -= RAMPA_DESCENSO
    
    ib.motor_1.throttle = v_actual
    ib.motor_2.throttle = v_actual
    time.sleep(0.02)
```
# Ejemplo 5: El Sensor con Memoria (Evitando el ruido con Histéresis)
En este ejemplo, usamos un sensor analógico en el pin de solo entrada IO34. Aplicamos histéresis definiendo que el sistema entre en alerta al superar los 20000, pero no se relaje hasta que el valor baje de 10000.

## Código: 05_histeresis_sm.py
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
from ideaboard import IdeaBoard
from StateMachine import StateMachine

ib = IdeaBoard()
sensor = ib.AnalogIn(board.IO34)

# Estados
NORMAL = "normal"
ALERTA = "alerta"

# Umbrales separados (Histéresis)
UMBRAL_ALTO = 20000  # Para activar la alerta
UMBRAL_BAJO = 10000  # Para volver a la normalidad

def estado_normal():
    ib.pixel = (0, 255, 0)  # Verde: Todo bien
    
    # Solo cambiamos si el valor supera el umbral alto
    if sensor.value > UMBRAL_ALTO:
        print("¡Nivel alto detectado! Pasando a ALERTA.")
        return ALERTA
    return NORMAL

def estado_alerta():
    ib.pixel = (255, 0, 0)  # Rojo: Peligro
    
    # Solo nos calmamos si el valor baja del umbral bajo
    if sensor.value < UMBRAL_BAJO:
        print("Nivel estabilizado. Pasando a NORMAL.")
        return NORMAL
    return ALERTA

sm = StateMachine(initial_state=NORMAL)
sm.add_state(NORMAL, estado_normal)
sm.add_state(ALERTA, estado_alerta)

print("--- Lector Analógico con Histéresis ---")
while True:
    sm.step()
    time.sleep(0.05)
```
**Importante:** La lógica de la máquina de estados (el cerebro) se mantiene clara e intacta, mientras que los parámetros de los umbrales (los sentidos) se calibran a la necesidad del entorno físico. El estado actúa como un amortiguador de la realidad.

# Ejemplo 6: La Barrera Automática (Servomotores y Secuencias)
Mover un servomotor es una acción casi instantánea para el código, pero gestionar lo que sucede después de moverlo es donde es crucial no congelar el microcontrolador. Imagina la barrera de un parqueo: se presiona un botón, sube, espera 5 segundos y luego baja automáticamente. La Máquina de Estados nos permite secuenciar esto controlando el tiempo sin usar pausas bloqueantes.

## Código: 06_barrera_servo_sm.py
``` python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
import board
import keypad
from ideaboard import IdeaBoard
from StateMachine import StateMachine

ib = IdeaBoard()
keys = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)

# Asumimos un servo conectado en IO4
servo = ib.Servo(board.IO4)

# Estados
CERRADO = "cerrado"
ABIERTO = "abierto"

# Variables de tiempo
tiempo_apertura = 0.0

def estado_cerrado():
    global tiempo_apertura
    servo.angle = 0  # Barrera abajo
    ib.pixel = (255, 0, 0) # Luz roja
    
    evento = keys.events.get()
    if evento and evento.pressed:
        print("Botón presionado. Abriendo barrera...")
        tiempo_apertura = time.monotonic()
        return ABIERTO
    return CERRADO

def estado_abierto():
    servo.angle = 90  # Barrera arriba
    ib.pixel = (0, 255, 0) # Luz verde
    
    # El estado vigila el tiempo para cerrarse solo
    if time.monotonic() - tiempo_apertura > 5.0:
        print("Tiempo de cortesía finalizado. Cerrando...")
        return CERRADO
    return ABIERTO

sm = StateMachine(initial_state=CERRADO)
sm.add_state(CERRADO, estado_cerrado)
sm.add_state(ABIERTO, estado_abierto)

print("--- Sistema de Peaje Automático ---")
while True:
    sm.step()
    time.sleep(0.05)
```
**Importante:** Este ejemplo ilustra la diferencia entre transiciones. Un estado puede tener una condición de salida basada en un evento externo (presionar el botón para abrir), mientras que otro tiene una condición de salida autónoma o temporal (cerrar después de 5 segundos).

# Ejemplo 7: El Interruptor Capacitivo (Manejo de Transiciones Seguras)
La IdeaBoard tiene pines táctiles (touch capacitivo). Leer este tipo de pines continuamente puede generar disparos múltiples si el usuario deja el dedo puesto una fracción de segundo de más. Queremos que un solo toque cambie el color del LED, obligando al usuario a quitar el dedo antes de registrar un nuevo toque.
Aquí la Máquina de Estados divide la interacción en dos fases estables: el toque activo y la liberación.

## Código: 07_touch_toggle_sm.py
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
from StateMachine import StateMachine

ib = IdeaBoard()
touch_pin = touchio.TouchIn(board.IO32)

# Estados
ESPERANDO_TOQUE = "esperando"
ESPERANDO_LIBERACION = "liberando"

# Variable para alternar colores
color_estado = False

def estado_esperando():
    global color_estado
    
    if touch_pin.value:
        # Alternamos el color solo en el instante inicial del toque
        color_estado = not color_estado
        if color_estado:
            ib.pixel = (0, 0, 255)  # Azul
        else:
            ib.pixel = (255, 0, 255)  # Magenta
            
        print("¡Toque detectado!")
        return ESPERANDO_LIBERACION
    return ESPERANDO_TOQUE

def estado_liberando():
    # Nos quedamos atascados aquí intencionalmente hasta que no haya toque
    if not touch_pin.value:
        print("Dedo liberado. Listo para otro toque.")
        return ESPERANDO_TOQUE
    return ESPERANDO_LIBERACION

sm = StateMachine(initial_state=ESPERANDO_TOQUE)
sm.add_state(ESPERANDO_TOQUE, estado_esperando)
sm.add_state(ESPERANDO_LIBERACION, estado_liberando)

print("--- Interruptor Táctil Seguro ---")
while True:
    sm.step()
    time.sleep(0.05)
```
**Importante:** El estado ESPERANDO_LIBERACION actúa como un candado físico. Protege nuestra lógica de ejecutarse cientos de veces por segundo, obligando a que se complete el ciclo natural del hardware (tocar y soltar) antes de continuar.

## Conclusión: El Poder de los Estados
Al finalizar, comprendí la verdadera naturaleza de una Máquina de Estados: es la estructura que impone orden sobre el tiempo y las entradas físicas. Pasé de tener un bucle reactivo a definir un sistema determinista basado en Estados (comportamientos fijos) y Transiciones (reglas de cambio). Esta metodología me permitió controlar procesos complejos, como tiempos de espera o inercia, asegurando que el microcontrolador siempre sepa exactamente en qué etapa se encuentra y qué debe ocurrir para avanzar a la siguiente.
