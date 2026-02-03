import time
from ideaboard import IdeaBoard

ib = IdeaBoard()

while True:
    ib.pixel = (255, 0, 0)   # rojo
    time.sleep(0.5)

    ib.pixel = (0, 0, 0)   # apagado
    time.sleep(0.5)

