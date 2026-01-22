# El-Blink-de-Turing: La computación vista desde un microcontrolador

Tomás de Camino Bec, Ph.D.  
Universidad CENFOTEC

## Antes de Empezar
Hace muchos años, cuando estudiaba la maestría en ciencias de la computación en el Tecnológico de Costa Rica, en un curso el profesor nos pidió hacer una presentación basada en un capítulo de un libro llamado “The Turing Ómnibus” (Dewdney, 1993). El libro me atrapó de inmediato, y más allá de preparar la presentación terminé recorriendo cada capítulo con una mezcla de sorpresa y claridad. Explora ideas esenciales de las ciencias de la computación y presenta de forma directa los fundamentos del pensamiento computacional.

Mucho después empecé a trabajar con arduinos. Además de los muchos proyectos de computación física que construí, siempre sentí una conexión cercana entre la computación más abstracta y estos pequeños dispositivos. En ellos se podía palpar cada concepto de manera concreta y casi tangible.

Este libro que estoy escribiendo sigue esa misma línea. Parte de la inspiración del “Turing Ómnibus”, pero se construye desde la programación directa de microcontroladores, en especial el ESP32. Con estudiantes, busco proponer proyectos sencillos que encapsulan ideas profundas en computación. No busco simplificarlas en exceso, sino tratarlas con la seriedad conceptual que merecen. No lo pienso como un libro de entrada a la computación física, sino como un punto de partida para pensar con computadoras a un nivel más fundamental.

Son veinte exploraciones que buscan explicar conceptos de computación. Cada capítulo es autocontenido y aborda una idea específica, acompañada de un proyecto sencillo. Se presenta el código en CircuitPython y la implementación con el ESP32, de forma directa y práctica. Lo llamo “Blink de Turing” porque el blink es el primer proyecto que uno prueba con un microcontrolador. Sirve para comprobar que todo funciona, que el código se carga bien y que el dispositivo responde. El código de un blink además es simple y transparente. “De Turing” porque siempre me ha fascinado su trabajo y su forma de pensar. Más que su papel como uno de los padres de la computación, me atrae cómo intentó entender los aspectos más profundos de las matemáticas y las ciencias. También uso ese nombre como un homenaje al libro que mencioné antes, que me inspiró a pensar más allá de simplemente programar computadoras.

