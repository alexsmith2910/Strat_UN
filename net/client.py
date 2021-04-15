import socket
import select

import json
import time
import globals
import threading


# s.setblocking(0)

def bytefixstrip(inp):
    inp = str(inp)
    output = inp[2:]
    output = output[:len(output) - 1]
    return output


count = 0


class ClientThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.name = "Client thread"
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("", 5469))
        self.connected = False
        if not self.connected and globals.checkIfFirstAcceptance():
            while not self.connected:
                try:
                    # pass
                    self.s.listen(5)
                    #  Listening completes the connection and starts the game for the person who does NOT listen first
                    connection, addr = self.s.accept()
                    # print(addr)
                    # TODO: maybe log address of connections? or log sent data that is unusual?
                    self.s = connection
                    #  Search for and accept the new connection, which will be used to receive data.
                    #  One connection object for each client
                    connectHeader = self.s.recv(4)
                    if int(bytefixstrip(connectHeader)) == 0:
                        self.connected = True
                except Exception as e:
                    print("Client first connect: " + str(e))

    def run(self):
        print("Starting client...")
        while True:
            try:
                if not self.connected and not globals.checkIfFirstAcceptance():
                    while not self.connected:
                        try:
                            self.s.listen(5)
                            connectHeader = self.s.recv(4)
                            if int(bytefixstrip(connectHeader)) == 0:
                                self.connected = True
                        except Exception as e:
                            print("Client second connect: " + str(e))
                            # This is trying to fix OSError 10060, which states no response is made
                            # So sending an empty header upon initialization should get the server on the other end as it comes up.
                            # (The server does seem to become alive even when this is in a while loop as it causes 10060)
                        # except Exception as e:
                        #     print("Client init: " + str(e))
                        #  Possible solution above is known to cause OSError 10057 as it constantly tries to send
                        #  Before the server is opened. Theory for test is that as the server for the other side
                        #  Receives this, the socket will be connected and messages can be sent as normal
                # time.sleep(0.05)
                # while True:
                #     clientConnection = s.accept()
                #     print(clientConnection)
                # s.connect((socket.gethostname(), 5469))
                # print(str(socket.gethostname()))
                # print(str(type(socket.gethostname())))

                header = self.s.recv(4)  # Original cause of 10057
                if header != b'':
                    header = int(bytefixstrip(header))
                    # print(int(str(header)))
                    # print("Message header shows {0} bytes of data.".format(str(header)))
                    if header > 0:
                        msg = self.s.recv(header)
                        jsonned = json.loads(msg)

                    globals.p2Pos = jsonned["position"]
                    if "spawn" in jsonned:
                        globals.online_received["spawn"] = jsonned["spawn"]
                    if "build" in jsonned:
                        globals.online_received["build"] = jsonned["build"]
                    if "move" in jsonned:
                        globals.online_received["move"] = jsonned["move"]

                    #  Syncing usernames
                    if not globals.recievedName:
                        if "username" in jsonned:
                            globals.p2_name = jsonned["username"]
                            globals.online_sending["confirm_u"] = jsonned["username"]
                        if "confirm_u" in jsonned:
                            if jsonned["confirm_u"] == globals.p1_name:
                                globals.recievedName = True
            except Exception as e:
                # raise e
                print("Client: " + str(e))

    def kill(self):
        self.s.close()
        del self

# if __name__ == "__main__":
#     pass
