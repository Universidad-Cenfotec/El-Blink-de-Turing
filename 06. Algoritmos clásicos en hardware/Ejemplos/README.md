# Ejemplos del capítulo 6: Algoritmos clásicos en hardware

Cuando conecto la IdeaBoard a un mecanismo físico como el Sumobot, descubro rápidamente que los algoritmos clásicos dejan de ser recetas cómodas. Ya no me basta con compilar sin errores de sintaxis; necesito que el código entienda la fricción, anticipe la inercia y negocie con la gravedad. Los siguientes tres ejemplos documentan mi experiencia programando la memoria, el tiempo y el control cuando el cálculo debe convertirse en fuerza motriz.


## Ejemplo 1: Recordar es construir historia (Calibración)

La primera barrera con la que me encuentro al intentar mover el robot no es lógica, sino física: el sensor miente un poco. El giroscopio tiene un error de fábrica, un ruido térmico constante llamado *drift*. Si escribo un algoritmo que le cree ciegamente a la primera lectura, el robot pensará que está girando cuando en realidad está quieto.

Por eso, me veo obligado a cambiar mi noción de variable. Aquí no uso la memoria como una simple caja para guardar un valor, sino como un proceso. Construyo un algoritmo que detiene al robot, recolecta cientos de muestras de su estado inerte y descarta anomalías. Promediar esos valores es mi forma de construir una historia; una historia que le permite a la máquina conocer su propio error antes de intentar moverse.

## Python

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
from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC

# Inicialización
ib = IdeaBoard()
i2c = board.I2C()
sensor = LSM6DS3TRC(i2c, 0x6b)

def calibrar_drift(sensor, segundos=2):
    print(f"Recordando el pasado por {segundos} segundos para limpiar el ruido...")
    suma = 0
    muestras = 0
    t0 = time.monotonic()
    
    # El bucle construye la historia
    while time.monotonic() - t0 < segundos:
        data = sensor.gyro[2]
        
        # Evita promediar saltos que son errores evidentes de hardware
        if abs(data) < 0.008:
            suma += data
            muestras += 1
            
        time.sleep(0.005)
        
    drift = suma / muestras
    print(f"Drift calculado: {drift:.4f} rad/s")
    return drift

# --- EJECUCIÓN PRINCIPAL ---
ib.pixel = (255, 0, 0) # Rojo: El robot está "pensando/recordando"

drift_real = calibrar_drift(sensor, 5)

ib.pixel = (0, 255, 0) # Verde: Ya tiene una historia limpia, listo para actuar

print("Calibración terminada. El algoritmo ahora conoce su propia física.")
```

## Reflexiones para el lector

- **El costo de la verdad física:**  
  Conocer el estado real del mundo requiere paciencia y energía. El robot debe sacrificar tiempo de operación al inicio para garantizar que sus decisiones futuras estén fundamentadas en la realidad y no en el ruido eléctrico.

- **La memoria como filtro temporal:**  
  Guardar información no es el objetivo final; el objetivo es usar ese registro temporal para promediar el caos y extraer la estructura subyacente del hardware.

- **La autoconciencia mecánica:**  
  La máquina arranca "ciega" a sus propios defectos mecánicos. A través de la iteración algorítmica, logra medir sus propios límites y compensarlos, volviéndose más confiable.


---

# Ejemplo 2: El tiempo como urgencia (Integración y Giro)

Cuando intento que el robot gire exactamente 90 grados, descubro que la instrucción clásica `sleep()` es una trampa.

Si enciendo los motores y pongo a dormir el procesador asumiendo que el giro tomará cierto tiempo fijo, la fricción del piso o la carga de la batería arruinarán el movimiento.

El mundo cambia más rápido que mi pausa, y la máquina se vuelve ciega.

En este algoritmo, decido tratar el tiempo no como un obstáculo, sino como el engranaje principal del cálculo matemático.

Mido continuamente el diferencial de tiempo:

```text
dt = t_actual - t_anterior
```

y lo utilizo para integrar la velocidad angular.

El tiempo se vuelve mi herramienta para rastrear el recorrido real de la materia en el espacio, permitiéndole a la máquina anticipar su llegada y frenar a tiempo.

## Python

```python
# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salazar Delgado
# Gabriela Urbina Hernández
# ----------------------------------------

import time
import math
import board
from ideaboard import IdeaBoard
from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC

ib = IdeaBoard()

i2c = board.I2C()

sensor = LSM6DS3TRC(i2c, 0x6b)

RAD_A_GRADOS = 180 / math.pi


def calibrar_drift(sensor, segundos=2):

    print(f"Recordando el pasado por {segundos} segundos para limpiar el ruido...")

    suma = 0
    muestras = 0
    t0 = time.monotonic()

    while time.monotonic() - t0 < segundos:

        data = sensor.gyro[2]

        if abs(data) < 0.008:

            suma += data
            muestras += 1

        time.sleep(0.005)

    drift = suma / muestras

    print(f"Drift calculado: {drift:.4f} rad/s")

    return drift


