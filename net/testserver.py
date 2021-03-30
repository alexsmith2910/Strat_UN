import socket
import time
from netscript import dicttomessage
while True:
    time.sleep(0.1)
    print("serving")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1235))
    s.setblocking(False)
    s.listen()

    data = {"one": 1, "hello": "true"}
    clientsocket, address = s.accept()
    clientsocket.send(dicttomessage(data))