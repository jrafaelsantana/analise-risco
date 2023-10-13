import OpenOPC

def connectOpc(opc_server, opc_host):
  opc = OpenOPC.client()
  opc.connect(opc_server, opc_host)

  return opc

