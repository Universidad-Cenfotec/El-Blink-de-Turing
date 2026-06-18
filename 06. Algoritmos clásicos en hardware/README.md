# Algoritmos clásicos en hardware

## Introducción

Quiero pensar los algoritmos clásicos de una manera menos cómoda. Si los miro solo como recetas cerradas, la computación se vuelve una colección de procedimientos que se memorizan, se copian y se entregan. Una búsqueda lineal, un ordenamiento, un filtro digital o un controlador PID pueden parecer pasos ya resueltos. Sin embargo, cada vez que los acerco al hardware, dejan de ser respuestas tranquilas y se convierten en preguntas: ¿qué significa recordar?, ¿qué significa decidir?, ¿qué significa medir?, ¿qué significa actuar?, ¿qué significa equivocarse cuando una máquina está conectada al mundo físico?

Empiezo por ahí porque un microcontrolador no ejecuta algoritmos en el vacío. Los ejecuta con poca memoria, con sensores ruidosos, con energía limitada, con relojes imperfectos y con consecuencias materiales: un motor se mueve, un led parpadea, una alarma suena, una válvula se abre, un robot gira demasiado tarde. Por eso, cuando pienso en algoritmos desde un microcontrolador, la pregunta cambia. Ya no me basta saber si el programa produce la salida correcta en una pantalla. Necesito preguntarme qué sabe realmente la máquina, cuánto tarda en saberlo, qué olvida, qué supone, qué ignora y qué transforma cuando convierte el mundo en números.

Desde esa inquietud, este ensayo avanza como una cadena de razonamientos. Primero me pregunto por la memoria, porque sin alguna forma de recuerdo no hay comportamiento que dure. Luego paso a la decisión, porque recordar solo importa si afecta lo que se hace. Después aparece el tiempo, porque decidir tarde puede equivaler a no decidir. A partir de ahí, la búsqueda, el ordenamiento, los bucles, las señales, el control y la arquitectura dejan de ser temas separados. Se vuelven estaciones de una misma idea: los algoritmos clásicos no son el objetivo final, sino el pretexto para mirar cómo una intención humana, una máquina finita y un mundo cambiante negocian entre sí.

## Recordar no es guardar una palabra

La primera imagen que necesito revisar es la de la variable como una caja con nombre. Esa metáfora ayuda, pero también simplifica demasiado. Cuando declaro una variable en un microcontrolador, no estoy creando una idea pura suspendida en el código. Estoy ocupando registros, memoria RAM, direcciones, bits cargados eléctricamente e instrucciones que leen y modifican ese estado. Lo que llamo "dato" existe porque una arquitectura física puede conservarlo e interpretarlo.

Al pensar esto, la memoria deja de parecerme un simple lugar. Se vuelve un proceso. Un sensor de temperatura leído una sola vez ofrece un dato; leído muchas veces ofrece una historia. Un botón presionado puede parecer un evento instantáneo, pero en realidad puede ser una secuencia inestable de rebotes eléctricos. Una máquina de estados recuerda dónde está para decidir qué hacer después. Un filtro recuerda muestras anteriores para suavizar el presente. Un controlador recuerda el error acumulado para corregir el futuro.

Así llego a una primera conclusión: recordar no consiste solamente en guardar valores, sino en construir una relación con el tiempo. Un sistema sin memoria reacciona al instante; un sistema con memoria compara, anticipa, corrige y aprende de una manera mínima. Entonces la pregunta importante ya no es solo cuántos bytes tiene el dispositivo, sino cuánta historia necesita para comportarse con cierta inteligencia. Esa pregunta me lleva inevitablemente a otra: si la máquina recuerda algo, ¿cómo usa ese recuerdo para decidir?

## Decidir entre reglas, ruido y mundo

Un condicional parece una estructura humilde: si ocurre esto, haz aquello. Pero en hardware esa frase se vuelve mucho más difícil de sostener. Para escribir un \texttt{if}, primero tengo que decidir qué significa que algo ocurra. ¿Cuándo un valor analógico se considera alto o bajo? ¿Cuándo una señal es una presencia real y no ruido? ¿Cuándo una lectura ambigua merece una acción irreversible?

