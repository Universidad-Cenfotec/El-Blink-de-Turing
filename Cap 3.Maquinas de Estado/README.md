# Máquinas de Estado

## Una introducción informal

Imagina que acabas de aprobar el examen práctico de licencia de conducir. El siguiente paso es ir a las oficinas centrales para obtener el documento oficial. Al llegar, te encuentras con una primera fila que debo hacer. En la ventanilla 1 entrego los documentos que certifican que aprobé el examen práctico.

Una vez que entrego los papeles en la ventanilla 1, te dan un nuevo documento y te indican que pase a la ventanilla 2, donde  toman la fotografía y registran la firma. Finalmente, piden que te sientes en la sala de espera; allí llamarán por el nombre para pasar a la ventanilla 3 y recoger el documento final.

<img src="https://github.com/Universidad-Cenfotec/El-Blink-de-Turing/blob/main/Cap%203.Maquinas%20de%20Estado/cap3fig1.jpeg?raw=true" width="400">


Cada una de estas ventanillas requiere que uno tenga cierta información y representa un fase, o me dicho **estado** en el que te encuentras dentro del proceso. Además, cada ventanilla (cada estado) solo puede ocurrir si antes estuviste en un estado anterior y se tiene la información necesaria para pasar a otraventanilla (estado). Hay también un **estado inicial**, donde comienza todo el proceso.

Visto de forma general, este procedimiento puede representarse de manera esquemática,

<img src="https://github.com/Universidad-Cenfotec/El-Blink-de-Turing/blob/main/Cap%203.Maquinas%20de%20Estado/cap3fig2.png?raw=true" width="400">

A cada círculo lo llamo **nodo**, y representa un estado (una ventanilla, en este caso). Cada línea indica cómo se pasa de un nodo —o estado— a otro. Así, cuando llego a la oficina con los papeles del examen de manejo, comienzo en el estado 1. La flecha que sale del estado 1 y regresa al mismo estado se denomina *loop*, e indica que me mantengo en ese estado, simplemente esperando mi turno.

Si estando en el estado 1 entrego los documentos, entonces paso al estado 2. El texto sobre las flechas indica la condición necesaria para pasar de un estado a otro. Para pasar del estado 1 al 2, los documentos deben haber sido entregados; para pasar del estado 2 al 3, ya deben haberme tomado la fotografía y la firma.

Todo este proceso, que usualmente se percibe como tedioso, lo estoy representando con nodos y flechas. A esta representación se le llama una **máquina de estados**. En el fondo, lo que estoy haciendo es construir un **modelo computacional de una situación real**. Antes de entrar en una definición demasiado formal, prefiero ver otro ejemplo sencillo.

Una **máquina de estados (ME)** es un sistema que puede encontrarse en cualquiera de un conjunto de estados y que cambia de estado dependiendo de la información que recibe y del estado en el que se encuentra en ese momento. Las máquinas de estados se utilizan para describir y manipular, de manera matemática y computacional, procesos del mundo real.

Un ejemplo clásico, el semáforo.

Un semáforo puede estar en verde, amarillo o rojo. El sistema inicia en rojo, se mantiene así por un tiempo, luego pasa a verde, se mantiene, y luego pasa a amarillo donde parpadea —encendiéndose y apagándose— un número determinado de veces, y finalmente pasa a rojo nuevamente. Después, el ciclo se repite.

Vámoslo en el siguiente diagrama,
<img src="https://github.com/Universidad-Cenfotec/El-Blink-de-Turing/blob/main/Cap%203.Maquinas%20de%20Estado/cap3fig3.png?raw=true" width="400">

Las reglas de su funcionamiento pueden describirse de la siguiente manera:

* Si está en rojo (estado S1), espera 20 segundos y luego va al estado S2 (verde).
* Si está en verde (estado S2), se mantiene en verde durante 15 segundos y luego pasa a amarillo encendido (estado S3).
* Si está en amarillo encendido (estado S3), espera 15 segundos quedanto intermitente, debido a una función intenra que hace que parpadee, y pasa a rojo (S1) luego de 5 segundos

En este modelo utilizo 3 estados uno para cada color, y podríamos iniciar o terminar el ciclo en cualquiera de los estados.

Noten cómo, tanto en el ejemplo de las ventanillas como en el del semáforo, lo que estoy intentando hacer es **describir situaciones y eventos del mundo real de manera formal y repetible**. No se trata solo de contar una historia, sino de capturarla de tal forma que pueda convertirse en un procedimiento automático, en algo que una máquina pueda ejecutar sin ambigüedad.

