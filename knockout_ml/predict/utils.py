import pandas as pd
import numpy as np
from config import TAGS_READ
from exceptions import SocketClosedError

def convert_to_df(arr, columns_names):
  return pd.DataFrame(arr, columns=columns_names)

def convert_to_input(arr, scaler, columns_names):
  df = convert_to_df(arr, columns_names)
  df['Label'] = 0

  df_scaled = scale_values(df, scaler)
  df_scaled = df_scaled.drop('Label', axis=1)
  df_scaled = np.array([df_scaled])

  return df_scaled

def convert_to_seconds(arr, scaler, columns_names):
  new_array = np.zeros((1, 7))
  new_array[0, -1] = arr[0]
  new_array = pd.DataFrame(new_array, columns=columns_names + ['Label'])

  final_arr = scaler.inverse_transform(new_array)
  return round(final_arr[0, -1])

def convert_to_plot_data(real_data, buffer, predicted_data, scaler, columns_names):
  # Inverse scale
  real_data = convert_to_df(real_data, TAGS_READ)

  predicted_data_scaled = np.zeros((predicted_data.shape[0], 7))
  predicted_data_scaled[:, -1] = predicted_data[0]
  predicted_data_scaled = pd.DataFrame(predicted_data_scaled, columns=columns_names + ['Label'])
  predicted_data_scaled = scaler.inverse_transform(predicted_data_scaled)
  predicted_data_scaled = predicted_data_scaled[:, -1]

  if len(buffer["predicted"]) == 0 and len(buffer["real"]) == 0:
    # Inicio do plot
    buffer["real"] = real_data['Drum.V1.L'].tail(15).to_numpy()
    buffer["predicted"] = np.empty(30)
    buffer["predicted"][-15:] = predicted_data_scaled[15:]
  else:
    # Atualizacao do plot
    buffer["real"] = real_data['Drum.V1.L'].tail(15).to_numpy()
    buffer["predicted"] = np.append(buffer["predicted"], [0])
    buffer["predicted"][-15:] = predicted_data_scaled[15:]
    buffer["predicted"] = buffer["predicted"][-30:]

  print(buffer["real"])
  print(buffer["predicted"])
  print(buffer["real"].shape)
  print(buffer["predicted"].shape)
  print('-----------------------')

  return [], buffer

def scale_values(df, scaler):
  df_scaled = pd.DataFrame(
        scaler.transform(df),
        index=df.index,
        columns=df.columns)
  
  return df_scaled

def handle_message(message):
  if message == 'CLOSE_SOCKET':
    raise SocketClosedError()
  else:
    return message