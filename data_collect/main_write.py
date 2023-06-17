import pywintypes
import time
import config
import utils
import random
from datetime import datetime

pywintypes.datetime = pywintypes.TimeType

opc = utils.connectOpc(config.OPC_SERVER, config.OPC_HOST)
TIME_START = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
interation = 0

VALVE5_OP = 'Valvula.VALVE5.OP' # Vazamento
VALVE1_OP = 'Valvula.VALVE1.OP' # Entrada
VALVE2_OP = 'Valvula.VALVE2.OP' # Saida
TR1_RUIDO = 'Variaveis.TR1_RUIDO'
TR2_RUIDO = 'Variaveis.TR2_RUIDO'
TR3_RUIDO = 'Variaveis.TR3_RUIDO'
VOTACAO_TRANSMISSORES = 'Variaveis.VOTACAO_TRANSMISSORES'

def init_simulation():
  return (
    (VALVE1_OP, 1.0),
    (VALVE2_OP, 1.0)
  )

def has_noise(tr1, tr2, tr3):
  arr = [tr1, tr2, tr3]
  
  if arr.count(1) >= 2:
    return True
  return False

def control_valve1_op():
  if random.random() < 0.7:
    op = 1.00
  else:
    op = round(random.random(), 2)
  return op

def control_valve2_op():
  if random.random() < 0.7:
    op = 1.00
  else:
    op = round(random.random(), 2)
  return op

def control_ruido_1():
  if random.random() < 0.15:
    return 1
  return 0
  
def control_ruido_2():
  if random.random() < 0.15:
    return 1
  return 0
  
def control_ruido_3():
  if random.random() < 0.15:
    return 1
  return 0

def control_vazamento():
  if random.random() < 0.10:
    return 1
  return 0

try:
  opc.write(init_simulation())
  count_valve1 = 0
  count_valve2 = 0
  count_ruido = 0
  count_vazamento = 0

  while True:
    data_send = {}

    # Controle da valvula de entrada de gas
    if count_valve1 == 100:
      data_valve1 = control_valve1_op()
      data_send[VALVE1_OP] = data_valve1
      count_valve1 = 0
    else:
      count_valve1 = count_valve1 + 1

    # Controle da valvula de saida de gas
    if count_valve2 == 10:
      data_valve2 = control_valve2_op()
      data_send[VALVE2_OP] = data_valve2
      count_valve2 = 0
    else:
      count_valve2 = count_valve2 + 1

    # Controle do ruido
    if count_ruido == 5:
      data_send[TR1_RUIDO] = control_ruido_1()
      data_send[TR2_RUIDO] = control_ruido_2()
      data_send[TR3_RUIDO] = control_ruido_3()
      count_ruido = 0
    else:
      count_ruido = count_ruido + 1

    # Controle do vazamento
    if count_vazamento == 10:
      data_send[VALVE5_OP] = control_vazamento()
      count_vazamento = 0
    else:
      count_vazamento = count_vazamento + 1

    if len(data_send.items()):
      data_tuple = tuple(data_send.items())
      print(data_tuple)
      opc.write(data_tuple)
    
    interation = interation + 1
    time.sleep(config.READ_SECONDS)

except KeyboardInterrupt:
  print("Programa finalizado")
