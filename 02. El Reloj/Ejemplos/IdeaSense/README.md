# La Construcción del Tiempo en el IdeaSense

Todo lo que hemos discutido sobre la ejecución de instrucciones cobra una nueva dimensión cuando introducimos el reloj del microcontrolador. Mientras que en la programación básica el tiempo es solo algo que transcurre de fondo, en la computación física el tiempo es una variable maleable.

El principio fundamental que rige este capítulo es:

> En la computación física, el tiempo no es algo que simplemente pasa o se espera; es una materia prima que el programador moldea, acumula y controla.

---

# Ejemplo 1: La Ilusión de Continuidad (Límites de la percepción)

El reloj de una computadora es muchísimo más rápido que el reloj biológico humano. En este ejemplo, vamos a jugar con esa diferencia fisiológica.

El programa enciende y apaga la matriz constantemente. Al principio, el tiempo de espera es largo y vemos un parpadeo claro y definido. Sin embargo, poco a poco el programa reduce la pausa, acelerando el latido del sistema. Llegará un punto donde la máquina seguirá encendiendo y apagando la luz, pero nuestros ojos ya no lograrán registrar el momento de oscuridad.

Al obligar a la luz a oscilar a altas velocidades, demostramos que la estabilidad visual de las pantallas que usamos a diario es, en realidad, un engaño sostenido por un reloj muy rápido.

## Código: `01_ilusion_continuidad.py`

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

# Inicialización
sense = IdeaSense()

tiempo_espera = 0.5
estado_luz = False

print("--- La Ilusión de Continuidad ---")
print("Observa como el parpadeo desaparece al acelerar el reloj")
time.sleep(2)

while True:
    # 1. Alternamos el estado lógico
    estado_luz = not estado_luz
    
    # 2. Dibujamos en memoria
    if estado_luz:
        sense.matrix.fill(1)
    else:
        sense.matrix.fill(0)
        
    # 3. Publicamos los cambios en la matriz física
    sense.matrix.show()
        
    # 4. Esperamos el tiempo dictado por nuestra variable
    time.sleep(tiempo_espera)
    
    # El reloj se vuelve un 5% más rápido en cada vuelta
    tiempo_espera = tiempo_espera * 0.95
    
    # Evitamos que el ciclo colapse a cero absoluto
    if tiempo_espera < 0.005:
        print("Límite de percepción alcanzado")
        time.sleep(3)
        
        # Reiniciamos la ilusión
        tiempo_espera = 0.5
```

---

# Para reflexionar sobre este código

## El reloj biológico frente al silicio

El cerebro humano comienza a fusionar imágenes en movimiento continuo cuando suceden a más de 24 o 30 veces por segundo. Para un microcontrolador que opera en el rango de los megahercios, esperar una trigésima de segundo es una eternidad.

Lo que para nosotros es "rápido", para la placa es un proceso lento y perfectamente controlado.

---

## La velocidad oculta el proceso

Cuando el valor de `tiempo_espera` cae por debajo de aproximadamente 0.02 segundos, la matriz parece emitir una luz constante.

Sin embargo, el procesador continúa ejecutando los ciclos de encendido y apagado. El estado físico sigue siendo discreto y alternante, pero nuestra percepción lo comprime en una señal aparentemente continua.

---

## El engaño de las pantallas

Este principio es exactamente el mismo que utilizan los monitores y televisores.

No emiten luz continua; actualizan sus píxeles decenas o cientos de veces por segundo. La sensación de continuidad emerge de la velocidad del reloj y de los límites de nuestra percepción.

---

# Concepto clave

> La continuidad que percibimos en el mundo digital suele ser una ilusión temporal. La máquina siempre está oscilando entre ceros y unos, pero cuando el reloj supera la velocidad de nuestra biología, el parpadeo se transforma en una realidad estable.

---

# Ejemplo 2: Reloj Regulador (Multitarea Cooperativa)

En la programación tradicional solemos usar `time.sleep()` para pausar el código. Pero `sleep` es ciego: congela absolutamente todo el sistema, impidiendo que la máquina lea sensores o reaccione al mundo físico.

Si queremos construir sistemas robustos, no podemos detenerlos. Debemos enseñarles a medir su propio tiempo de ejecución utilizando `time.monotonic()`.

En este ejemplo, el sistema tiene dos tareas simultáneas:

1. Leer el sensor de luz.
2. Mantener un reloj lógico preciso.

Para lograr que cada segundo lógico corresponda exactamente a un segundo real, el programa calcula cuánto tiempo tomó ejecutar sus tareas y ajusta automáticamente el tiempo restante de espera.

## Código: `02_reloj_regulador.py`

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

# Inicialización
sense = IdeaSense()

periodo_objetivo = 0.02
ciclos_por_segundo = int(1 / periodo_objetivo)

ciclo = 0
segundo = 0
minuto = 0

print("--- Reloj Regulador (Multitarea Cooperativa) ---")
print("Inicio mi reloj autorregulado")
time.sleep(2)

while True:
    # 1. Marcamos el instante exacto de inicio
    inicio = time.monotonic()

    # Tarea 1: Evaluar el mundo exterior
    valor_luz = sense.light

    # Tarea 2: Manifestar el tiempo lógico
    if segundo % 2 == 0:
        sense.matrix.fill(1)
    else:
        sense.matrix.fill(0)

    sense.matrix.show()

    # Avance del reloj lógico
    ciclo += 1

    if ciclo >= ciclos_por_segundo:
        ciclo = 0
        segundo += 1

        if segundo >= 60:
            segundo = 0
            minuto += 1
            print(f"Ciclo mayor completado. Total de minutos: {minuto}")

        print(f"Min: {minuto} | Seg: {segundo} | Luz: {valor_luz:>5.1f}")

    # Corrección temporal activa
    duracion = time.monotonic() - inicio
    espera = periodo_objetivo - duracion

    if espera > 0:
        time.sleep(espera)
```

