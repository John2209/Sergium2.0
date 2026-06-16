# Define o painel do terminal
# Exibe logs, erros e saída do programa
# Inclui campo de entrada e exibição de saída

import customtkinter as ctk


class TerminalPanel(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._criar_widgets()
        self._configurar_layout()

    def _criar_widgets(self):
        self.titulo = ctk.CTkLabel(self, text="Terminal", font=("Segoe UI", 14, "bold"))

        # ── Log ──────────────────────────────────────
        self.texto = ctk.CTkTextbox(
            self,
            state="disabled",
            font=("Courier New", 12),
            height=80,
            wrap="word",
        )
        self.texto._textbox.tag_configure("erro",  foreground="#FF6B6B")
        self.texto._textbox.tag_configure("saida", foreground="#6BCB77")
        self.texto._textbox.tag_configure("info",  foreground="#A8DADC")

        # ── Entrada ───────────────────────────────────
        self.frame_entrada = ctk.CTkFrame(self, fg_color="transparent")

        self.label_entrada = ctk.CTkLabel(
            self.frame_entrada,
            text="Entrada:",
            font=("Courier New", 12),
            text_color="gray60",
        )
        self.campo_entrada = ctk.CTkEntry(
            self.frame_entrada,
            placeholder_text="Digite um valor e pressione Enter...",
            font=("Courier New", 12),
            width=220,
        )
        self.botao_entrada = ctk.CTkButton(
            self.frame_entrada,
            text="Enviar",
            width=70,
            corner_radius=8,
            command=self._enviar_entrada,
        )

        self.campo_entrada.bind("<Return>", lambda e: self._enviar_entrada())

        # ── Saída ─────────────────────────────────────
        self.frame_saida = ctk.CTkFrame(self, fg_color="transparent")

        self.label_saida = ctk.CTkLabel(
            self.frame_saida,
            text="Saída:",
            font=("Courier New", 12),
            text_color="gray60",
        )
        self.valor_saida = ctk.CTkLabel(
            self.frame_saida,
            text="—",
            font=("Courier New", 12, "bold"),
            text_color="#6BCB77",
        )

        # callback chamado pelo app quando há entrada disponível
        self._callback_entrada = None

    def _configurar_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titulo.grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))
        self.texto.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 6))

        # linha inferior: entrada à esquerda, saída à direita
        self.frame_entrada.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 12))
        self.frame_saida  .grid(row=2, column=0, sticky="e", padx=16, pady=(0, 12))

        self.label_entrada.grid(row=0, column=0, padx=(0, 6))
        self.campo_entrada.grid(row=0, column=1, padx=(0, 6))
        self.botao_entrada.grid(row=0, column=2)

        self.label_saida.grid(row=0, column=0, padx=(0, 8))
        self.valor_saida.grid(row=0, column=1)

    # ─────────────────────────────────────────────
    # API pública
    # ─────────────────────────────────────────────

    def definir_callback_entrada(self, fn):
        """Registra a função chamada quando o usuário envia um valor de entrada."""
        self._callback_entrada = fn

    def get_entrada(self) -> str | None:
        """Retorna o valor atual do campo de entrada, ou None se vazio."""
        valor = self.campo_entrada.get().strip()
        return valor if valor else None

    def mostrar_saida(self, valor):
        """Atualiza o label de saída e registra no log."""
        self.valor_saida.configure(text=str(valor))
        self.saida(f"Saída: {valor}")

    def resetar_saida(self):
        self.valor_saida.configure(text="—")

    def log(self, mensagem: str):
        self._escrever(f"[info]  {mensagem}\n", "info")

    def erro(self, mensagem: str):
        self._escrever(f"[erro]  {mensagem}\n", "erro")

    def saida(self, mensagem: str):
        self._escrever(f"[saída] {mensagem}\n", "saida")

    def limpar(self):
        self.texto.configure(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.configure(state="disabled")
        self.resetar_saida()

    # ─────────────────────────────────────────────
    # Interno
    # ─────────────────────────────────────────────

    def _enviar_entrada(self):
        valor = self.campo_entrada.get().strip()
        if not valor:
            return
        self.log(f"Entrada definida: {valor}")
        self.campo_entrada.delete(0, "end")

        if self._callback_entrada:
            self._callback_entrada(valor)

    def _escrever(self, texto: str, tag: str):
        self.texto.configure(state="normal")
        self.texto._textbox.insert("end", texto, tag)
        self.texto.see("end")
        self.texto.configure(state="disabled")