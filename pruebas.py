from database import init_db
from ingestion import handle_raw_message

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Conectado con código:", rc)
    client.subscribe("facu/test")

def on_message(client, userdata, msg):
    print("Topic:", msg.topic)
    print("Payload:", msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883)
client.loop_forever()


