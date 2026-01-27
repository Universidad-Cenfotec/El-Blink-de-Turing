# Ejemplos del capítulo: El Bit

He escrito estos scripts como complemento práctico de la lectura.  
Mi objetivo es materializar los conceptos filosóficos del capítulo: analizar cómo nace una decisión (un bit) a partir del ruido y cómo la manipulación del tiempo permite crear matices en el comportamiento del sistema.

Para mí, el código no es más que una herramienta que hace visibles fenómenos físicos, permitiéndonos observar, experimentar y razonar sobre ellos.

## Ejemplo 1: El nacimiento del bit (Histéresis)

En este código busco demostrar cómo una señal ruidosa e inestable (analógica) puede transformarse en una decisión firme y estable (digital).

En el mundo físico, el voltaje nunca es perfecto. Si utilizo un único punto de corte para decidir si algo es “1” o “0”, el ruido hará que el sistema dude y oscile.  
Para resolver este problema implemento **histéresis**: doto al sistema de una forma mínima de memoria. Una vez que se toma una decisión, el sistema se resiste a cambiarla hasta que la señal varía de manera significativa, creando así una **zona de seguridad** frente al ruido.
