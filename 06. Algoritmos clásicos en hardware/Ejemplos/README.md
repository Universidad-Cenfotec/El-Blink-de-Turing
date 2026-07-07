# Ejemplos del capítulo 6: Algoritmos clásicos en hardware

Cuando conecto la IdeaBoard a un mecanismo físico como el Sumobot, descubro rápidamente que los algoritmos clásicos dejan de ser recetas cómodas. Ya no me basta con compilar sin errores de sintaxis; necesito que el código entienda la fricción, anticipe la inercia y negocie con la gravedad. Los siguientes tres ejemplos documentan mi experiencia programando la memoria, el tiempo y el control cuando el cálculo debe convertirse en fuerza motriz.


## Ejemplo 1: Recordar es construir historia (Calibración)

La primera barrera con la que me encuentro al intentar mover el robot no es lógica, sino física: el sensor miente un poco. El giroscopio tiene un error de fábrica, un ruido térmico constante llamado *drift*. Si escribo un algoritmo que le cree ciegamente a la primera lectura, el robot pensará que está girando cuando en realidad está quieto.

Por eso, me veo obligado a cambiar mi noción de variable. Aquí no uso la memoria como una simple caja para guardar un valor, sino como un proceso. Construyo un algoritmo que detiene al robot, recolecta cientos de muestras de su estado inerte y descarta anomalías. Promediar esos valores es mi forma de construir una historia; una historia que le permite a la máquina conocer su propio error antes de intentar moverse.



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

# 1. Inicialización de la materia
# Preparamos la tarjeta, el bus de comunicación y el sensor giroscópico
ib = IdeaBoard()
i2c = board.I2C()
sensor = LSM6DS3TRC(i2c, 0x6b)

def calibrar_drift(sensor, segundos=2):
    print(f"Recordando el pasado por {segundos} segundos para limpiar el ruido...")
    
    # Variables de memoria: construirán la historia de lecturas
    suma = 0
    muestras = 0
    
    # Registramos el instante en que inicia el proceso
    t0 = time.monotonic()
    
    # El bucle mantiene atrapada a la máquina leyendo la realidad
    # hasta que el tiempo establecido se agote.
    while time.monotonic() - t0 < segundos:
        # Extraemos la velocidad angular en el eje Z (giro horizontal)
        data = sensor.gyro[2]
        
        # Filtro de anomalías: 
        # Si el valor es demasiado alto, asumimos que fue un pico de ruido 
        # o un golpe físico, por lo que lo ignoramos y no entra en la memoria.
        if abs(data) < 0.008:
            suma += data
            muestras += 1
            
        # Pequeña pausa para no saturar el bus de comunicación I2C
        time.sleep(0.005)
        
    # El promedio final es nuestra "verdad" calculada sobre el error del sensor
    drift = suma / muestras
    print(f"Drift calculado: {drift:.4f} rad/s")
    return drift

# --- EJECUCIÓN PRINCIPAL ---

# Encendemos el LED en rojo puro indicando que la máquina está "ciega" y pensando
ib.pixel = (255, 0, 0) 

# Ejecutamos la calibración por 5 segundos antes de permitir cualquier movimiento
drift_real = calibrar_drift(sensor, 5)

# LED en verde: la máquina ahora conoce su propia física y está lista
ib.pixel = (0, 255, 0) 
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

# Constante para traducir los radianes del sensor a grados comprensibles
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
    # Determinamos si el motor gira hacia la izquierda o derecha
    sentido = 1 if grados > 0 else -1
    
    # Restamos 2 grados para compensar la inercia del robot (frenado imperfecto)
    grados = abs(grados) - 2 
    acumulado = 0
    
    # Marca de tiempo inicial antes de empezar a movernos
    t_anterior = time.monotonic()

    # Arrancamos aplicando fuerza bruta inicial a los motores (uno adelante, otro atrás)
    ib.motor_1.throttle = velocidad * sentido
    ib.motor_2.throttle = -velocidad * sentido

    # El bucle se mantiene vivo mientras no hayamos alcanzado el ángulo deseado
    while acumulado < grados:
        # 1. El tiempo como engranaje (dt)
        t_actual = time.monotonic()
        dt = t_actual - t_anterior
        t_anterior = t_actual

        # 2. Integración: Velocidad angular compensada multiplicada por el tiempo transcurrido
        vel_angular = sensor.gyro[2] - drift
        delta_grados = vel_angular * dt * RAD_A_GRADOS
        
        # Sumamos el pequeño desplazamiento de este milisegundo al total
        acumulado += abs(delta_grados)

        # 3. Anticipación al futuro
        # Si ya completamos más de la mitad del giro, reducimos la velocidad.
        # Esto evita el "overshoot" causado por la inercia del chasis pesado.
        if grados - acumulado <= grados / 2:
            ib.motor_1.throttle = 0.15 * sentido
            ib.motor_2.throttle = -0.15 * sentido

        time.sleep(0.005)

    # El objetivo se cumplió: cortamos la energía por completo
    ib.motor_1.throttle = 0
    ib.motor_2.throttle = 0

