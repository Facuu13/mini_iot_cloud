from database import init_db
from ingestion import handle_raw_message

init_db()

# Caso 3: JSON inválido
handle_raw_message('{"device_id": "sensor_05", "temp": 21.5,,}')


