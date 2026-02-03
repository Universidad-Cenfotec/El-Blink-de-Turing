import time
from ideaboard import IdeaBoard
from StateMachine import StateMachine

ib = IdeaBoard()

# Definición de estados (pueden ser strings, números, constantes)
Q0 = "q0"
Q1 = "q1"

# Funciones de estado
def estado_q0():
    ib.pixel = (255, 0, 0)  # rojo
    time.sleep(1)
    return Q1

def estado_q1():
    ib.pixel = (0, 0, 0)  # apagado
    time.sleep(1)
    return Q0

# Construcción de la máquina
sm = StateMachine(initial_state=Q0)
sm.add_state(Q0, estado_q0)
sm.add_state(Q1, estado_q1)

# Loop principal del microcontrolador
while True:
    sm.step()
