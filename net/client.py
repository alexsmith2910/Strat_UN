import socket
import json
import time
import globals
import threading


# s.setblocking(0)

def bytefixstrip(inp):
    inp = str(inp)
    output = inp[2:]
    output = output[:len(output)-1]
    return output

count = 0


class ClientThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.name = "Client thread"

    def run(self):
        print("Starting client...")
        while True:
            try:
                # time.sleep(0.05)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((socket.gethostname(), 5469))
                # print(str(socket.gethostname()))
                # print(str(type(socket.gethostname())))
                header = s.recv(4)
                if header != b'':
                    header = int(bytefixstrip(header))
                    # print(int(str(header)))
                    # print("Message header shows {0} bytes of data.".format(str(header)))
                    msg = s.recv(header)
                    jsonned = json.loads(msg)

                    globals.p2Pos = jsonned["position"]
                    if "spawn" in jsonned:
                        globals.online_received["spawn"] = jsonned["spawn"]
                    if "build" in jsonned:
                        globals.online_received["build"] = jsonned["build"]
            except Exception as e:
                print("client: " + str(e))

    def kill(self):
        self.s.close()
        del self


# if __name__ == "__main__":
#     pass