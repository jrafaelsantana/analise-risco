import random
import tkinter as tk
from tkinter import Label, Entry, Checkbutton
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

x_data, y_data = [], []

# Função para atualizar o tempo restante
def update_plot():
    x_data.append(len(x_data))
    y_data.append(random.randint(0, 100))
    line.set_data(x_data, y_data)
    ax.relim()
    ax.autoscale_view()
    canvas.draw()
    root.after(1000, update_plot)

# Configuração da janela principal
root = tk.Tk()
root.title("Vaso Knockout")
root.resizable(False, False)

# Configuração do gráfico do Matplotlib
fig = Figure(figsize=(6, 4))
ax = fig.add_subplot(111)
line, = ax.plot(x_data, y_data)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Rótulo do tempo
tempo_label = Label(root, text="Tempo para o trip: 0 segundos")
tempo_label.pack()

# Entrada de quantidade de líquido
input_liquido = Entry(root)
input_liquido.pack()

# Checkbox para controle automático
ativar_controle = tk.IntVar()
checkbox = Checkbutton(root, text="Controle automático", variable=ativar_controle)
checkbox.pack()

update_plot()

root.mainloop()
