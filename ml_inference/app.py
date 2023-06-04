import os
import torch
import numpy as np
import pandas as pd
from pymongo import MongoClient
from models.liquid_level.model import NeuralNet
from pathlib import Path
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')

app = Flask(__name__)
mongoClient = MongoClient(MONGODB_URI)
sensorDataDb = mongoClient.sensor_data
historicTable = sensorDataDb.historic

liquid_level_model = NeuralNet()
liquid_level_model.load_state_dict(torch.load(Path('./models/liquid_level', 'model.pt')))
liquid_level_model.eval()


@app.route('/liquid_level', methods=['GET'])
def predict_liquid_level():
  lastRecord = historicTable.find().sort('_id', -1 ).limit(1)
  list_record = list(lastRecord)

  df = pd.DataFrame(list_record)
  df = df.drop('_id', axis=1)
  df = df.drop('Datetime', axis=1)
  
  features = torch.Tensor(np.array(df))
  output = liquid_level_model(features)
    
  return jsonify({'probability': output.item(), 'class': np.around(output.item())})


if __name__ == '__main__':
  app.run()