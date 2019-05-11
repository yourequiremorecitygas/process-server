from socket import *

import os
import uuid


serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
serverSock.bind(('', 8110))
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
    print(data)

    if data == b"AT+IMGEND":
        f.close()
        os.system(f'/Users/senghyun/workspace/RawCamera-data-converter/convert -f ~/workspace/socketTest/{filename}.raw')
        connectionSock.close()
        connectionSock, addr = serverSock.accept()

    elif data == b"AT+IMGSTART":
        filename = uuid.uuid4().hex.upper()[0:6]
        f = open(f'{filename}.raw', 'a+b')
        print("Started!")

    else:
        f.write(data)
