# El Bit

Un bit es la unidad más simple de información en un sistema digital. Representa una elección entre dos posibilidades, que lo podemos pensar como 0 ó 1, apagado o encendido, falso o verdadero. Es la manera en que una computadora distingue entre dos estados y, a partir de esa distinción mínima, construye todo lo demás, números, texto, imágenes, sonidos y programas completos.

## ¿Porqué las computadoras usan bits?

A nosotros, los humanos, siempre nos ha fascinado la idea de que máquinas hagan los cálculos por nosotros. Aunque podemos aprender a hacer cuentas con precisión, siempre queda una duda, si le pido a alguien que me calcule $234 \times 358$ y lo hace muy rápido, ¿cómo sé que no se equivocó? Tengo que confiar en esa persona. En cambio, si el cálculo lo realiza una máquina cuyos mecanismos son verificables y repetibles, puedo estar mucho más seguro de que el resultado será correcto una y otra vez, sin errores.

La idea de pensar el cómputo como algo discreto surgió al entender que cualquier cálculo puede describirse mediante símbolos y reglas finitas, sin depender de magnitudes continuas. En la matemática, los números naturales forman un conjunto discreto y manejable, mientras que los números reales son infinítamente densos (simepre puedo encontrar un número en medio de dos reales) y no pueden representarse completamente en una máquina física. Esta diferencia llevó a reconocer que los sistemas discretos, basados en estados claros como 0 y 1, son los únicos que permiten representar, almacenar y procesar información de manera estable, reproducible y computable. Por eso la computación moderna descansa en lo discreto y no en lo continuo.

Cuando entendemos que la computación necesita símbolos discretos, aparece la pregunta de cómo llevarlos al mundo físico. La electrónica resulta ser una opción natural, porque un circuito puede distinguir con facilidad entre un nivel de voltaje alto y uno bajo, sin necesidad de medir cantidades exactas. Basta con que un estado esté por encima o por debajo de un umbral para considerarlo distinto, lo que vuelve al sistema estable y confiable incluso si hay ruido o variaciones en el ambiente. En ese gesto simple, un fenómeno eléctrico pasa a representar un símbolo, y el símbolo se convierte en la base de la computación digital, el bit.

Con un bit bien definido se puede construir una memoria, y con muchas memorias se puede construir una arquitectura completa donde las instrucciones y los datos comparten el mismo espacio. La gracia es que esta arquitectura no solo calcula; también puede imitar funciones elementales de un cerebro, en el sentido de procesar señales discretas con estructuras repetibles y confiables. En ese cruce entre estabilidad física y lógica formal aparece la esencia de la computación digital (ver von Neuman 1958).

## El Bit en los microcontroladores

Cuando pensamos en un bit, solemos imaginarlo como un 0 o un 1. Pero dentro de un microcontrolador, los bits no son solo valores almacenados. Son el material con el cual la máquina piensa y también la forma en que se comunica con el mundo. Un bit es parte de dos procesos distintos, por un lado, la computación interna hecha de circuitos lógicos, y por otro, el envío y la recepción de información digital a través de sus pines. Esta doble vida del bit explica por qué un microcontrolador puede tomar decisiones complejas, pero también mover motores, leer sensores o controlar luces.

Aunque el microcontrolador piense en binario, el mundo a su alrededor no siempre lo es. Para comunicarse con sensores, motores y otros dispositivos, necesita interpretar señales y convertirlas en información útil. Aquí aparecen dos elementos importantes: el ADC y el PWM.

### ADC: cómo el micro convierte lo continuo en bits

Muchos sensores no entregan un 0 o un 1, sino un valor continuo. La luz en un LDR, la posición de un potenciómetro o la temperatura en un termistor producen voltajes que cambian suavemente. El microcontrolador usa un conversor analógico-digital, el ADC, para traducir ese voltaje en un número discreto.

Por ejemplo, si su ADC es de 12 bits, puede representar el voltaje en 4096 niveles distintos. No mide el voltaje con precisión infinita: lo cuantiza, lo convierte en un grupo de bits que se aproximan al valor real.
Así, un potenciómetro en una posición determinada no se lee como “0.74 voltios exactos”, sino como un número cercano, tal vez 1950. Ese número no deja de ser un conjunto de bits, otro patrón que el micro puede procesar.

### PWM: cómo el micro convierte bits en un comportamiento “analógico”

El caso contrario ocurre cuando el microcontrolador quiere producir una señal que parezca continua, como controlar la intensidad de un LED o la velocidad de un motor. Aunque el micro solo puede generar 0 o 1, puede combinar esos estados a gran velocidad para crear lo que vemos como un valor intermedio. Esto se llama modulación por ancho de pulso, o PWM.

