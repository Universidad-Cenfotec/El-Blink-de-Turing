# Preliminares: Todo sobre el IdeaBoard

## 1. ¿Qué es la IdeaBoard?

La **IdeaBoard** es una placa educativa basada en **ESP32**, diseñada para reducir la fricción entre **pensar una idea** y **hacerla ejecutable**. Integra en una sola tarjeta:

* Microcontrolador ESP32
* Driver de motores dual (L9110S)
* LED RGB direccionable (WS2812B)
* Acceso directo a:

  * Entradas analógicas
  * Salidas PWM
  * I2C, SPI
  * DAC
  * Sensores táctiles

---

## 2. Arquitectura general de hardware

### Componentes integrados clave

| Componente   | Descripción                           |
| ------------ | ------------------------------------- |
| ESP32        | Doble núcleo, WiFi/BLE, ADC, DAC, PWM |
| L9110S       | Driver de dos motores DC              |
| WS2812B      | LED RGB direccionable                 |
| Regulador    | Entrada 4.5–9V para motores           |
| Headers GPIO | Acceso directo a pines críticos       |

---

## 3. Alimentación eléctrica

### Entradas de poder

* **Motores**: 4.5–9 VDC (terminal dedicado)
* **Lógica**: regulada internamente a 3.3 V
* **GND común** para todo el sistema

⚠️ **Importante**:
Los motores **no deben alimentarse desde 3.3V** del ESP32.

---

## 4. Pinout explicado por subsistemas

### 4.1 Motores DC (Driver L9110S integrado)

| Motor   | Pin A | Pin B |
| ------- | ----- | ----- |
| Motor 1 | IO12  | IO14  |
| Motor 2 | IO13  | IO15  |

La librería ya crea objetos `DCMotor` listos para usar.

```python
from ideaboard import IdeaBoard
ib = IdeaBoard()

ib.motor_1.throttle = 0.5    # adelante
ib.motor_1.throttle = -0.5   # atrás
ib.motor_1.throttle = 0      # detener
```

Esto es un **ejemplo claro de abstracción**: no programas pines, programas **intención**.

---

### 4.2 LED RGB WS2812B integrado

* **Pin físico**: IO2
* **Cantidad**: 1 LED
* **Control**: NeoPixel

```python
ib.pixel = (255, 0, 0)   # rojo
ib.pixel = (0, 255, 0)   # verde
ib.pixel = (0, 0, 255)   # azul
```

Modo arcoíris:

```python
ib.arcoiris = 120
```

Ideal para:

* Estados del sistema
* Debug visual
* Feedback inmediato

---

### 4.3 Entradas analógicas (ADC)

| Pin  | Nota               |
| ---- | ------------------ |
| IO27 | ADC                |
| IO33 | ADC                |
| IO32 | ADC                |
| IO35 | ADC (solo entrada) |
| IO34 | ADC (solo entrada) |
| IO36 | ADC (solo entrada) |
| IO39 | ADC (solo entrada) |

Uso:

```python
sensor = ib.AnalogIn(board.IO33)
print(sensor.value)  # 0 – 65535
```

---

### 4.4 Salidas analógicas (DAC)

Solo dos pines soportan DAC real:

| Pin  | DAC |
| ---- | --- |
| IO25 | Sí  |
| IO26 | Sí  |

```python
dac = ib.AnalogOut(board.IO26)
dac.value = 32768  # ~1.65V
```

Útil para:

* Audio simple
* Control analógico
* Señales continuas

---

### 4.5 Entradas y salidas digitales

```python
boton = ib.DigitalIn(board.IO27, pull=ib.UP)
led = ib.DigitalOut(board.IO4)

if not boton.value:
    led.value = True
```

Esto permite **modelar el mundo como eventos discretos**, ideal para máquinas de estado.

---

### 4.6 Servos (PWM)

Cualquier pin PWM puede usarse:

```python
servo = ib.Servo(board.IO4)
servo.angle = 90
```

Perfecto para:

* Brazos
* Direcciones
* Interacción física

---

### 4.7 I2C y SPI

#### I2C

* SDA: IO21
* SCL: IO22

```python
import busio
i2c = busio.I2C(board.IO22, board.IO21)
```

#### SPI

* CS: IO5
* CLK: IO18
* MISO: IO19
* MOSI: IO23

Esto habilita sensores complejos, pantallas, memorias, etc.

---

### 4.8 Touch sensors (capacitivo)

| Pin  | Touch |
| ---- | ----- |
| IO4  | Sí    |
| IO27  | Sí    |
| IO32 | Sí    |
| IO33 | Sí    |

Permite interacción **sin botones físicos**, algo pedagógicamente potente.

---

## 5. La librería `ideaboard`: filosofía y diseño

La librería oficial encapsula:

* Motores
* LED
* PWM
* ADC / DAC
* Digital IO

Todo en una sola clase:

```python
from ideaboard import IdeaBoard
ib = IdeaBoard()
```

Conceptualmente:

* No programas pines
* Programas **capacidades**
* El hardware desaparece como problema


La implementación oficial puede consultarse directamente en el archivo de la librería .

---

## 6. IdeaBoard como plataforma pedagógica

La IdeaBoard es ideal para enseñar:

* Máquinas de estado físicas
* Sensar es computar
* Sistemas reactivos
* Robótica mínima
* Cibernética básica
* Control en tiempo real

Ejemplos típicos:

* Robot seguidor de línea
* Semáforo físico
* Instrumento musical generativo
* Sistema de feedback sensorial
* Autómata encarnado




