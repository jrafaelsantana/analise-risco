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
TR1_RUIDO = 'Variaveis.TR1_RUIDO'
TR2_RUIDO = 'Variaveis.TR2_RUIDO'
TR3_RUIDO = 'Variaveis.TR3_RUIDO'
H2O_QTD = 'Variaveis.H2O_QTD'

MAX_INPUT = 5.1
SHOULD_CONTROL = True

LIQUIDO_ATUAL = 2.1
ESTADO_ANTERIOR = 1.0
TAGS_READ = ['Valvula.VALVE_SHUTOFF.L']

def init_simulation():
  return ((H2O_QTD, LIQUIDO_ATUAL))

def control_h2o():
  return random.uniform(0.0, 2.0)

def control_ruido_1():
  if random.random() < 0.02:
    return 1
  return 0
  
def control_ruido_2():
  if random.random() < 0.02:
    return 1
  return 0
  
def control_ruido_3():
  if random.random() < 0.02:
    return 1
  return 0

def control_vazamento():
  if random.random() < 0.2:
    return 1
  return 0

try:
  opc.write(init_simulation())
  count_ruido = 0
  count_vazamento = 0
  count_h2o = 0

  while True:
    read = opc.read(TAGS_READ)
    valve_shutoff = [tag[1] for tag in read][0]
    data_send = {}

    if SHOULD_CONTROL:
      # Controle quantidade de liquido
      if valve_shutoff < 1 and ESTADO_ANTERIOR == 1.0:
        LIQUIDO_ATUAL = LIQUIDO_ATUAL + 0.5
        data_send[H2O_QTD] = LIQUIDO_ATUAL
        ESTADO_ANTERIOR = 0.0

      if valve_shutoff == 1 and ESTADO_ANTERIOR == 0:
        ESTADO_ANTERIOR = 1.0
      
      if LIQUIDO_ATUAL > MAX_INPUT:
        SHOULD_CONTROL = False
        LIQUIDO_ATUAL = 1.0
        data_send[H2O_QTD] = LIQUIDO_ATUAL
    else:
      if count_h2o == 20:
        data_send[H2O_QTD] = control_h2o()
        count_h2o = 0
      else:
        count_h2o = count_h2o + 1
    
    # Controle do ruido
    if count_ruido == 10:
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
