import threading
import socket
import json

import globals

def dicttomessage(dictionary):
    """Converts a dictionary object to a UTF-8 bytes object prepended with a 4-byte header.
    expects size to be 9999 chars or less, and will otherwise raise a ValueError."""
    if (dictlen := (len(strdict := str(dictionary)))) > 9999:
        raise ValueError("Message size is too long. Try splitting the message to send seperately.")
    stringlen = ("0" * (4 - len(str(dictlen)))) + str(dictlen)
    strdict = strdict.replace("\'", "\"")
    return bytes(stringlen+strdict, "utf-8")

# dicttomessage({"move": "right", "building"})

# diction = {"move": "down-left", "building": ["drill", 12]}
# print(dicttomessage(diction))

def net_id_gen():
    pass  # Create incase UUID becomes too likely to duplicate IDs

def netlistener():
    while True:
        # now our endpoint knows about the OTHER endpoint.
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")
        clientsocket.send(dicttomessage(globals.building_costs))


if __name__ == "__main__":
    # create the socket
    # AF_INET == ipv4
    # SOCK_STREAM == TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((socket.gethostname(), 5482))

    s.listen(5)

    serthr = threading.Thread(target=netlistener, name="Server thread", daemon=False)
    serthr.start()
    # netlistener()
