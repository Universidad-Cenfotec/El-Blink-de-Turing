# Ejemplos del capítulo: **Sensar es Computar**

He escrito estos scripts como complemento práctico de la lectura para que experimentemos juntos cómo la tarjeta IdeaSense interactúa con su entorno. Mi objetivo es materializar el concepto central del capítulo: demostrar que un sensor no es un dispositivo pasivo que solo acumula números, sino el punto de partida donde el microcontrolador procesa, filtra y transforma la realidad física en estados lógicos.

A través de estos cuatro códigos, observaremos cómo el programa inventa contextos a través de la memoria, cómo utiliza el tiempo de ejecución como un reloj implícito y cómo impone fronteras digitales al flujo continuo de la naturaleza. Para mí, el código es la herramienta que nos permite razonar sobre el comportamiento del sistema y convertir los fenómenos invisibles del entorno en pura computación.

---

# Ejemplo 1: Inventando el contexto (Sensor de Luz)

En este primer script, quiero demostrarte que un sensor por sí solo no sabe qué significan sus lecturas. El sensor de luz de nuestra tarjeta solo entrega números abstractos; no sabe si está en un cuarto oscuro o bajo el sol, ni entiende lo que es una "sombra".

**Sensar es computar** porque mi programa guarda en su memoria cómo estaba la luz al principio (creo una línea base) y, a partir de ahí, calculo de forma matemática si algo tapó la tarjeta. Además, incluí un truco en mi código para que el sistema no falle si lo enciendes en oscuridad absoluta.

## Código: `01_luz_discreta.py`

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

# 1. Inicializo la placa con sus sensores integrados
dispositivo = IdeaSense()

print("Calibrando sensor de luz... No tapes la placa.")
time.sleep(1.0)

# 2. Capturo del estado inicial del entorno (Línea Base)
# Protección: Si la luz base es 0 lx, asigno 1 lx para evitar divisiones por cero en el bucle
linea_base_luz = dispositivo.light if dispositivo.light > 0 else 1
umbral_tolerancia = 0.70

print(f"Calibración completada. Luz ambiente base: {linea_base_luz} lx")

while True:
    luz_actual = dispositivo.light

    if luz_actual < (linea_base_luz * umbral_tolerancia):
        objeto_detectado = True
        dispositivo.matrix.fill(True)
    else:
        objeto_detectado = False
        dispositivo.matrix.fill(False)

    dispositivo.matrix.show()

    proporcion = (luz_actual / linea_base_luz) * 100

    estado_texto = "¡SOMBRA DETECTADA!" if objeto_detectado else "Normal"
    print(f"Luz Actual: {luz_actual:4d} lx | Proporción: {proporcion:5.1f}% | Estado: {estado_texto}")

    time.sleep(0.1)
```

## Reflexiones para el lector

### La invención del contexto

El sensor de luz solo entrega un número plano en luxes. El número por sí solo no significa "luz" o "sombra". Es el microcontrolador el que, al guardar la `linea_base_luz` en su memoria al inicio, inventa un punto de comparación para decidir cuándo el entorno ha cambiado de forma significativa.

### La adaptación al espacio

Si ejecutas este código en un cuarto oscuro o bajo la luz del sol, el sistema funcionará igual de bien porque computa de forma matemática una proporción relativa, demostrando que la certeza de un sistema ciberfísico puede ser dinámica.

---

# Ejemplo 2: Inventando la idea de "Agitación" (Giroscopio)

En este ejemplo transformo tres lecturas de movimiento separadas (los ejes X, Y, Z del giroscopio) en un concepto abstracto que ningún sensor físico puede medir directamente: saber si estamos agitando la tarjeta.

Aquí, **sensar es computar** porque mi código toma esos datos crudos, calcula la fuerza total combinando las tres direcciones en tiempo real y decide si el movimiento es lo suficientemente caótico.

## Código: `02_deteccion_agitacion.py`

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

dispositivo = IdeaSense()

UMBRAL_AGITACION = 3.5

print("--- Monitor Cinético Inercial Activo ---")

while True:
    gyro_x, gyro_y, gyro_z = dispositivo.gyro

    energia_rotacional = abs(gyro_x) + abs(gyro_y) + abs(gyro_z)

    if energia_rotacional > UMBRAL_AGITACION:
        print(f"[MOVIMIENTO] Magnitud: {energia_rotacional:.2f} rad/s -> ¡Agitando Placa!")
        dispositivo.matrix.fill(True)
    else:
        dispositivo.matrix.fill(False)

    dispositivo.matrix.show()

    time.sleep(0.08)
```

