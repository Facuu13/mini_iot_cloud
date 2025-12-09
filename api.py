# api.py
from flask import Flask, jsonify
import sqlite3

DB_NAME = "iot_data.db"

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    # Para poder acceder a las columnas por nombre: row["device_id"]
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/devices")
def list_devices():
    """
    Devuelve la lista de device_id únicos.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT device_id FROM readings ORDER BY device_id")
    rows = cursor.fetchall()
    conn.close()

    # Filtramos posibles 'unknown' o None si no los querés mostrar
    devices = [row["device_id"] for row in rows if row["device_id"] is not None]

    return jsonify(devices)


@app.get("/devices/<device_id>/last")
def last_reading(device_id):
    """
    Devuelve la última lectura de un dispositivo.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT device_id, temperature, humidity, status, error_msg, timestamp
        FROM readings
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (device_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Device not found"}), 404

    data = {
        "device_id": row["device_id"],
        "temperature": row["temperature"],
        "humidity": row["humidity"],
        "status": row["status"],
        "error_msg": row["error_msg"],
        "timestamp": row["timestamp"],
    }

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