Aquí descubro que programar decisiones en un microcontrolador obliga a distinguir entre reaccionar y decidir. Reaccionar puede ser encender un led si una lectura supera cierto umbral. Decidir implica construir condiciones, tolerancias, prioridades, estados previos y consecuencias. Un robot que evita obstáculos no entiende el obstáculo como concepto humano, pero organiza datos de distancia, tiempo y movimiento para escoger una acción. Esa elección no es pensamiento pleno, aunque tampoco es simple pasividad. Es razonamiento operacional encarnado en reglas.

Por eso los condicionales me parecen una forma mínima de epistemología. La máquina no ve el mundo; lo clasifica. No escucha el sonido; procesa amplitudes muestreadas. No siente peligro; evalúa rangos. Si se equivoca, tengo que preguntarme si el error pertenece a la máquina o a las categorías que yo diseñé para ella. Tal vez una máquina no "cree" nada, pero todo algoritmo contiene una apuesta sobre qué diferencias importan. Y una vez que acepto eso, aparece una nueva inquietud: aun si la regla es correcta, ¿llega a tiempo?

## El tiempo también se programa

En una explicación abstracta, el tiempo suele aparecer como complejidad: $O(n)$, $O(n \log n)$, $O(n^2)$. En un microcontrolador, en cambio, el tiempo aparece además como urgencia. Un algoritmo lento no es solo ineficiente; puede llegar tarde. Si el mundo cambia más rápido que el ciclo de lectura, cálculo y acción, el programa produce una respuesta correcta para una realidad que ya dejó de existir.

Por eso, cuando implemento algoritmos clásicos en hardware, la complejidad temporal deja de ser una notación distante. Buscar en una lista pequeña puede parecer trivial, hasta que esa lista crece o hasta que la búsqueda debe ocurrir entre dos interrupciones. Ordenar datos puede parecer elegante, hasta que consume el tiempo necesario para leer un sensor crítico. Filtrar una señal puede reducir ruido, pero también introducir retraso. Promediar muchas muestras puede dar estabilidad, pero sacrificar reacción.

El tiempo computacional no está separado del mundo: forma parte del comportamiento. Un microcontrolador percibe el tiempo mediante relojes, temporizadores, retardos, interrupciones y ciclos de instrucción. Pero el mundo no espera a que el programa termine. Entonces mi razonamiento se vuelve más concreto: ¿cuándo conviene gastar memoria para ahorrar tiempo y cuándo conviene gastar tiempo porque no queda memoria? La eficiencia deja de ser una virtud decorativa y se convierte en condición de posibilidad. Con esa tensión en mente, puedo volver a un algoritmo aparentemente simple: buscar.

## Buscar sin comprender

La búsqueda lineal me interesa porque contiene una paradoja hermosa: una máquina puede encontrar algo sin comprenderlo. Recorre una colección, compara valores y se detiene cuando aparece una coincidencia. No sabe qué significa el dato. No sabe por qué importa. Solo sabe que una relación formal se cumplió.

Pero esa simpleza me obliga a preguntar qué conocimiento previo necesita un algoritmo para buscar bien. Si los datos están desordenados, quizá deba revisar uno por uno. Si están ordenados, puede descartar grandes regiones mediante búsqueda binaria. Si conozco ciertas probabilidades, puedo revisar primero los casos más frecuentes. Si el espacio de búsqueda crece, lo que parecía razonable se vuelve impracticable.

En hardware, buscar rara vez es una escena puramente intelectual. Puede significar identificar un patrón en lecturas de sensores, reconocer una clave, ubicar un valor máximo, detectar una anomalía o encontrar una ruta. Cada estrategia de búsqueda revela una relación distinta entre ignorancia y estructura. Buscar no es simplemente mirar; es decidir qué partes del mundo puedo descartar sin perder lo que me importa. Y si descartar depende de la estructura, entonces el siguiente paso es preguntarme qué significa ordenar.

## Ordenar es imponer una teoría

Ordenar datos parece una tarea administrativa, pero no lo es. Ordenar es imponer una noción de mundo: menor a mayor, prioridad alta antes que baja, más reciente antes que antiguo, más cercano antes que lejano, más probable antes que raro. No existe un único orden natural; existen criterios diseñados para responder mejor a una pregunta.

Cuando implemento burbuja, inserción, selección o cualquier otro método, no solo sigo pasos. Aprendo que organizar cuesta. Cada intercambio consume tiempo. Cada comparación supone una medida. Cada arreglo ordenado es el resultado de haber gastado energía computacional para ganar claridad posterior. Ordeno porque espero buscar mejor, decidir más rápido o comunicar con menos ambigüedad.

