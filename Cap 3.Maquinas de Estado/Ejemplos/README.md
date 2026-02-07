# Ejemplos de capítulo 3: Máquinas de estado

A continuación, presento algunas implementaciones que construyen la realidad paso a paso. En cada ejemplo, mi objetivo no es solo encender luces o mover motores, sino demostrar cómo el concepto de "Máquina de Estados" actúa como el intermediario entre mi intención lógica y la realidad expresada mediante el microcontrolador.

## Ejemplo 1: El Semáforo (Intermediario entre Tiempo y Etapas)
Este es el ejemplo fundamental. El tiempo fluye de manera continua e imparable, pero mi lógica necesita pasos discretos y ordenados (Verde, Amarillo, Rojo).

Aquí, la Máquina de Estados actúa como un organizador temporal. Sin ella, tendría que paralizar el procesador con un comando sleep para generar una espera. Con ella, cambio la estrategia: puedo "vigilar" el tiempo activamente. El Estado es quien mira el reloj por mí y decide cuándo es el momento exacto de cerrar una etapa y abrir la siguiente.

### Código: 01_semaforo_temporal.py

```python

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

Hasta ahora, hemos construido nuestras máquinas de estado utilizando una larga cadena de bloques if y elif dentro de un ciclo infinito. Esta técnica es válida y muy visual para empezar, pero tiene un defecto fundamental: mezcla la gestión del sistema con la lógica del comportamiento.

A medida que nuestro sistema crece (imagina un robot con 10 o 20 estados distintos), ese bloque if/elif se convierte en una torre inestable. Si quieres cambiar algo en el estado 15, corres el riesgo de romper accidentalmente el estado 3. El código se vuelve difícil de leer, difícil de mantener y propenso a errores humanos.

Para solucionar esto, cambiaremos la estrategia hacia un diseño modular. La filosofía es simple: Divide y vencerás.

En lugar de tener toda la lógica amontonada en el ciclo principal, aislaremos cada estado en su propia función independiente.


### La Librería: StateMachine.py
Primero, definimos la pequeña librería que vamos a utilizar. Esta pieza de código nos permite registrar nuestros estados y ejecutarlos paso a paso sin ensuciar el código principal.

```python

# Tomas de Camino
# Máquina de Estados

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

## 
