# El Bit

Hoy en día, cuando hablamos de computadoras, casi siempre se nos habla del bit. Parece una respuesta obvia, casi automática. Las computadoras digitales funcionan con bits, y toda su operación interna se reduce a manipular esas unidades mínimas mediante reglas lógicas. Sin embargo, comenzar por el bit suele ocultar algo importante: el bit no fue el punto de partida, fue el resultado de un largo proceso de pensamiento y de limitaciones físicas muy concretas.

Antes de que existieran los bits, las computadoras eran máquinas mecánicas. Computar significaba mover piezas. Engranajes, ejes, levas y manivelas eran los elementos fundamentales del cálculo. Un engranaje no es solo un objeto físico, es una operación matemática. Dos engranajes acoplados implementan una relación de multiplicación; una serie de engranajes puede sumar, restar o dividir. El ejemplo cotidiano de una bicicleta lo ilustra bien. Cambiar de marcha es cambiar un factor de multiplicación entre el pedaleo y el movimiento de la rueda. Allí no hay números escritos, pero hay aritmética ocurriendo.

Estas máquinas mecánicas calculaban en pasos discretos. Existieron muchas antes de la computadora digital. Desde la máquina de Anticitera, un complejo sistema de engranajes del mundo helenístico usado para predecir movimientos astronómicos, hasta la Pascalina de Blaise Pascal, diseñada para sumar y restar, o la máquina de Leibniz, capaz de multiplicar y dividir mediante un tambor escalonado. Más tarde, los diseños de Charles Babbage llevaron esta idea al extremo, proponiendo una máquina general basada enteramente en engranajes para ejecutar operaciones de manera secuencial. Cada giro de una manivela ejecutaba un paso de cómputo. El tiempo estaba incorporado de forma explícita. Un ciclo mecánico correspondía a una operación.

Ada Lovelace comprendió algo fundamental al trabajar con estas máquinas. Matemática y visionaria del siglo XIX, es considerada la primera programadora de la historia. Al estudiar la Máquina Analítica de Charles Babbage, entendió que no se trataba solo de una calculadora avanzada. No estaban limitadas a calcular números. Si una máquina podía manipular símbolos siguiendo reglas, entonces podía, en principio, operar sobre cualquier sistema formal. En sus notas, Lovelace anticipó la idea de que una máquina podía trabajar con música, texto o cualquier otro símbolo formalizable, una intuición extraordinariamente adelantada a su tiempo.

Aquí aparece una idea clave. Las mismas operaciones que permiten hacer aritmética también permiten construir lógica. Por ejemplo, si representamos verdadero como 1 y falso como 0, una multiplicación actúa como una operación lógica AND. Solo cuando ambos valores son 1, el resultado es 1. De este modo, operaciones matemáticas básicas pueden implementar decisiones lógicas. La frontera entre calcular y razonar comienza a desdibujarse.

## La lógica desde la matemática

Esta intuición fue llevada mucho más lejos por George Boole. Matemático y filósofo inglés del siglo XIX, Boole no estaba pensando en máquinas, sino en el pensamiento humano. Su objetivo era matematizar el razonamiento, eliminar las ambigüedades del lenguaje natural y operar con reglas mecánicas. Para ello, desarrolló lo que hoy llamamos álgebra booleana, un sistema en el que el razonamiento lógico se expresa mediante operaciones algebraicas simples. En ella, las variables no representan números, sino clases o proposiciones. Las operaciones algebraicas pasan a representar operaciones lógicas. Con esto, la lógica se convierte en una forma de cálculo. En un sistema binario, ciertas operaciones aritméticas se comportan exactamente como operaciones lógicas. Por ejemplo, si usamos los valores 0 y 1, la multiplicación funciona como una conjunción lógica AND y la suma módulo 2 funciona como una disyunción exclusiva XOR.

Cuando Boole desarrolló estas ideas, las computadoras no existían. Su trabajo era puramente teórico, Sin embargo, su trabajo estableció un puente decisivo entre aritmética, álgebra y lógica. Si el razonamiento podía formalizarse como un sistema de operaciones, entonces era concebible una máquina que lo ejecutara. La pregunta ya no era si se podía mecanizar el razonamiento, sino cómo hacerlo físicamente.

## De los engranajes a la electricidad

Las computadoras mecánicas tenían límites muy claros. Transmitían información como movimiento. Cada pieza tenía fricción, holgura y desgaste. El error se acumulaba. A mayor tamaño y velocidad, mayor inestabilidad. La mecánica apostaba por la precisión geométrica, pero esa precisión era costosa y frágil. En algún punto, el sistema simplemente dejaba de escalar.