def girar_grados(sensor, grados, drift, velocidad=0.25):

    sentido = 1 if grados > 0 else -1

    grados = abs(grados) - 2

    acumulado = 0

    t_anterior = time.monotonic()


    ib.motor_1.throttle = velocidad * sentido
    ib.motor_2.throttle = -velocidad * sentido


    while acumulado < grados:

        t_actual = time.monotonic()

        dt = t_actual - t_anterior

        t_anterior = t_actual


        vel_angular = sensor.gyro[2] - drift

        delta_grados = vel_angular * dt * RAD_A_GRADOS

        acumulado += abs(delta_grados)


        if grados - acumulado <= grados / 2:

            ib.motor_1.throttle = 0.15 * sentido

            ib.motor_2.throttle = -0.15 * sentido


        time.sleep(0.005)


    ib.motor_1.throttle = 0

    ib.motor_2.throttle = 0



# --- EJECUCIÓN PRINCIPAL ---

ib.pixel = (255, 255, 0)

drift = calibrar_drift(sensor, 2)

ib.pixel = (0, 0, 255)


print("Iniciando giro exacto de 90 grados...")

girar_grados(sensor, 90, drift)

print("Acción física terminada.")

ib.pixel = (0, 0, 0)
```

## Reflexiones para el lector

- **El tiempo como variable activa:**  
  El tiempo no es un escenario estático donde ocurre el programa; es una métrica activa (`dt`) que, al ser capturada por la lógica, cuantifica la realidad física.

- **La anticipación como conducta:**  
  Disminuir la velocidad al acercarse a la meta demuestra cómo una instrucción algorítmica debe adaptarse a la inercia del mundo físico.

- **La presencia continua:**  
  Al eliminar las pausas forzadas, el bucle de control permite que el microcontrolador mantenga una atención constante sobre el comportamiento de sus propios motores.


---

# Ejemplo 3: Cuando el cálculo toca la materia (Control PID en movimiento recto)

Avanzar en línea recta parece la instrucción más sencilla del mundo, hasta que la envío a los motores.

Me doy cuenta de que enviar un `0.5` de energía al motor izquierdo y un `0.5` al motor derecho no produce un avance recto perfecto.

Un motor tiene más fricción, el piso está levemente inclinado o la batería entrega corrientes distintas. La física ensucia la ecuación.

Para resolver esto, implemento un controlador PID discreto.

Ya no le dicto una orden cerrada a la máquina; establezco una conversación continua.

El algoritmo mide la desviación actual usando el giroscopio, recuerda el error acumulado y calcula una compensación que se suma o resta a la fuerza de las ruedas en tiempo real.

La matemática aquí no emite un resultado final; sostiene un comportamiento.

## Python

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
from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC

ib = IdeaBoard()

i2c = board.I2C()

sensor = LSM6DS3TRC(i2c, 0x6b)


def calibrar_drift(sensor, segundos=2):

    suma = 0
    muestras = 0

    t0 = time.monotonic()

    while time.monotonic() - t0 < segundos:

        data = sensor.gyro[2]

        if abs(data) < 0.008:

            suma += data
            muestras += 1

        time.sleep(0.005)

    return suma / muestras



def straight_move(velocidad, duracion, drift, Kp=0.15, Ki=0.8, Kd=0.05):

    t0 = time.monotonic()

    velocidad_base = abs(velocidad)

    direccion = 1 if velocidad > 0 else -1


    error_anterior = 0

    error_integral = 0


    while time.monotonic() - t0 < duracion:

        dt = 1


        error = sensor.gyro[2] - drift


        error_integral += error * dt

        error_derivativo = (error - error_anterior) / dt


        correccion = (

            Kp * error +

            Ki * error_integral +

            Kd * error_derivativo

        )


        correccion = max(-0.3, min(0.3, correccion))


        v1 = velocidad_base * direccion + correccion

        v2 = velocidad_base * direccion - correccion


        ib.motor_1.throttle = v1

        ib.motor_2.throttle = v2


        error_anterior = error


        time.sleep(0.01)


    ib.motor_1.throttle = 0

    ib.motor_2.throttle = 0
```

## Reflexiones para el lector

- **La negociación perpetua:**  
  Un lazo de control no busca ser perfecto en el primer intento, sino estar en constante diálogo con su propio error.

- **Límites de la matemática:**  
  Aunque la ecuación del PID pueda producir correcciones extremas, el algoritmo debe considerar las restricciones físicas del sistema.

- **La diferencia entre instrucción y comportamiento:**  
  Mandar un voltaje fijo a un motor es una instrucción; ajustar dinámicamente ese voltaje según el entorno es lo que transforma el código en conducta autónoma.