En PWM el pin se enciende y apaga muy rápido. Si está encendido la mitad del tiempo, el LED parece brillar a mitad de fuerza. Si está encendido un 80 por ciento del tiempo, el motor se mueve más rápido. El truco está en que el micro solo genera bits, pero los usa de tal forma que nuestro ojo o el motor interpretan un promedio. De nuevo, un comportamiento continuo nace de decisiones discretas.

##  De Bits al mundo cintinuo

Cuando el micro lee el mundo, parte de un voltaje continuo y lo recorta en niveles, convirtiéndolo en patrones de bits. Cuando actúa sobre el mundo, toma patrones de bits y los transforma en pulsos rápidos que parecen continuos. Por eso, en la vida de un microcontrolador, un bit no es solamente un número pequeño. Es el puente entre la lógica interna del sistema y el mundo físico que lo rodea.

---

## 1. Qué vas a construir en el IdeaBoard

Vas a usar tres cosas

* Un potenciómetro, que da un valor “continuo”
* El ADC del ESP32 en la IdeaBoard, que convierte ese valor en un número
* El NeoPixel integrado de la IdeaBoard, que cambia de color según un bit interno

La idea central es que el microcontrolador toma algo continuo, lo pasa a un número discreto, lo convierte en una decisión binaria, y esa decisión se ve como un color en el LED RGB.

## 2. Teoría detrás del proyecto

### 2.1 El potenciómetro y el mundo continuo

Cuando girás un potenciómetro, la resistencia cambia de forma suave.
Eso produce un voltaje que también cambia de forma continua entre 0 V y 3.3 V.

En el mundo físico no hay “saltos” perfectos, todo se mueve con pequeñas variaciones.
Ese es el mundo continuo.

### 2.2 El ADC y el paso al mundo discreto

El ESP32 no trabaja con voltajes “infinitamente precisos”.
En la IdeaBoard, la función `AnalogIn` de la librería convierte el voltaje del pin en un número entero entre 0 y 65535, es decir un valor de 16 bits ([GitHub][1])

Ese número es una versión cuantizada del voltaje real.
Sigue cambiando, pero ahora solo puede tomar uno de 65536 valores posibles.
Ya no es continuo, es discreto.

### 2.3 El umbral y el nacimiento del bit

Luego hacemos algo todavía más radical.
Definimos un umbral, por ejemplo 30000.

Si el valor del ADC es mayor que ese umbral, el micro decide que el “estado” es uno.
Si es menor o igual, decide que el estado es cero.

En ese momento aparece el bit

* Antes teníamos un rango entero de posibles valores
* Ahora tenemos solo dos posibilidades: abajo de la frontera o arriba de la frontera

El bit es esa decisión mínima.

### 2.4 El NeoPixel como “pantalla del bit”

La IdeaBoard trae un NeoPixel integrado que se controla con la propiedad `ib.pixel` de la librería ([GitHub][1])

* Si el bit interno vale 0, mostramos un color, por ejemplo azul
* Si el bit interno vale 1, mostramos otro color, por ejemplo rojo

Entonces

* El potenciómetro vive en el mundo continuo
* El ADC lo traduce a un número discreto
* El umbral lo reduce a un bit
* El NeoPixel nos enseña ese bit como color

## 3. Montaje físico

### Materiales

* IdeaBoard con CircuitPython y librería `ideaboard` instalada
* 1 potenciómetro (10 kΩ funciona bien)
* 3 cables jumper

### Conexiones

* Patita 1 del potenciómetro a 3V3 de la IdeaBoard
* Patita 3 del potenciómetro a GND
* Patita central del potenciómetro a un pin analógico, por ejemplo `IO33`

En el código usaremos `board.IO33` como entrada analógica, igual que en el ejemplo de la wiki ([GitHub][1])

El NeoPixel ya está cableado en la placa, no tenés que conectar nada para el LED.

## 4. Código completo

El código bit.py va en `code.py` en la IdeaBoard.

## 5. Explicación línea a línea

```python
import time
import board
from ideaboard import IdeaBoard
```

* `import time`
  Importa el módulo de tiempo, lo usamos para poner pausas entre lecturas.
* `import board`
  Importa los nombres de pines de la placa, por ejemplo `board.IO33`.
* `from ideaboard import IdeaBoard`
  Importa la clase `IdeaBoard` de la librería oficial, que simplifica el uso del NeoPixel, entradas analógicas, motores y otros elementos ([GitHub][1])

```python
ib = IdeaBoard()
```

* Crea una instancia llamada `ib`.
  Este objeto representa a la IdeaBoard y nos da acceso a métodos y propiedades especiales, como `ib.pixel`, `ib.brightness` y `ib.AnalogIn`.

```python
pot = ib.AnalogIn(board.IO33)
```

