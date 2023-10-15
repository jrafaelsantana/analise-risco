import pandas as pd
import numpy as np
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