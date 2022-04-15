#REL 2022.020.1010
from ManOfTheClient import ManOfTheClient
from ManOfTheMessage import *
import glv
import socket
import sys

glv.init()

if len(sys.argv) > 1:
    print("argv[1] = "+sys.argv[1])
    esito = elaboraInput(str(sys.argv[1]))
    print("OUTCOME:"+esito)
    sys.exit()

socketport = glv.config.getint("DEFAULT","socket_port")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', socketport))

print("Do Ctrl+c to exit the program !!")

while True:
    print("####### Server is listening #######")
    data, address = s.recvfrom(1024)
    print("CONNECTION FROM:", address)
    inputmsg = data.decode('utf-8')
    print(inputmsg)
    if len(inputmsg) > 0:
        MOTC = ManOfTheClient(s,address,inputmsg)
        MOTC.start()
    else:
        sent = s.sendto(buildErrMesg("Empty message").encode('utf-8'), address)
