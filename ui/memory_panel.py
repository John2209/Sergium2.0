# define o painel de memória
# mostra os endereços e seus valores; destaca células alteradas

import customtkinter as ctk
from tkinter import ttk


class MemoryPanel(ctk.CTkFrame):

    def __init__(self, master, **kwargs):  # inicializa o painel de memória
        super().__init__(master, **kwargs)

        self._mem_anterior = [0] * 256  # guarda a memória anterior para detectar mudanças

        self._criar_widgets()      # cria a tabela e a barra de rolagem
        self._configurar_layout()  # posiciona os elementos na grade
        self._popular_tabela()     # cria as linhas fixas da memória

    def _criar_widgets(self):
        self.titulo = ctk.CTkLabel(
            self,
            text="Memória",
            font=("Segoe UI", 14, "bold"),
        )

        style = ttk.Style()

        style.configure(
            "Mem.Treeview",
            background="#1e1e1e",
            foreground="#e0e0e0",
            fieldbackground="#1e1e1e",
            rowheight=20,
            font=("Courier New", 10),
            borderwidth=0,
        )

        style.configure(
            "Mem.Treeview.Heading",
            background="#2a2a2a",
            foreground="#9AA0A6",
            font=("Segoe UI", 9, "bold"),
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
        self.tree.heading("valor", text="Valor")

        self.tree.column(
            "endereco",
            width=72,
            minwidth=60,
            anchor="center",
            stretch=False,
        )

        self.tree.column(
            "valor",
            width=72,
            minwidth=60,
            anchor="center",
            stretch=True,
        )

        self.tree.tag_configure("alterado", foreground="#FFD166")

        self.scrollbar = ctk.CTkScrollbar(
            self,
            command=self.tree.yview,
        )

        self.tree.configure(yscrollcommand=self.scrollbar.set)

    def _configurar_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titulo.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=16,
            pady=(8, 4),
        )

        self.tree.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(12, 0),
            pady=(0, 10),
        )

        self.scrollbar.grid(
            row=1,
            column=1,
            sticky="ns",
            padx=(0, 8),
            pady=(0, 10),
        )

    def _popular_tabela(self):
        """cria as 256 linhas uma única vez; atualizar() só muda os valores."""
        for i in range(256):
            self.tree.insert(
                "",
                "end",
                iid=str(i),
                values=(f"{i:03d}", "0"),
            )

    # ─────────────────────────────────────────────
    # api pública
    # ─────────────────────────────────────────────

    def atualizar(self, snapshot):
        """atualiza apenas as células cujo valor mudou e destaca em amarelo."""
        for i, valor in enumerate(snapshot.mem):
            anterior = self._mem_anterior[i]  # valor anterior no mesmo endereço

            if valor != anterior:
                tag = "alterado" if valor != 0 else ""  # destaca apenas valores diferentes de zero

                self.tree.item(
                    str(i),
                    values=(f"{i:03d}", str(valor)),
                    tags=(tag,),
                )

        self._mem_anterior = snapshot.mem.copy()  # guarda uma cópia para a próxima comparação

    def resetar(self):
        """volta todos os endereços para 0 e remove destaques."""
        for i in range(256):
            self.tree.item(
                str(i),
                values=(f"{i:03d}", "0"),
                tags=(),
            )

        self._mem_anterior = [0] * 256  # reinicia o estado usado para comparação
