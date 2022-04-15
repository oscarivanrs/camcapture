#REL 2022.020.1010
from ManOfTheMessage import *
import threading
import socket

class ManOfTheClient(threading.Thread):
    def __init__(self,clientsocket,address,inputmsg):
        threading.Thread.__init__(self)
        self.__clientsocket = clientsocket
        self.__address = address
        self.inputmsg = inputmsg

    # Overrriding of run() method in the subclass
    def run(self):
        print("ManOfTheClient: "+self.inputmsg)
        try:
            esito = elaboraInput(self.inputmsg)
        except Exception as err:
            print(err.args)
            esito = buildErrMesg("Exception {"+str(err)+"}")
        self.__clientsocket.sendto(esito.encode('utf-8'), self.__address)
