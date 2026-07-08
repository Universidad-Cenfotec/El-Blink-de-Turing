Algoritmos clásicos para interpretar el mundo físico

Después de explorar cómo los algoritmos clásicos permiten comprender la relación entre memoria, tiempo, decisión y control, el siguiente paso consiste en observar cómo estas ideas toman forma sobre hardware real. Al pasar del Sumobot a la IdeaSense, el problema cambia de naturaleza. Ya no intento mover la materia mediante motores, sino interpretar los fenómenos físicos que los sensores capturan continuamente.

La tarjeta IdeaSense está inmersa en un flujo permanente de información: la gravedad actúa sobre el acelerómetro, los fotones llegan al sensor de luz y las variaciones de capacitancia permiten detectar el contacto de los dedos con los botones táctiles del ideaboard. Sin embargo, estos fenómenos físicos no llegan al microcontrolador como conceptos, sino como secuencias de valores numéricos que deben ser procesados antes de convertirse en información útil.

En este contexto, los algoritmos clásicos adquieren un significado diferente. Digitalizar deja de ser únicamente convertir una señal analógica en números; también implica reducir el ruido para obtener una representación estable del entorno. Ordenar ya no consiste solamente en reorganizar datos, sino en establecer prioridades cuando múltiples eventos físicos ocurren al mismo tiempo. Buscar, finalmente, significa recorrer continuamente un flujo de mediciones para detectar patrones que permitan tomar una decisión, aun cuando la máquina no comprenda el significado de aquello que encuentra.

Los siguientes ejemplos muestran cómo estos algoritmos se convierten en mecanismos para interpretar el mundo físico mediante la IdeaSense, transformando fenómenos continuos en decisiones discretas que el sistema puede ejecutar.

---

# Ejemplo 1: Digitalizar es perder para pensar (Filtro exponencial sobre el acelerómetro)

El acelerómetro nunca permanece completamente inmóvil. Incluso cuando la tarjeta descansa sobre una superficie estable, el sensor continúa registrando pequeñas vibraciones mecánicas, ruido eléctrico y variaciones propias de la electrónica. Si estos datos se utilizaran directamente para controlar la matriz LED, el resultado sería una representación errática del movimiento, haciendo imposible distinguir entre un cambio real y una simple perturbación.

Para obtener una lectura útil, es necesario filtrar la información antes de interpretarla. En este ejemplo se implementa un filtro de media móvil exponencial (*Exponential Moving Average*, EMA). Este algoritmo reduce la influencia de las mediciones instantáneas y otorga mayor importancia a la historia reciente del sistema.

Desde la perspectiva del capítulo, este algoritmo demuestra que digitalizar no significa conservar toda la información disponible. Por el contrario, implica renunciar deliberadamente a una parte de los datos para construir una representación más estable del mundo físico. La máquina pierde sensibilidad frente a pequeñas fluctuaciones, pero gana estabilidad para tomar decisiones posteriores.

