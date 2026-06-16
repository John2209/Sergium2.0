# Define o painel de memória
# Mostra os endereços e seus valores; destaca células alteradas

import customtkinter as ctk
from tkinter import ttk


class MemoryPanel(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._mem_anterior = [0] * 256
        self._criar_widgets()
        self._configurar_layout()
        self._popular_tabela()  # preenche os 256 endereços uma única vez

    def _criar_widgets(self):
        self.titulo = ctk.CTkLabel(self, text="Memória", font=("Segoe UI", 14, "bold"))

        style = ttk.Style()
        style.configure(
            "Mem.Treeview",
            background="#1e1e1e",
            foreground="#e0e0e0",
            fieldbackground="#1e1e1e",
            rowheight=22,
            font=("Courier New", 11),
            borderwidth=0,
        )
        style.configure(
            "Mem.Treeview.Heading",
            background="#2a2a2a",
            foreground="#888888",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        style.map(
            "Mem.Treeview",
            background=[("selected", "#1e1e1e")],
            foreground=[("selected", "#e0e0e0")],
        )

        self.tree = ttk.Treeview(
            self,
            style="Mem.Treeview",
            columns=("endereco", "valor"),
            show="headings",
            selectmode="none",
        )

        self.tree.heading("endereco", text="Endereço")
        self.tree.heading("valor",    text="Valor")

        self.tree.column("endereco", width=80,  anchor="center", stretch=False)
        self.tree.column("valor",    width=80,  anchor="center")

        # tag para células alteradas
        self.tree.tag_configure("alterado", foreground="#FFD166")

        self.scrollbar = ctk.CTkScrollbar(self, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

    def _configurar_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(12, 6))
        self.tree.grid(row=1, column=0, sticky="nsew", padx=(12, 0), pady=(0, 12))
        self.scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 8), pady=(0, 12))

    def _popular_tabela(self):
        """Cria as 256 linhas uma única vez; atualizar() só muda os valores."""
        for i in range(256):
            self.tree.insert("", "end", iid=str(i), values=(f"{i:03d}", "0"))

    # ─────────────────────────────────────────────
    # API pública
    # ─────────────────────────────────────────────

    def atualizar(self, snapshot):
        """Atualiza apenas as células cujo valor mudou e destaca em amarelo."""
        for i, valor in enumerate(snapshot.mem):
            anterior = self._mem_anterior[i]
            if valor != anterior:
                tag = "alterado" if valor != 0 else ""
                self.tree.item(str(i), values=(f"{i:03d}", str(valor)), tags=(tag,))

        self._mem_anterior = snapshot.mem.copy()

    def resetar(self):
        """Volta todos os endereços para 0 e remove destaques."""
        for i in range(256):
            self.tree.item(str(i), values=(f"{i:03d}", "0"), tags=())
        self._mem_anterior = [0] * 256