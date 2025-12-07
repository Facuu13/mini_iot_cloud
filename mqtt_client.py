from database import init_db, save_reading

def procesar_mensaje(data: dict) -> dict:
    """
    Normaliza y valida un mensaje proveniente de un sensor.

    data: diccionario con los datos crudos (decodificados desde JSON)

    Devuelve un diccionario normalizado con:
    - device_id
    - temperature
    - humidity
    - status ("ok" o "error")
    - error_msg (si aplica)
    """
    device_id = data.get("device_id")
    temperature = data.get("temperature") or data.get("temp")
    humidity = data.get("humidity") or data.get("hum")
    error_msg = None
    status = "ok"

    # 1) Validación de device_id
    if not device_id:
        status = "error"
        error_msg = "Missing device_id"

    # 2) Verificar si vino un campo de error desde el sensor
    if "error" in data:
        status = "error"
        # Si ya había un error previo, los concatenamos
        if error_msg:
            error_msg = error_msg + f" | sensor_error={data['error']}"
        else:
            error_msg = f"sensor_error={data['error']}"

    # 3) Validación básica de datos
    if temperature is None and humidity is None:
        status = "error"
        if error_msg:
            error_msg = error_msg + " | no valid measurements"
        else:
            error_msg = "no valid measurements"

    return {
        "device_id": device_id,
        "temperature": temperature,
        "humidity": humidity,
        "status": status,
        "error_msg": error_msg,
    }

ok = procesar_mensaje({
    "device_id": "sensor_03",
    "temp": 23.5,
    "hum": 40
})

save_reading(ok)