**Código:** `01_filtro_ema.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideasense import IdeaSense

# 1. Inicialización
# Activamos la tarjeta, la matriz y los sensores I2C (LTR303, SHT31D, LSM6DS3TRC)
sense = IdeaSense()

# Factor de ponderación (Alpha) para el filtro matemático:
# Un valor de 0.2 significa que la máquina solo creerá un 20% en la lectura nueva
# y confiará un 80% en lo que ya recordaba.
ALPHA = 0.2

print("--- Filtrando ruido físico para encontrar estabilidad ---")
print("Mueve la tarjeta para ver el píxel reaccionar a la gravedad.")

# Estado inicial en la memoria de la máquina
mem_x, mem_y, _ = sense.accel

# El bucle infinito mantiene a la máquina observando el mundo
while True:

    # Capturamos la realidad cruda y ruidosa del acelerómetro
    crudo_x, crudo_y, _ = sense.accel

    # 2. Digitalizar es perder para pensar:
    # El filtro digital aplasta las microvibraciones. Negociamos con la física
    # estabilizando los números matemáticamente antes de usarlos.
    mem_x = (ALPHA * crudo_x) + ((1.0 - ALPHA) * mem_x)
    mem_y = (ALPHA * crudo_y) + ((1.0 - ALPHA) * mem_y)

    # 3. Restricción al plano material (Matriz 5x5):
    # Asumimos que la gravedad varía entre -9.8 y 9.8 m/s².
    # Transformamos ese espectro continuo en un índice discreto de 0 a 4.
    # La función max() y min() asegura que el cálculo no desborde el hardware.
    pos_x = int(max(0, min(4, (mem_x + 9.8) / 19.6 * 5)))
    pos_y = int(max(0, min(4, (mem_y + 9.8) / 19.6 * 5)))

    # 4. Actuar sobre la interfaz visual:
    # Borramos el lienzo del pasado
    sense.matrix.fill(0)

    # Encendemos la coordenada calculada y filtrada
    sense.matrix[pos_x, pos_y] = 1
    sense.matrix.show()

    # Pequeña pausa para no saturar el bus de comunicación
    time.sleep(0.05)
```

## Reflexiones para el lector

- **La destrucción como condición para comprender.** Un sistema digital no necesita conservar cada detalle del mundo físico. Para producir una representación útil, debe descartar parte de la información y conservar únicamente aquello que resulta significativo para la tarea que realiza.

- **La memoria como herramienta de interpretación.** El filtro exponencial demuestra que el pasado puede ser más confiable que el presente cuando las mediciones están contaminadas por ruido. La memoria deja de ser un simple almacenamiento y se convierte en un mecanismo para construir estabilidad.

- **La discretización del mundo físico.** El acelerómetro mide una magnitud continua, pero la matriz LED únicamente puede representar cinco posiciones por eje. El algoritmo transforma una realidad continua en un conjunto reducido de estados discretos, recordándonos que toda representación digital es una aproximación del mundo y no una copia exacta de él.

## Ejemplo 2: Ordenar es descubrir estabilidad (Ordenamiento de mediciones del sensor de luz)

Cuando observo el sensor de luz de la IdeaSense noto que nunca entrega exactamente el mismo valor. Aunque la tarjeta permanezca inmóvil sobre la mesa, pequeñas variaciones del ambiente, el ruido electrónico y las fluctuaciones naturales producen una secuencia continua de mediciones ligeramente diferentes.

Si reaccionara a cada lectura individual, el programa respondería a variaciones insignificantes y el comportamiento del sistema sería inestable. Antes de interpretar el entorno necesito organizar la información.

Aquí aparece uno de los algoritmos clásicos más importantes de la computación: el **ordenamiento**. En lugar de analizar una única medición, el programa recopila varias muestras consecutivas del sensor de luz y las ordena de menor a mayor. Gracias a esta organización resulta sencillo identificar el valor mínimo, el máximo y la mediana, obteniendo una representación mucho más confiable del estado real del ambiente.

El algoritmo no modifica la realidad física. Lo que transforma es la manera en que la máquina organiza sus observaciones para descubrir estructura dentro del ruido.

**Código:** `02_ordenar_lecturas_luz.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideasense import IdeaSense

# Inicialización
idea = IdeaSense()

print("--- Ordenando mediciones del sensor de luz ---")

while True:

    # 1. Capturar varias mediciones consecutivas
    lecturas = []

    for i in range(15):
        lecturas.append(idea.light)
        time.sleep(0.05)

    # 2. Ordenar las mediciones de menor a mayor
    lecturas.sort()

    # 3. Obtener estadísticas básicas
    minimo = lecturas[0]
    maximo = lecturas[-1]
    mediana = lecturas[len(lecturas) // 2]

    print("\nLecturas ordenadas:")
    print(lecturas)

    print(f"Mínimo : {minimo}")
    print(f"Mediana: {mediana}")
    print(f"Máximo : {maximo}")

    # 4. Representar visualmente la intensidad de la mediana
    idea.matrix.fill(0)

    if mediana < 300:
        idea.matrix[2, 4] = 1

    elif mediana < 700:
        for y in range(5):
            idea.matrix[2, y] = 1

    else:
        idea.matrix.fill(1)

    idea.matrix.show()

    time.sleep(1)
```

