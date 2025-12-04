import json
from dataclasses import dataclass

import serial
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings


# === CONFIGURACIÓN DEL PUERTO SERIE ===
# Ajusta esto según tu sistema:
#  - Windows: "COM3", "COM4", etc.
SERIAL_PORT = "COM3"      # <-- CAMBIA ESTO AL COM REAL DE TU IDEABOARD
BAUDRATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)


# === DEFINIMOS EL SERVIDOR MCP ===
# stateless_http + json_response: recomendado para conectores tipo ChatGPT.
# transport_security con DNS rebinding apagado: necesario para que acepte el host de ngrok.
mcp = FastMCP(
    "IdeaBoard Server",
    json_response=True,
    stateless_http=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    ),
)

# Importante: exponemos el endpoint HTTP del MCP en /mcp
mcp.settings.streamable_http_path = "/mcp"


@dataclass
class PotReading:
    value_raw: int
    value_0_1: float


def _send_command(cmd: str) -> dict:
    """Manda un comando por serie al IdeaBoard y devuelve un dict JSON."""
    ser.write((cmd.strip() + "\n").encode("utf-8"))
    line = ser.readline().decode("utf-8").strip()
    if not line:
        raise RuntimeError("Sin respuesta del IdeaBoard")
    try:
        data = json.loads(line)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Respuesta no es JSON válido: {line}") from e
    return data


@mcp.tool()
def read_potentiometer() -> PotReading:
    """
    Lee el potenciómetro del IdeaBoard.

    Devuelve:
      - value_raw: entero ADC 0–65535
      - value_0_1: valor normalizado entre 0.0 y 1.0
    """
    data = _send_command("POT")
    return PotReading(
        value_raw=int(data["value_raw"]),
        value_0_1=float(data["value_0_1"]),
    )


@mcp.tool()
def set_led(level: float) -> dict:
    """
    Ajusta el brillo del NeoPixel del IdeaBoard según un nivel entre 0.0 y 1.0.
    Devuelve el nivel aplicado.
    """
    data = _send_command(f"LED {level}")
    return {
        "led_level": float(data.get("led_level", level))
    }


if __name__ == "__main__":
    # Arrancamos el servidor MCP usando HTTP "streamable"
    # Por defecto sirve en http://127.0.0.1:8000/mcp
    mcp.run(transport="streamable-http")
