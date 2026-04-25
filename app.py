import tkinter as tk

class App(tk.Tk):
    def __init__(self, minha_cpu):
        super().__init__()
        self.minha_cpu = minha_cpu
        self.title("Simulador Sergium")