## Reflexiones para el lector

### El sensor como reloj implícito

La velocidad angular describe el cambio de ángulo por unidad de tiempo (rad/s). El giroscopio ya encapsula el tiempo dentro de su medición física.

### La construcción de la narrativa del movimiento

Mover la placa suavemente en línea recta no activa la alerta, pero rotarla o agitarla sí. La máquina computa una estructura específica de movimiento.

---

# Ejemplo 3: Adivinar el futuro con el clima (Temperatura y Humedad)

Los cambios del clima en el mundo real ocurren lentamente. En este script, **sensar es computar** porque el microcontrolador compara el presente con el pasado inmediato para inferir una tendencia.

## Código: `03_tendencia_climatica.py`

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

dispositivo = IdeaSense()

humedad_anterior = dispositivo.humid
TOLERANCIA_CAMBIO = 0.15

print("--- Analizador Climático del Entorno Iniciado ---")

while True:
    temperatura_c = dispositivo.temp
    humedad_actual = dispositivo.humid

    delta_humedad = humedad_actual - humedad_anterior

    if abs(delta_humedad) > TOLERANCIA_CAMBIO:
        if delta_humedad > 0:
            tendencia = "INCREMENTANDO (Humedeciendo/Evaporación) 📈"
        else:
            tendencia = "DECRECIENDO (Secado/Ventilación) 📉"
    else:
        tendencia = "ESTABLE 🔄"

    print(f"[CLIMA] Temp: {temperatura_c:.1f}°C | Humedad: {humedad_actual:.2f}% | Tendencia HR: {tendencia}")

    humedad_anterior = humedad_actual

    time.sleep(2.0)
```

## Reflexiones para el lector

### La escala del tiempo computacional

Mientras que para el acelerómetro medimos centésimas de segundo, para el clima utilizamos ventanas temporales mucho mayores.

### La invención del futuro inmediato

Al calcular `delta_humedad`, el sistema adquiere la capacidad de inferir hacia dónde evoluciona el fenómeno físico.

---

# Ejemplo 4: Obligar al mundo a tomar un bando (Acelerómetro)

La naturaleza cambia de forma continua, pero las computadoras necesitan decisiones discretas. En este ejemplo, **sensar es computar** porque imponemos un umbral que transforma una magnitud continua en una decisión binaria.

## Código: `04_umbral_equilibrio.py`

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

UMBRAL_INCLINACION = 3.0

print("--- El Umbral del Equilibrio ---")
print("Gira la tarjeta IdeaSense hacia la izquierda o derecha.")
time.sleep(2)

while True:
    aceleracion_x, aceleracion_y, aceleracion_z = sense.accel

    sense.matrix.fill(0)

    if aceleracion_x > UMBRAL_INCLINACION:
        bit_estado = 1
        direccion = "DERECHA"
        sense.matrix[4, 2] = 1

    elif aceleracion_x < -UMBRAL_INCLINACION:
        bit_estado = 1
        direccion = "IZQUIERDA"
        sense.matrix[0, 2] = 1

    else:
        bit_estado = 0
        direccion = "CENTRO (Plano)"
        sense.matrix[2, 2] = 1

    sense.matrix.show()

    print(f"Gravedad X: {aceleracion_x:>6.2f} | Estado: {direccion:<15} | Bit: {bit_estado}")

    time.sleep(0.2)
```

## Reflexiones para el lector

### El juicio digital como frontera

El universo físico no conoce la "izquierda" ni la "derecha". Es el programador quien impone una frontera lógica mediante un umbral.

### La reducción del caos sensorial

Una lectura tridimensional del acelerómetro termina convertida en un único LED encendido. El sistema descarta información irrelevante y conserva únicamente aquella necesaria para tomar una decisión.

---

# Conclusión

Estos cuatro ejemplos muestran que **sensar no consiste únicamente en leer un sensor**, sino en transformar las señales del mundo físico mediante memoria, tiempo, umbrales y operaciones matemáticas. El sensor proporciona datos; el programa construye significado. En ese proceso de interpretación, clasificación y decisión, el acto de **sensar se convierte en computar**.
