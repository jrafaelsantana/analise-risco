import time
import zmq
import tensorflow as tf
import joblib
from exceptions import SocketClosedError
from utils import convert_to_input, convert_to_plot_data, convert_to_seconds, handle_message
from config import COLUMNS_NAMES_LEVEL, COLUMNS_NAMES_SECONDS

def predict_seconds(data, model, scaler):
    input = convert_to_input(data, scaler, COLUMNS_NAMES_SECONDS)
    predict = model.predict(input).flatten()
    seconds = convert_to_seconds(predict, scaler, COLUMNS_NAMES_SECONDS)

    return seconds

def predict_level(data, model, scaler):
    input = convert_to_input(data, scaler, COLUMNS_NAMES_LEVEL)
    predict = model.predict(input).flatten()
    plot_data = convert_to_plot_data(predict, scaler, COLUMNS_NAMES_LEVEL)

    return plot_data

def close_connection(socket, context):
    socket.close()
    context.term()

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

    while True:
        try:
            message = socket.recv_pyobj()
            data = handle_message(message)
            print("Received request")

            seconds = predict_seconds(data, lstm_seconds_model, scaler_seconds)
            level = predict_level(data, lstm_level_model, scaler_level)

            time.sleep(1)

            socket.send(b"Ok")
        except SocketClosedError:
            close_connection(socket, context)
            print("Killed.")
            exit()
        except:
            socket.send(b"CLOSE_SOCKET")
            close_connection(socket, context)
            exit()
