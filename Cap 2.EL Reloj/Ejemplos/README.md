# Ejemplos de capítulo 2: El reloj

He escrito estos scripts para materializar la idea del tiempo como una construcción y no solo como una medida técnica. A través de ellos, exploro cómo sostengo un presente continuo mediante el ciclo infinito, demostrando que la computación es, esencialmente, mi gestión de una secuencia de pulsos. Para mí, el reloj no es un accesorio; es la condición de posibilidad para que el sistema exista y actúe sobre el mundo físico.

# Ejemplo 1: Multitarea por intercalado temporal
Aquí demostramos que la simultaneidad es una ilusión creada por la velocidad del reloj. Dos procesos con ritmos distintos conviven en el mismo while True. No ocurren a la vez, pero ocurren tan cerca uno del otro que para nosotros son un solo comportamiento complejo.

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

