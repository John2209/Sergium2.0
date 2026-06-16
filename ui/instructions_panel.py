# Define a tabela de instruções
# Mostra rótulo, mnemônico, operando e destaca a instrução atual durante a execução

import customtkinter as ctk
from tkinter import ttk


_ESTILO_APLICADO = False  # garante que o estilo ttk só é aplicado uma vez


def _aplicar_estilo_treeview():
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
        rowheight=24,
        font=("Courier New", 11),
        borderwidth=0,
    )
    style.configure(
        "Sergium.Treeview.Heading",
        background="#2a2a2a",
        foreground="#888888",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
    )
    style.map(
        "Sergium.Treeview",
        background=[("selected", "#2a4a7f")],
        foreground=[("selected", "#ffffff")],
    )

    _ESTILO_APLICADO = True


class InstructionsPanel(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        _aplicar_estilo_treeview()
        self._item_atual = None     # id do item destacado no momento
        self._criar_widgets()
        self._configurar_layout()

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

        self.tree.column("rotulo",    width=70,  minwidth=70,  anchor="center", stretch=False)
        self.tree.column("mnemonico", width=200, minwidth=100, anchor="w",      stretch=True)
        self.tree.column("operando",  width=70,  minwidth=70,  anchor="center", stretch=False)

        # tag para a instrução apontada pelo PC
        self.tree.tag_configure("atual", background="#1a3a6a", foreground="#ffffff")

        self.scrollbar = ctk.CTkScrollbar(self, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.bind("<Configure>", self._redistribuir_colunas)

    def _configurar_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(12, 6))
        self.tree.grid(row=1, column=0, sticky="nsew", padx=(12, 0), pady=(0, 12))
        self.scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 8), pady=(0, 12))

    # ─────────────────────────────────────────────
    # API pública
    # ─────────────────────────────────────────────

    def carregar(self, instrucoes: dict):
        """
        Preenche a tabela com o programa montado.
        instrucoes: dicionário {rótulo: (mnemonico, operando)} igual ao que a CPU usa.
        """
        self._limpar()
        for rotulo, (mnemonico, operando) in instrucoes.items():
            self.tree.insert("", "end", iid=rotulo, values=(rotulo, mnemonico, operando))

    def atualizar(self, snapshot):
        """Destaca a linha apontada pelo PC atual."""
        # remove destaque anterior
        if self._item_atual and self.tree.exists(self._item_atual):
            self.tree.item(self._item_atual, tags=())

        rotulo = snapshot.rotulo_atual
        if rotulo and self.tree.exists(rotulo):
            self.tree.item(rotulo, tags=("atual",))
            self.tree.see(rotulo)   # rola para manter a linha visível
            self._item_atual = rotulo
        else:
            self._item_atual = None

    def resetar(self):
        """Limpa a tabela e remove destaques."""
        self._limpar()

    # ─────────────────────────────────────────────
    # Interno
    # ─────────────────────────────────────────────

    def _redistribuir_colunas(self, event=None):
        largura_total = self.tree.winfo_width()
        largura_fixa  = 70 + 70     # rotulo + operando
        largura_livre = largura_total - largura_fixa - 20   # 20 para a scrollbar
        if largura_livre > 0:
            self.tree.column("mnemonico", width=largura_livre)

    def _limpar(self):
        self._item_atual = None
        for item in self.tree.get_children():
            self.tree.delete(item)