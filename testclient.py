import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

def bytefixstrip(inp):
    inp = str(inp)
    output = inp[2:]
    output = output[:len(output)-1]
    return output

header = s.recv(4)
header = int(bytefixstrip(header))
print(int(str(header)))
print("Message header shows {0} bytes of data.".format(str(header)))
msg = s.recv(header)
jsonned = json.loads(msg)
print(jsonned["move"])
print("message: {0}".format(msg.decode("utf-8")))