## Reflexiones para el lector

- **Ordenar revela estructura.** Antes del ordenamiento existe únicamente una colección de números obtenidos del sensor. Después de aplicar el algoritmo aparecen relaciones entre ellos que permiten identificar el valor mínimo, el máximo y una medición representativa del conjunto.

- **La estabilidad surge del conjunto y no de una sola lectura.** Una medición aislada puede estar afectada por pequeñas perturbaciones del ambiente. Al organizar varias observaciones consecutivas, el sistema obtiene una descripción mucho más confiable del fenómeno físico.

- **Los algoritmos organizan la experiencia del mundo.** El sensor únicamente produce una secuencia de valores numéricos. Es el algoritmo de ordenamiento quien transforma esa secuencia en información útil, permitiendo que la máquina interprete el entorno de forma más consistente antes de tomar una decisión.

## Ejemplo 3: Buscar es reconocer un patrón (Búsqueda secuencial en mediciones de luz)

Buscar suele asociarse con recorrer listas, bases de datos o archivos. Sin embargo, cuando trabajo con la IdeaSense descubro que también es posible buscar dentro del mundo físico. La diferencia es que los datos no están almacenados de antemano: aparecen conforme los sensores observan el entorno.

En este ejemplo, la tarjeta toma una secuencia de mediciones del sensor de luz y las almacena temporalmente en memoria. Después, el algoritmo realiza una **búsqueda secuencial**, recorriendo una a una las lecturas hasta encontrar la primera que supera un umbral definido.

La máquina no comprende qué significa una sombra, una linterna o la luz del sol. Únicamente compara números. Cuando una medición satisface la condición establecida, la búsqueda termina y el sistema actúa. Así, un algoritmo clásico permite detectar un fenómeno físico sin necesidad de comprender su significado.

**Código:** `03_busqueda_secuencial_luz.py`

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
from ideasense import IdeaSense

# Inicialización
idea = IdeaSense()

# Umbral considerado como "luz intensa"
UMBRAL_LUZ = 700

print("--- Búsqueda secuencial de un patrón de luz ---")

while True:

    # 1. Capturar varias mediciones consecutivas
    lecturas = []

    for i in range(20):
        lecturas.append(idea.light)
        time.sleep(0.03)

    # 2. Buscar secuencialmente la primera lectura
    # que supera el umbral establecido
    encontrada = False

    for valor in lecturas:

        if valor >= UMBRAL_LUZ:
            encontrada = True
            break

    # 3. Mostrar el resultado de la búsqueda
    idea.matrix.fill(0)

    if encontrada:
        print("Patrón encontrado.")
        print(f"Lectura detectada: {valor}")

        # Encender toda la matriz
        idea.matrix.fill(1)

    else:
        print("No se encontró ninguna lectura superior al umbral.")

        # Dibujar una X sencilla
        for i in range(5):
            idea.matrix[i, i] = 1
            idea.matrix[4 - i, i] = 1

    idea.matrix.show()

    time.sleep(1)
```

## Reflexiones para el lector

- **Buscar implica recorrer información.** La máquina no conoce de antemano dónde aparecerá el evento que busca. Debe inspeccionar cada medición una por una hasta encontrar una que cumpla la condición establecida.

- **La búsqueda termina cuando aparece una coincidencia.** En una búsqueda secuencial, no es necesario revisar el resto de los datos una vez que el objetivo ha sido encontrado. El algoritmo concluye inmediatamente y puede actuar sobre el mundo físico.

- **La interpretación surge de una condición matemática.** El sensor únicamente entrega números. Es el algoritmo quien decide que un valor superior al umbral representa un evento relevante, transformando una simple comparación numérica en una acción observable para el usuario.
