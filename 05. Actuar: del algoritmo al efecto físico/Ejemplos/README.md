# Ejemplos del capítulo 5: Actuar es Computar

Después de comprender que un programa puede producir cambios reales sobre el mundo, surge una pregunta natural: ¿cómo ocurre esa transformación? Un microcontrolador no mueve un motor ni enciende un LED por sí solo. Lo que hace es ejecutar, una tras otra, millones de instrucciones que organizan el flujo de energía hacia distintos dispositivos. Cada decisión lógica termina convirtiéndose en una acción física.

He preparado estos tres ejemplos para observar ese proceso desde distintas perspectivas. En el primero veremos el momento más simple y directo en que un algoritmo produce un efecto visible al encender un LED. En el segundo exploraremos cómo el tiempo puede utilizarse como una herramienta computacional para crear la ilusión de una luz continua mediante una rápida sucesión de estados binarios. Finalmente, estudiaremos cómo un programa coordina el movimiento de motores utilizando únicamente su propio reloj interno, revelando las posibilidades y limitaciones de un sistema que actúa sin conocer lo que ocurre a su alrededor.

Mi intención no es únicamente mostrar cómo controlar actuadores, sino evidenciar que cada acción física es el resultado de una construcción computacional. La luz, el movimiento y la energía no aparecen por sí mismos; son la consecuencia de algoritmos que organizan señales eléctricas en el tiempo. Cuando el programa modifica el estado de un actuador, el código deja de ser una representación y se convierte en una causa. En ese instante, **actuar también es computar**.

---

# Ejemplo 1: El código sale de la pantalla (Encendido de un LED)

Cuando escribes código en una computadora, parece que todo se queda dentro de la pantalla. Pero al usar la IdeaBoard, esa ilusión se rompe.

Este código demuestra que **programar es una forma de actuar**: cuando cambias el valor a `(255, 0, 0)`, el programa deja de ser solo texto y se convierte en una orden real que envía electricidad a un componente. El resultado es inmediato: una pequeña luz se enciende en el mundo físico. No estás describiendo la luz, la estás produciendo.

## Código: `01_pulso_actuador.py`

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

# Inicializo la tarjeta para interactuar con el mundo real
ib = IdeaBoard()

print("--- El algoritmo produce un efecto físico ---")

while True:
    # A. Abrimos el paso de la electricidad: la orden se convierte en luz
    print("Enviando comando: ENCENDER")
    ib.pixel = (255, 0, 0)  # Rojo brillante: la energía sale al mundo
    time.sleep(1.5)

    # B. Cerramos el paso de la electricidad: el componente vuelve a la calma
    print("Enviando comando: APAGAR")
    ib.pixel = (0, 0, 0)    # Apagado: cortamos la corriente
    time.sleep(1.5)
```

## Reflexiones para el lector

### El algoritmo se convierte en energía

El LED nunca recibe el programa escrito en Python. Lo único que llega hasta él es una señal eléctrica generada por el microcontrolador. Entre el código y la luz existe una cadena de transformaciones donde las instrucciones se convierten en voltaje y el voltaje produce un efecto visible. El algoritmo deja de ser una idea para convertirse en un fenómeno físico.

### Actuar es modificar el estado del mundo

Encender un LED puede parecer una acción sencilla, pero representa el principio fundamental de toda la robótica. Cada vez que un programa cambia el estado de un actuador, está alterando el entorno mediante energía organizada por una secuencia de instrucciones.

---

# Ejemplo 2: La Manivela del Tiempo (PWM Manual y la Ilusión de Continuidad)

Como analizamos a fondo el funcionamiento del reloj computacional, sabemos que un microcontrolador ejecuta instrucciones de manera discreta. En este script aprovechamos precisamente esa naturaleza para fabricar la **ilusión de continuidad**.

Un microcontrolador es una máquina completamente binaria: sus pines solo pueden estar encendidos o apagados. No existe un estado intermedio donde el LED brille al cincuenta por ciento. Sin embargo, si alternamos ambos estados cientos de veces por segundo y controlamos con precisión cuánto tiempo permanece activo y cuánto tiempo permanece apagado, el ojo humano percibe un brillo continuo cuya intensidad parece variar suavemente.

## Código: `02_pwm_manual.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez López
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
import math
from ideaboard import IdeaBoard

ib = IdeaBoard()

COLOR_ENCENDIDO = (0, 0, 255)
COLOR_APAGADO = (0, 0, 0)

DURACION_CICLO = 0.02

print("--- Fabricando la ilusión de continuidad ---")

