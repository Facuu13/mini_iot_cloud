import sqlite3
from datetime import datetime

DB_NAME = 'iot_data.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            status TEXT NOT NULL,
            error_msg TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_reading(reading: dict):
    """
    Guarda una lectura procesada en la base de datos.

    reading tiene las claves:
    - device_id
    - temperature
    - humidity
    - status
    - error_msg
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    cursor.execute('''
        INSERT INTO readings (device_id, temperature, humidity, status, error_msg, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        reading['device_id'],
        reading['temperature'],
        reading['humidity'],
        reading['status'],
        reading['error_msg'],
        timestamp
    ))
    conn.commit()
    conn.close()

