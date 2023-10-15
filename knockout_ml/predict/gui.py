import tkinter as tk
from tkinter import Label, Entry, Checkbutton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# Função para atualizar o tempo restante
def atualizar_tempo():
    tempo_restante = int(input_lquido.get()) if ativar_controle.get() else 0
    tempo_label.config(text=f"Tempo para o trip: {tempo_restante} segundos")
    root.after(1000, atualizar_tempo)

# Configuração da janela principal
root = tk.Tk()
root.title("Vaso Knockout")

# Configuração do gráfico do Matplotlib
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Rótulo do tempo
tempo_label = Label(root, text="Tempo para o trip: 0 segundos")
tempo_label.pack()

# Entrada de quantidade de líquido
input_lquido = Entry(root)
input_lquido.pack()

# Checkbox para controle automático
ativar_controle = tk.IntVar()
checkbox = Checkbutton(root, text="Controle automático", variable=ativar_controle)
checkbox.pack()

# Iniciar a atualização do tempo
atualizar_tempo()

root.mainloop()