Esta idea conecta los datos con el conocimiento. La información sin estructura puede estar presente y aun así ser inútil. La estructura permite inferir, anticipar y reducir esfuerzo. Pero también puede ocultar. Ordenar por un criterio puede volver invisibles otros. Así, un algoritmo de ordenamiento deja de ser solo una técnica y se vuelve una advertencia sobre el poder y el costo de clasificar. Sin embargo, ordenar todavía parece producir un resultado. En los microcontroladores, muchas veces lo que necesito no es llegar a un resultado final, sino sostener una conducta. Ahí aparecen los bucles.

## Repetir hasta que aparezca conducta

Los bucles son tan comunes que puedo dejar de verlos. Pero casi todo comportamiento computacional persistente depende de ellos. Leer, comparar, actuar y volver a leer: esa repetición mínima puede producir termostatos, semáforos, robots, alarmas, instrumentos musicales, sistemas de riego o prótesis experimentales.

La repetición permite que una regla simple se convierta en conducta. Un led que parpadea no es interesante por encenderse una vez, sino por sostener un patrón. Un robot sigue una línea porque repite correcciones pequeñas. Una alarma vigila porque nunca deja de preguntar. Una máquina de estados parece tener personalidad porque conserva una situación interna y actualiza su respuesta según eventos.

Pero todo ciclo contiene una amenaza: ¿cómo sabe una máquina cuándo detenerse? En un computador personal, un programa que no termina puede ser un error. En un microcontrolador, no terminar puede ser precisamente la tarea. Esta diferencia me obliga a pensar la computación no solo como cálculo de resultados, sino como producción de presencia: sistemas que permanecen atentos, repiten hábitos y modifican su comportamiento según el entorno. Para que esa presencia tenga sentido, la máquina debe percibir algo del mundo. Entonces la pregunta se desplaza hacia la medición.

## Digitalizar es perder para poder pensar

La luz, el sonido, la presión y la temperatura no llegan al microcontrolador como conceptos. Llegan como voltajes, pulsos, cambios de resistencia o señales convertidas por un ADC. Digitalizar el mundo significa reducir una continuidad física a números discretos. Esa reducción es poderosa, pero no inocente.

Cada muestra captura algo y pierde algo. La resolución limita las diferencias visibles. La frecuencia de muestreo decide qué cambios pueden detectarse. El ruido introduce variaciones que no siempre pertenecen al fenómeno que quiero observar. Filtrar una señal consiste en defender una interpretación: esto es información, aquello es ruido. Pero esa frontera no siempre está dada; se diseña.

Por eso los algoritmos de transformación de señales me parecen preguntas sobre representación, no simples trucos para limpiar datos. ¿Qué parte de la realidad cabe en un número? ¿Qué se destruye al cuantizar? ¿Qué se inventa al interpolar? ¿Hasta qué punto reconstruyo el mundo y hasta qué punto construyo una versión útil de él? Esta pregunta es incómoda porque muestra que medir no basta. Después de medir, muchas veces quiero actuar. Y cuando el cálculo toca la materia, el problema cambia otra vez.

## Cuando el cálculo toca la materia

Un algoritmo que controla un motor no vive en el mismo universo que una función evaluada en papel. El motor tiene inercia, fricción, tolerancias, retrasos, consumo, vibración y desgaste. El sensor que informa su posición puede estar contaminado por ruido. La señal de control puede saturarse. El cable puede fallar. El mundo físico no obedece con la limpieza de una ecuación.

Por eso el control me parece una frontera privilegiada entre computación y realidad. No quiero pensar un PID solo como una fórmula con tres términos, sino como una conversación imperfecta entre error, corrección y consecuencia. El término proporcional reacciona al presente; el integral recuerda una deuda acumulada; el derivativo intenta leer la tendencia del futuro. En conjunto, el controlador revela que actuar bien requiere medir, recordar, anticipar y moderar.

Aquí la pregunta más importante no es dónde termina el algoritmo en el código, sino dónde comienza la física en el comportamiento. Un programa puede calcular una orden, pero la acción ocurre en materiales concretos. Allí el algoritmo deja de ser texto y se convierte en fuerza. Y como toda fuerza tiene costo, vuelvo a las restricciones que atraviesan todo el razonamiento: memoria, tiempo, energía y precisión.

