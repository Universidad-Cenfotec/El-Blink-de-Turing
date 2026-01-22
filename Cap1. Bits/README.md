# EL Bit y lo Discreto 

Hoy en día, cuando hablamos de computadoras, casi siempre se nos habla del **bit**. Las computadoras digitales fundamentan todas sus operaciones internas en esta unidad mínima de información y en operaciones lógicas realizadas sobre conjuntos de bits. En esencia, eso es todo lo que hacen. No hay nada “más profundo” ocurriendo dentro de la máquina, solo bits, lógica y tiempo.

El bit apareció como una solución práctica para construir una computadora que, en lugar de ser mecánica (basada en engranajes), pudiera ser **eléctrica**. De ahí el nombre *computadora digital*: trabaja con dígitos, con estados discretos. Hacia mediados de los años cuarenta, alrededor de 1945, cuando se buscaba convertir el flujo continuo de electricidad en información confiable, se tomó una decisión crucial: dividir el voltaje en dos regiones. Un voltaje alto representaría el “1” y un voltaje bajo representaría el “0”. Con esta decisión, la electricidad dejó de ser solo energía y pasó a ser portadora de significado lógico: verdadero o falso.

Ya desde antes se sabía que toda la matemática podía expresarse en términos lógicos. Si en una máquina eléctrica era posible representar el 1 y el 0, y además construir dispositivos que combinaran esos estados de manera sistemática, entonces esa máquina podría hacer matemáticas. Aquí aparecen los **transistores**: dispositivos electrónicos que funcionan como interruptores controlados. Un transistor puede permitir o bloquear el paso de corriente dependiendo de su entrada, lo que lo convierte en un realizador físico de decisiones lógicas. Combinando muchos transistores se pueden implementar operaciones como AND, OR o NOT, y a partir de ellas, toda la aritmética.

## Antes del bit

Sin embargo, las primeras computadoras no trabajaban con 0 y 1. Trabajaban con **engranajes**. Los engranajes son, en el fondo, dispositivos matemáticos: permiten sumar, restar, multiplicar y dividir. Cuando un engranaje gira cierto número de dientes y hace girar a otro, está realizando una transformación cuantitativa muy precisa.

Un ejemplo cotidiano de esto es una bicicleta. El sistema de platos y piñones multiplica o reduce el esfuerzo según la relación de engranajes. Cambiar de marcha es, literalmente, cambiar un factor de multiplicación. Ahí no hay números escritos, pero sí hay aritmética materializada.

Estas operaciones fundamentales no solo permiten hacer aritmética, sino también álgebra y, en última instancia, lógica. Ada Lovelace lo entendió con una claridad extraordinaria para su época. Al trabajar con la máquina de Babbage, se dio cuenta de que una máquina que manipula símbolos según reglas podía ir mucho más allá de calcular números. Podía manipular ideas formales.

Por ejemplo, una operación lógica AND puede construirse a partir de multiplicación en un sistema binario: si representamos verdadero como 1 y falso como 0, entonces
$1 \times 1 = 1$ (verdadero AND verdadero es verdadero)
$1 \times 0 = 0$
$0 \times 1 = 0$
$0 \times 0 = 0$
Aquí, una operación aritmética simple está implementando una operación lógica.

Las computadoras mecánicas, desde la máquina de Anticitera, pasando por los dispositivos de Pascal, Newton y Leibniz, hasta los diseños de Babbage, funcionaban todas bajo el mismo principio: **cómputo en pasos discretos**. Una manivela que gira una vuelta completa ejecuta un paso de cómputo. Cada ciclo produce un resultado parcial, y la secuencia de ciclos produce el cálculo completo. El tiempo está explícitamente ligado al cómputo.

Fue en este contexto que George Boole dio un salto conceptual decisivo. Boole fue el primero en ver con claridad que la lógica podía tratarse como una forma de álgebra. Lo que hoy llamamos **álgebra booleana** nació de su intento por matematizar el pensamiento. La lógica, entendida como una formalización del razonamiento, podía operar con reglas tan estrictas como las de la aritmética.

Boole se dio cuenta además de algo fundamental: sus “variables” no representaban números, sino **clases**. Una variable podía representar el conjunto de cosas que cumplen cierta propiedad. Al operar con esas variables, las operaciones algebraicas dejaban de ser numéricas y pasaban a representar operaciones lógicas. Esto tenía consecuencias profundas: evitaba las ambigüedades del lenguaje natural, permitía operar con reglas mecánicas y separaba el contenido semántico (de qué se habla) de la forma del razonamiento (cómo se razona).

