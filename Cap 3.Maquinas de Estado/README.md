# Máquinas de Estado

Imagine que acabas de aprobar el examen práctico de licencia de conducir. El siguiente paso es ir a las oficinas centrales para obtener el documento oficial. Al llegar, te encuentras con una primera fila que debo hacer. En la ventanilla 1 entrego los documentos que certifican que aprobé el examen práctico.

Una vez que entrego los papeles en la ventanilla 1, me dan un nuevo documento y me indican que pase a la ventanilla 2, donde me toman la fotografía y registran mi firma. Finalmente, me piden que me siente en la sala de espera; allí me llamarán por mi nombre para pasar a la ventanilla 3 y recoger el documento final.

<img src="https://github.com/Universidad-Cenfotec/El-Blink-de-Turing/blob/main/Cap%203.Maquinas%20de%20Estado/cap3fig1.jpeg?raw=true" width="600">


Cada una de estas ventanillas requiere que yo tenga cierta información y representa un **estado** en el que me encuentro dentro del proceso. Además, cada ventanilla —cada estado— solo puede ocurrir si antes estuve en un estado anterior y tengo la información necesaria. Hay también un **estado inicial**, donde comienza todo el proceso.

Visto de forma general, este procedimiento puede representarse de manera esquemática.

A cada círculo lo llamo **nodo**, y representa un estado (una ventanilla, en este caso). Cada línea indica cómo se pasa de un nodo —o estado— a otro. Así, cuando llego a la oficina con los papeles del examen de manejo, comienzo en el estado 1. La flecha que sale del estado 1 y regresa al mismo estado se denomina *loop*, e indica que me mantengo en ese estado, simplemente esperando mi turno.

Si estando en el estado 1 entrego los documentos, entonces paso al estado 2. El texto sobre las flechas indica la condición necesaria para pasar de un estado a otro. Para pasar del estado 1 al 2, los documentos deben haber sido entregados; para pasar del estado 2 al 3, ya deben haberme tomado la fotografía y la firma.

Todo este proceso, que usualmente se percibe como tedioso, lo estoy representando con nodos y flechas. A esta representación se le llama una **máquina de estados**. En el fondo, lo que estoy haciendo es construir un **modelo computacional de una situación real**. Antes de entrar en una definición demasiado formal, prefiero ver otro ejemplo sencillo.

Una **máquina de estados (ME)** es un sistema que puede encontrarse en cualquiera de un conjunto de estados y que cambia de estado dependiendo de la información que recibe y del estado en el que se encuentra en ese momento. Las máquinas de estados se utilizan para describir y manipular, de manera matemática y computacional, procesos del mundo real.

Un ejemplo clásico es el semáforo.

Un semáforo puede estar en verde, amarillo o rojo. El sistema inicia en verde, se mantiene así por un tiempo, luego pasa a amarillo, donde parpadea —encendiéndose y apagándose— un número determinado de veces, y finalmente pasa a rojo. Después, el ciclo se repite.

Las reglas de su funcionamiento pueden describirse de la siguiente manera:

* Si está en verde (estado 0), se mantiene en verde durante 3 segundos y luego pasa a amarillo encendido (estado 1).
* Si está en amarillo encendido (estado 1), espera 1 segundo y pasa a amarillo apagado (estado 2).
* Si está en amarillo apagado (estado 2), espera 1 segundo y vuelve al estado 1.
* Los estados 1 y 2 se repiten exactamente 5 veces; al finalizar la quinta repetición, el sistema pasa a rojo (estado 3).
* Si está en rojo (estado 3), espera 3 segundos y vuelve al estado 0 (verde).

En este modelo utilizo cuatro estados: uno para cada color, considerando el amarillo encendido y apagado como estados distintos para producir el efecto de parpadeo.

Ahora que entiendo el funcionamiento del semáforo, la forma más sencilla de visualizar una máquina de estados es mediante un esquema de nodos y flechas.


El doble círculo en el estado 0 indica que se trata del **estado inicial**, es decir, el punto donde arranca todo el proceso. Con este esquema ya tengo todo lo necesario para **programar** mi máquina de estados.
