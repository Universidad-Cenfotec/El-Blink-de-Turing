# Ejemplos de capítulo: El reloj

He escrito estos scripts para materializar la idea del tiempo como una construcción y no solo como una medida técnica. A través de ellos, exploro cómo sostengo un presente continuo mediante el ciclo infinito, demostrando que la computación es, esencialmente, mi gestión de una secuencia de pulsos. Para mí, el reloj no es un accesorio; es la condición de posibilidad para que el sistema exista y actúe sobre el mundo físico.

## Ejemplo 1: Multitarea por intercalado temporal
Aquí demostramos que la simultaneidad es una ilusión creada por la velocidad del reloj. Dos procesos con ritmos distintos conviven en el mismo while True. No ocurren a la vez, pero ocurren tan cerca uno del otro que para nosotros son un solo comportamiento complejo.

**Código:** 01_intercalado.py 

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

ib = IdeaBoard()

# Cada tarea tiene su propio ritmo definido por el número de ciclos
ciclo = 0

while True:
    # El ciclo corre a alta velocidad para permitir fluidez
    
    # Tarea A: Destello rápido cada 5 ciclos
    if ciclo % 5 == 0:
        # Una acción breve que no detiene el flujo
        pass 
    
    # Tarea B: Cambio de color cada 50 ciclos
    if ciclo % 50 == 0:
        ib.pixel = (0, 0, 10)
    
    # Tarea C: Apagar cada 100 ciclos
    if ciclo % 100 == 0:
        ib.pixel = (0, 0, 0)

    # Incremento constante que mantiene el orden
    ciclo = ciclo + 1
    
    # Un pequeño respiro para dar estabilidad al hardware
    time.sleep(0.01)

```

## Ejemplo 2: La luz como proceso (Latido lógico)

En este código busco demostrar que lo que percibo como una intensidad estática es en realidad un flujo constante de cambios. Nada en mi programa permanece quieto. La luz del LED RGB "respira" porque obligo a un contador a avanzar y retroceder en sincronía con el reloj interno. Al agregar mensajes en la consola, hago visible el pulso numérico que sostiene la ilusión del brillo, transformando un fenómeno visual en una evidencia matemática. 


**Código:**  02_latido_logico.py

``` python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------

import time
import board
from ideaboard import IdeaBoard

ib = IdeaBoard()

paso = 0
direccion = 1

while True:
    # La intensidad es el resultado de un contador en movimiento
    ib.pixel = (0, paso, 0)
    
    # Hacemos visible el interior del flujo temporal
    print("Pulso lógico actual", paso)
    
    paso = paso + direccion
    
    # El tiempo lógico rebota al llegar a los límites físicos
    if paso >= 255:
        direccion = -1
        print("Límite superior alcanzado, invirtiendo dirección")
    
    if paso <= 0:
        direccion = 1
        print("Límite inferior alcanzado, iniciando ascenso")
    
    # La pausa sincroniza el ritmo digital con nuestra percepción
    time.sleep(0.005)

```

## Ejemplo 3: El pulso y la historia (Cronometrando el ciclo)

En este código busco enfrentar la teoría con la práctica. No solo le pido al microcontrolador que espere un tiempo determinado, sino que utilizo un cronómetro interno para medir la duración exacta de cada latido y el tiempo total que el sistema lleva existiendo.

Al observar los motores acelerar, puedo ver en la consola la relación directa entre el tiempo entre ciclos (mi resolución) y el tiempo total transcurrido (mi historia). Si el tiempo entre ciclos varía, mi percepción del movimiento también lo hará.


**Código:** 03cronometro_reloj.py

``` python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideaboard import IdeaBoard

ib = IdeaBoard()

# Registro del inicio
tiempo_inicio_global = time.monotonic()
tiempo_ultimo_ciclo = time.monotonic()

velocidad = 0.0
incremento_por_ciclo = 0.005
direccion = 1