Cuando describo las ventanillas como estados, o los colores del semáforo como transiciones gobernadas por el tiempo, estoy imponiendo una estructura precisa sobre fenómenos cotidianos. Esa estructura permite que el proceso se repita siempre de la misma manera y, más importante aún, que pueda ser implementado como un programa de computadora. En ese momento, la situación deja de ser solo una experiencia humana y se transforma en un **objeto computacional**.

Esta idea es mucho más profunda de lo que parece a primera vista. Está en el corazón de la computación, pero también en el corazón de las matemáticas mismas. Formalizar un proceso no es solo una cuestión técnica; es una forma de afirmar que entendemos ese proceso lo suficiente como para **reconstruirlo**, paso a paso, sin depender de intuiciones externas.

Desde esta perspectiva, no es descabellado pensar que un objeto matemático existe en la medida en que puede ser construido. Para muchos de nosotros, una matemática que no puede, al menos en principio, ser llevada a una computadora, resulta sospechosa. No porque la computadora sea el juez último de la verdad, sino porque la computación nos obliga a ser explícitos, constructivos y rigurosos.

Así, las máquinas de estados funcionan como un puente natural que conectan situaciones del mundo real con procesos computables, y esos procesos, a su vez, con una visión de las matemáticas donde **existir es poder construirse**.

---
## Autómatas en un microcontrolador

## Autómatas en microcontroladores

Cuando trabajo con microcontroladores, las máquinas de estados dejan de ser una herramienta conceptual elegante y se convierten en **una necesidad práctica**. Un microcontrolador no ejecuta programas como lo hace una computadora de escritorio; no hay un inicio, un cálculo largo y un final. Un microcontrolador está, esencialmente, **siempre avanzando**.

Su lógica fundamental es un ciclo infinito, que consiste en leer entradas, actualizar estados internos, actuar sobre el mundo físico y volver a empezar. Ese “moverse constantemente hacia adelante” hace que el modelo de programación secuencial tradicional resulte incómodo y, en muchos casos, peligroso. Bloquear el programa esperando algo —un tiempo, un sensor, una respuesta— suele ser una mala idea.

Aquí es donde las máquinas de estados encajan de forma natural.

Un autómata modela exactamente este tipo de comportamiento. El sistema **siempre está en algún estado**, y en cada iteración del ciclo principal evalúa qué debe hacer según ese estado y según lo que está ocurriendo en el entorno, de esa manera en realidad no espera sino que **reacciona**.

En un microcontrolador, un estado como en el ejemplo del semáforo, no es solo algo abstracto, sino que puede ser algo concreto como:

* un motor encendido o apagado
* un LED parpadeando o fijo
* un robot avanzando, girando o detenido
* un sensor siendo leído o ignorado

Cada estado define qué acciones se ejecutan y qué eventos pueden provocar una transición. El programa completo se convierte entonces en una descripción clara del comportamiento del sistema a lo largo del tiempo.

Además, las máquinas de estados permiten manejar el tiempo sin bloquear la ejecución. En lugar de “esperar 3 segundos”, el sistema entra en un estado que recuerda cuándo comenzó y verifica, en cada iteración, si ya transcurrió el tiempo necesario. El microcontrolador sigue vivo, atento a otros eventos, mientras el tiempo pasa.

Esta forma de programar es especialmente poderosa porque coincide con la naturaleza física del hardware. El mundo no se detiene mientras un microcontrolador piensa. Los sensores cambian, los botones se presionan, los motores siguen girando. Las máquinas de estados permiten que el software habite ese mismo ritmo continuo.

Por eso, cuando programo microcontroladores, no pienso primero en funciones o en algoritmos, sino en **estados y transiciones**. Pienso en qué modos puede tener el sistema, cómo pasa de uno a otro y bajo qué condiciones. El código se vuelve entonces una traducción directa de esa estructura.

En este contexto, programar es diseñar un autómata que vive en el mundo físico. Un autómata que avanza paso a paso, ciclo tras ciclo, exactamente igual que el microcontrolador que lo ejecuta.

---

## Máquinas de estado, números y construcción

Quiero ahora detenerme en una idea que, aunque parece abstracta, es fundamental para entender la relación entre computación y matemáticas. La idea de que **un número no es solo algo que existe**, sino algo que **se puede construir**.

<img src="https://github.com/Universidad-Cenfotec/El-Blink-de-Turing/blob/main/Cap%203.Maquinas%20de%20Estado/cap3fig4.png?raw=true" width="400">