La electricidad ofrecía una alternativa radical. Permitía transmitir estado sin mover materia macroscópica. Un relé o un tubo de vacío podía cambiar de estado mucho más rápido que cualquier engranaje. Sin embargo, la electricidad es, por naturaleza, continua. El voltaje puede tomar infinitos valores. En principio, esto parecía una ventaja: se podían representar magnitudes con gran precisión. De hecho, así funcionaron las computadoras analógicas, especialmente para resolver ecuaciones diferenciales.

Pero esta continuidad escondía un problema profundo. En un sistema continuo, cada valor importa. Cada pequeña perturbación altera el resultado. El ruido eléctrico no es una imperfección accidental, es inevitable. Es térmico, electromagnético, omnipresente. En cálculos largos y encadenados, el error se propaga y se amplifica. La continuidad, lejos de ser una fortaleza, se convertía en un obstáculo para el cómputo general.

La solución no fue refinar la precisión, sino renunciar a ella. En lugar de usar todos los valores posibles del voltaje, se decidió dividirlo en regiones. Un voltaje suficientemente alto representaría un estado, y uno suficientemente bajo representaría otro. No importaba el valor exacto, solo en qué región se encontraba. Así, un medio continuo se transformó en un sistema de estados discretos.

## De lo contínuo a lo discreto

Este paso fue decisivo. Al introducir umbrales, el sistema se volvió robusto al ruido. Las señales podían regenerarse. El significado ya no estaba atado al soporte físico exacto, sino al estado lógico. Aquí es donde la lógica de Boole encontró su realización física. Claude Shannon, ingeniero y matemático estadounidense, demostró que los circuitos eléctricos podían diseñarse y analizarse usando álgebra booleana. Su trabajo estableció una correspondencia directa entre puertas lógicas y circuitos físicos, mostrando que la lógica podía implementarse con interruptores eléctricos. Más adelante, John von Neumann integraría estas ideas en una arquitectura completa de computadora, donde datos y programas comparten la misma memoria, sentando las bases de la computación moderna. La lógica dejó de ser abstracta y se convirtió en ingeniería.

Con esto, la computadora pasó a entenderse como una máquina de estados discretos que evolucionan en el tiempo. La arquitectura propuesta por von Neumann consolidó esta visión al organizar la computadora como un sistema secuencial gobernado por estados, instrucciones y memoria. Cada estado está representado por voltajes, pero interpretado como decisiones. De esta convergencia entre engranajes, lógica y electricidad emerge el bit.

## Aparece el Bit

El bit, abreviatura de binary digit, es la unidad mínima de información en este nuevo paradigma. No representa una cantidad, sino una distinción. Un antes y un después. Un sí o un no. Internamente, mediante transistores, la computadora almacena y transforma estos bits en unidades de tiempo bien definidas.

A partir de bits se construyen números, símbolos, imágenes y sonidos. Ocho bits permiten representar 256 valores distintos. Dieciséis bits, 65 536. Con pocos bits se pueden representar números suficientemente grandes para toda la matemática práctica que conocemos. La potencia de la computación digital no proviene de la continuidad ni de la precisión infinita, sino de la combinación disciplinada de decisiones simples.

La computación digital no nace de la abundancia, sino de la restricción. De aceptar un mundo físico imperfecto y diseñar sistemas que sobrevivan a él. El bit no es el origen de la computación, es la construcción del mundo desde su representación.

Aquí tienes una **lista corta de lecturas indispensables**, pensada específicamente para **estudiantes**, no como erudición histórica sino como **soporte conceptual directo** para entender de dónde viene la computación discreta y por qué el bit existe. He priorizado textos legibles, fundacionales y con alto valor formativo.

---

# Del bit al microcontrolador

## Computación discreta en el ESP32 y la IdeaBoard

Todo lo que se ha dicho hasta ahora puede parecer abstracto o lejano, pero en realidad está ocurriendo, en este mismo momento, dentro del microcontrolador que tenemos en las manos. El **ESP32**, diseñado por Espressif Systems, no es una excepción a la historia de la computación discreta. Es su consecuencia directa.

El ESP32 es, en esencia, una máquina de estados discretos gobernada por un reloj. Internamente no “mide” el mundo de forma continua ni “entiende” voltajes como magnitudes físicas. Todo lo que ocurre dentro del microcontrolador termina convertido en bits, procesado como decisiones, almacenado como estados y ejecutado en pasos de tiempo bien definidos.

## El reloj

El reloj del microcontrolador cumple un rol similar al de la manivela en las máquinas mecánicas. Cada pulso de reloj marca un paso de cómputo. No hay operaciones fuera del tiempo. Cada instrucción, cada lectura, cada escritura ocurre sincronizada con ese ritmo interno. El tiempo deja de ser una abstracción y se convierte en parte del mecanismo mismo de la computación.

