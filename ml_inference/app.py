import os
import joblib
from sklearn.preprocessing import MinMaxScaler
import torch
import numpy as np
import pandas as pd
from pymongo import MongoClient
from models.liquid_level.model import LiquidLevelNet
from models.vazamento.model import VazamentoNet
from pathlib import Path
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')

app = Flask(__name__)
mongoClient = MongoClient(MONGODB_URI)
sensorDataDb = mongoClient.sensor_data
historicTable = sensorDataDb.historic

liquid_level_model = LiquidLevelNet(51)  # TODO: Refactor to pass num_features
liquid_level_model.load_state_dict(torch.load(Path('./models/liquid_level', 'model.pt')))
liquid_level_model.eval()
liquid_level_scaler = joblib.load(Path('./models/liquid_level', 'scaler.gz'))

vazamento_model = VazamentoNet(51)  # TODO: Refactor to pass num_features
vazamento_model.load_state_dict(torch.load(Path('./models/vazamento', 'model.pt')))
vazamento_model.eval()
vazamento_scaler = joblib.load(Path('./models/vazamento', 'scaler.gz'))

liquid_level_blocked_features = [
    'Drum.V1.VOL',
    'Valvula.VALVE_SHUTOFF.CL',
    'Valvula.VALVE_SHUTOFF.DP',
    'Valvula.VALVE_SHUTOFF.OP',
    'Variaveis.TR1_RUIDO',
    'Variaveis.TR2_RUIDO',
    'Variaveis.TR3_RUIDO',
    'Tubo.S25.T',
    'Tubo.S25.P',
    'Tubo.S25.W',
    'Tubo.S2.P',
    'Valvula.VALVE4.CL',
    'Valvula.VALVE4.OP',
    'StreamSend.SAIDA_LIQUIDO.P',
    'Variaveis.VOTACAO_TRANSMISSORES'
]

liquid_level_blocked_features_old = [
  'Drum.V1.VOL',
  'Valvula.VALVE_SHUTOFF.CL',
  'Valvula.VALVE_SHUTOFF.DP',
  'Valvula.VALVE_SHUTOFF.OP',
  'Variaveis.TR1_RUIDO',
  'Variaveis.TR2_RUIDO',
  'Variaveis.TR3_RUIDO',
  'Tubo.S6.T',
  'Tubo.S6.P',
  'Tubo.S6.W',
  'Tubo.S25.T',
  'Tubo.S25.P',
  'Tubo.S25.W',
  'Valvula.VALVE4.CL',
  'Valvula.VALVE4.OP',
  'StreamSend.SAIDA_LIQUIDO.P'
]

vazamento_blocked_features = [
  'Drum.V1.VOL',
  'Valvula.VALVE_SHUTOFF.CL',
  'Valvula.VALVE_SHUTOFF.DP',
  'Valvula.VALVE_SHUTOFF.OP',
  'Variaveis.TR1_RUIDO',
  'Variaveis.TR2_RUIDO',
  'Variaveis.TR3_RUIDO',
  'Tubo.S25.T',
  'Tubo.S25.P',
  'Tubo.S25.W',
  'Valvula.VALVE5.CL',
  'Valvula.VALVE5.OP',
  'Tubo.S28.T',
  'Tubo.S28.P',
  'Tubo.S28.W',
]

@app.route('/liquid_level', methods=['GET'])
def predict_liquid_level():
  lastRecord = historicTable.find().sort('_id', -1 ).limit(1)
  list_record = list(lastRecord)

  df = pd.DataFrame(list_record)
  df = df.drop('_id', axis=1)
  df = df.drop('Datetime', axis=1)
  df = df.drop(liquid_level_blocked_features, axis=1)
  
  df['Target'] = 0
  df = pd.DataFrame(liquid_level_scaler.transform(df), index=df.index, columns=df.columns)
  df = df.drop('Target', axis=1)
  
  features = torch.Tensor(np.array(df))
  output = liquid_level_model(features)
    
  return jsonify({'probability': output.item()})

@app.route('/vazamento', methods=['GET'])
def predict_vazamento():
  lastRecord = historicTable.find().sort('_id', -1 ).limit(1)
  list_record = list(lastRecord)
  print(list_record)

  df = pd.DataFrame(list_record)
  df = df.drop('_id', axis=1)
  df = df.drop('Datetime', axis=1)
  df = df.drop(vazamento_blocked_features, axis=1)
  
  df['Label'] = 0
  df = pd.DataFrame(vazamento_scaler.transform(df), index=df.index, columns=df.columns)
  df = df.drop('Label', axis=1)
  
  features = torch.Tensor(np.array(df))
  output = vazamento_model(features)
    
  return jsonify({'probability': output.item(), 'class': np.around(output.item())})


if __name__ == '__main__':
  app.run()