# --- EJECUCIÓN PRINCIPAL ---
ib.pixel = (255, 255, 0) # Amarillo (calibrando)
drift = calibrar_drift(sensor, 2)
ib.pixel = (0, 0, 255)   # Azul (listo para actuar)

print("Iniciando giro exacto de 90 grados...")
girar_grados(sensor, 90, drift)
print("Acción física terminada.")

ib.pixel = (0, 0, 0) # Apagamos el LED al terminar
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

# Función con variables predeterminadas del PID (Proporcional, Integral, Derivativa)
def straight_move(velocidad, duracion, drift, Kp=0.15, Ki=0.8, Kd=0.05):
    t0 = time.monotonic()
    velocidad_base = abs(velocidad)
    direccion = 1 if velocidad > 0 else -1

    # Memorias para los componentes del PID
    error_anterior = 0
    error_integral = 0
    t_anterior = time.monotonic()

    # El lazo cerrado: mantenemos el control durante el tiempo especificado
    while time.monotonic() - t0 < duracion:
        t_actual = time.monotonic()
        
        # En esta implementación fijamos el dt en 1 para estabilizar los cálculos 
        # matemáticos de las ganancias Kp, Ki y Kd en tiempo real.
        dt = 1 
        t_anterior = t_actual

        # 1. Medir error (La realidad): 
        # Si el robot va perfectamente recto, sensor.gyro[2] menos el drift debería ser 0.
        # Cualquier valor distinto es un error físico que el robot está cometiendo.
        error = sensor.gyro[2] - drift

        # 2. Recordar e inferir:
        # Integral: Acumulamos los errores pasados. Ayuda a vencer fricciones constantes.
        error_integral += error * dt
        # Derivativa: Calculamos la velocidad del error. Ayuda a anticipar y suavizar correcciones rápidas.
        error_derivativo = (error - error_anterior) / dt

        # 3. Negociar la corrección (El cálculo):
        # Convertimos los errores matemáticos en una fuerza de corrección aplicable.
        correccion = (Kp * error) + (Ki * error_integral) + (Kd * error_derivativo)
        
        # Evitamos la sobrecorrección. El motor no puede arreglar un problema
        # instantáneamente, restringimos el impacto al 30% de la fuerza.
        correccion = max(-0.3, min(0.3, correccion)) 

        # 4. Actuar sobre la materia:
        # Aplicamos la velocidad base y le sumamos/restamos la compensación a cada motor.
        v1 = max(-1.0, min(1.0, velocidad_base * direccion + correccion))
        v2 = max(-1.0, min(1.0, velocidad_base * direccion - correccion))

        # Enviamos la energía a las ruedas
        ib.motor_1.throttle = v1
        ib.motor_2.throttle = v2

        # Guardamos el error actual para usarlo como pasado en el siguiente ciclo
        error_anterior = error
        
        # Pequeña pausa para no colapsar la lectura del I2C
        time.sleep(0.01)

    # Detenemos la máquina al agotar la duración
    ib.motor_1.throttle = 0
    ib.motor_2.throttle = 0

# --- EJECUCIÓN PRINCIPAL ---
ib.pixel = (255, 0, 255) # Magenta (calibrando)
drift = calibrar_drift(sensor, 2)
ib.pixel = (0, 255, 255) # Cian (listo)

print("Avanzando recto por 3 segundos. El algoritmo corrige la fricción en tiempo real.")
straight_move(0.5, 3, drift)
print("Movimiento terminado.")

ib.pixel = (0, 0, 0)
```

## Reflexiones para el lector

- **La negociación perpetua:**  
  Un lazo de control no busca ser perfecto en el primer intento, sino estar en constante diálogo con su propio error.

- **Límites de la matemática:**  
  Aunque la ecuación del PID pueda producir correcciones extremas, el algoritmo debe considerar las restricciones físicas del sistema.

- **La diferencia entre instrucción y comportamiento:**  
  Mandar un voltaje fijo a un motor es una instrucción; ajustar dinámicamente ese voltaje según el entorno es lo que transforma el código en conducta autónoma.
