# Define o painel do editor de código Sergium
# Inclui numeração de linhas sincronizada e destaque da linha atual

import customtkinter as ctk
import tkinter as tk


class EditorPanel(ctk.CTkFrame):

    COR_LINHA_ATUAL = "#1a3a6a"

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._criar_widgets()
        self._configurar_layout()
        self._conectar_eventos()
        self._atualizar_numeracao()

    def _criar_widgets(self):
        self.titulo = ctk.CTkLabel(self, text="Editor", font=("Segoe UI", 14, "bold"))

        # container interno para editor + numeração lado a lado
        self.container = ctk.CTkFrame(self, fg_color="transparent")

        # numeração de linhas (widget tk puro para controle fino de cores)
        self.nums = tk.Text(
            self.container,
            width=4,
            padx=6,
            state="disabled",
            font=("Courier New", 13),
            bg="#1a1a1a",
            fg="#555555",
            bd=0,
            highlightthickness=0,
            cursor="arrow",
            selectbackground="#1a1a1a",
        )

        # área de edição principal
        self.editor = tk.Text(
            self.container,
            font=("Courier New", 13),
            bg="#1e1e1e",
            fg="#e0e0e0",
            insertbackground="#e0e0e0",
            selectbackground="#2a4a7f",
            bd=0,
            highlightthickness=0,
            undo=True,
            wrap="none",
            padx=8,
            pady=4,
        )
        self.editor.tag_configure("linha_atual", background=self.COR_LINHA_ATUAL)

        self.scrollbar_v = ctk.CTkScrollbar(self.container, command=self._scroll_y_ambos)
        self.scrollbar_h = ctk.CTkScrollbar(self.container, orientation="horizontal", command=self.editor.xview)

        self.editor.configure(
            yscrollcommand=self._on_scroll_editor,
            xscrollcommand=self.scrollbar_h.set,
        )
        self.nums.configure(yscrollcommand=self._on_scroll_nums)

    def _configurar_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titulo.grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))
        self.container.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        self.nums.grid(row=0, column=0, sticky="ns")
        self.editor.grid(row=0, column=1, sticky="nsew")
        self.scrollbar_v.grid(row=0, column=2, sticky="ns")
        self.scrollbar_h.grid(row=1, column=1, sticky="ew")

    def _conectar_eventos(self):
        self.editor.bind("<KeyRelease>",    self._on_modificado)
        self.editor.bind("<ButtonRelease>", self._on_modificado)
        self.editor.bind("<MouseWheel>",    self._on_scroll_mouse)
        self.nums.bind("<MouseWheel>",      self._on_scroll_mouse)

    # ─────────────────────────────────────────────
    # API pública
    # ─────────────────────────────────────────────

    def get_texto(self) -> str:
        """Retorna o conteúdo atual do editor (sem a quebra de linha final do tk)."""
        return self.editor.get("1.0", "end-1c")

    def set_texto(self, texto: str):
        """Substitui todo o conteúdo do editor."""
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", texto)
        self._atualizar_numeracao()

    def destacar_linha(self, numero: int | None):
        """
        Destaca a linha `numero` (1-indexado) com a cor de instrução atual.
        Passa None para remover o destaque.
        """
        self.editor.tag_remove("linha_atual", "1.0", "end")
        if numero is not None:
            inicio = f"{numero}.0"
            fim    = f"{numero}.end+1c"
            self.editor.tag_add("linha_atual", inicio, fim)
            self.editor.see(inicio)

    def resetar_destaque(self):
        self.editor.tag_remove("linha_atual", "1.0", "end")

    # ─────────────────────────────────────────────
    # Scroll sincronizado
    # ─────────────────────────────────────────────

    def _scroll_y_ambos(self, *args):
        self.editor.yview(*args)
        self.nums.yview(*args)

    def _on_scroll_editor(self, primeiro, ultimo):
        self.scrollbar_v.set(primeiro, ultimo)
        self.nums.yview_moveto(primeiro)

    def _on_scroll_nums(self, primeiro, ultimo):
        # nums não tem scrollbar própria; sincroniza com editor
        self.editor.yview_moveto(primeiro)

    def _on_scroll_mouse(self, event):
        delta = -1 * (event.delta // 120) if event.delta else (1 if event.num == 5 else -1)
        self.editor.yview_scroll(delta, "units")
        self.nums.yview_scroll(delta, "units")
        return "break"

    # ─────────────────────────────────────────────
    # Numeração de linhas
    # ─────────────────────────────────────────────

    def _on_modificado(self, event=None):
        self._atualizar_numeracao()

    def _atualizar_numeracao(self):
        total = int(self.editor.index("end-1c").split(".")[0])
        conteudo = "\n".join(str(i) for i in range(1, total + 1))

        self.nums.configure(state="normal")
        self.nums.delete("1.0", "end")
        self.nums.insert("1.0", conteudo)
        self.nums.configure(state="disabled")