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

OP_VALVE_5 = 'Controllers.PV5.OP'
SP_VALVE_5 = 0

while True:
  opc.write((OP_VALVE_5, SP_VALVE_5))

  os.system('cls' if os.name=='nt' else 'clear')

  if SP_VALVE_5 is 0:
    print('Aperte enter para ativar a valvula')
    input()
    SP_VALVE_5 = 1
  else:
    print('Aperte enter para desativar a valvula')
    input()
    SP_VALVE_5 = 0

