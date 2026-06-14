# Ponto de entrada da interface gráfica
# Inicialização da aplicação

import customtkinter as ctk
from tkinter import ttk  # Vamos usar no futuro para Treeview: instruções, registradores e memória.

class App(ctk.CTk):

    def __init__(self, minha_cpu):
        super().__init__()

        self.minha_cpu = minha_cpu

        self.configurar_janela()
        self.criar_widgets()
        self.configurar_layout()

    def configurar_janela(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Sergium 2.0")
        self.geometry("1200x700")
        self.minsize(900, 500)

        # A linha 1 é a área principal; ela deve crescer quando a janela crescer.
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        # =========================
        # Containers principais
        # =========================
        self.toolbar = ctk.CTkFrame(self, corner_radius=12)
        self.area_principal = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.painel_lateral = ctk.CTkFrame(self.area_principal, corner_radius=0, fg_color="transparent")

        # =========================
        # Botões da toolbar
        # =========================
        self.botao_abrir = ctk.CTkButton(self.toolbar, text="Abrir", width=80, corner_radius=8)
        self.botao_salvar = ctk.CTkButton(self.toolbar, text="Salvar", width=80, corner_radius=8)
        self.botao_montar = ctk.CTkButton(self.toolbar, text="Montar", width=80, corner_radius=8)
        self.botao_run = ctk.CTkButton(self.toolbar, text="Run", width=80, corner_radius=8)
        self.botao_step = ctk.CTkButton(self.toolbar, text="Step", width=80, corner_radius=8)
        self.botao_reset = ctk.CTkButton(self.toolbar, text="Reset", width=80, corner_radius=8)

        # =========================
        # Cards principais
        # =========================
        self.painel_editor = ctk.CTkFrame(self.area_principal, corner_radius=12)
        self.titulo_editor = ctk.CTkLabel(self.painel_editor, text="Editor", font=("Segoe UI", 14, "bold"))

        self.painel_instrucoes = ctk.CTkFrame(self.painel_lateral, corner_radius=12)
        self.titulo_instrucoes = ctk.CTkLabel(self.painel_instrucoes, text="Instruções", font=("Segoe UI", 14, "bold"))

        self.painel_registradores = ctk.CTkFrame(self.painel_lateral, corner_radius=12)
        self.titulo_registradores = ctk.CTkLabel(self.painel_registradores, text="Registradores", font=("Segoe UI", 14, "bold"))

        self.painel_memoria = ctk.CTkFrame(self.painel_lateral, corner_radius=12)
        self.titulo_memoria = ctk.CTkLabel(self.painel_memoria, text="Memória", font=("Segoe UI", 14, "bold"))

        self.painel_terminal = ctk.CTkFrame(self, corner_radius=12)
        self.titulo_terminal = ctk.CTkLabel(self.painel_terminal, text="Terminal", font=("Segoe UI", 14, "bold"))

        # =========================
        # Placeholders temporários
        # =========================
        self.label_editor = ctk.CTkLabel(self.painel_editor, text="Editor ficará aqui")
        self.label_instrucoes = ctk.CTkLabel(self.painel_instrucoes, text="Tabela de instruções ficará aqui")
        self.label_registradores = ctk.CTkLabel(self.painel_registradores, text="Registradores ficarão aqui")
        self.label_memoria = ctk.CTkLabel(self.painel_memoria, text="Memória ficará aqui")
        self.label_terminal = ctk.CTkLabel(self.painel_terminal, text="Erros e logs aparecerão aqui")

    def configurar_layout(self):
        # =========================
        # Layout geral da janela
        # =========================
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        self.area_principal.grid(row=1, column=0, sticky="nsew", padx=8)
        self.painel_terminal.grid(row=2, column=0, sticky="ew", padx=8, pady=8)

        # =========================
        # Layout da toolbar
        # =========================
        self.botao_abrir.grid(row=0, column=0, padx=4, pady=8)
        self.botao_salvar.grid(row=0, column=1, padx=4, pady=8)
        self.botao_montar.grid(row=0, column=2, padx=4, pady=8)
        self.botao_run.grid(row=0, column=3, padx=4, pady=8)
        self.botao_step.grid(row=0, column=4, padx=4, pady=8)
        self.botao_reset.grid(row=0, column=5, padx=4, pady=8)

        # =========================
        # Layout da área principal
        # =========================
        self.area_principal.grid_rowconfigure(0, weight=1)
        self.area_principal.grid_columnconfigure(0, weight=3)
        self.area_principal.grid_columnconfigure(1, weight=2)

        self.painel_editor.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.painel_lateral.grid(row=0, column=1, sticky="nsew")

        # =========================
        # Layout do painel lateral
        # =========================
        self.painel_lateral.grid_rowconfigure(0, weight=2)
        self.painel_lateral.grid_rowconfigure(1, weight=1)
        self.painel_lateral.grid_rowconfigure(2, weight=2)
        self.painel_lateral.grid_columnconfigure(0, weight=1)

        self.painel_instrucoes.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        self.painel_registradores.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        self.painel_memoria.grid(row=2, column=0, sticky="nsew")

        # =========================
        # Layout interno dos cards
        # =========================
        self.configurar_card(self.painel_editor, self.titulo_editor, self.label_editor)
        self.configurar_card(self.painel_instrucoes, self.titulo_instrucoes, self.label_instrucoes)
        self.configurar_card(self.painel_registradores, self.titulo_registradores, self.label_registradores)
        self.configurar_card(self.painel_memoria, self.titulo_memoria, self.label_memoria)
        self.configurar_card(self.painel_terminal, self.titulo_terminal, self.label_terminal, terminal=True)

    def configurar_card(self, painel, titulo, conteudo, terminal=False):
        painel.grid_rowconfigure(1, weight=1)
        painel.grid_columnconfigure(0, weight=1)

        titulo.grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))

        if terminal:
            conteudo.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))
        else:
            conteudo.grid(row=1, column=0, padx=16, pady=16)
