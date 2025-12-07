import json
from datetime import datetime

from database import save_reading
from procesamiento import procesar_mensaje

def handle_raw_message(payload):
    """
    Recibe un payload crudo (como texto o bytes),
    intenta decodificarlo como JSON, lo procesa
    y lo guarda en la base de datos.
    """
    # 1) Asegurarnos de tener un string
    if isinstance(payload, bytes):
        payload_str = payload.decode()
    else:
        payload_str = payload

    try:
        # 2) Intentar parsear JSON
        data = json.loads(payload_str)

        # 3) Pasar por procesar_mensaje
        reading = procesar_mensaje(data)
    
    except Exception as e:
        # En caso de error, armar un reading de error genérico
        reading = {
            "device_id": "Uknown",
            "temperature": None,
            "humidity": None,
            "status": "error",
            "error_msg": f"Exception during processing: {str(e)}"
        }
    
    # 4) Guardar en la base de datos
    save_reading(reading)