while True:
    # Captura de marcas temporales
    ahora = time.monotonic()
    duracion_ciclo = ahora - tiempo_ultimo_ciclo
    tiempo_total = ahora - tiempo_inicio_global
    
    # Control de hardware
    ib.motor_1.throttle = velocidad
    ib.motor_2.throttle = velocidad
    
    # Indicador visual de velocidad
    brillo = int(abs(velocidad) * 255)
    ib.pixel = (0, 0, brillo)
    
    # Monitoreo del reloj
    print(f"Total: {tiempo_total:.2f}s | Entre ciclos: {duracion_ciclo:.4f}s | Velocidad: {velocidad:.3f}")
    
    # Evolución del estado según el ciclo
    velocidad = velocidad + (incremento_por_ciclo * direccion)
    
    # Gestión de límites y dirección
    if velocidad >= 1.0:
        velocidad = 1.0
        direccion = -1
        print("--- Desacelerando ---")
        
    if velocidad <= -1.0:
        velocidad = -1.0
        direccion = 1
        print("--- Acelerando ---")
    
    # Actualización para el próximo pulso
    tiempo_ultimo_ciclo = ahora
    
    # Definición del ritmo base
    time.sleep(0.01)
```

## Reflexiones para el lector

- Multitarea por intercalado temporal: La multitarea emerge como un efecto de la velocidad del reloj, no como una ejecución simultánea real.
El sistema sostiene un único presente secuencial que, al acelerarse, se vuelve indistinguible de la simultaneidad.
 
- La verdad del cronómetro: Notarás que el tiempo "Entre ciclos" no es exactamente 0.01. Siempre es un poco más, porque el tiempo que el ESP32 tarda en calcular la velocidad y mover los motores también suma.

- El tiempo es historia: Mientras que la velocidad sube y baja de forma cíclica, el "Tiempo Total" siempre avanza. Es la flecha del tiempo sobre un proceso repetitivo.

- Inercia y frecuencia: Si cambias el time.sleep a un valor más alto, verás cómo la duración del ciclo aumenta y el movimiento de los motores se siente menos fluido.

## Ejemplo 4: El servo y la fragmentación del tiempo

**Código:** 04_servo_inercia.py

En la programación tradicional suelo pensar que una orden matemática se ejecuta de manera instantánea. El mundo físico sin embargo tiene masa e inercia. Si le exijo al servo que salte de cero a ciento ochenta grados de inmediato estoy ignorando el tiempo mecánico que le toma al engranaje moverse.

En este código rastreo el momento exacto en que el motor empieza a moverse y el momento en que llega a su destino. Como el potenciómetro es analógico y tiene ruido natural decido agregar un margen de seguridad. Así logro que mi sistema sepa claramente cuándo registrar el inicio y el final del trayecto. Al pedirte que gires la perilla de extremo a extremo mi intención es que la consola te revele cuántos segundos de ejecución necesité para fragmentar ese movimiento y hacerlo posible en el mundo real.

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
servo = ib.Servo(board.IO4)
pot = ib.AnalogIn(board.IO33)

angulo_actual = 90
angulo_objetivo = 90
en_movimiento = False
tiempo_inicio = time.monotonic()

print("Inicio mi reloj mediador y espero interaccion")
time.sleep(1)

while True:
    lectura = pot.value
    nuevo_objetivo = int((lectura / 65535) * 180)

    # Filtro el ruido fisico del potenciometro
    if abs(nuevo_objetivo - angulo_objetivo) > 2:
        angulo_objetivo = nuevo_objetivo

    # Detecto el nacimiento del movimiento temporal
    if angulo_actual != angulo_objetivo and not en_movimiento:
        en_movimiento = True
        tiempo_inicio = time.monotonic()
        print("Inicio mi desplazamiento mecanico")

    # Mi realidad fisica avanza paso a paso
    if angulo_actual < angulo_objetivo:
        angulo_actual += 1
    elif angulo_actual > angulo_objetivo:
        angulo_actual -= 1
    else:
        # Detecto la culminacion del proceso en el tiempo
        if en_movimiento:
            en_movimiento = False
            duracion = time.monotonic() - tiempo_inicio
            print("Destino alcanzado en segundos", round(duracion, 3))

    servo.angle = angulo_actual

    # El reloj que construyo dicta la fluidez del mundo fisico
    time.sleep(0.015)
```

## Ejemplo 5: El botón y el tiempo maleable

Si asumo que el bucle infinito es verdaderamente el reloj de mi programa entonces alterar la velocidad de ese ciclo debería alterar la realidad física del sistema.

En este código programo el servo para que oscile de lado a lado incesantemente como un péndulo. Guardo una marca de tiempo cada vez que el mecanismo toca los extremos lógicos de cero y ciento ochenta grados. Al pedirte que presiones el botón BOOT te doy el poder de alterar el latido fundamental del sistema. Observarás en la consola cómo el mismo trayecto pasa de tomar unos pocos segundos a tomar muchísimo más tiempo. Con este experimento te demuestro de forma contundente que la velocidad de la máquina depende enteramente de la cadencia de mi ciclo interno y no de una propiedad física de los objetos.