* `ib.AnalogIn(...)` crea una entrada analógica usando el pin que le indiquemos.
* `board.IO33` es el pin donde conectamos la patita central del potenciómetro.
* El objeto `pot` tiene una propiedad `value` que da un número entero de 0 a 65535, que representa el voltaje leído en ese pin.

Aquí ya tenés el paso de continuo a discreto

* El voltaje del potenciómetro es continuo
* `pot.value` lo convierte en un número entero gestionable por el microcontrolador

```python
ib.brightness = 0.2
```

* Ajusta el brillo global del NeoPixel.
* El valor va de 0.0 a 1.0, donde 0 apaga el LED y 1 es el brillo máximo.
* Usamos 0.2 para que se vea bien sin ser molesto.

```python
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
```

* Definimos dos colores como tuplas RGB.
* `AZUL` significa sin rojo, sin verde y azul al máximo.
* `ROJO` significa rojo al máximo, sin verde ni azul.
* Estas constantes hacen el código más legible que usar números sueltos.

```python
UMBRAL = 30000
```

* Aquí definimos el umbral que separa las dos regiones.
* El ADC puede devolver valores entre 0 y 65535.
* Con 30000 elegimos un punto aproximadamente a la mitad del rango.
* Todo lo que esté por encima se interpretará como “región alta”.
* Todo lo que esté por debajo o igual como “región baja”.

En este punto, el umbral es el que crea el bit.
Sin este número, el valor seguiría siendo un dato analógico.

```python
while True:
```

* Iniciamos un bucle infinito.
* El microcontrolador va a leer el potenciómetro y actualizar el NeoPixel una y otra vez.

```python
    valor = pot.value          # entero entre 0 y 65535
```

* Leemos el valor actual del ADC en `pot.value`.
* `valor` es un número entero que ya representa el voltaje de forma cuantizada.
* Este número sigue recordando el origen analógico, pero ahora vive en el mundo discreto de los enteros.

```python
    print("ADC =", valor)
```

* Mostramos el valor leído en el puerto serial.
* Esto sirve para que el estudiante vea cómo cambia al mover el potenciómetro y entienda que no hay saltos mágicos, sino una progresión de números.

```python
    if valor > UMBRAL:
        bit = 1
        ib.pixel = ROJO        # cuando el bit es 1 el NeoPixel se pone rojo
    else:
        bit = 0
        ib.pixel = AZUL        # cuando el bit es 0 el NeoPixel se pone azul
```

Este bloque es el corazón conceptual del programa.

* La condición `if valor > UMBRAL` compara el valor analógico cuantizado con el umbral.
* Si el valor está por encima, decidimos que el bit vale 1.

  * Guardamos `bit = 1` para tener ese estado como información interna.
  * Cambiamos el NeoPixel a rojo con `ib.pixel = ROJO`.
* Si el valor no supera el umbral, caemos en el `else`.

  * Guardamos `bit = 0`.
  * Cambiamos el NeoPixel a azul con `ib.pixel = AZUL`.

Aquí pasa algo muy importante

* Un rango continuo de valores se agrupa en solo dos categorías.
* El mundo del potenciómetro se reduce a una decisión binaria en el microcontrolador.
* Esa decisión se convierte en un símbolo visible: rojo o azul.

El bit ya no es una idea abstracta, es algo que ves cambiar cuando girás el potenciómetro.

```python
    print("bit =", bit)
```

* Imprimimos el bit interno para ver en consola cuándo cambia de 0 a 1.
* Esto ayuda al estudiante a relacionar el valor numérico del ADC con el cambio de estado lógico.

```python
    time.sleep(0.05)
```

* Hacemos una pausa de 0.05 segundos.
* Evitamos saturar la salida serial y damos tiempo a que el ojo perciba el cambio de color.
* Sin esta pausa todo pasaría demasiado rápido y el monitor serial sería difícil de leer.

## 6. Preguntas y variaciones para trabajar en clase

Algunas preguntas que podés hacer a estudiantes

* ¿Qué pasaría si el ADC solo tuviera 8 bits en lugar de 16?
* ¿Qué ocurre si movés el potenciómetro muy cerca del umbral, ves parpadeos?
* ¿Cómo cambia el comportamiento si movemos el umbral a 10000 o a 50000?
* ¿Podés elegir otros colores para el bit 0 y el bit 1?
* ¿Cómo escribirías un código que muestre tres regiones con tres colores, en lugar de solo dos?

Variaciones sencillas

* Que el brillo del NeoPixel cambie según la distancia al umbral.
* Que el color sea rojo cuando `bit = 1` y verde cuando `bit = 0`, pero que el azul indique una “zona de incertidumbre” cerca del umbral.
* Que el valor del ADC también se envíe por serie a otra placa para mostrar cómo ese bit se puede comunicar.

