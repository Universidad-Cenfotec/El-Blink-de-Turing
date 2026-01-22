# El Bit

Un bit no es solo un número, es una separación de cosas. Es el acto más pequeño posible de separar el mundo en dos estados diferentes. Antes de que existieran las computadoras, esa distinción ya estaba ahí, cada vez que algo podía ser o no ser, estar o no estar, ocurrir o no ocurrir, ser verdadero o falso. La computación digital simplemente tomó esa idea elemental y la convirtió en la base de todo nuesro mudo tecnológico.

Decimos que un bit puede ser 0 o 1, apagado o encendido, falso o verdadero. Lo importante no es el símbolo, sino la diferencia. Un bit existe cuando un sistema puede reconocer, sin ambigüedad, que se encuentra en uno de dos estados posibles. A partir de esa diferencia mínima se construye todo lo demás, números, texto, imágenes, sonidos y programas completos.

## ¿Por qué las computadoras usan bits?

A los humanos siempre nos ha atraído la idea de delegar el cálculo en máquinas. Podemos aprender a hacer cuentas con cuidado y precisión, pero incluso así siempre queda una duda. Si le pido a alguien que calcule $234 \times 358$ y lo hace muy rápido, no tengo una forma inmediata de saber si está bien. Debo confiar en esa persona. Incluso recuerdo esos programas de televisión donde tiene a alguien que puede calcular rápido, al final es una calculadora que lo verifica, pues podría decir cualquier número que ninguna persona normal podría verificarlo. Una máquina, en cambio, no inspira confianza por intuición, sino por estructura. Si conozco cómo funciona, si sus pasos son claros y repetibles, puedo confiar en el resultado no porque “sepa”, sino porque sigue reglas que no cambian.

Ese deseo de confianza llevó a una pregunta más profunda, qué significa realmente calcular. Se entendió que cualquier cálculo puede describirse como una secuencia finita de pasos, aplicados sobre símbolos bien definidos, siguiendo reglas precisas. No se necesita continuidad para calcular; se necesita estructura.

Aquí aparece una diferencia clave entre conjuntos de números. Los números naturales avanzan a saltos, uno tras otro. Son discretos y manejables. Los números reales, en cambio, son infinitamente densos. Entre dos números reales siempre hay otro más. Esa riqueza infinita es perfecta para la matemática, pero imposible de capturar por completo en una máquina física. Ningún sistema real puede almacenar infinitos decimales ni operar con precisión infinita. Esta limitación no es un defecto de las computadoras, sino una característica del mundo físico.

Por eso la computación se apoya en lo discreto. Los sistemas discretos permiten estados claros, repetibles y verificables. Un sistema que solo debe distinguir entre dos posibilidades puede tolerar ruido, imperfecciones y variaciones del entorno sin perder significado. Esa estabilidad es la base de la computación real.

Incluso los números que solemos pensar como continuos, dentro de una computadora aparecen como una secuencia finita de casillas, cada una con solo dos posibilidades. En la práctica, lo continuo se representa como una aproximación construida paso a paso. Por grandes o pequeños que parezcan esos números, nunca son infinitos ni arbitrariamente precisos. Siempre están hechos de un número limitado de bits.

Cuando esta idea se traslada al mundo físico, la electrónica se vuelve una aliada natural. Un circuito no necesita medir un voltaje exacto. Solo necesita saber si está por encima o por debajo de un umbral. Esa decisión es robusta. No depende de la perfección, sino de la diferencia. En ese gesto simple, un fenómeno eléctrico continuo se convierte en un símbolo. Y ese símbolo es el bit.

Con bits bien definidos se puede construir memoria. Con memoria, se puede construir una arquitectura donde datos e instrucciones conviven y se transforman mutuamente. Esa arquitectura no solo calcula; procesa información de forma estable y repetible. En ese punto, la computación deja de ser solo aritmética y se convierte en un sistema general para manipular símbolos.

El uso del binario no es una moda ni una convención cultural. Es una consecuencia directa de cómo funcionan la lógica, la física y la necesidad de confiabilidad. A una computadora no le interesa medir con exactitud infinita. Le interesa distinguir estados sin ambigüedad. Dos estados bien separados son suficientes para construir sistemas enormes, escalables y verificables. A partir de decisiones simples se pueden encadenar millones de operaciones sin que los errores se acumulen de forma incontrolable.

## El bit en los microcontroladores

En un microcontrolador, el bit tiene una vida doble. Por un lado, es el material con el que se realiza la computación interna. Por otro, es el lenguaje con el que la máquina se comunica con el mundo exterior. Esta doble naturaleza explica por qué un microcontrolador puede, al mismo tiempo, ejecutar lógica compleja y controlar objetos físicos.

Internamente, todo ocurre en forma de bits que se combinan, se comparan y se almacenan. Puertas lógicas, registros y memorias trabajan únicamente con estados discretos. Pero el mundo externo no siempre habla ese idioma. La luz, la temperatura, el sonido o la posición cambian de forma continua. Para interactuar con ese mundo, el microcontrolador necesita traducir.

Ahí aparece el conversor analógico-digital, el ADC. Un sensor entrega un voltaje que varía suavemente. El ADC toma ese valor y lo transforma en un número entero. No captura la continuidad completa, sino una versión discretizada de ella. Ese número es un conjunto de bits que representa una aproximación del fenómeno físico.

El proceso inverso ocurre cuando el microcontrolador quiere actuar sobre el mundo. Aunque solo puede generar estados digitales, puede organizarlos en el tiempo para producir efectos que parecen continuos. Con PWM, el micro enciende y apaga un pin muy rápido. El promedio de esos encendidos y apagados es interpretado por un LED como brillo, o por un motor como velocidad. Lo continuo emerge, otra vez, a partir de decisiones discretas.

En este ir y venir, el bit deja de ser una abstracción matemática y se convierte en un puente. Es el punto donde la lógica interna del sistema toca el mundo físico. No es solo un 0 o un 1. Es una frontera, una decisión y una forma de hacer que lo real sea computable.


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

