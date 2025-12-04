import time
import json
import sys
import supervisor
import board

from ideaboard import IdeaBoard   # :contentReference[oaicite:1]{index=1}

# Crear objeto IdeaBoard
ib = IdeaBoard()

# === CONFIG: POTENCIÓMETRO EN IO35 ===
pot = ib.AnalogIn(board.IO35)  # el valor estará en pot.value (0–65535)

# === CONFIG: NEOPIXEL INTEGRADO ===
# Control con:
#   ib.pixel     -> color
#   ib.brightness -> brillo global (0.0 a 1.0)
ib.pixel = (0, 0, 0)
ib.brightness = 0.0


# -----------------------------
# Funciones de protocolo simple
# -----------------------------

def read_pot():
    raw = pot.value            # 0–65535
    norm = raw / 65535.0
    return {
        "value_raw": raw,
        "value_0_1": norm
    }


def set_led(level: float):
    # Asegurar 0–1
    if level < 0:
        level = 0.0
    if level > 1:
        level = 1.0

    ib.pixel = (0, 0, 255 if level > 0 else 0)
    ib.brightness = level

    return {"led_level": level}


print("IdeaBoard lista. Canal: supervisor + stdin/stdout")


# -----------------------------
# Bucle principal
# -----------------------------
buffer = ""

while True:
    if supervisor.runtime.serial_bytes_available:
        c = sys.stdin.read(1)

        if c == "\n":
            line = buffer.strip()
            buffer = ""

            # --- Comando POT ---
            if line == "POT":
                data = read_pot()
                sys.stdout.write(json.dumps(data) + "\n")

            # --- Comando LED <valor> ---
            elif line.startswith("LED "):
                try:
                    level = float(line.split(" ", 1)[1])
                    data = set_led(level)
                    sys.stdout.write(json.dumps(data) + "\n")
                except Exception as e:
                    sys.stdout.write(json.dumps({"error": str(e)}) + "\n")

        else:
            buffer += c

    time.sleep(0.01)
