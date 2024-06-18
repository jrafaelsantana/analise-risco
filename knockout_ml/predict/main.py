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

MAX_LEVEL = 1.75
OP_CONCESSIONARIA_NAME = 'Variaveis.OP_CONCESSIONARIA'
H2O_QTD_NAME = 'Variaveis.H2O_QTD'

buffer = {
    'data': []
}

buffer_map = {
    'real': np.full(30, np.nan),
    'predicted': np.full(30, np.nan)
}

actual_op_concessionaria = 0

def manage_buffer(data, buffer):
    input_data = convert_to_df(data, TAGS_READ)

    if len(buffer['data']) == 0:
        buffer['data'] = input_data
    else:
        buffer['data'] = pd.concat([buffer['data'], input_data])
    
    buffer['data'] = buffer['data'].tail(30)
    return buffer

def predict_seconds(buffer_data, model, scaler):
    data = pd.DataFrame(buffer_data)
    data = data[FEATURES_SECONDS]

    input = convert_to_input(data, scaler, FEATURES_SECONDS)
    predict = model.predict(input).flatten()
    seconds = convert_to_seconds(predict, scaler, FEATURES_SECONDS)
    print("Faltam {} segundos para o trip".format(seconds))

    return seconds

def predict_seconds_test(buffer_predicted, buffer_real):
    predicted_valid = buffer_predicted[~np.isnan(buffer_predicted)]
    real_valid = buffer_real[~np.isnan(buffer_real)]

    left_level = MAX_LEVEL - real_valid[-1]
    growth_average = np.abs(np.mean(np.diff(predicted_valid)))

    seconds = left_level / growth_average

    return np.floor(seconds)

def predict_level(buffer_data, model, scaler):
    data = pd.DataFrame(buffer_data)
    data = data[FEATURES_LEVEL]

    input = convert_to_input(data, scaler, FEATURES_LEVEL)
    predict = model.predict(input).flatten()

    return predict


def close_connection(socket, context):
    socket.close()
    context.term()

def validar_entrada(P):
    if P.isdigit() or P == "":
        return True
    return False

def obter_valor():
    valor = entrada_segundos.get()
    if valor.isdigit():
        return int(valor)
    
    return None

def update_data():
    global buffer
    global buffer_map
    global actual_op_concessionaria

    try:
        message = socket.recv_pyobj()
        data = handle_message(message)
        print("Received request")

        buffer = manage_buffer(data, buffer)

        if ativar_ruido.get():
            print('Ativado novo valor {}'.format(ativar_ruido.get()))
            buffer['data'].at[buffer['data'].index[-1], 'Tubo.S6.W'] += 2000

        level_predicted = predict_level(buffer['data'], lstm_level_model, scaler_level)
        
        predicted_data_scaled = np.empty((level_predicted.shape[0], 50))
        predicted_data_scaled[:, -1] = level_predicted
        predicted_data_scaled = pd.DataFrame(predicted_data_scaled, columns=FEATURES_LEVEL + ['Label'])
        predicted_data_scaled.replace([np.inf, -np.inf], 0, inplace=True)
        predicted_data_scaled = scaler_level.inverse_transform(predicted_data_scaled)
        predicted_data_scaled = predicted_data_scaled[:, -1]

        buffer_map = convert_to_plot_data(buffer_map, buffer['data'], predicted_data_scaled)
    
        line_real.set_data(level_x_data, buffer_map['real'])
        line_predict.set_data(level_x_data, buffer_map['predicted'])

        seconds = predict_seconds_test(buffer_map['predicted'], buffer_map['real'])

        if seconds < 0:
            tempo_label_txt.set("Previsão de trip indisponível.")
        elif seconds > 1000:
            tempo_label_txt.set("Não há previsão para ocorrência de trip.")
        else:
            tempo_label_txt.set("Tempo para o trip: {} segundos".format(seconds or 0))

        segundos_max = obter_valor()
        last_drum_level = buffer['data'].at[buffer['data'].index[-1], 'Variaveis.VOTACAO_TRANSMISSORES']
        if segundos_max and segundos_max>= seconds and actual_op_concessionaria == 0:
            data_send = {}
            data_send[OP_CONCESSIONARIA_NAME] = 1
            data_send[H2O_QTD_NAME] = 0
            actual_op_concessionaria = 1
            socket.send_pyobj(data_send)
            
        elif segundos_max and last_drum_level <= 0.150 and actual_op_concessionaria == 1:
            data_send = {}
            data_send[OP_CONCESSIONARIA_NAME] = 0
            data_send[H2O_QTD_NAME] = 2.5
            actual_op_concessionaria = 0
            socket.send_pyobj(data_send)
        else:
            socket.send_pyobj(None)

        ax.relim()
        ax.autoscale_view()
        canvas.draw()

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
    lstm_level_model = tf.keras.models.load_model('../model/model_level.hdf5')

    print("Loading scalers...")
    scaler_level = joblib.load('../model/scaler_level.gz')

    level_x_data = list(range(-14, 16))

    # Cria tela
    root = tk.Tk()
    root.title("Vaso Knockout")
    root.resizable(False, False)
    vcmd = root.register(validar_entrada)

    # Configuração do gráfico do Matplotlib
    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    line_predict, = ax.plot(level_x_data, np.empty((len(level_x_data),)), color='green')
    line_real, = ax.plot(level_x_data, np.empty((len(level_x_data),)), color='blue')

    ax.axhline(y=MAX_LEVEL, color='red', linestyle='--')
    ax.axvline(x=0, color='black', linestyle='--')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    # Rótulo do tempo
    tempo_label_txt = tk.StringVar()
    tempo_label = Label(root, textvariable=tempo_label_txt)
    tempo_label.pack()

    # Checkbox para adicionar ruído na simulação
    ativar_ruido = tk.IntVar()
    checkbox = Checkbutton(root, text="Ruído", variable=ativar_ruido)
    checkbox.pack()

    # Label
    label_segundos = tk.Label(root, text="Segundos para Ativar Controle:")
    label_segundos.pack()

    # Campo de texto (Entry)
    entrada_segundos = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entrada_segundos.pack()

    update_data()

    root.mainloop()
