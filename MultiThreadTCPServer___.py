from socket import *
from _thread import *
import threading
import datetime
import signal
import sys

import paho.mqtt.client as mqtt
from s3_upload import upload_to_s3
import os
import signal
import uuid
import threading

from time import sleep

serverPort = 8110
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
# serverSock.settimeout(None)

clientNumber = 0
countOfTotalClient = 0
countOfRequest = 0
connectionSocket = None

threadArr = []
timerThread = None

ConverterSemaphore = 1

# timer function
def timerFunction() :
    print ('Scheduler : {0} Clients connected now.'.format(countOfTotalClient))

# set timer
def repeatTimer(interval) :
    global timerThread
    timerThread = threading.Timer(interval, lambda : (timerFunction(), repeatTimer(interval)))
    timerThread.start()

# ctrl + c handler
def signal_handler(sig, frame):
    for t in threadArr :
        if t != None :
            t._exit()
    if timerThread != None :
        timerThread.cancel()
    if serverSocket != None :
        serverSocket.close()
    print('Bye bye~')   
    sys.exit(0)

# MyThread Class
class MyThread(threading.Thread) :
    def __init__(self, _connectionSocket, _clientAddress, _clientNumber) :
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = threading.Event()
        self._connectionSocket = _connectionSocket
        self._clientAddress = _clientAddress
        self._clientNumber = _clientNumber

    def _exit(self) :
        if (self._connectionSocket != None) :
            self._connectionSocket.shutdown(SHUT_RDWR)
            self._connectionSocket.close()
        self.__exit.set()

    def run(self) :
        #self._connectionSocket.settimeout(1)
        global countOfTotalClient
        global countOfRequest
        # reset request count (for Menu 4)
        
        # recv File information
        filename = ""
        f = None
        file_path = ""
        # communicate with client
        while (not self.__exit.is_set()) :

            # menu that selected by client
            choose = None
            payload = None

            # exception handling ( when client closes TCP connection )
            try :
                # menu that selected by client
                if (self.__exit.is_set()) :
                    break

                payload = self._connectionSocket.recv(4096)
                if payload.find(b'AT+IMGEND') != -1:
                    f.close()
                    
                    os.system('./convert -f '+filename+".raw")
                    print(file_path)
                    upload_to_s3(str(filename)+".raw.png",str(file_path))

                elif payload.find(b"AT+IMGSTART") != -1:

                    print(payload)
                    now = datetime.datetime.now()+datetime.timedelta(hours=9)
                    filename = now.strftime('%Y-%m-%d-%H:%M:%S') + "AA"

                    f = open(f'{filename}.raw', 'a+b')

                    payload = payload.replace(b'AT+IMGSTART;;',b'')
                    print(payload)
                    path_idx = payload.find(b';;')
                    file_path = payload[:path_idx].decode('utf-8')

                    print("Path_index : " + str(path_idx))
                    print("File Path_ : " + file_path)
                    if path_idx == -1:
                        print("not vailid Packet.")
                        continue

                    #f.write(payload)
                    print("Started!")

                elif not payload :
                    countOfTotalClient = countOfTotalClient - 1
                    print('Client {0} disconnected. Number of connected clients = {1}'.format(self._clientNumber, countOfTotalClient))
                    self._connectionSocket.close()
                    self._connectionSocket = None
                    break

                else:
                    f.write(payload)

                payload = payload
                #print(payload[-100:])
                choose = payload[0]

                if (choose == '') :
                    raise BrokenPipeError
            except timeout :
                continue
            except (ConnectionAbortedError, BrokenPipeError) :
                print('the connection socket has been closed by client! Bye bye~')
                countOfTotalClient = countOfTotalClient - 1
                print('Client {1} disconnected. Number of connected clients = {2}'.format(self._clientNumber, countOfTotalClient))
                self._connectionSocket.close()
                self._connectionSocket = None
                break

            modifiedMessage = 'message'
            #handle other input (error)
            #self._connectionSocket.send(modifiedMessage.encode())

        # close connectionSocket and wait to connect again
        if self._connectionSocket != None : 
            self._connectionSocket.close()

# Main Function below

# bind handler 
signal.signal(signal.SIGINT, signal_handler)
print("The server is ready to receive on port", serverPort)

# set timer to 60 seconds
repeatTimer(60)

# server process (listen)
while True:
    
    # set connection with client
    (connectionSocket, clientAddress) = serverSocket.accept()
    print('Connection requested from', clientAddress)

    clientNumber += 1
    countOfTotalClient += 1
    print('Client {0} connected. Number of connected clients = {1}'.format(clientNumber, countOfTotalClient))

    t = MyThread(connectionSocket, clientAddress, clientNumber)
    t.start()
    threadArr.append(t)
    
# close server socket
if serverSocket != None :
    serverSocket.close()
