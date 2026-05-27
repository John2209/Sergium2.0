# Ponto de entrada da interface gráfica
# Inicialização da aplicação

import tkinter as tk
from tkinter import ttk

class App(tk.Tk):

    def __init__(self, minha_cpu):      ## Inicializa a classe App
        super().__init__()              # Inicializa a classe Tk

        self.minha_cpu = minha_cpu

        self.configurar_janela()
        self.criar_widgets()
        self.configurar_layout()

    def configurar_janela(self):
        self.title("Sergium 2.0")
        self.geometry("1200x700")
        self.minsize(900, 500)

        # Permite que a linha 1 e a coluna 0 cresçam quando a janela for redimensionada.
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        # Barra superior de botões.
        self.toolbar = ttk.Frame(self)

        self.botao_abrir = ttk.Button(self.toolbar, text="Abrir")
        self.botao_salvar = ttk.Button(self.toolbar, text="Salvar")
        self.botao_montar = ttk.Button(self.toolbar, text="Montar")
        self.botao_run = ttk.Button(self.toolbar, text="Run")
        self.botao_step = ttk.Button(self.toolbar, text="Step")
        self.botao_reset = ttk.Button(self.toolbar, text="Reset")

        # Área principal da interface.
        self.area_principal = ttk.Frame(self)

        self.painel_editor = ttk.LabelFrame(self.area_principal, text="Editor")
        self.painel_lateral = ttk.Frame(self.area_principal)

        self.painel_instrucoes = ttk.LabelFrame(self.painel_lateral, text="Instruções")
        self.painel_registradores = ttk.LabelFrame(self.painel_lateral, text="Registradores")
        self.painel_memoria = ttk.LabelFrame(self.painel_lateral, text="Memória")

        # Terminal inferior.
        self.painel_terminal = ttk.LabelFrame(self, text="Terminal")

        # Placeholders temporários.
        self.label_editor = ttk.Label(self.painel_editor, text="Editor ficará aqui")
        self.label_instrucoes = ttk.Label(self.painel_instrucoes, text="Tabela de instruções ficará aqui")
        self.label_registradores = ttk.Label(self.painel_registradores, text="Registradores ficarão aqui")
        self.label_memoria = ttk.Label(self.painel_memoria, text="Memória ficará aqui")
        self.label_terminal = ttk.Label(self.painel_terminal, text="Erros e logs aparecerão aqui")

    def configurar_layout(self):
        # Layout geral da janela.
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        self.area_principal.grid(row=1, column=0, sticky="nsew", padx=8)
        self.painel_terminal.grid(row=2, column=0, sticky="ew", padx=8, pady=8)

        # Layout da toolbar.
        self.botao_abrir.grid(row=0, column=0, padx=4)
        self.botao_salvar.grid(row=0, column=1, padx=4)
        self.botao_montar.grid(row=0, column=2, padx=4)
        self.botao_run.grid(row=0, column=3, padx=4)
        self.botao_step.grid(row=0, column=4, padx=4)
        self.botao_reset.grid(row=0, column=5, padx=4)

        # Faz a área principal crescer.
        self.area_principal.grid_rowconfigure(0, weight=1)
        self.area_principal.grid_columnconfigure(0, weight=3)
        self.area_principal.grid_columnconfigure(1, weight=2)

        self.painel_editor.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.painel_lateral.grid(row=0, column=1, sticky="nsew")

        # Layout lateral.
        self.painel_lateral.grid_rowconfigure(0, weight=2)
        self.painel_lateral.grid_rowconfigure(1, weight=1)
        self.painel_lateral.grid_rowconfigure(2, weight=2)
        self.painel_lateral.grid_columnconfigure(0, weight=1)

        self.painel_instrucoes.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        self.painel_registradores.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        self.painel_memoria.grid(row=2, column=0, sticky="nsew")

        # Placeholders.
        self.label_editor.grid(row=0, column=0, padx=16, pady=16)
        self.label_instrucoes.grid(row=0, column=0, padx=16, pady=16)
        self.label_registradores.grid(row=0, column=0, padx=16, pady=16)
        self.label_memoria.grid(row=0, column=0, padx=16, pady=16)
        self.label_terminal.grid(row=0, column=0, padx=16, pady=16)