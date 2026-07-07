# Cuando el algoritmo se hace visible

La IdeaSense incorpora una matriz de LEDs que amplía considerablemente las posibilidades de interacción entre el software y el mundo físico. Mientras que un LED individual solo puede representar un único estado luminoso, una matriz permite construir patrones, desplazamientos y representaciones espaciales que evolucionan en el tiempo. La acción deja de concentrarse en un único punto y comienza a distribuirse sobre una superficie.

En estos ejemplos exploraremos cómo un algoritmo puede controlar esa superficie luminosa para producir distintos comportamientos. Primero veremos cómo una única instrucción es capaz de transformar toda la matriz en una pantalla física. Después utilizaremos nuevamente el tiempo como herramienta para modificar la percepción del brillo sin alterar el hardware. Finalmente, cerraremos el ciclo entre percepción y acción haciendo que la matriz responda continuamente a los movimientos de la tarjeta mediante el acelerómetro.

Más que aprender a encender LEDs, estos programas muestran cómo un sistema ciberfísico convierte decisiones computacionales en representaciones visibles del estado del mundo. Cada punto iluminado es el resultado de cálculos que organizan energía, espacio y tiempo para construir un comportamiento observable.

---

# Ejemplo 1: Dibujar en el espacio (La Matriz LED)

En la tarjeta IdeaSense la acción va un paso más allá. Ya no controlamos una única luz, sino una cuadrícula completa formada por veinticinco LEDs.

Aquí, **actuar es organizar el espacio**. El algoritmo toma una decisión lógica y la proyecta sobre toda la superficie de la matriz. Lo que antes era una única señal eléctrica ahora se distribuye entre múltiples puntos luminosos, transformando una instrucción escrita en una imagen física visible para cualquier observador.

## Código: `01_pulso_matriz.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez López
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideasense import IdeaSense

# Inicializo la tarjeta IdeaSense
sense = IdeaSense()

print("--- Despliegue de energía en la pantalla física ---")

while True:
    # A. Encendemos la cuadrícula completa de un solo golpe
    print("[MATRIZ] Enviando energía a los 25 LEDs...")
    sense.matrix.fill(True)
    sense.matrix.show()
    time.sleep(1.0)

    # B. Apagamos la cuadrícula completa
    print("[MATRIZ] Cortando el paso de energía...")
    sense.matrix.fill(False)
    sense.matrix.show()
    time.sleep(1.0)
```

## Reflexiones para el lector

### La acción puede ocupar un espacio

Mientras que un LED representa un único punto de salida, una matriz permite distribuir una misma decisión sobre una superficie completa. El algoritmo deja de controlar un solo actuador y comienza a construir imágenes mediante la coordinación de múltiples dispositivos físicos.

### La pantalla también es un actuador

Solemos pensar en una pantalla como un medio para mostrar información, pero desde el punto de vista de un sistema embebido sigue siendo un actuador. Cada LED recibe energía únicamente porque el programa decidió encenderlo en ese instante.

---

# Ejemplo 2: Domar el brillo con ráfagas de tiempo

La matriz de LEDs tampoco puede producir niveles intermedios de luz de manera directa. Cada LED únicamente conoce dos estados posibles: encendido o apagado. Sin embargo, el algoritmo puede utilizar el tiempo para crear la sensación de diferentes intensidades luminosas.

Al controlar cuánto tiempo permanece encendida la matriz durante cada ciclo y cuánto tiempo permanece apagada, el programa modifica la energía promedio que percibe nuestro sistema visual. La diferencia entre un brillo tenue y uno intenso no proviene del hardware, sino de la organización temporal que realiza el software.

## Código: `02_ciclo_matriz.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez López
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideasense import IdeaSense

sense = IdeaSense()

# Ventana de tiempo base (10 milisegundos)
VENTANA = 0.01

print("--- Controlando el brillo mediante ráfagas de tiempo ---")

while True:
    # Fase A: Brillo Tenue
    print("Modo de acción: Brillo bajo por software")
    for _ in range(100):
        sense.matrix.fill(True)
        sense.matrix.show()
        time.sleep(VENTANA * 0.10)

        sense.matrix.fill(False)
        sense.matrix.show()
        time.sleep(VENTANA * 0.90)

    # Fase B: Brillo Intenso
    print("Modo de acción: Brillo alto por software")
    for _ in range(100):
        sense.matrix.fill(True)
        sense.matrix.show()
        time.sleep(VENTANA * 0.90)

        sense.matrix.fill(False)
        sense.matrix.show()
        time.sleep(VENTANA * 0.10)