El autómata de la figura es un buen punto de partida. Este autómata reconoce —o, si se quiere, computa— los múltiplos de 3 escritos en binario. Tiene tres estados: $q_0$, $q_1$ y $q_2$. Intuitivamente, cada estado representa el **residuo módulo 3** del número que se ha leído hasta ese momento.

Este autómata puede entenderse como una **máquina para construir números binarios paso a paso**. El estado $q_0$ es el punto de partida y también el estado de aceptación: solo cuando el recorrido termina en $q_0$ considero que el número construido está completo y es un múltiplo de 3.

Desde $q_0$ puedo generar un 0 y permanecer en el mismo estado, lo que corresponde a construir el número binario `0`, que es divisible entre 3. Alternativamente, desde $q_0$ puedo generar un 1 y pasar al estado $q_1$, indicando que he comenzado a construir un número cuyo residuo módulo 3 es 1.

Una vez en $q_1$, puedo generar otro 1 y regresar a $q_0$, construyendo así el número binario `11`, que corresponde a 3 en decimal. Al volver a $q_0$, el autómata llega a un estado de aceptación, y el número queda completo: se trata de un múltiplo de 3. También desde $q_1$ puedo generar un 0 y pasar al estado $q_2$, extendiendo el número construido con un nuevo bit y cambiando su residuo.

Desde $q_2$, el proceso continúa de manera análoga: cada transición agrega un nuevo bit al número binario, y el estado actual refleja en todo momento el residuo módulo 3 del número parcial que se ha construido hasta ese instante. El autómata puede seguir generando bits indefinidamente, pero **solo cuando el recorrido vuelve a $q_0$ el número se considera terminado**.

Visto así, el autómata no se limita a reconocer números que ya existen, sino que **los construye activamente**. Cada número múltiplo de 3 existe, para esta máquina, únicamente como el resultado de un recorrido que comienza en $q_0$, avanza bit a bit siguiendo las reglas del autómata, y finalmente regresa a $q_0$. En este sentido, el número no es un objeto estático, sino un proceso que se realiza en el tiempo.


Lo interesante no es solo que el autómata “verifique” si un número es múltiplo de 3, sino **cómo lo hace**. El número no se evalúa al final como un objeto completo; se va **construyendo bit a bit**, y cada bit provoca una transición de estado. En cada paso, el autómata mantiene toda la información relevante del número leído hasta ahora únicamente en su estado actual.

Dicho de otra forma: el número existe, para el autómata, **solo en la medida en que puede ser construido y representado como un proceso**.

## El número como proceso, no como objeto

Esta forma de pensar está muy alineada con el **intuicionismo matemático**. Desde esta perspectiva, un objeto matemático no existe simplemente porque podamos definirlo de manera abstracta, sino porque podemos **construirlo efectivamente**. No basta con afirmar que “existe un número con cierta propiedad”; es necesario mostrar cómo se llega a él.

En este sentido, el autómata no está trabajando con un número “ya dado”. El número emerge del recorrido por los estados. Cada transición es un paso constructivo, y el estado final no es una evaluación externa, sino el resultado natural del proceso de construcción.

Si el autómata termina en $q_0$, el múltiplo de 3 **existe computacionalmente**, porque ha sido construido paso a paso y su divisibilidad está encarnada en el estado final alcanzado. No hay una verificación posterior; el proceso mismo es la prueba.

## Computación como matemática encarnada

Desde esta mirada, la computación no es solo una herramienta para calcular resultados matemáticos. Es una forma de **hacer matemática**. Una matemática donde los objetos no flotan en un espacio platónico, sino que existen en tanto pueden ser ejecutados, recorridos, transitados.

Una máquina de estados, entonces, no solo reconoce lenguajes o procesa entradas. **Construye significado**. Construye números. Construye propiedades matemáticas como procesos finitos y observables.

Este autómata no “sabe” qué es el número 12 en abstracto. Pero sabe construir el 12 como una secuencia de bits y, al hacerlo, sabe que termina en un estado que representa divisibilidad por 3. Para la máquina, eso es todo lo que significa que 12 sea múltiplo de 3.

## Cuando existir es poder ejecutarse

Desde esta perspectiva, decir que “un número existe” en computación es decir que **existe una máquina que lo construye**, o al menos un proceso finito que lo representa. La matemática se vuelve operacional, y la noción de existencia se vuelve inseparable de la noción de ejecución.

Este es uno de los puntos donde las máquinas de estado dejan de ser un simple recurso técnico y se convierten en una **puerta conceptual**: nos obligan a pensar los objetos matemáticos no como cosas estáticas, sino como **fenómenos dinámicos**, que existen en el tiempo, en el recorrido, en la transición.




