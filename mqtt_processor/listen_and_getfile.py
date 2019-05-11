import paho.mqtt.client as mqtt
import datetime

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("topic")

def on_message(client, userdata, msg):
    print("Topic: " + msg.topic + "\nMessage" + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("52.194.252.52", 1883, 60)
client.loop_forever()