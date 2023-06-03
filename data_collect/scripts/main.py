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
READ_SECONDS = 1
CSV_FILENAME = 'Logs 13-05-2023-2.csv'
TAGS_READ = [
  'Controlador.PC1.OUT',
  'Drum.V1.L',
  'Drum.V1.P',
  'Drum.V1.T',
  'Drum.V1.VOL',
  'Source.SRC1.PB',
  'StreamSend.FLARE.P',
  'StreamSend.SAIDA_GAS.P',
  'StreamSend.SAIDA_LIQUIDO.P',
  'Transmissor.TR1.OUT',
  'Transmissor.TR2.OUT',
  'Transmissor.TR3.OUT',
  'Tubo.S1.P',
  'Tubo.S1.T',
  'Tubo.S1.W',
  'Tubo.S10.P',
  'Tubo.S10.T',
  'Tubo.S10.W',
  'Tubo.S2.P',
  'Tubo.S2.T',
  'Tubo.S2.W',
  'Tubo.S25.P',
  'Tubo.S25.T',
  'Tubo.S25.W',
  'Tubo.S26.P',
  'Tubo.S26.T',
  'Tubo.S26.W',
  'Tubo.S27.P',
  'Tubo.S27.T',
  'Tubo.S27.W',
  'Tubo.S28.P',
  'Tubo.S28.T',
  'Tubo.S28.W',
  'Tubo.S3.P',
  'Tubo.S3.T',
  'Tubo.S3.W',
  'Tubo.S4.P',
  'Tubo.S4.T',
  'Tubo.S4.W',
  'Tubo.S5.P',
  'Tubo.S5.T',
  'Tubo.S5.W',
  'Tubo.S6.P',
  'Tubo.S6.T',
  'Tubo.S6.W',
  'Valvula.VALVE1.CL',
  'Valvula.VALVE1.OP',
  'Valvula.VALVE1.STOP',
  'Valvula.VALVE1.DP',
  'Valvula.VALVE2.CL',
  'Valvula.VALVE2.OP',
  'Valvula.VALVE2.DP',
  'Valvula.VALVE3.OP',
  'Valvula.VALVE3.DP',
  'Valvula.VALVE4.CL',
  'Valvula.VALVE4.OP',
  'Valvula.VALVE5.CL',
  'Valvula.VALVE5.OP',
  'Valvula.VALVE5.DP',
  'Valvula.VALVE_SHUTOFF.CL',
  'Valvula.VALVE_SHUTOFF.OP',
  'Valvula.VALVE_SHUTOFF.DP'
]

# Codigo das cores das mensagens do terminal
COLOR_RED = '\033[91m'
COLOR_BLUE = '\033[94m'
COLOR_WARN = '\033[93m'
COLOR_RST = '\033[0m'

# Comunicacao com o servidor OPC
opc = OpenOPC.client()
opc.connect(OPC_SERVER, OPC_HOST)

TIME_START = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
interation = 0

# Verifica se o arquivo ja existe
file_exists = os.path.exists(CSV_FILENAME)
if file_exists:
  print(COLOR_RED + "Aviso: Já existe um arquivo chamado " + CSV_FILENAME + COLOR_RST)
  print(COLOR_WARN + "Se você continuar a execução, os novos dados serão adicionados ao final do arquivo." + COLOR_RST)
  print()
  print('Você deseja continuar? [S/n]')
  
  choice = input()

  if choice.lower() == 'n':
    raise SystemExit

# Funcoes auxiliares
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def printInfos():
  print(COLOR_BLUE + "Captura iniciada as: " + TIME_START)
  print(str(interation) + ' novas linhas salvas.')

# Leitura dos dados
try:
  while True:
    cls()
    printInfos()
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]

    read = opc.read(TAGS_READ)
    data = [tag[1] for tag in read]
    data.insert(0, date)

    df = pd.DataFrame([data], columns=['Datetime'] + TAGS_READ)
    df.to_csv(CSV_FILENAME, mode='a', header=not file_exists and interation == 0, index=False)
    interation = interation + 1

    time.sleep(READ_SECONDS)
except KeyboardInterrupt:
  print(COLOR_WARN + "Programa finalizado" + COLOR_RST)
