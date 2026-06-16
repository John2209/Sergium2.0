# Ponto de entrada da interface gráfica
# Inicialização da aplicação

import customtkinter as ctk
from tkinter import filedialog
import tempfile
import os

from ui import RegistersPanel, EditorPanel, InstructionsPanel, TerminalPanel, MemoryPanel


class App(ctk.CTk):

    def __init__(self, minha_cpu):
        super().__init__()

        self.minha_cpu = minha_cpu
        self._instrucoes_montadas = None
        self._caminho_arquivo = None

        self.configurar_janela()
        self.criar_widgets()
        self.configurar_layout()
        self.conectar_botoes()
        self.painel_terminal.definir_callback_entrada(self._acao_entrada)

    def configurar_janela(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Sergium 2.0")
        self.geometry("1356x864")
        self.minsize(900, 500)

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
        self.botao_abrir  = ctk.CTkButton(self.toolbar, text="Abrir",  width=80, corner_radius=8)
        self.botao_salvar = ctk.CTkButton(self.toolbar, text="Salvar", width=80, corner_radius=8)
        self.botao_montar = ctk.CTkButton(self.toolbar, text="Montar", width=80, corner_radius=8)
        self.botao_run    = ctk.CTkButton(self.toolbar, text="Run",    width=80, corner_radius=8)
        self.botao_step   = ctk.CTkButton(self.toolbar, text="Step",   width=80, corner_radius=8)
        self.botao_reset  = ctk.CTkButton(self.toolbar, text="Reset",  width=80, corner_radius=8)

        # =========================
        # Painéis
        # =========================
        self.painel_editor        = EditorPanel      (self.area_principal, corner_radius=12)
        self.painel_instrucoes    = InstructionsPanel(self.painel_lateral,  corner_radius=12)
        self.painel_registradores = RegistersPanel   (self.painel_lateral,  corner_radius=12)
        self.painel_memoria       = MemoryPanel      (self.painel_lateral,  corner_radius=12)
        self.painel_terminal      = TerminalPanel    (self,                 corner_radius=12)

    def configurar_layout(self):
        # =========================
        # Layout geral da janela
        # =========================
        self.toolbar.grid        (row=0, column=0, sticky="ew",   padx=8, pady=8)
        self.area_principal.grid (row=1, column=0, sticky="nsew", padx=8)
        self.painel_terminal.grid(row=2, column=0, sticky="ew",   padx=8, pady=8)

        # =========================
        # Layout da toolbar
        # =========================
        self.botao_abrir .grid(row=0, column=0, padx=4, pady=8)
        self.botao_salvar.grid(row=0, column=1, padx=4, pady=8)
        self.botao_montar.grid(row=0, column=2, padx=4, pady=8)
        self.botao_run   .grid(row=0, column=3, padx=4, pady=8)
        self.botao_step  .grid(row=0, column=4, padx=4, pady=8)
        self.botao_reset .grid(row=0, column=5, padx=4, pady=8)

        # =========================
        # Layout da área principal
        # =========================
        self.area_principal.grid_rowconfigure(0, weight=1)
        self.area_principal.grid_columnconfigure(0, weight=3)
        self.area_principal.grid_columnconfigure(1, weight=2)

        self.painel_editor .grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.painel_lateral.grid(row=0, column=1, sticky="nsew")

        # =========================
        # Layout do painel lateral
        # =========================
        self.painel_lateral.grid_rowconfigure(0, weight=2)
        self.painel_lateral.grid_rowconfigure(1, weight=1)
        self.painel_lateral.grid_rowconfigure(2, weight=2)
        self.painel_lateral.grid_columnconfigure(0, weight=1)

        self.painel_instrucoes   .grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        self.painel_registradores.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        self.painel_memoria      .grid(row=2, column=0, sticky="nsew")

    def conectar_botoes(self):
        self.botao_abrir .configure(command=self._acao_abrir)
        self.botao_salvar.configure(command=self._acao_salvar)
        self.botao_montar.configure(command=self._acao_montar)
        self.botao_run   .configure(command=self._acao_run)
        self.botao_step  .configure(command=self._acao_step)
        self.botao_reset .configure(command=self._acao_reset)

    # ─────────────────────────────────────────────
    # Atualização da UI
    # ─────────────────────────────────────────────

    def _atualizar_ui(self):
        snap = self.minha_cpu.snapshot()
        self.painel_registradores.atualizar(snap)
        self.painel_instrucoes.atualizar(snap)
        self.painel_memoria.atualizar(snap)

        if snap.finalizado:
            self.painel_editor.destacar_linha(None)
        elif snap.rotulo_atual is not None:
            self.painel_editor.destacar_linha(snap.pc + 1)

        saida = self.minha_cpu.consumir_saida()
        if saida is not None:
            self.painel_terminal.mostrar_saida(saida)

        if snap.finalizado:
            self.painel_terminal.log("Programa finalizado.")

    # ─────────────────────────────────────────────
    # Ações dos botões
    # ─────────────────────────────────────────────

    def _acao_abrir(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivos Sergium", "*.srg"), ("Todos", "*.*")]
        )
        if not caminho:
            return

        self._caminho_arquivo = caminho
        with open(caminho, "r", encoding="utf-8") as f:
            self.painel_editor.set_texto(f.read())
        self.painel_terminal.log(f"Arquivo aberto: {caminho}")

    def _acao_salvar(self):
        caminho = self._caminho_arquivo or filedialog.asksaveasfilename(
            defaultextension=".srg",
            filetypes=[("Arquivos Sergium", "*.srg"), ("Todos", "*.*")],
        )
        if not caminho:
            return

        self._caminho_arquivo = caminho
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(self.painel_editor.get_texto())
        self.painel_terminal.log(f"Arquivo salvo: {caminho}")

    def _acao_montar(self):
        from core import Parser, ParserError

        texto = self.painel_editor.get_texto()
        if not texto.strip():
            self.painel_terminal.erro("Editor vazio. Escreva um programa antes de montar.")
            return

        # Parser lê arquivos, então salva em temporário
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".srg", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(texto)
            caminho_tmp = tmp.name

        try:
            parser = Parser(caminho_tmp)
            instrucoes = parser.parsear()
            self.minha_cpu.carregar_programa(instrucoes)
            self._instrucoes_montadas = instrucoes

            self.painel_instrucoes.carregar(instrucoes)
            self.painel_registradores.resetar()
            self.painel_memoria.resetar()
            self.painel_terminal.limpar()
            self.painel_terminal.log(f"Montado com sucesso: {len(instrucoes)} instrução(ões).")
            self._atualizar_ui()

        except Exception as e:
            self.painel_terminal.erro(str(e))

        finally:
            os.unlink(caminho_tmp)

    def _acao_run(self):
        if self._instrucoes_montadas is None:
            self.painel_terminal.erro("Monte o programa antes de executar.")
            return

        try:
            terminou = self.minha_cpu.executar_tudo()
            if terminou is False:
                self.painel_terminal.log("Programa pausado. Aguardando valor de entrada.")
        except Exception as e:
            self.painel_terminal.erro(str(e))
        finally:
            self._atualizar_ui()

    def _acao_step(self):
        if self._instrucoes_montadas is None:
            self.painel_terminal.erro("Monte o programa antes de executar.")
            return
        try:
            self.minha_cpu.executar_instrucao()
        except Exception as e:
            self.painel_terminal.erro(str(e))
        finally:
            self._atualizar_ui()

    def _acao_entrada(self, valor: str):
        """Chamado pelo terminal quando o usuário envia um valor de entrada."""
        try:
            self.minha_cpu.definir_entrada(valor)
        except Exception as e:
            self.painel_terminal.erro(str(e))

    def _acao_reset(self):
        self.minha_cpu.resetar()
        self._instrucoes_montadas = None
        self.painel_instrucoes.resetar()
        self.painel_registradores.resetar()
        self.painel_memoria.resetar()
        self.painel_editor.resetar_destaque()
        self.painel_terminal.limpar()
        self.painel_terminal.resetar_saida()
        self.painel_terminal.log("CPU resetada.")