## Entradas digitales

Cuando leemos una entrada digital en la IdeaBoard, no estamos midiendo un voltaje exacto. Estamos preguntando si el voltaje está por encima o por debajo de un umbral. El mundo físico, continuo y ruidoso, se reduce a una decisión. Verdadero o falso. 1 o 0. Aquí aparece el bit de manera explícita. La lógica de Boole se manifiesta como una condición eléctrica.

## ADC y entradas analógicas

Las entradas analógicas parecen, a primera vista, romper con esta lógica discreta. El ADC convierte un voltaje continuo en un número. Pero lo que realmente hace es **muestrear** el mundo. En instantes discretos de tiempo, el voltaje se cuantiza en uno de un número finito de valores posibles. No hay continuidad infinita. Hay tiempo discreto y niveles discretos. El ADC no elimina el bit. Lo utiliza de forma intensiva.

## PWM

El PWM es otro ejemplo poderoso de esta filosofía. No genera un voltaje analógico real. Genera una señal digital que alterna entre 0 y 1, pero controlando el tiempo que permanece en cada estado. De nuevo, la continuidad aparente emerge de la discreción. Es el mismo principio por el cual una sucesión rápida de pasos mecánicos puede parecer un movimiento suave.

## De la lógica al movimiento

Cuando un motor gira, un LED cambia de brillo o un servo se posiciona, no estamos viendo continuidad pura. Estamos viendo el resultado de decisiones binarias ejecutadas rápidamente. El microcontrolador no “siente” el mundo como nosotros. Lo discretiza, lo decide y actúa sobre él.

## La IdeaBoard como máquina pedagógica

La IdeaBoard no es solo una placa. Es una representación tangible de toda esta historia. Cada pin, cada sensor y cada actuador materializa la transición del engranaje al bit. Programar la IdeaBoard no es aprender sintaxis. Es aprender a pensar el mundo como una secuencia de estados, decisiones y tiempos.

En ese sentido, trabajar con el ESP32 no es muy distinto a girar una manivela, diseñar una tabla lógica o escribir una ecuación. Es continuar una tradición. La computación discreta no es una limitación del hardware moderno. Es la forma en que hemos aprendido a hacer cálculo largo y confiable en un mundo físico imperfecto.


---

# Lecturas Sugeridas
next_t = time.monotonic()
prev_btn = True

while True:
    now = time.monotonic()
    if now < next_t:
        time.sleep(0.0005)
        continue

    # Asegura paso discreto, si hay atraso se recupera sin acelerar de golpe
    while now >= next_t:
        next_t += DT

    # Lecturas
    v = adc_filtered()
    b = read_button_debounced()

    # Evento de borde, botón soltado a presionado
    if prev_btn and (not b):
        toggle_mode()
    prev_btn = b

    # Umbral lógico derivado de lo analógico
    bit_from_world = update_logic_from_adc(v)

    # Selección de objetivo según modo
    if mode == MODE_MANUAL:
        # Pot controla velocidad, 0..65535 a -1..1
        target_throttle = (v / 65535.0) * 2.0 - 1.0
    else:
        # Un pulso que depende del reloj interno
        pulse_phase += (2.0 * 3.14159265) * (PULSE_HZ * DT)
        if pulse_phase > (2.0 * 3.14159265):
            pulse_phase -= (2.0 * 3.14159265)

        # Pulso binario hecho con tiempo, discreto en decisiones
        target_throttle = 0.8 if (pulse_phase < 3.14159265) else -0.8

    # Rampa suave, control discreto
    max_step = SLEW_PER_SEC * DT
    diff = target_throttle - current_throttle
    diff = clamp(diff, -max_step, max_step)
    current_throttle += diff

    # PWM a motor, internamente son conmutaciones
    ib.motor_1.throttle = current_throttle

    # NeoPixel como visualización de estado interno
    # Verde cuando bit_from_world True
    # Rojo cuando False
    # Azul indica modo PULSE
    if mode == MODE_PULSE:
        ib.pixel = (0, 0, 30) if bit_from_world else (30, 0, 30)
    else:
        ib.pixel = (0, 30, 0) if bit_from_world else (30, 0, 0)
```

## Cómo leer este ejemplo con las ideas del capítulo

* El reloj no es adorno, es el mecanismo que convierte la ejecución en una secuencia de pasos
* El ADC convierte un fenómeno continuo en números discretos, además lo hace en instantes discretos
* La histéresis muestra algo crucial, no basta un umbral, hay que diseñar robustez contra ruido
* El PWM muestra continuidad emergente, no hay voltaje fino, hay tiempo repartido entre 0 y 1
* La máquina de estados muestra que el comportamiento del sistema es una coreografía de decisiones.
