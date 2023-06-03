import pywintypes
import time
import pandas as pd
import config
import utils
import os
from datetime import datetime

pywintypes.datetime = pywintypes.TimeType

opc = utils.connectOpc(config.OPC_SERVER, config.OPC_HOST)
TIME_START = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
file_exists = os.path.exists(config.CSV_FILENAME)
interation = 0

try:
  while True:
    utils.cls()
    utils.printInfos(interation, TIME_START)

    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
    read = opc.read(config.TAGS_READ)
    data = [tag[1] for tag in read]
    data.insert(0, date)

    df = pd.DataFrame([data], columns=['Datetime'] + config.TAGS_READ)
    df_json = df.to_json(orient='records')
    message_id = utils.publishMessageToSns(config.ARN_TOPIC, config.AWS_REGION_NAME, df_json)
    
    interation = interation + 1

    time.sleep(config.READ_SECONDS)
except KeyboardInterrupt:
  print("Programa finalizado")