while True:
    now = time.monotonic()
    intensidad = (1 + math.sin(now * 3)) / 2

    tiempo_on = DURACION_CICLO * intensidad
    tiempo_off = DURACION_CICLO - tiempo_on

    ib.pixel = COLOR_ENCENDIDO
    time.sleep(tiempo_on)

    ib.pixel = COLOR_APAGADO
    time.sleep(tiempo_off)
```

## Reflexiones para el lector

### El tiempo también puede programarse

La intensidad de la luz no se controla modificando el voltaje del LED, sino administrando cuidadosamente el tiempo durante el cual permanece encendido. El algoritmo utiliza el reloj del microcontrolador como un recurso computacional para producir un efecto que ningún estado individual podría generar.

### La continuidad emerge de estados discretos

Lo que percibimos como una transición suave es, en realidad, una rápida sucesión de encendidos y apagados. El brillo continuo no existe físicamente; emerge del ritmo con que el algoritmo organiza la energía en el tiempo.

---

# Ejemplo 3: El algoritmo ciego (Acción de motores a lazo abierto)

En robótica, uno de los desafíos prácticos más comunes consiste en coordinar acciones mecánicas durante largos periodos sin perder precisión temporal. En este ejemplo construimos un reloj interno por software que mide la duración de cada ciclo y corrige automáticamente cualquier retraso para mantener un ritmo constante.

Ese reloj organiza la marcha de los motores: el robot avanza, se detiene, retrocede y vuelve a detenerse siguiendo una secuencia perfectamente definida. Sin embargo, el programa trabaja completamente **a lazo abierto**. El algoritmo controla el tiempo con precisión, pero nunca observa el resultado de sus acciones. Para él es irrelevante si el robot realmente avanzó, chocó contra un obstáculo o permaneció suspendido en el aire; la secuencia continúa exactamente igual.

## Código: `03_actuacion_ciega.py`

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

periodo_objetivo = 0.02
ciclos_por_segundo = int(1 / periodo_objetivo)

ciclo = 0
segundos_logicos = 0

print("--- Iniciando secuencia de motores a lazo abierto ---")
time.sleep(2.0)

while True:
    inicio_ciclo = time.monotonic()

    if segundos_logicos % 4 == 0:
        ib.motor_1.throttle = 0.5
        ib.motor_2.throttle = 0.5
        ib.pixel = (0, 20, 0)

    elif segundos_logicos % 4 == 1:
        ib.motor_1.throttle = 0
        ib.motor_2.throttle = 0
        ib.pixel = (0, 0, 0)

    elif segundos_logicos % 4 == 2:
        ib.motor_1.throttle = -0.5
        ib.motor_2.throttle = -0.5
        ib.pixel = (20, 0, 0)

    else:
        ib.motor_1.throttle = 0
        ib.motor_2.throttle = 0
        ib.pixel = (0, 0, 0)

    ciclo += 1
    if ciclo >= ciclos_por_segundo:
        ciclo = 0
        segundos_logicos += 1
        print(f"Paso actual: {segundos_logicos}s | Motores ejecutando la secuencia a ciegas.")

    duracion_trabajo = time.monotonic() - inicio_ciclo
    espera_compensada = periodo_objetivo - duracion_trabajo

    if espera_compensada > 0:
        time.sleep(espera_compensada)
```

## Reflexiones para el lector

### Un reloj puede coordinar comportamientos

El microcontrolador utiliza su propio reloj para organizar el movimiento de los motores. Midiendo el tiempo que tarda cada iteración y compensando automáticamente los retrasos, el algoritmo mantiene un comportamiento estable independientemente de pequeñas variaciones en la ejecución.

### Actuar no implica comprender

Este programa ejecuta correctamente todas sus acciones, pero nunca verifica si produjeron el efecto esperado. Es capaz de mover motores con precisión temporal y, al mismo tiempo, ser completamente indiferente a lo que ocurre en el entorno. La acción existe, pero carece de percepción.

---

# Conclusión

Los tres ejemplos muestran distintas formas en que un algoritmo produce cambios sobre el mundo físico. En un caso organiza el flujo de electricidad para generar luz; en otro utiliza el tiempo como herramienta para crear una apariencia continua; y finalmente coordina el movimiento de motores mediante un reloj interno. Aunque los actuadores sean diferentes, todos responden al mismo principio: el software organiza energía.

Al observar estos ejemplos resulta evidente que un actuador nunca ejecuta instrucciones por sí mismo. Lo que realmente hace es responder a señales eléctricas cuidadosamente producidas por el microcontrolador. Cada decisión lógica termina convirtiéndose en una transformación física. El algoritmo deja de ser únicamente información almacenada en memoria y pasa a formar parte de la cadena causal que modifica el entorno. En ese sentido, **programar también es una forma de actuar**.
