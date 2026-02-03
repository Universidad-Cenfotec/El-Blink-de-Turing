import time
from ideaboard import IdeaBoard

ib = IdeaBoard()

while True:
    ib.pixel = (255, 0, 0)   # rojo
    time.sleep(0.5)

    ib.pixel = (0, 0, 255)   # azul
    time.sleep(0.5)