## Hacer más con menos

Los microcontroladores me recuerdan una lección que las computadoras abundantes suelen ocultar: toda decisión tiene costo. La memoria es poca, el tiempo es finito, la energía importa y los pines disponibles se acaban. En ese ambiente, la optimización no es obsesión prematura; es una forma de pensar bajo restricciones.

Hacer más con menos no significa escribir código oscuro ni celebrar la escasez por sí misma. Significa comprender las consecuencias de cada representación. Un arreglo ocupa espacio. Una tabla precalculada ahorra tiempo pero consume memoria. Una variable de más puede parecer irrelevante hasta que el dispositivo no puede sostener todas las tareas. Una operación con punto flotante puede ser elegante, pero quizá sea innecesaria frente a una aproximación entera bien diseñada.

Las restricciones no empobrecen la creatividad; la obligan a volverse precisa. Cuando no todo cabe, debo elegir qué importa. Cuando no todo puede calcularse a tiempo, debo decidir qué puede aproximarse. Cuando no todo puede medirse, debo inferir. La eficiencia, entonces, no es solamente una propiedad técnica: es una decisión de diseño sobre qué mundo quiero que la máquina pueda habitar. Pero esa decisión nunca ocurre en abstracto. Depende de la arquitectura que la sostiene.

## Del algoritmo a la arquitectura

No todos los algoritmos se sienten igual dentro del hardware. Algunos encajan naturalmente con registros, temporizadores, interrupciones, buses y periféricos. Otros exigen más memoria, más paralelismo o más precisión de la que el sistema posee. La arquitectura física no es un detalle posterior: moldea lo que resulta fácil, difícil o directamente inviable.

Un algoritmo escrito en pseudocódigo parece independiente del soporte. Pero al ejecutarlo en un microcontrolador aparecen preguntas materiales: ¿cuántos bits tiene cada dato?, ¿qué tan rápida es la conversión analógica-digital?, ¿qué ocurre durante una interrupción?, ¿cuánta pila queda?, ¿qué periférico puede hacer trabajo sin ocupar al procesador?, ¿qué pasa si la alimentación cae? El hardware no solo ejecuta ideas computacionales; las transforma.

Por eso termino entendiendo los algoritmos clásicos de otra manera. No son piezas aisladas ni ejercicios cerrados. Son formas de razonar dentro de límites concretos. Pensar computacionalmente exige entender representaciones, memorias, tiempos, arquitecturas, energías y efectos. Un algoritmo no es solo una secuencia de pasos: es una negociación entre una intención humana, una máquina finita y un mundo que no deja de cambiar.

## Comentario Final

Al final de este recorrido, no quiero tratar los algoritmos como piezas de museo. Prefiero ponerlos frente a problemas donde una receta no alcance: sensores que mienten un poco, motores que obedecen tarde, memorias que se llenan, datos que crecen, señales que se confunden, decisiones que deben tomarse con información incompleta.

Preguntas generadoras de proyectos (o retos)

Construya una máquina que recuerde un evento.
Diseñe un sistema que cuente sin utilizar software.
Implemente una operación matemática usando únicamente lógica digital.
Cree un dispositivo capaz de tomar una decisión binaria.
Construya un mecanismo físico que ejecute una secuencia de instrucciones.
Diseñe un lenguaje mínimo para controlar un dispositivo.
Replique una función de un microcontrolador utilizando componentes discretos.
Descubra cuál es el conjunto mínimo de componentes para construir una computadora.

En ese contexto, los algoritmos clásicos recuperan su potencia. La búsqueda lineal deja de ser una lista recorrida y se convierte en una pregunta sobre ignorancia. El ordenamiento deja de ser intercambio de elementos y se convierte en una teoría de la organización. Los bucles dejan de ser sintaxis y se convierten en comportamiento. Los filtros dejan de ser fórmulas y se convierten en criterios para separar mundo y ruido. El control deja de ser ecuación y se convierte en acción responsable.

Aprender computación con microcontroladores no consiste simplemente en hacer que algo funcione. Para mí, consiste en descubrir qué tuve que suponer para que funcionara, qué quedó fuera, qué costo tuvo, qué memoria necesitó, cuánto tiempo tomó y qué tipo de mundo fue capaz de reconocer. Allí, en esa incomodidad fértil, los algoritmos dejan de ser respuestas y vuelven a ser preguntas.
