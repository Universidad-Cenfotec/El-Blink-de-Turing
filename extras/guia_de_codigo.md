# Guía para la Generación de Códigos de Ejemplo  
Libro: Blink de Turing

Esta guía está dirigida a estudiantes y colaboradores que apoyan la creación de códigos de ejemplo para el libro. El objetivo no es solo producir código funcional, sino construir ejemplos pedagógicos, coherentes y consistentes a lo largo de todo el texto. Cada ejemplo debe ayudar a pensar la computación desde el microcontrolador, no solo a hacer que algo funcione.

## 1. Rol del código dentro del libro

En este libro el código no es un fin en sí mismo. El código funciona como una mediación entre intención y acción física. Cada ejemplo existe para ilustrar una idea computacional concreta, no para cubrir exhaustivamente una tecnología o una librería. El lector no debe sentirse abrumado por complejidad innecesaria. Menos líneas de código, más significado. Antes de escribir código, pregúntese siempre qué idea computacional está mostrando ese ejemplo.

## 2. Coherencia global del código

Todos los ejemplos del libro deben compartir reglas comunes para mantener coherencia conceptual y pedagógica. Se utiliza CircuitPython exclusivamente, asumiendo siempre el uso de un ESP32 con IdeaBoard. Debe priorizarse el uso de la librería ideaboard cuando exista, evitando acceder directamente a pines si hay una abstracción pedagógica definida. El código debe ser plano y legible, evitando trucos, optimizaciones prematuras o estilos ingeniosos. Se debe preferir claridad sobre elegancia, utilizar nombres de variables descriptivos y evitar abreviaturas crípticas.

## 3. Estructura base de todo ejemplo

Todo código del libro debe responder a una estructura mental reconocible, aunque no siempre esté explícitamente comentada. Esta estructura incluye las importaciones, la inicialización del hardware, la definición de la intención del programa, el bucle principal y una acción observable. No todos los ejemplos requieren comentarios en cada línea, pero sí deben permitir que el lector reconstruya fácilmente esta estructura al leer el código.

## 4. El while True como eje pedagógico

El uso de while True no es solo un detalle técnico, sino un elemento conceptual central. Representa la naturaleza cíclica del cómputo en microcontroladores. El microcontrolador no termina, está siempre observando y actuando. Los comportamientos emergen de la repetición y no de una ejecución lineal con inicio y fin. Por esta razón, el while True debe mantenerse visible, evitando esconder la lógica principal en funciones innecesarias o fragmentar el ciclo sin una razón pedagógica clara.

## 5. Uso pedagógico del tiempo

Cuando aparezca el tiempo en el código, mediante sleep, contadores o ciclos, debe entenderse como una convención interna y no como un tiempo absoluto. Se deben usar valores simples y comprensibles, evitando valores arbitrarios o excesivamente precisos sin sentido pedagógico. El uso del tiempo debe reforzar la idea de ritmo, espera, muestreo o repetición, no confundir al lector.

## 6. Documentación del código

La documentación del código debe ser orientadora, no exhaustiva. Los comentarios deben explicar la intención y el porqué de una decisión, no repetir lo que el código ya expresa claramente. Un buen comentario ayuda a entender la relación entre la idea computacional y la acción que se ejecuta. Además del código, cada ejemplo debe ir acompañado de un breve texto conceptual que lo contextualice dentro del capítulo, evitando descripciones línea por línea y enfocándose en el concepto que se quiere transmitir.

## 7. Uso de IA para generar ideas y código

El uso de IA es válido y esperado en este proyecto. La IA puede utilizarse para buscar ideas de proyectos, explorar variaciones de un concepto, generar borradores iniciales o identificar errores comunes. Sin embargo, no debe usarse para copiar código sin comprenderlo, introducir complejidad innecesaria o aceptar estructuras que oculten la intención pedagógica. Si una persona no puede explicar el código con sus propias palabras, ese código no debe incluirse.

## 8. Nivel de complejidad de los ejemplos

Cada ejemplo debe introducir un solo concepto nuevo o reutilizar conceptos ya vistos en un contexto distinto. No deben introducirse múltiples conceptos nuevos simultáneamente. La complejidad debe crecer de forma gradual, permitiendo que el lector construya comprensión paso a paso. Un buen ejemplo es aquel que se siente accesible y modificable.

## 9. Proyectos sugeridos y apertura a la exploración

Cuando se propongan proyectos o ejemplos, estos no deben cerrar completamente la solución. Deben dejar espacio para la exploración, la modificación y el error. El lector debe sentir que puede intervenir el código, cambiarlo y experimentar sin romper un sistema frágil o demasiado complejo.

## 10. Criterio final de calidad

Antes de entregar un ejemplo, es necesario preguntarse si alguien que nunca ha programado microcontroladores puede aprender algo relevante con ese código, si el ejemplo refuerza la idea central del capítulo, si invita a ser modificado y si puede explicarse sin necesidad de mirar la pantalla. Si alguna de estas respuestas es negativa, el ejemplo debe revisarse.

## 11. Espíritu del libro

Este libro no enseña simplemente a programar dispositivos. Enseña a pensar computacionalmente a través de dispositivos. El código es una excusa. La computación es el tema central.
```
