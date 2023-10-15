import OpenOPC
from exceptions import SocketClosedError

def connect_opc(opc_server, opc_host):
  opc = OpenOPC.client()
  opc.connect(opc_server, opc_host)

  return opc

def handle_message(message):
  if message == b'CLOSE_SOCKET':
    raise SocketClosedError()
  else:
    return message