Un ejemplo claro aparece si pensamos en aritmética modular. En un sistema módulo 2, solo existen dos valores posibles: 0 y 1. La suma y multiplicación en este sistema no describen cantidades, sino relaciones lógicas. La suma módulo 2 se comporta como un XOR lógico, y la multiplicación como un AND. Así, un sistema algebraico extremadamente simple puede capturar toda la lógica proposicional.

Cuando Boole desarrolló estas ideas, las computadoras no existían. Sin embargo, su trabajo estableció un puente crucial entre aritmética, álgebra y lógica. Ese puente hacía plausible la idea de construir una máquina que **mecanizara el razonamiento**, no solo el cálculo numérico. La lógica dejaba de ser una actividad exclusivamente mental y pasaba a ser algo implementable físicamente.

Las computadoras mecánicas calculaban **magnitudes**, no decisiones lógicas explícitas. Dependían de cinemática, precisión geométrica y tolerancias mecánicas muy estrictas. El paso del engranaje a la electricidad ocurrió porque la mecánica tenía límites físicos insalvables. Los sistemas mecánicos transmiten información como movimiento, acumulan error por fricción y desgaste, requieren alineación perfecta y tienen inercia. Cada operación cuesta energía y tiempo.

A partir de cierto tamaño y velocidad, estos sistemas se vuelven inestables. La electricidad, en cambio, permite transmitir estado sin mover materia macroscópica. Un **relé** (un interruptor electromecánico controlado eléctricamente) o un **tubo de vacío** (un dispositivo electrónico previo al transistor que controla el flujo de electrones en el vacío) puede cambiar de estado mucho más rápido que cualquier mecanismo. Mientras la mecánica apuesta por precisión geométrica, la electricidad apuesta por repetibilidad de estado.

El paso final fue establecer la relación entre **circuitos eléctricos y lógica**. Aquí entra Claude Shannon, quien demostró que los circuitos eléctricos podían analizarse y diseñarse utilizando álgebra booleana. Con esto, la computadora pasó a entenderse como una **máquina de estados discretos**. Manipulando voltajes, podía almacenar, transformar y transmitir estados.

La electricidad sí se utilizó de forma continua en otros contextos: amplificadores, radios, control industrial y computadoras analógicas para resolver ecuaciones diferenciales. Pero ese enfoque no escalaba para cómputo general. El problema central era el ruido. En un sistema continuo, cada valor importa y cada perturbación altera el resultado. El error se propaga y se amplifica. El ruido eléctrico no es accidental: es térmico, electromagnético e inevitable.

Para cálculos largos y encadenados, esto es fatal. En cambio, al dividir el voltaje en franjas que representan 0 y 1, se pueden establecer umbrales claros. Mientras el voltaje esté “suficientemente alto” o “suficientemente bajo”, el sistema funciona correctamente. Esto convierte un medio continuo en un sistema lógico robusto, capaz de regenerar señales y corregir errores.

No se aprovechó la continuidad eléctrica para cómputo general porque:

* el ruido la vuelve inestable,
* no permite regeneración confiable,
* no escala en complejidad,
* ata el significado al soporte físico.

Los estados discretos no fueron una renuncia, sino una **estrategia de supervivencia**: hacer posible el cálculo largo en un mundo físico imperfecto.

Todo esto desemboca en el **bit**. El término proviene de *binary digit*, dígito binario. El bit es, literalmente, una decisión mínima entre dos estados posibles. Internamente, mediante transistores, la electricidad se maneja como bits de información. Estos bits están profundamente ligados al tiempo. En cada unidad de tiempo se almacenan estados y se realizan operaciones sobre ellos.

Los bits pueden capturar tanto lo numérico como lo simbólico. La percepción del mundo puede transformarse en voltajes y luego en bits. Cuando una computadora recibe una señal eléctrica por una de sus entradas, la convierte en listas de bits. Con 8 bits se pueden representar 256 valores distintos. Con 16 bits, 65 536 valores. Con 32 bits, más de cuatro mil millones. Con muy pocos bits se pueden representar números suficientemente grandes como para realizar toda la matemática práctica que conocemos. No hace falta representar infinitos para que la computación sea poderosa.

La computación digital no nace de la abundancia, sino de la restricción. Y es precisamente esa restricción la que la hace posible.
