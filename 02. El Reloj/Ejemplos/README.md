# Ejemplos de capítulo 2: El reloj

He escrito estos scripts para materializar la idea del tiempo como una construcción y no solo como una medida técnica. A través de ellos, exploro cómo sostengo un presente continuo mediante el ciclo infinito, demostrando que la computación es, esencialmente, mi gestión de una secuencia de pulsos. Para mí, el reloj no es un accesorio; es la condición de posibilidad para que el sistema exista y actúe sobre el mundo físico.

## Ejemplo 1: Multitarea por intercalado temporal
Aquí demostramos que la simultaneidad es una ilusión creada por la velocidad del reloj. Dos procesos con ritmos distintos conviven en el mismo while True. No ocurren a la vez, pero ocurren tan cerca uno del otro que para nosotros son un solo comportamiento complejo.

### Código: 01_intercalado.py 

```python
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


### Código:  02_latido_logico.py

``` python

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


### Código: 03cronometro_reloj.py

``` python
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
