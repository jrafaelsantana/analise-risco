import zmq
import pywintypes
import time
from utils import connectOpc
from config import OPC_HOST, OPC_SERVER, TAGS_READ, READ_SECONDS

print("Connecting to Matrikon OPC...")
pywintypes.datetime = pywintypes.TimeType
opc = connectOpc(OPC_SERVER, OPC_HOST)

print("Connecting to inference server…")
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

buffer = []
request = 0

while True:
    print("Reading simulation %s …" % request)

    read_opc = opc.read(TAGS_READ)
    data = [tag[1] for tag in read_opc]
    buffer.append(data)
    
    if len(buffer) >= 30:
        socket.send_pyobj(buffer[-30:])

        #  Wait for OK.
        message = socket.recv()
        print("Received [ %s ]" % (message))
    
    time.sleep(READ_SECONDS)
    request = request + 1
