from socket import *
from _thread import *
import threading
import datetime
import signal
import sys

serverPort = 9999
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

clientNumber = 0
countOfTotalClient = 0
countOfRequest = 0
connectionSocket = None

threadArr = []
timerThread = None

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

                payload = self._connectionSocket.recv(2048)
                    
                if not payload :
                    countOfTotalClient = countOfTotalClient - 1
                    print('Client {0} disconnected. Number of connected clients = {1}'.format(self._clientNumber, countOfTotalClient))
                    self._connectionSocket.close()
                    self._connectionSocket = None
                    break

                payload = payload.decode().split(',', 1)
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
            self._connectionSocket.send(modifiedMessage.encode())

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