**Código:** 05_tiempo_maleable.py

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------
import board
import keypad
import time
from ideaboard import IdeaBoard

ib = IdeaBoard()
servo = ib.Servo(board.IO4)
keys = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)

angulo = 0
direccion = 1
ritmo_reloj = 0.01
tiempo_extremo = time.monotonic()

print("Presiona el boton BOOT para dilatar el tiempo de mi pendulo")
time.sleep(1)

while True:
    angulo += direccion
    
    # Marco el tiempo al llegar al limite superior
    if angulo >= 180:
        direccion = -1
        duracion = time.monotonic() - tiempo_extremo
        print("Llegada a 180 grados en segundos", round(duracion, 3))
        tiempo_extremo = time.monotonic()
        
    # Marco el tiempo al llegar al limite inferior
    if angulo <= 0:
        direccion = 1
        duracion = time.monotonic() - tiempo_extremo
        print("Llegada a 0 grados en segundos", round(duracion, 3))
        tiempo_extremo = time.monotonic()

    servo.angle = angulo

    # El evento digital altera mi estructura del tiempo
    event = keys.events.get()
    if event and event.pressed:
        if ritmo_reloj == 0.01:
            ritmo_reloj = 0.08
            ib.pixel = (255, 0, 0)
            print("Mi reloj se ha vuelto denso y lento")
        else:
            ritmo_reloj = 0.01
            ib.pixel = (0, 0, 255)
            print("Mi reloj ha recuperado su fluidez")

    # Mi reloj espera y define la duracion de este instante
    time.sleep(ritmo_reloj)
```

## Ejemplo 6: El tiempo como regulador y la multitarea cooperativa

En este proyecto el reloj que construyo no solo cuenta ciclos mecánicos. Aquí diseño un reloj que coordina varias tareas simultáneas y que además se corrige a sí mismo. Mi idea es que el sistema adquiera un tiempo lógico propio construido sobre las vueltas del bucle pero que intente mantenerse estable a pesar de las variaciones en la carga de trabajo.

El principio que utilizo es simple y elegante. El bucle infinito sigue siendo el único motor de mi sistema y hago que todo ocurra en estricta secuencia. Mi reloj interno avanza contando ciclos pero obligo al programa a medir cuánto tardó realmente cada vuelta en el mundo físico para ajustar el descanso del siguiente paso. Para escalar esta idea agrupo los segundos y convierto cada minuto en un ciclo mayor completo llevando la cuenta exacta de cuántos de estos ciclos de sesenta segundos han transcurrido.

De esta forma logro que el reloj deje de ser un simple contador ciego y se convierta en un regulador inteligente del ritmo. Esto me permite desacoplar parcialmente el tiempo lógico del tiempo físico sin perder estabilidad demostrando que el ESP32 me brinda la libertad de construir nociones de tiempo distintas usando el mismo hardware.

**Código:** 06_reloj_regulador.py

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------
import time
import board
from ideaboard import IdeaBoard

ib = IdeaBoard()
pot = ib.AnalogIn(board.IO33)

periodo_objetivo = 0.02
ciclos_por_segundo = int(1 / periodo_objetivo)

ciclo = 0
segundo = 0
minuto = 0

print("Inicio mi reloj autoregulado")

while True:
    inicio = time.monotonic()

    # Tarea uno evalua el mundo exterior
    valor = pot.value

    # Tarea dos manifiesta mi tiempo logico
    if segundo % 2 == 0:
        ib.pixel = (0, 10, 0)
    else:
        ib.pixel = (0, 0, 0)

    # Avanzo mi reloj logico interno
    ciclo += 1
    if ciclo >= ciclos_por_segundo:
        ciclo = 0
        segundo += 1

        # El minuto se convierte en nuestro contador de ciclos mayores
        if segundo >= 60:
            segundo = 0
            minuto += 1
            print("Ciclo mayor completado. Total de ciclos de un minuto", minuto)

        # Imprimo la evidencia de mi construccion temporal
        print("Ciclo Mayor (Minutos)", minuto, "Segundo", segundo, "Lectura ADC", valor)

    # Correccion temporal activa
    # Mido el peso de este ciclo y ajusto el descanso
    duracion = time.monotonic() - inicio
    espera = periodo_objetivo - duracion

    if espera > 0:
        time.sleep(espera)
```




