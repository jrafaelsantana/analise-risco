import zmq
import pywintypes
import time
from exceptions import SocketClosedError
from utils import connect_opc, handle_message
from config import OPC_HOST, OPC_SERVER, TAGS_READ, READ_SECONDS

print("Connecting to Matrikon OPC...")
pywintypes.datetime = pywintypes.TimeType
opc = connect_opc(OPC_SERVER, OPC_HOST)

print("Connecting to inference server…")
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

buffer = []
request = 0

def close_connection(socket, context):
    socket.close()
    context.term()

if __name__ == '__main__':
    while True:
        try:
            print("Reading simulation %s …" % request)

            read_opc = opc.read(TAGS_READ)
            data = [tag[1] for tag in read_opc]
            buffer.append(data)
            
            if len(buffer) >= 30:
                socket.send_pyobj(buffer[-30:])

                message = socket.recv()
                received = handle_message(message)
                print("Received [ %s ]" % (received))
            
            time.sleep(READ_SECONDS)
            request = request + 1
        except SocketClosedError:
            close_connection(socket, context)
            print("Killed.")
            exit()
        except:
            socket.send(b"CLOSE_SOCKET")
            close_connection(socket, context)
            exit()