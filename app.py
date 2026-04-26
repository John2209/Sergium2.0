import tkinter as tk

class App(tk.Tk):

    def __init__(self, minha_cpu):      ## Inicializa a classe App

        super().__init__()              # Inicializa a classe Tk
        self.minha_cpu = minha_cpu      # Guarda referência da CPU
        self.title("Sergium 2.0")       # Define o título da janela
