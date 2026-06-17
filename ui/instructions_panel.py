# define a tabela de instruções
# mostra rótulo, mnemônico, operando

import customtkinter as ctk
from tkinter import ttk

_ESTILO_APLICADO = False  # garante que o estilo ttk só é aplicado uma vez

def _aplicar_estilo_treeview():  # aplica o estilo visual usado pela tabela
    global _ESTILO_APLICADO
    if _ESTILO_APLICADO:
        return

    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "Sergium.Treeview",
        background="#1e1e1e",
        foreground="#e0e0e0",
        fieldbackground="#1e1e1e",
        rowheight=21,
        font=("Courier New", 10),
        borderwidth=0,
    )
    style.configure(
        "Sergium.Treeview.Heading",
        background="#2a2a2a",
        foreground="#9AA0A6",
        font=("Segoe UI", 9, "bold"),
        relief="flat",
    )
    style.map(
        "Sergium.Treeview",
        background=[("selected", "#2a4a7f")],
        foreground=[("selected", "#ffffff")],
    )

    _ESTILO_APLICADO = True  # marca o estilo como configurado


class InstructionsPanel(ctk.CTkFrame):

    def __init__(self, master, **kwargs):  # inicializa o painel de instruções
        super().__init__(master, **kwargs)
        _aplicar_estilo_treeview()
        self._item_atual = None     # id do item destacado no momento
        self._criar_widgets()       # cria a tabela e a barra de rolagem
        self._configurar_layout()   # posiciona os elementos na grade


    def _criar_widgets(self):
        self.titulo = ctk.CTkLabel(self, text="Instruções", font=("Segoe UI", 14, "bold"))

        self.tree = ttk.Treeview(
            self,
            style="Sergium.Treeview",
            columns=("rotulo", "mnemonico", "operando"),
            show="headings",
            selectmode="none",
        )

        self.tree.heading("rotulo",    text="Rótulo")
        self.tree.heading("mnemonico", text="Mnemônico")
        self.tree.heading("operando",  text="Operando")

        self.tree.column("rotulo", width=62, minwidth=55, anchor="center", stretch=False)
        self.tree.column("mnemonico", width=200, minwidth=100, anchor="w", stretch=True)
        self.tree.column("operando", width=62, minwidth=55, anchor="center", stretch=False)

        # tag para a instrução apontada pelo pc
        self.tree.tag_configure("atual", background="#1a3a6a", foreground="#ffffff")

        self.scrollbar = ctk.CTkScrollbar(self, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.bind("<Configure>", self._redistribuir_colunas)


    def _configurar_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(8, 4))
        self.tree.grid(row=1, column=0, sticky="nsew", padx=(12, 0), pady=(0, 10))
        self.scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 8), pady=(0, 10))

    # ===============
    # api
    # ==============
    def carregar(self, instrucoes: dict):
        # preenche a tabela com o programa montado.
        # instrucoes: dicionário {rótulo: (mnemonico, operando)} igual ao que a cpu usa.
        self._limpar()
        for rotulo, (mnemonico, operando) in instrucoes.items():
            self.tree.insert("", "end", iid=rotulo, values=(rotulo, mnemonico, operando))  # adiciona uma linha por instrução


    def atualizar(self, snapshot):
        # destaca a linha apontada pelo pc atual
        # remove destaque anterior
        if self._item_atual and self.tree.exists(self._item_atual):
            self.tree.item(self._item_atual, tags=())

        rotulo = snapshot.rotulo_atual  # rótulo da instrução atual no snapshot
        if rotulo and self.tree.exists(rotulo):
            self.tree.item(rotulo, tags=("atual",))
            self.tree.see(rotulo)   # rola para manter a linha visível
            self._item_atual = rotulo
        else:
            self._item_atual = None


    def resetar(self):
        # limpa a tabela e remove destaques
        self._limpar()

    # =============================================
    # interno
    # =============================================
    def _redistribuir_colunas(self, event=None):
        largura_total = self.tree.winfo_width()  # largura real da tabela
        largura_fixa  = 70 + 70     # rotulo + operando
        largura_livre = largura_total - largura_fixa - 20   # 20 para a scrollbar
        if largura_livre > 0:
            self.tree.column("mnemonico", width=largura_livre)  # deixa o mnemônico ocupar o espaço restante


    def _limpar(self):
        self._item_atual = None
        for item in self.tree.get_children():
            self.tree.delete(item)  # remove cada linha da tabela