Para trabajar de forma sencilla con el ESP32 utilizo una placa llamada [IdeaBoard](https://github.com/CRCibernetica/circuitpython-ideaboard/wiki), desarrollada en Costa Rica por Bentley Born, pionero del movimiento maker en el país. Los conceptos funcionan en cualquier microcontrolador y los códigos pueden traducirse sin mayor problema a otros lenguajes como C o C++ con ayuda de IA.

Aunque escribo este libro en primera persona, en esta aventura me acompañan estudiantes universitarias que son coautoras del texto. Han construido y probado la gran mayoría de los ejemplos, y también han creado los tutoriales y el material adicional. Escribo en primera persona, pero pensando en un trabajo colectivo. Tal vez hacerlo así sea una forma de rebeldía, porque en ciencias se espera una escritura impersonal, y eso nunca me ha convencido.

### Mitos sobre la computadora y computación

En este libro no seguimos las recetas habituales ni los discursos tradicionales sobre la computación. Nos interesa ir más allá de esa narrativa. Proponemos pensar la computadora no como una “cosa”, sino como un evento que ocurre en el tiempo, resultado directo de nuestra forma de pensar y de cómo descomponemos el mundo en pasos, estados y procesos. La computación, en este sentido, no es algo externo a nosotros, sino una proyección de nuestra manera de razonar y de construir significado. Con esa perspectiva, a lo largo del libro mantendremos presentes una serie de mitos que se han instalado en la enseñanza de la computación y que vale la pena revisar críticamente.

La razón principal es que la computación moderna se enseñó y se difundió **a través de una narrativa técnica simplificada**, no como una historia epistemológica. En ese proceso se consolidaron varios **mitos fundacionales** que, aunque útiles para la ingeniería, oscurecen la naturaleza real de la computación como fenómeno discreto, temporal y procedimental.

A continuación, sintetizo los mitos que pienso son los más influyentes y por qué persisten.

#### 1. El mito del bit como origen

Se suele presentar la computación como si **todo comenzara con el bit (0/1)**. Esto es falso históricamente y confuso conceptualmente. El bit es una solución de ingeniería para reducir ruido, costo y ambigüedad física. Lo fundamental no es el binario, sino **la discretización del proceso**. Antes del bit hubo ruedas decimales, engranajes, tarjetas perforadas y estados mecánicos múltiples. El mito persiste porque el binario es fácil de explicar, fácil de enseñar y encaja bien con la electrónica digital.

#### 2. El mito de la computación como matemática “pura”

Otro relato dominante es que la computación es simplemente **matemática formal ejecutada por máquinas**. Esto invisibiliza algo esencial, y es que la computación es matemática **puesta en el tiempo**. El cálculo computacional no es una igualdad verdadera o falsa, sino una **construcción paso a paso**, cercana a la visión intuicionista de los números naturales como sucesión (busquen sobre matemática intuisionista). Esta dimensión temporal resulta incómoda para una tradición matemática que privilegia objetos atemporales, pero aparece de forma natural en la computadora.

#### 3. El mito del algoritmo como receta abstracta

Se enseña el algoritmo como una entidad lógica independiente de su ejecución. En la práctica, un algoritmo **no existe fuera de su despliegue temporal**.
Las máquinas mecánicas lo mostraban de manera cruda, cada paso toma tiempo, puede fallar, puede atascarse. La computación moderna oculta esto bajo capas de abstracción. El resultado es que las personas piensan en algoritmos como ideas platónicas y no como **procesos físicos ejecutados**.

#### 4. El mito del computador como “caja negra inteligente”

Culturalmente, el computador se presenta como un artefacto que “sabe”, “decide” o “razona”. Esto desplaza la atención desde el proceso hacia el resultado. Esta narrativa se refuerza con la IA contemporánea, donde el énfasis está en la salida “inteligente” y no en la secuencia de transformaciones discretas que la producen. El proceso desaparece; queda solo la ilusión de inteligencia.

#### 5. El mito de Alan Turing como origen absoluto

Yo soy fan extremo de Turing, pero Turing lo convirtieron en un punto cero casi mítico. Sin embargo, su máquina no “inventa” la computación, sino que **formaliza una intuición ya presente**: el cálculo como sucesión finita de acciones elementales.  Al reducir la historia a Turing, se pierde la continuidad con la aritmética mecánica, el pensamiento discreto y la relación entre matemática y tiempo.

#### 6. El mito de la neutralidad temporal

Hay un mito muy profundo, y es que el tiempo es un detalle de implementación. En realidad, el tiempo **es constitutivo del cálculo**.
Un programa no es solo qué hace, sino **cuándo y en qué orden lo hace**, también cuanto tarda en hacerlo. Esta idea choca con la forma tradicional de enseñar matemática y lógica, que elimina el tiempo para ganar elegancia (vanal) formal.

#### Por qué estos mitos se mantienen

* Razones pedagígicas, es más fácil enseñar resultados que procesos.
* Razones industriales, la abstracción vende estabilidad y control.
* Razones culturales, preferimos objetos a procesos, productos a ejecuciones.
* Razones cognitivas, el pensamiento humano tiende a olvidar el tiempo cuando el resultado funciona.

#### Una consecuencia importante

Al perder esta visión, la computación se percibe como algo ajeno, casi mágico, en lugar de como lo que realmente es:
un dispositivo para convertir intuiciones discretas en procesos ejecutables en el tiempo. Recuperar esta mirada no es solo un ejercicio histórico. Es clave para entender la programación, la IA, y otros avances tecnológicos y, en general, por qué la computación no es una cosa, sino un evento.

### ¿Porqué Python?

En este libro utilizamos Python, más específicamente CircuitPython [1], que es un dialecto de Python diseñado para microcontroladores. En lo personal, Python no es un lenguaje que me apasione. Sin embargo, desde el punto de vista pedagógico, es probablemente el mejor lenguaje disponible hoy. Su sintaxis es simple, legible y cercana al lenguaje natural, lo que permite asociar con facilidad ideas matemáticas y conceptos fundamentales de la computación con el código mismo. Esto hace posible aprender a computar primero, y a programar después; la sintaxis pasa a un segundo plano y deja de ser una barrera inicial.

Por esa razón, en este libro no se enseña a programar como un ejercicio de memorización de reglas sintácticas. Aquí se aprende a programar estableciendo una relación directa entre lo que se desea hacer, la intención, el código que expresa esa intención y una acción física concreta en un microcontrolador. El programa no es un texto abstracto que corre en una pantalla, sino algo que ocurre en el mundo, es decir, un LED que enciende, un sensor que mide, un motor que se mueve. Esa conexión inmediata entre pensamiento, código y acción es lo que hace al microcontrolador un punto de partida ideal para aprender computación.

Además, los programas en CircuitPython tienden a ser cortos y directos. Las funciones complejas no están dispersas en el código principal, sino encapsuladas en librerías. Esto tiene dos efectos importantes. Por un lado, permite que alguien pueda programar cosas interesantes sin necesidad de comprender toda la complejidad subyacente desde el inicio. Por otro, deja abierta la puerta para que, más adelante, quien tenga curiosidad pueda explorar esas librerías y descubrir cómo está construida esa complejidad. La abstracción no oculta, sino que ordena.

Sé que este enfoque funciona porque no es solo una idea teórica. Lo he puesto en práctica durante años, particularmente en el torneo de Sumobot, donde este mismo modelo permitió que, para el 2025, más de 2000 estudiantes aprendieran a programar. No empezaron escribiendo código por escribir código, sino entendiendo que programar es una forma de pensar, de expresar intención y de hacer que algo ocurra en el mundo físico. Ese es el espíritu que recorre todo este libro.

## Capítulos
1. [El bit y computación discreta](https://github.com/Universidad-Cenfotec/El-Blink-de-Turing/tree/main/Cap1.%20Bits)
2. El loop infinito
3. Máquinas de estados en el mundo físico
4. el reloj en la computación
5. Sensar es computar
6. Actuar: del algoritmo al efecto físico
7. Algoritmos clásicos en hardware
8. La máquina de Turing en un microcontrolador
9. Aleatoriedad y simulación
10. Programación reactiva
11. Computación distribuida mínima
12. Cibernética y retroalimentación
13. El sensor como oráculo
14. Computación analógica–digital
15. Aprendizaje mínimo en microcontroladores
16. Robots como agentes computacionales
17. Estigmergia digital
18. Computación evolutiva básica
19. Protocolos como algoritmos sociales
20. Límites computacionales prácticos
21. Universalidad
22. [Sistemas Inteligentes](https://github.com/Universidad-Cenfotec/El-Blink-de-Turing/tree/main/Cap.%2021%20Sistemas%20Inteligentes)

## ¿Porqué en GitHub?

La idea de este documento es que sea compartido en todos lados y que pueda evolucionar con la computación misma.


## Referencias

- A. K. Dewdney, The Turing Omnibus: 66 Excursions in Computer Science. New York, NY, USA: W. H. Freeman, 1993.
- J. von Neumann, The Computer and the Brain. New Haven, CT, USA: Yale Univ. Press, 1958.