```

## Reflexiones para el lector

### El brillo es una construcción temporal

Cada LED continúa funcionando únicamente como un interruptor binario. La diferencia entre un brillo alto y uno bajo aparece porque el algoritmo controla cuidadosamente el tiempo durante el cual la corriente permanece circulando.

### Programar también significa administrar energía

El software nunca modifica la batería ni el circuito eléctrico de la tarjeta. Lo único que administra es el momento exacto en que permite el paso de la corriente. Desde esa organización temporal emerge una nueva propiedad perceptible para el usuario.

---

# Ejemplo 3: El lazo ciberfísico en dos dimensiones (Reaccionar al espacio en X e Y)

Hasta ahora los ejemplos mostraban acciones completamente definidas por el propio programa. En este caso ocurre algo diferente: el comportamiento depende continuamente de lo que sucede en el entorno.

El acelerómetro mide la inclinación de la tarjeta sobre los ejes X e Y. El algoritmo interpreta esas mediciones, calcula una nueva posición dentro de la matriz y desplaza un punto luminoso para representar el movimiento detectado. El programa ya no ejecuta únicamente una secuencia fija de instrucciones; responde en tiempo real a las acciones del usuario, cerrando el ciclo entre percepción, decisión y actuación.

## Código: `03_lazo_bidimensional.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez López
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideasense import IdeaSense

sense = IdeaSense()

# Línea de corte para ignorar pequeños movimientos
UMBRAL_CORRECCION = 2.0

print("--- Lazo cerrado activo: el código reacciona a tus movimientos ---")

while True:
    # Lectura del acelerómetro
    aceleracion_x, aceleracion_y, _ = sense.accel

    sense.matrix.fill(0)

    columna_led = 2
    fila_led = 2
    estado = "Centro estable"

    # Movimiento en X
    if aceleracion_x > UMBRAL_CORRECCION:
        columna_led = 4
        estado = "Inclinado a la DERECHA"
    elif aceleracion_x < -UMBRAL_CORRECCION:
        columna_led = 0
        estado = "Inclinado a la IZQUIERDA"

    # Movimiento en Y
    if aceleracion_y > UMBRAL_CORRECCION:
        fila_led = 0
        estado += " y ARRIBA" if estado != "Centro estable" else "Inclinado hacia ARRIBA"
    elif aceleracion_y < -UMBRAL_CORRECCION:
        fila_led = 4
        estado += " y ABAJO" if estado != "Centro estable" else "Inclinado hacia ABAJO"

    # Encendemos el LED calculado por el algoritmo
    sense.matrix[columna_led, fila_led] = 1
    sense.matrix.show()

    print(
        f"Mano -> X: {aceleracion_x:+5.2f} "
        f"Y: {aceleracion_y:+5.2f} | "
        f"Luz -> Matriz: [{columna_led},{fila_led}] ({estado})"
    )

    time.sleep(0.08)
```

## Reflexiones para el lector

### La acción depende del entorno

En un sistema de lazo cerrado el programa deja de ejecutar una secuencia completamente predefinida. Cada nueva lectura modifica la siguiente decisión, haciendo que el comportamiento evolucione junto con el entorno.

### La matriz representa un cálculo

El punto luminoso no se mueve porque exista un mecanismo físico dentro de la pantalla. Su posición es el resultado directo de un cálculo realizado por el algoritmo a partir de los datos del acelerómetro. La imagen que observamos es una representación visible del estado computado por el sistema.

---

# Conclusión

La matriz LED de la IdeaSense demuestra que un actuador puede ser mucho más que un dispositivo que simplemente se enciende o se apaga. Gracias a ella, el software puede construir imágenes, representar información, responder al movimiento y hacer visibles procesos que normalmente ocurren únicamente dentro del microcontrolador.

En estos ejemplos observamos cómo el algoritmo organiza el espacio iluminando una superficie completa, administra el tiempo para crear diferentes niveles aparentes de brillo y, finalmente, integra percepción y actuación para reaccionar continuamente al movimiento de la tarjeta. En todos los casos ocurre el mismo principio fundamental: las decisiones computacionales terminan manifestándose como cambios físicos que pueden observarse directamente.

Cuando un punto luminoso cambia de posición o toda la matriz modifica su estado, no estamos viendo únicamente LEDs encenderse y apagarse. Estamos observando el resultado tangible de un algoritmo que interpreta información, toma decisiones y utiliza la energía para actuar sobre el mundo. En la IdeaSense, la computación literalmente se hace visible.
