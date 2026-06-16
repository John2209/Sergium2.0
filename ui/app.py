# Ponto de entrada da interface gráfica
# Inicialização da aplicação

import customtkinter as ctk
import tkinter as tk
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

        # Estado dos divisores redimensionáveis da interface.
        # Guardamos proporções, não pixels, para funcionar bem em janela e tela cheia.
        self._estado_layout_atual = "janela"
        self._ratios_layout = {}
        self._aplicando_layout_salvo = False

        self.configurar_janela()
        self.criar_widgets()
        self.configurar_layout()
        self.conectar_botoes()
        self._atualizar_estado_botoes()
        self._conectar_eventos_layout()
        self.painel_terminal.definir_callback_entrada(self._acao_entrada)

    def configurar_janela(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Sergium 2.0")
        self.geometry("1180x700")
        self.minsize(1000, 620)

        # Fundo geral mais escuro para os painéis parecerem blocos flutuando
        self.configure(fg_color="#111111")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        # =========================
        # Cores principais
        # =========================
        cor_fundo = "#111111"
        cor_toolbar = "#242424"
        cor_painel = "#2B2B2B"

        cor_botao = "#1F6AA5"
        cor_botao_hover = "#2A7DBF"

        cor_reset = "#C62828"
        cor_reset_hover = "#E53935"

        # =========================
        # Containers principais
        # =========================
        self.toolbar = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=cor_toolbar,
        )

        self.area_principal = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=cor_fundo,
        )

        self.divisor_principal = tk.PanedWindow(
            self.area_principal,
            orient=tk.HORIZONTAL,
            sashwidth=4,
            sashrelief="flat",
            bd=0,
            bg=cor_fundo,
            showhandle=False,
        )

        self.area_esquerda = ctk.CTkFrame(
            self.divisor_principal,
            corner_radius=0,
            fg_color=cor_fundo,
        )

        self.divisor_esquerdo = tk.PanedWindow(
            self.area_esquerda,
            orient=tk.VERTICAL,
            sashwidth=4,
            sashrelief="flat",
            bd=0,
            bg=cor_fundo,
            showhandle=False,
        )

        self.painel_lateral = ctk.CTkFrame(
            self.divisor_principal,
            corner_radius=0,
            fg_color=cor_fundo,
        )

        self.divisor_lateral = tk.PanedWindow(
            self.painel_lateral,
            orient=tk.VERTICAL,
            sashwidth=4,
            sashrelief="flat",
            bd=0,
            bg=cor_fundo,
            showhandle=False,
        )

        # =========================
        # Botões da toolbar
        # =========================
        self.botao_abrir = ctk.CTkButton(
            self.toolbar,
            text="Abrir",
            width=80,
            height=28,
            corner_radius=8,
            fg_color=cor_botao,
            hover_color=cor_botao_hover,
        )

        self.botao_salvar = ctk.CTkButton(
            self.toolbar,
            text="Salvar",
            width=80,
            height=28,
            corner_radius=8,
            fg_color=cor_botao,
            hover_color=cor_botao_hover,
        )

        self.botao_montar = ctk.CTkButton(
            self.toolbar,
            text="Montar",
            width=80,
            height=28,
            corner_radius=8,
            fg_color=cor_botao,
            hover_color=cor_botao_hover,
        )

        self.botao_run = ctk.CTkButton(
            self.toolbar,
            text="Run",
            width=80,
            height=28,
            corner_radius=8,
            fg_color=cor_botao,
            hover_color=cor_botao_hover,
            state="disabled",
        )

        self.botao_step = ctk.CTkButton(
            self.toolbar,
            text="Step",
            width=80,
            height=28,
            corner_radius=8,
            fg_color=cor_botao,
            hover_color=cor_botao_hover,
            state="disabled",
        )

        self.botao_reset = ctk.CTkButton(
            self.toolbar,
            text="Reset",
            width=80,
            height=28,
            corner_radius=8,
            fg_color=cor_reset,
            hover_color=cor_reset_hover,
            state="disabled",
        )

        # =========================
        # Painéis
        # =========================
        self.painel_editor = EditorPanel(
            self.divisor_esquerdo,
            corner_radius=12,
            fg_color=cor_painel,
        )

        self.painel_terminal = TerminalPanel(
            self.divisor_esquerdo,
            corner_radius=12,
            fg_color=cor_painel,
        )

        self.painel_instrucoes = InstructionsPanel(
            self.divisor_lateral,
            corner_radius=12,
            fg_color=cor_painel,
        )

        self.painel_registradores = RegistersPanel(
            self.divisor_lateral,
            corner_radius=12,
            fg_color=cor_painel,
        )

        self.painel_memoria = MemoryPanel(
            self.divisor_lateral,
            corner_radius=12,
            fg_color=cor_painel,
        )

    def configurar_layout(self):
        # =========================
        # Layout geral da janela
        # =========================
        self.toolbar.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=(8, 4),
        )

        self.area_principal.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(4, 8),
        )

        # =========================
        # Layout da toolbar
        # =========================
        self.botao_abrir.grid(row=0, column=0, padx=(8, 4), pady=8)
        self.botao_salvar.grid(row=0, column=1, padx=4, pady=8)
        self.botao_montar.grid(row=0, column=2, padx=4, pady=8)
        self.botao_run.grid(row=0, column=3, padx=4, pady=8)
        self.botao_step.grid(row=0, column=4, padx=4, pady=8)
        self.botao_reset.grid(row=0, column=5, padx=4, pady=8)

        # =========================
        # Layout da área principal
        # =========================
        self.area_principal.grid_rowconfigure(0, weight=1)
        self.area_principal.grid_columnconfigure(0, weight=1)

        self.divisor_principal.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.divisor_principal.add(
            self.area_esquerda,
            minsize=620,
            padx=2,
            pady=0,
            sticky="nsew",
        )

        self.divisor_principal.add(
            self.painel_lateral,
            minsize=320,
            padx=2,
            pady=0,
            sticky="nsew",
        )

        # =========================
        # Coluna esquerda: editor + terminal
        # =========================
        self.area_esquerda.grid_rowconfigure(0, weight=1)
        self.area_esquerda.grid_columnconfigure(0, weight=1)

        self.divisor_esquerdo.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.divisor_esquerdo.add(
            self.painel_editor,
            minsize=320,
            padx=0,
            pady=2,
            sticky="nsew",
        )

        self.divisor_esquerdo.add(
            self.painel_terminal,
            minsize=120,
            padx=0,
            pady=2,
            sticky="nsew",
        )

        # =========================
        # Coluna direita: instruções + registradores + memória
        # =========================
        self.painel_lateral.grid_rowconfigure(0, weight=1)
        self.painel_lateral.grid_columnconfigure(0, weight=1)

        self.divisor_lateral.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.divisor_lateral.add(
            self.painel_instrucoes,
            minsize=130,
            padx=0,
            pady=2,
            sticky="nsew",
        )

        self.divisor_lateral.add(
            self.painel_registradores,
            minsize=135,
            padx=0,
            pady=2,
            sticky="nsew",
        )

        self.divisor_lateral.add(
            self.painel_memoria,
            minsize=150,
            padx=0,
            pady=2,
            sticky="nsew",
        )

        self.after(100, self._ajustar_divisor_esquerdo)
        self.after(100, self._ajustar_divisor_principal)
        self.after(100, self._ajustar_divisor_lateral)

    def _ajustar_divisor_esquerdo(self):
        altura = self.area_esquerda.winfo_height()

        if altura <= 0:
            return

        posicao = int(altura * 0.70)
        self.divisor_esquerdo.sash_place(0, 0, posicao)

    def _ajustar_divisor_principal(self):
        largura = self.area_principal.winfo_width()

        if largura <= 0:
            return

        posicao = int(largura * 0.58)
        self.divisor_principal.sash_place(0, posicao, 0)

    def _ajustar_divisor_lateral(self):
        altura = self.painel_lateral.winfo_height()

        if altura <= 0:
            return

        posicao_instrucoes = int(altura * 0.34)
        posicao_registradores = int(altura * 0.60)

        self.divisor_lateral.sash_place(0, 0, posicao_instrucoes)
        self.divisor_lateral.sash_place(1, 0, posicao_registradores)

    def conectar_botoes(self):
        self.botao_abrir .configure(command=self._acao_abrir)
        self.botao_salvar.configure(command=self._acao_salvar)
        self.botao_montar.configure(command=self._acao_montar)
        self.botao_run   .configure(command=self._acao_run)
        self.botao_step  .configure(command=self._acao_step)
        self.botao_reset .configure(command=self._acao_reset)

    def _atualizar_estado_botoes(self):
        programa_montado = self._instrucoes_montadas is not None
        programa_em_execucao = programa_montado and not self.minha_cpu.finalizado

        estado_execucao = "normal" if programa_em_execucao else "disabled"
        estado_reset = "normal" if programa_montado else "disabled"

        self.botao_run.configure(state=estado_execucao)
        self.botao_step.configure(state=estado_execucao)
        self.botao_reset.configure(state=estado_reset)

    def _conectar_eventos_layout(self):
        # Quando o usuário solta um divisor, salvamos a proporção atual.
        self.divisor_principal.bind("<ButtonRelease-1>", self._ao_soltar_divisor)
        self.divisor_esquerdo.bind("<ButtonRelease-1>", self._ao_soltar_divisor)
        self.divisor_lateral.bind("<ButtonRelease-1>", self._ao_soltar_divisor)

        # Detecta troca entre modo janela e maximizado.
        self.bind("<Configure>", self._ao_configurar_janela)

        # Depois que os divisores iniciais forem posicionados, salva o layout inicial de janela.
        self.after(200, self._salvar_layout_atual)

    def _estado_visual_janela(self):
        # No Windows, janela maximizada normalmente aparece como "zoomed".
        # Para o nosso caso, tratamos isso como tela cheia/maximizado.
        return "maximizado" if self.state() == "zoomed" else "janela"

    def _ao_soltar_divisor(self, event=None):
        # Espera o Tk terminar de atualizar a posição visual do divisor.
        self.after(50, self._salvar_layout_atual)

    def _ao_configurar_janela(self, event=None):
        # Ignora eventos de widgets internos. Queremos só mudanças da janela principal.
        if event is not None and event.widget is not self:
            return

        novo_estado = self._estado_visual_janela()

        if novo_estado == self._estado_layout_atual:
            return

        self._estado_layout_atual = novo_estado

        if novo_estado in self._ratios_layout:
            self.after(100, lambda: self._aplicar_layout_salvo(self._ratios_layout[novo_estado]))
            return

        # Primeira vez entrando em maximizado:
        # aplica uma distribuição usual, confortável para apresentação.
        if novo_estado == "maximizado":
            ratios_padrao = {
                "principal": 0.58,
                "esquerdo": 0.70,
                "lateral_1": 0.34,
                "lateral_2": 0.60,
            }

            self._ratios_layout["maximizado"] = ratios_padrao
            self.after(100, lambda: self._aplicar_layout_salvo(ratios_padrao))

    def _salvar_layout_atual(self):
        if self._aplicando_layout_salvo:
            return

        estado = self._estado_visual_janela()
        self._estado_layout_atual = estado

        try:
            largura_principal = self.area_principal.winfo_width()
            altura_esquerda = self.area_esquerda.winfo_height()
            altura_lateral = self.painel_lateral.winfo_height()

            if largura_principal <= 0 or altura_esquerda <= 0 or altura_lateral <= 0:
                return

            principal_x = self.divisor_principal.sash_coord(0)[0]
            esquerdo_y = self.divisor_esquerdo.sash_coord(0)[1]
            lateral_1_y = self.divisor_lateral.sash_coord(0)[1]
            lateral_2_y = self.divisor_lateral.sash_coord(1)[1]

            self._ratios_layout[estado] = {
                "principal": principal_x / largura_principal,
                "esquerdo": esquerdo_y / altura_esquerda,
                "lateral_1": lateral_1_y / altura_lateral,
                "lateral_2": lateral_2_y / altura_lateral,
            }

        except tk.TclError:
            # Pode acontecer durante a criação inicial da janela.
            return

    def _aplicar_layout_salvo(self, ratios):
        self._aplicando_layout_salvo = True

        try:
            self.update_idletasks()

            largura_principal = self.area_principal.winfo_width()
            if largura_principal > 0:
                x_principal = int(largura_principal * ratios["principal"])
                self.divisor_principal.sash_place(0, x_principal, 0)

            self.update_idletasks()

            altura_esquerda = self.area_esquerda.winfo_height()
            if altura_esquerda > 0:
                y_esquerdo = int(altura_esquerda * ratios["esquerdo"])
                self.divisor_esquerdo.sash_place(0, 0, y_esquerdo)

            altura_lateral = self.painel_lateral.winfo_height()
            if altura_lateral > 0:
                y_lateral_1 = int(altura_lateral * ratios["lateral_1"])
                y_lateral_2 = int(altura_lateral * ratios["lateral_2"])

                self.divisor_lateral.sash_place(0, 0, y_lateral_1)
                self.divisor_lateral.sash_place(1, 0, y_lateral_2)

        finally:
            self.after(100, self._finalizar_aplicacao_layout_salvo)

    def _finalizar_aplicacao_layout_salvo(self):
        self._aplicando_layout_salvo = False
        self._salvar_layout_atual()

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

        # Ao abrir um novo arquivo, o programa anterior deixa de ser válido.
        self._instrucoes_montadas = None
        self.minha_cpu.resetar()

        # Reseta os painéis visuais ligados à execução anterior.
        self.painel_instrucoes.resetar()
        self.painel_registradores.resetar()
        self.painel_memoria.resetar()
        self.painel_editor.resetar_destaque()
        self.painel_terminal.limpar()

        # Atualiza os botões: Run, Step e Reset voltam a ficar desativados.
        self._atualizar_estado_botoes()

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
            self._atualizar_estado_botoes()
        except Exception as e:
            self._instrucoes_montadas = None
            self.painel_terminal.erro(str(e))
            self._atualizar_estado_botoes()
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
            self._atualizar_estado_botoes()

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
            self._atualizar_estado_botoes()

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
        self._atualizar_estado_botoes()