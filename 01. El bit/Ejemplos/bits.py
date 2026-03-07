# ----------------------------------------
# Universidad Cenfotec
# Ph. Tomás de Camino Beck
# Fiorella Perez
# Aylin Salas
# Gabriela Urbina Hernández
# ----------------------------------------

import time
import board
from ideaboard import IdeaBoard

ib = IdeaBoard()

# Potenciómetro en IO33 (entrada analógica)
pot = ib.AnalogIn(board.IO33)

# Brillo general del NeoPixel (0.0 a 1.0)
ib.brightness = 0.2

# Colores en formato RGB
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

# Umbral para convertir el valor continuo en un bit
UMBRAL = 30000   # puedes ajustarlo probando

while True:
    valor = pot.value          # 0 a 65535, valor continuo ya cuantizado
    print("ADC =", valor)

    # Aquí nace el bit interno
    if valor > UMBRAL:
        bit = 1
        ib.pixel = ROJO
    else:
        bit = 0
        ib.pixel = AZUL

    # Imprimimos también el bit para verlo en el serial
    print("bit =", bit)
    time.sleep(0.05)
