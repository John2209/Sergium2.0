# define o painel de registradores
# mostra pc, ac, z, p e aux0–aux3 em cards compactos organizados em duas colunas

import customtkinter as ctk


class RegistersPanel(ctk.CTkFrame):
    COR_CARD = "#222222"
    COR_CARD_MUDOU = "#33280F"

    COR_BORDA = "#3A3A3A"
    COR_BORDA_MUDOU = "#D99A24"

    COR_ROTULO = "#9AA0A6"
    COR_VALOR = "#F1F3F4"

    def __init__(self, master, **kwargs):  # inicializa o painel de registradores
        super().__init__(master, **kwargs)

        self._valores_anteriores = {}  # guarda valores anteriores para destacar mudanças
        self._labels = {}              # guarda labels e cards por chave de registrador

        self._campos = [  # lista dos campos exibidos no painel
            ("pc",   "PC"),
            ("ac",   "AC"),
            ("z",    "Z"),
            ("p",    "P"),
            ("aux0", "AUX0"),
            ("aux1", "AUX1"),
            ("aux2", "AUX2"),
            ("aux3", "AUX3"),
        ]

        self._criar_widgets()      # cria os cards de registradores
        self._configurar_layout()  # organiza os cards em duas colunas

    def _criar_widgets(self):
        self.titulo = ctk.CTkLabel(
            self,
            text="Registradores",
            font=("Segoe UI", 13, "bold"),
        )

        # scrollableframe evita que os cards sumam quando a janela fica baixa.
        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color="#444444",
            scrollbar_button_hover_color="#555555",
        )

        for chave, rotulo in self._campos:
            card = ctk.CTkFrame(
                self.container,
                corner_radius=8,
                fg_color=self.COR_CARD,
                border_width=1,
                border_color=self.COR_BORDA,
            )

            lbl_nome = ctk.CTkLabel(
                card,
                text=rotulo,
                font=("Courier New", 10, "bold"),
                text_color=self.COR_ROTULO,
                anchor="w",
            )

            lbl_valor = ctk.CTkLabel(
                card,
                text="0",
                font=("Courier New", 11, "bold"),
                text_color=self.COR_VALOR,
                anchor="e",
            )

            card.grid_columnconfigure(0, weight=1)
            card.grid_columnconfigure(1, weight=1)

            lbl_nome.grid(
                row=0,
                column=0,
                sticky="w",
                padx=(8, 4),
                pady=5,
            )

            lbl_valor.grid(
                row=0,
                column=1,
                sticky="e",
                padx=(4, 8),
                pady=5,
            )

            self._labels[chave] = (lbl_nome, lbl_valor, card)  # guarda referências para atualizar depois

    def _configurar_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titulo.grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=(10, 4),
        )

        self.container.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=12,
            pady=(0, 10),
        )

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        for i, (chave, _) in enumerate(self._campos):
            linha = i // 2
            coluna = i % 2

            self.container.grid_rowconfigure(linha, weight=0)

            _, _, card = self._labels[chave]
            card.grid(
                row=linha,
                column=coluna,
                sticky="ew",
                padx=3,
                pady=3,
            )

    # ─────────────────────────────────────────────
    # api pública
    # ─────────────────────────────────────────────

    def atualizar(self, snapshot):
        novos = {  # monta os valores atuais vindos da cpu
            "pc":   snapshot.pc,
            "ac":   snapshot.ac,
            "z":    snapshot.z,
            "p":    snapshot.p,
            "aux0": snapshot.auxs[0],
            "aux1": snapshot.auxs[1],
            "aux2": snapshot.auxs[2],
            "aux3": snapshot.auxs[3],
        }

        for chave, valor in novos.items():
            _, lbl_valor, card = self._labels[chave]
            lbl_valor.configure(text=str(valor))

            mudou = self._valores_anteriores.get(chave) != valor  # compara com a última atualização

            if mudou:
                card.configure(
                    fg_color=self.COR_CARD_MUDOU,
                    border_color=self.COR_BORDA_MUDOU,
                )
            else:
                card.configure(
                    fg_color=self.COR_CARD,
                    border_color=self.COR_BORDA,
                )

        self._valores_anteriores = novos  # guarda os valores para a próxima comparação

    def resetar(self):
        self._valores_anteriores = {}  # limpa o histórico de mudanças

        for chave, _ in self._campos:
            _, lbl_valor, card = self._labels[chave]

            lbl_valor.configure(text="0")
            card.configure(
                fg_color=self.COR_CARD,
                border_color=self.COR_BORDA,
            )
