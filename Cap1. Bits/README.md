# El Bit

Un bit es la unidad más simple de información en un sistema digital. Representa una elección entre dos posibilidades, que lo podemos pensar como 0 ó 1, apagado o encendido, falso o verdadero. Es la manera en que una computadora distingue entre dos estados y, a partir de esa distinción mínima, construye todo lo demás, números, texto, imágenes, sonidos y programas completos.

## ¿Porqué las computadoras usan bits?

A nosotros, los humanos, siempre nos ha fascinado la idea de que máquinas hagan los cálculos por nosotros. Aunque podemos aprender a hacer cuentas con precisión, siempre queda una duda, si le pido a alguien que me calcule $234 \times 358$ y lo hace muy rápido, ¿cómo sé que no se equivocó? Tengo que confiar en esa persona. En cambio, si el cálculo lo realiza una máquina cuyos mecanismos son verificables y repetibles, puedo estar mucho más seguro de que el resultado será correcto una y otra vez, sin errores.

La idea de pensar el cómputo como algo discreto surgió al entender que cualquier cálculo puede describirse mediante símbolos y reglas finitas, sin depender de magnitudes continuas. En la matemática, los números naturales forman un conjunto discreto y manejable, mientras que los números reales son infinítamente densos (simepre puedo encontrar un número en medio de dos reales) y no pueden representarse completamente en una máquina física. Esta diferencia llevó a reconocer que los sistemas discretos, basados en estados claros como 0 y 1, son los únicos que permiten representar, almacenar y procesar información de manera estable, reproducible y computable. Por eso la computación moderna descansa en lo discreto y no en lo continuo.

Cuando entendemos que la computación necesita símbolos discretos, aparece la pregunta de cómo llevarlos al mundo físico. La electrónica resulta ser una opción natural, porque un circuito puede distinguir con facilidad entre un nivel de voltaje alto y uno bajo, sin necesidad de medir cantidades exactas. Basta con que un estado esté por encima o por debajo de un umbral para considerarlo distinto, lo que vuelve al sistema estable y confiable incluso si hay ruido o variaciones en el ambiente. En ese gesto simple, un fenómeno eléctrico pasa a representar un símbolo, y el símbolo se convierte en la base de la computación digital, el bit.

## EL Bit en los microcontroladores

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

