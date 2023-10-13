import os
import joblib
import torch
import numpy as np
import pandas as pd
from pymongo import MongoClient
from models.liquid_level.model import LiquidLevelNet
from models.vazamento.model import VazamentoNet
from pathlib import Path
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime, timedelta
import json
from bson import ObjectId

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

mongoClient = MongoClient(MONGODB_URI)
sensorDataDb = mongoClient.sensor_data
historicTable = sensorDataDb.historic
alertTable = sensorDataDb.alerts

liquid_level_model = LiquidLevelNet(66)  # TODO: Refactor to pass num_features
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

def serialize_obj(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(repr(obj) + " is not JSON serializable")

@app.route('/liquid_level', methods=['GET'])
def predict_liquid_level():
  lastRecord = historicTable.find().sort('_id', -1 ).limit(1)
  list_record = list(lastRecord)

  df = pd.DataFrame(list_record)
  datetime = df['Datetime'][0]

  df = df.drop('_id', axis=1)
  df = df.drop('Datetime', axis=1)
  #df = df.drop(liquid_level_blocked_features, axis=1)
  
  df['Target'] = 0
  df = pd.DataFrame(liquid_level_scaler.transform(df), index=df.index, columns=df.columns)
  df = df.drop('Target', axis=1)
  
  features = torch.Tensor(np.array(df))
  output = liquid_level_model(features)
    
  return jsonify({
    'datetime': datetime,
    'probability': output.item()
  })

@app.route('/vazamento', methods=['GET'])
def predict_vazamento():
  lastRecord = historicTable.find().sort('_id', -1 ).limit(1)
  list_record = list(lastRecord)

  df = pd.DataFrame(list_record)
  datetime = df['Datetime'][0]

  df = df.drop('_id', axis=1)
  df = df.drop('Datetime', axis=1)
  df = df.drop(vazamento_blocked_features, axis=1)
  
  df['Label'] = 0
  df = pd.DataFrame(vazamento_scaler.transform(df), index=df.index, columns=df.columns)
  df = df.drop('Label', axis=1)
  
  features = torch.Tensor(np.array(df))
  output = vazamento_model(features)
    
  return jsonify({
    'datetime': datetime, 
    'probability': output.item(), 
    'class': np.around(output.item())
  })

@app.route('/alerts', methods=['GET'])
def alerts():
  limite_tempo = datetime.now() - timedelta(hours=1)
  query = {"lastViewed": {"$gt": limite_tempo}}

  lastRecords = alertTable.find(query).sort('lastViewed', -1 ).limit(5)
  listLastRecords = list(lastRecords)
  jsonListLastRecords = json.dumps(listLastRecords, default=serialize_obj)

  print(jsonListLastRecords)
    
  return { "alerts": json.loads(jsonListLastRecords) }

if __name__ == '__main__':
  app.run()