---

# Para reflexionar sobre este código

## El procesamiento no es gratuito

Toda instrucción consume tiempo.

Leer sensores, actualizar LEDs o ejecutar operaciones matemáticas requiere recursos físicos y tiempo de procesamiento.

Si utilizáramos simplemente `time.sleep(1)` en cada ciclo, el tiempo real sería:

```text
1 segundo + tiempo de procesamiento
```

Con el paso de los minutos, el reloj terminaría acumulando errores.

---

## La compensación activa

La línea:

```python
espera = periodo_objetivo - duracion
```

es el corazón de muchos sistemas en tiempo real.

El sistema mide cuánto tardó en trabajar y ajusta automáticamente el tiempo restante para conservar un período constante.

---

## La ilusión de la multitarea

Un microcontrolador no necesariamente ejecuta múltiples tareas exactamente al mismo tiempo.

Sin embargo, al alternarlas rápidamente y evitar pausas largas, produce la ilusión de simultaneidad.

Mientras actualiza el reloj, también atiende sensores y controla la matriz LED.

---

# Concepto clave

> Un sistema robusto no espera a ciegas. Mide constantemente su propia velocidad de ejecución y compensa matemáticamente sus retrasos para mantenerse sincronizado con el mundo real.

---

# Ejemplo 3: El Reloj de Arena Digital (Tiempo Acumulado)

Hasta ahora hemos utilizado el reloj para controlar la velocidad del programa. En este ejemplo lo utilizaremos como una herramienta para representar visualmente el paso del tiempo.

Cada segundo que transcurra se transformará en un píxel encendido dentro de la matriz LED. Mediante operaciones matemáticas sencillas, convertiremos un contador lineal en coordenadas espaciales.

La matriz se transformará en un reloj de arena digital donde cada segundo deja una huella visible.

## Código: `03_reloj_arena.py`

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

# Inicialización
sense = IdeaSense()

columnas = 5
filas = 5
total_leds = columnas * filas

contador_segundos = 0

print("--- El Reloj de Arena Digital ---")
print("Cada segundo quedará registrado como un punto de luz")

sense.matrix.fill(0)
sense.matrix.show()

time.sleep(2)

while True:
    # Convertimos el tiempo en coordenadas
    x = contador_segundos % columnas
    y = contador_segundos // columnas

    # Dibujamos el segundo actual
    sense.matrix[x, y] = 1
    sense.matrix.show()

    print(
        f"Segundo {contador_segundos + 1} completado. "
        f"Luz en ({x}, {y}) encendida."
    )

    contador_segundos += 1

    # Reinicio cuando la matriz se llena
    if contador_segundos >= total_leds:
        print("¡Matriz llena! Reiniciando el reloj de arena...")
        time.sleep(2)

        sense.matrix.fill(0)
        sense.matrix.show()

        contador_segundos = 0

    # Latido exacto del reloj
    time.sleep(1)
```

---

# Para reflexionar sobre este código

## El tiempo como espacio físico

Normalmente representamos el tiempo como una secuencia lineal:

```text
1, 2, 3, 4, 5...
```

Sin embargo, utilizando el operador módulo (`%`) y la división entera (`//`), podemos convertir ese contador en coordenadas espaciales.

Cada instante adquiere una ubicación física dentro de la matriz LED.

---

## La acumulación de estados

A diferencia de muchos programas que borran la pantalla en cada ciclo, aquí cada segundo permanece registrado.

La matriz conserva el historial reciente del sistema y construye una memoria visual temporal.

---

## El ciclo inquebrantable

Los relojes físicos rara vez avanzan hacia el infinito.

Los relojes analógicos, digitales y los relojes de arena funcionan mediante ciclos.

Cuando el contador alcanza la capacidad máxima de la matriz, el sistema reinicia el proceso y vuelve a comenzar.

---

# Concepto clave

> El tiempo lineal e invisible puede representarse físicamente mediante la matemática. Al asignar coordenadas espaciales a cada instante, transformamos una variable abstracta en una experiencia visual y tangible.
