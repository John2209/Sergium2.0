# Define o painel de registradores
# Mostra AC, AUX0–AUX3, Z, P, PC

import customtkinter as ctk


class RegistersPanel(ctk.CTkFrame):
    COR_NORMAL = ("gray14", "gray14")
    COR_MUDOU  = ("#7B4F00", "#7B4F00")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self._valores_anteriores = {}
        self._labels = {}

        self._criar_widgets()
        self._configurar_layout()

    def _criar_widgets(self):
        self.titulo = ctk.CTkLabel(self, text="Registradores", font=("Segoe UI", 14, "bold"))

        self.container = ctk.CTkFrame(self, fg_color="transparent")

        self._campos = [
            ("pc",   "PC"),
            ("ac",   "AC"),
            ("z",    "Z"),
            ("p",    "P"),
            ("aux0", "AUX0"),
            ("aux1", "AUX1"),
            ("aux2", "AUX2"),
            ("aux3", "AUX3"),
        ]

        for chave, rotulo in self._campos:
            celula = ctk.CTkFrame(self.container, corner_radius=6)

            lbl_nome = ctk.CTkLabel(
                celula,
                text=rotulo,
                font=("Courier New", 11, "bold"),
                text_color="gray60",
            )
            lbl_valor = ctk.CTkLabel(
                celula,
                text="0",
                font=("Courier New", 11),
            )

            celula.grid_columnconfigure(0, weight=1)
            celula.grid_columnconfigure(1, weight=1)

            lbl_nome.grid(row=0, column=0, padx=(4, 2), pady=8, sticky="w")
            lbl_valor.grid(row=0, column=1, padx=(2, 4), pady=8, sticky="e")

            self._labels[chave] = (lbl_nome, lbl_valor, celula)

    def _configurar_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titulo.grid(row=0, column=0, sticky="w", padx=16, pady=(12, 6))
        self.container.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        self.container.grid_columnconfigure(0, weight=1)

        for i, (chave, _) in enumerate(self._campos):
            self.container.grid_rowconfigure(i, weight=1)
            _, _, celula = self._labels[chave]
            celula.grid(row=i, column=0, padx=3, pady=3, sticky="nsew")

    # ─────────────────────────────────────────────
    # API pública
    # ─────────────────────────────────────────────

    def atualizar(self, snapshot):
        novos = {
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
            _, lbl_valor, celula = self._labels[chave]
            lbl_valor.configure(text=str(valor))

            mudou = self._valores_anteriores.get(chave) != valor
            celula.configure(fg_color=self.COR_MUDOU if mudou else self.COR_NORMAL)

        self._valores_anteriores = novos

    def resetar(self):
        self._valores_anteriores = {}
        for chave, _ in self._campos:
            _, lbl_valor, celula = self._labels[chave]
            lbl_valor.configure(text="0")
            celula.configure(fg_color=self.COR_NORMAL)