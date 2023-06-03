import OpenOPC
import pywintypes
import random
import time
import pandas as pd
import os
from datetime import datetime

pywintypes.datetime = pywintypes.TimeType

# Variaveis de configuracao
OPC_SERVER = 'Matrikon.OPC.Simulation'
OPC_HOST = 'localhost'
WAIT_SECONDS = 3.5
CSV_FILENAME = 'Logs 12-02-2023.csv'

# Comunicacao com o servidor OPC
opc = OpenOPC.client()
opc.connect(OPC_SERVER, OPC_HOST)

TAGS_READ = [
  'Sources.GTGA', 
  'Sources.GTGFA', 
  'Sources.GTGLOADA',
  'Controllers.PV5.OP',
  'Equipments.BURNA'
]

# Variaveis para escrita
POSSIBLE_VALVE_5_VALUES = [0.0, 0.25, 0.5, 0.75, 1.0]
OP_VALVE_5 = 'Controllers.PV5.OP'
SP_VALVE_5 = 0

GTGLOADA = 'Sources.GTGLOADA'
GTGLOADA_VALUE = 0

opc.write(((OP_VALVE_5, SP_VALVE_5), (GTGLOADA, GTGLOADA_VALUE)))
interation = 0
file_exists = os.path.exists(CSV_FILENAME)

while True:
  # Escreve valores na simulacao
  SP_VALVE_5 = POSSIBLE_VALVE_5_VALUES[random.randint(0, 4)]
  GTGLOADA_VALUE = random.randint(0,100)

  opc.write(((OP_VALVE_5, SP_VALVE_5), (GTGLOADA, GTGLOADA_VALUE)))
  
  print(f'{interation} \t PV5.OP \t {SP_VALVE_5} \t GTGLOADA \t {GTGLOADA_VALUE}')
  time.sleep(WAIT_SECONDS)

  # Salva resultados no CSV
  date = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
  data = [date]

  for tag in TAGS_READ:
    read = opc.read(tag)
    data.append(read[0])

  df = pd.DataFrame([data], columns=['Datetime'] + TAGS_READ)
  df.to_csv(CSV_FILENAME, mode='a', header=not file_exists and interation == 0, index=False)

  interation += 1
