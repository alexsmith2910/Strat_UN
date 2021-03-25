import socket
import json
import time


# s.setblocking(0)

def bytefixstrip(inp):
    inp = str(inp)
    output = inp[2:]
    output = output[:len(output)-1]
    return output

count = 0

while True:
    # s.accept()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5469))
    header = s.recv(4)
    # print("recieving...")
    # if header == b'':
    #     print("found no data")
    if header != b'':  # TODO: get client to recieve multiple messages, client only seems to recieve one, server seems okay
        print(header)
        header = int(bytefixstrip(header))
        # print(int(str(header)))
        print("Message header shows {0} bytes of data.".format(str(header)))
        msg = s.recv(header)
        jsonned = json.loads(msg)
        # print(jsonned["move"])
        print("message: {0}".format(msg.decode("utf-8")))
        print("Packet {0}".format(count))
        count += 1
    s.close()