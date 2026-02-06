import time
import random

# Representa la detección de un flanco (transición)
estado_anterior = 0 

while True:
    # Sensor como generador de estados (0 o 1)
    estado_actual = 1 if random.random() > 0.8 else 0
    
    # La computación ocurre solo en la frontera del cambio
    if estado_actual != estado_anterior:
        if estado_actual == 1:
            print("Transición detectada: Ascenso (Evento iniciado)")
        else:
            print("Transición detectada: Descenso (Evento finalizado)")
            
    estado_anterior = estado_actual
    time.sleep(0.1)
