import time
import zmq
import tensorflow as tf
import joblib
from utils import convert_to_input, convert_to_seconds

print("Starting inference model...")
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Loading model...")
lstm_model = tf.keras.models.load_model('../model/model.hdf5')

print("Loading scaler...")
scaler = joblib.load('../model/scaler.gz')

while True:
    message = socket.recv_pyobj()
    print("Received request")

    input = convert_to_input(message, scaler)
    predict = lstm_model.predict(input).flatten()
    seconds = convert_to_seconds(predict, scaler)

    print(seconds)
    time.sleep(1)

    socket.send(b"Ok")