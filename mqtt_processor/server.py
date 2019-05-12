from socket import *

import os
import uuid
from _thread import *
import threading
import paho.mqtt.client as mqtt
import datetime
from s3_upload import upload_to_s3
from time import sleep

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
serverSock.bind(('', 8110))
serverSock.listen(10)
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
    if data == b"AT+IMGEND":
        f.close()
        connectionSock.close()
        connectionSock, addr = serverSock.accept()

    elif data == b"AT+IMGSTART":
        filename = uuid.uuid4().hex.upper()[0:6]
        f = open(f'{filename}.raw', 'a+b')
        print("Started!")

    else:
        if(data == b''):
            connectionSock.close()
            os.system('./convert -f '+filename+".raw")
            sleep(2)
            upload_to_s3(filename+".raw.png",1)
            filename = uuid.uuid4().hex.upper()[0:6]
            connectionSock, addr = serverSock.accept()

        #print(data)
        f.write(data)