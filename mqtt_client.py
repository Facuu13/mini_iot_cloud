import paho.mqtt.client as mqtt

from ingestion import handle_raw_message

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
TOPIC = "facu/iot/sensors"  

def on_connect(client, userdata, flags, rc):
    """
    Callback que se ejecuta cuando el cliente se conecta al broker.
    """
    print("Conectado al broker con código:", rc)
    client.subscribe(TOPIC)
    print(f"Suscrito al tópico: {TOPIC}")

def on_message(client, userdata, msg):
    """
    Callback que se ejecuta cuando llega un mensaje a un topic suscripto.
    """
    print(f"Mensaje recibido en {msg.topic}: {msg.payload}")
    handle_raw_message(msg.payload)

def start_mqtt():
    """
    Crea el cliente, configura los callbacks y entra en el loop.
    """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT)
    print(f"Conectando a {MQTT_BROKER}:{MQTT_PORT}...")
    client.loop_forever()