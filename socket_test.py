from socket import *
import socketserver
import paho.mqtt.client as mqtt
import datetime
from os.path import exists

HOST = ''
PORT = 8110
f = None
client = None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/Seoul/Dongjak/1")

def on_message(client, userdata, msg):
    received_topic = msg.topic
    received_msg = msg.payload
    print(msg.payload)
    if(received_msg == b'AT'):
        send_file()

    elif(received_msg == b'BT'):
        send_battery()

def send_file():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))

    imgstart = "AT+IMGSTART"
    s.send(imgstart.encode())

    f_send = "A89B08.raw"

    f = open(f_send, "rb")

    data = f.read(4096)
    print("Data Send")
    while (data):
        s.send(data)
        sleep(0.5)
        data = f.read(4096)
        
    s.send(b'AT+IMGEND')
    f.close()
    
    imgend = "AT+IMGEND"

    print("IMGEND send")
    client.publish("/Seoul/Dongjak/1","AT+IMGEND")

    s.close()

def send_battery():
    client.publish("/Seoul/Dongjak/1","22%")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("52.194.252.52",1883,60)
client.loop_forever()