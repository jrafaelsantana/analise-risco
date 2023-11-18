import pandas as pd
import numpy as np
from exceptions import SocketClosedError

def convert_to_df(arr, columns_names):
  return arredondar_dataframe(pd.DataFrame(arr, columns=columns_names))

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

def convert_to_plot_data(buffer_map, buffer_data, predicted_data_scaled):
  buffer_map["real"][:15] = buffer_data['Drum.V1.L'].tail(15).to_numpy()
  
  buffer_map["predicted"] = np.append(buffer_map["predicted"], np.nan)
  buffer_map["predicted"][-15:] = predicted_data_scaled
  buffer_map["predicted"] = buffer_map["predicted"][-30:]
  
  return buffer_map

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
  
def arredondar_dataframe(df, casas_decimais=5):
    return df.round(casas_decimais)