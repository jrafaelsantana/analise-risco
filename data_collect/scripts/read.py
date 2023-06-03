import OpenOPC
import pywintypes
import time
import pandas as pd
import os
from datetime import datetime

pywintypes.datetime = pywintypes.TimeType

# Variaveis de configuracao
OPC_SERVER = 'Matrikon.OPC.Simulation'
OPC_HOST = 'localhost'

# Comunicacao com o servidor OPC
opc = OpenOPC.client()
opc.connect(OPC_SERVER, OPC_HOST)

STREAM_S6A = 'Streams.S6A'

while True:
  read = opc.read(STREAM_S6A)
  print(read)
  time.sleep(2)

  os.system('cls' if os.name=='nt' else 'clear')


