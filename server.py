from socket import *
from _thread import *

import os
import uuid
import threading

import paho.mqtt.client as mqtt
import datetime
import signal
from s3_upload import upload_to_s3
from time import sleep

serverPort = 8110

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSock.bind(('', serverPort))
serverSock.listen(1)
serverSock.settimeout(None)
print(serverSock.gettimeout())

connectionSock, addr = serverSock.accept()
connectionSock.settimeout(None)

print(str(addr), '[Process Server] connected to this Server.')
print(connectionSock.gettimeout())

# socket.setdefaulttimeout(60)

filename = ""
f = None

while True:
    data = connectionSock.recv(4096)
    if data.find(b"AT+IMGEND") != -1:
        f.close()
        print(data)
        connectionSock.close()

        os.system('./convert -f '+filename+".raw")
        upload_to_s3(filename+".raw.png",1)

        connectionSock, addr = serverSock.accept()

    elif data.find(b"AT+IMGSTART") != -1:
        filename = uuid.uuid4().hex.upper()[0:6]
        f = open(f'{filename}.raw', 'a+b')
        print("Started!")

    else:
        if(data == b''):
            print(data)
            connectionSock.close()
            connectionSock, addr = serverSock.accept()

        # print(data)
        f.write(data)