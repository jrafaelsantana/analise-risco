import tkinter as tk
import zmq
import tensorflow as tf
import joblib
import traceback
import numpy as np
import pandas as pd
from exceptions import SocketClosedError
from utils import convert_to_df, convert_to_input, convert_to_plot_data, convert_to_seconds, handle_message
from config import FEATURES_SECONDS, FEATURES_LEVEL, TAGS_READ
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Label, Entry, Checkbutton
from matplotlib.figure import Figure

buffer = {
    'data': [],
    'seconds': []
}

buffer_map = {
    'real': np.full(30, np.nan),
    'predicted': np.full(30, np.nan)
}

def manage_buffer(data, buffer):
    input_data = convert_to_df(data, TAGS_READ)

    if len(buffer['data']) == 0:
        buffer['data'] = input_data
    else:
        buffer['data'] = buffer['data'].iloc[:-14]
        buffer['data'] = pd.concat([buffer['data'], input_data])
    
    buffer['data'] = buffer['data'].tail(30)
    return buffer

def predict_seconds(data_read, model, scaler):
    data = pd.DataFrame(data_read)
    data = data[FEATURES_SECONDS].tail(15)
    input = convert_to_input(data, scaler, FEATURES_SECONDS)
    predict = model.predict(input).flatten()
    seconds = convert_to_seconds(predict, scaler, FEATURES_SECONDS)
    print("Faltam {} segundos para o trip".format(seconds))

    return seconds

def predict_level(buffer_data, model, scaler):
    data = pd.DataFrame(buffer_data)
    data = data[FEATURES_LEVEL]

    input = convert_to_input(data, scaler, FEATURES_LEVEL)
    predict = model.predict(input).flatten()

    return predict

def close_connection(socket, context):
    socket.close()
    context.term()

def update_data():
    global buffer
    global buffer_map

    try:
        message = socket.recv_pyobj()
        data = handle_message(message)
        print("Received request")

        buffer = manage_buffer(data, buffer)

        seconds = predict_seconds(buffer['data'], lstm_seconds_model, scaler_seconds)
        buffer['seconds'].append(seconds)
        buffer['seconds'] = buffer['seconds'][-30:]
        tempo_label_txt.set("Tempo para o trip: {} segundos".format(seconds or 0))

        if len(buffer['seconds']) == 30:
            level_predicted = predict_level(buffer['data'], lstm_level_model, scaler_level)
            
            predicted_data_scaled = np.empty((level_predicted.shape[0], 7))
            predicted_data_scaled[:, -1] = level_predicted
            predicted_data_scaled = pd.DataFrame(predicted_data_scaled, columns=FEATURES_LEVEL + ['Label'])
            predicted_data_scaled = scaler_level.inverse_transform(predicted_data_scaled)
            predicted_data_scaled = predicted_data_scaled[:, -1]

            buffer_map = convert_to_plot_data(buffer_map, buffer['data'], predicted_data_scaled)
        
            line_real.set_data(level_x_data, buffer_map['real'])
            line_predict.set_data(level_x_data, buffer_map['predicted'])

            ax.relim()
            ax.autoscale_view()
            canvas.draw()
        else:
            print('Ainda n eh possivel calcular o grafico. {} segundos no buffer'.format(len(buffer['seconds'])))

        socket.send(b"Ok")
        root.after(1000, update_data)
    except SocketClosedError:
        close_connection(socket, context)
        print("Killed.")
        exit()
    except:
        socket.send(b"CLOSE_SOCKET")
        traceback.print_exc()
        close_connection(socket, context)
        exit()

if __name__ == '__main__':
    print("Starting inferences models...")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Loading models...")
    lstm_seconds_model = tf.keras.models.load_model('../model/model_seconds.hdf5')
    lstm_level_model = tf.keras.models.load_model('../model/model_level.hdf5')

    print("Loading scalers...")
    scaler_seconds = joblib.load('../model/scaler_seconds.gz')
    scaler_level = joblib.load('../model/scaler_level.gz')

    level_x_data = list(range(-14, 16))

    # Cria tela
    root = tk.Tk()
    root.title("Vaso Knockout")
    root.resizable(False, False)

    # Configuração do gráfico do Matplotlib
    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    line_predict, = ax.plot(level_x_data, np.empty((len(level_x_data),)), color='green')
    line_real, = ax.plot(level_x_data, np.empty((len(level_x_data),)), color='blue')

    ax.axhline(y=0.700, color='red', linestyle='--')
    ax.axvline(x=0, color='black', linestyle='--')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    # Rótulo do tempo
    tempo_label_txt = tk.StringVar()
    tempo_label = Label(root, textvariable=tempo_label_txt)
    tempo_label.pack()

    # Entrada de quantidade de líquido
    input_liquido = Entry(root)
    input_liquido.pack()

    # Checkbox para controle automático
    ativar_controle = tk.IntVar()
    checkbox = Checkbutton(root, text="Controle automático", variable=ativar_controle)
    checkbox.pack()

    update_data()

    root.mainloop()
