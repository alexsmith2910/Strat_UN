import socket
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

    def run(self):
        # count = 0
        print("Starting client...")
        while True:
            try:
                # time.sleep(0.05)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((socket.gethostname(), 5469))
                # s.accept()
                header = s.recv(4)
                # print("recieving...")
                # if header == b'':
                #     print("found no data")
                if header != b'':  # TODO: get client to recieve multiple messages, client only seems to recieve one, server seems okay
                    # try:
                    # print(header)
                    header = int(bytefixstrip(header))
                    # print(int(str(header)))
                    # print("Message header shows {0} bytes of data.".format(str(header)))
                    msg = s.recv(header)
                    jsonned = json.loads(msg)
                    # print(jsonned["move"])
                    # print("message: {0}".format(msg.decode("utf-8")))
                    # print("Packet {0}".format(count))
                    # TODO: Standardize message to send, and change from test client with no action
                    # TODO: to acting in-game
                    # print(jsonned["akey"])
                    # except KeyError:
                    #     print("key invalid")
                    globals.p2Pos = jsonned["position"]
                    # print(globals.p2Pos)
                    # count += 1
                # s.close()
            except Exception as e:
                print("client: " + str(e))

    def kill(self):
        self.s.close()
        del self

# client = ClientThread()
# client.start()

# while True:
#     try:
#         # s.accept()
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect((socket.gethostname(), 5469))
#         header = s.recv(4)
#         # print("recieving...")
#         # if header == b'':
#         #     print("found no data")
#         if header != b'':  # TODO: get client to recieve multiple messages, client only seems to recieve one, server seems okay
#             # try:
#             print(header)
#             header = int(bytefixstrip(header))
#             # print(int(str(header)))
#             print("Message header shows {0} bytes of data.".format(str(header)))
#             msg = s.recv(header)
#             jsonned = json.loads(msg)
#             # print(jsonned["move"])
#             print("message: {0}".format(msg.decode("utf-8")))
#             print("Packet {0}".format(count))
#             # TODO: Standardize message to send, and change from test client with no action
#             # TODO: to acting in-game
#             # print(jsonned["akey"])
#             # except KeyError:
#             #     print("key invalid")
#             globals.p2Pos = jsonned["position"]
#             count += 1
#         s.close()
#     except:
#         pass

# if __name__ == "__main__":
#     pass
