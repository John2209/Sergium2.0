import sys
import tkinter as tk
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.cpu import CPU
from ui.app import App


PROGRAMA_SIMPLES = """
| COP VAL => AC | 1
| SAI AC => PORTA | 2
| PARA | 0
"""

app = None


def preparar_app():
    app._acao_reset()
    app.painel_editor.set_texto("")
    app.painel_terminal.limpar()
    app.painel_terminal.campo_entrada.delete(0, "end")
    app._caminho_arquivo = None
    app.update()


def montar(texto):
    app.painel_editor.set_texto(texto)
    app._acao_montar()
    app.update()


def texto_terminal():
    return app.painel_terminal.texto.get("1.0", "end")


class TemporarioComFalhaNaEscrita:
    def __init__(self, caminho):
        self.name = str(caminho)

    def __enter__(self):
        Path(self.name).touch()
        return self

    def __exit__(self, tipo, valor, traceback):
        return False

    def write(self, texto):
        raise OSError("disco cheio")


def teste_abrir_com_erro_preserva_arquivo_e_editor():
    preparar_app()
    app.painel_editor.set_texto("conteúdo anterior")
    app._caminho_arquivo = "arquivo-anterior.srg"

    with TemporaryDirectory(prefix="msergium_ui_") as pasta:
        caminho = Path(pasta) / "invalido.srg"
        caminho.write_bytes(b"\xff\xfe\x00")

        with patch("ui.app.filedialog.askopenfilename", return_value=str(caminho)):
            app._acao_abrir()

    assert app._caminho_arquivo == "arquivo-anterior.srg"
    assert app.painel_editor.get_texto() == "conteúdo anterior"
    assert "Não foi possível abrir" in texto_terminal()


def teste_salvar_com_erro_nao_atualiza_caminho():
    preparar_app()
    app.painel_editor.set_texto("| PARA | 0")

    with TemporaryDirectory(prefix="msergium_ui_") as pasta:
        caminho = Path(pasta) / "pasta-inexistente" / "programa.srg"

        with patch("ui.app.filedialog.asksaveasfilename", return_value=str(caminho)):
            app._acao_salvar()

    assert app._caminho_arquivo is None
    assert "Não foi possível salvar" in texto_terminal()


def teste_salvar_grava_utf8_e_atualiza_caminho():
    preparar_app()
    app.painel_editor.set_texto("início | PARA | 0")

    with TemporaryDirectory(prefix="msergium_ui_") as pasta:
        caminho = Path(pasta) / "programa.srg"

        with patch("ui.app.filedialog.asksaveasfilename", return_value=str(caminho)):
            app._acao_salvar()

        assert caminho.read_text(encoding="utf-8") == "início | PARA | 0"
        assert app._caminho_arquivo == str(caminho)


def teste_falha_ao_substituir_preserva_arquivo_original():
    preparar_app()

    with TemporaryDirectory(prefix="msergium_ui_") as pasta:
        caminho = Path(pasta) / "programa.srg"
        caminho.write_text("conteúdo original", encoding="utf-8")
        app._caminho_arquivo = str(caminho)
        app.painel_editor.set_texto("novo conteúdo")

        with patch("ui.app.os.replace", side_effect=OSError("arquivo ocupado")):
            app._acao_salvar()

        assert caminho.read_text(encoding="utf-8") == "conteúdo original"
        assert not list(Path(pasta).glob(".sergium_*.tmp"))
        assert "Não foi possível salvar" in texto_terminal()


def teste_falha_na_escrita_remove_temporario_de_salvamento():
    preparar_app()
    app.painel_editor.set_texto("| PARA | 0")

    with TemporaryDirectory(prefix="msergium_ui_") as pasta:
        caminho = Path(pasta) / "programa.srg"
        caminho_tmp = Path(pasta) / ".sergium_falha.tmp"
        temporario = TemporarioComFalhaNaEscrita(caminho_tmp)

        with (
            patch("ui.app.filedialog.asksaveasfilename", return_value=str(caminho)),
            patch("ui.app.tempfile.NamedTemporaryFile", return_value=temporario),
        ):
            app._acao_salvar()

        assert not caminho_tmp.exists()

    assert app._caminho_arquivo is None
    assert "Não foi possível salvar" in texto_terminal()


def teste_falha_na_escrita_remove_temporario_de_montagem():
    preparar_app()
    app.painel_editor.set_texto("| PARA | 0")

    with TemporaryDirectory(prefix="msergium_ui_") as pasta:
        caminho_tmp = Path(pasta) / "montagem_falha.srg"
        temporario = TemporarioComFalhaNaEscrita(caminho_tmp)

        with patch(
            "ui.app.tempfile.NamedTemporaryFile", return_value=temporario
        ):
            app._acao_montar()

        assert not caminho_tmp.exists()

    assert app._instrucoes_montadas is None
    assert app.minha_cpu.instrucoes == {}
    assert "disco cheio" in texto_terminal()


def teste_edicao_invalida_montagem():
    preparar_app()
    montar(PROGRAMA_SIMPLES)
    assert app.botao_run.cget("state") == "normal"

    app.painel_editor.editor.insert("end", "\n# alteração")
    app.update()

    assert app._instrucoes_montadas is None
    assert app.minha_cpu.instrucoes == {}
    assert app.botao_run.cget("state") == "disabled"
    assert app.botao_step.cget("state") == "disabled"
    assert "Monte o programa novamente" in texto_terminal()


def teste_remontagem_invalida_limpa_estado_anterior():
    preparar_app()
    montar(PROGRAMA_SIMPLES)
    assert app.minha_cpu.instrucoes

    app.painel_editor.set_texto("BANANA | 0")
    app._acao_montar()
    app.update()

    assert app._instrucoes_montadas is None
    assert app.minha_cpu.instrucoes == {}
    assert app.painel_instrucoes.tree.get_children() == ()
    assert app.botao_reset.cget("state") == "disabled"


def teste_programa_sem_instrucoes_nao_monta():
    preparar_app()
    montar("# apenas comentário\n# formato: rótulo | mnemônico | operando")

    assert app._instrucoes_montadas is None
    assert app.botao_run.cget("state") == "disabled"
    assert "não contém instruções" in texto_terminal()


def teste_run_mostra_todas_as_saidas():
    preparar_app()
    montar(
        """
        | COP VAL => AC | 1
        | SAI AC => PORTA | 2
        | COP VAL => AC | 2
        | SAI AC => PORTA | 2
        | PARA | 0
        """,
    )

    app._acao_run()
    log = texto_terminal()

    assert "Saída: 1" in log
    assert "Saída: 2" in log
    assert log.index("Saída: 1") < log.index("Saída: 2")


def teste_entrada_retorna_execucao_run():
    preparar_app()
    montar(
        """
        | ENT PORTA => AC | 0
        | SAI AC => PORTA | 2
        | PARA | 0
        """,
    )

    app._acao_run()
    assert app._modo_entrada_pendente == "run"

    app.painel_terminal.campo_entrada.insert(0, "7")
    app.painel_terminal._enviar_entrada()
    app.update()

    assert app.minha_cpu.finalizado is True
    assert app.painel_terminal.valor_saida.cget("text") == "7"
    assert app.painel_terminal.campo_entrada.get() == ""
    log = texto_terminal()
    assert log.index("Entrada definida: 7") < log.index("Saída: 7")
    assert log.index("Saída: 7") < log.index("Programa finalizado")


def teste_entrada_no_step_executa_somente_ent():
    preparar_app()
    montar(
        """
        | ENT PORTA => AC | 0
        | SOM AC + VAL => AC | 1
        | PARA | 0
        """,
    )

    app._acao_step()
    assert app._modo_entrada_pendente == "step"

    app.painel_terminal.campo_entrada.insert(0, "5")
    app.painel_terminal._enviar_entrada()
    app.update()

    assert app.minha_cpu.pc == 1
    assert app.minha_cpu.ac == 5
    assert app.minha_cpu.finalizado is False


def teste_entradas_consecutivas_mantem_ordem_do_terminal():
    preparar_app()
    montar(
        """
        | ENT PORTA => AC | 0
        | COP AC => AUX | 0
        | ENT PORTA => AC | 0
        | SOM AC + AUX => AC | 0
        | SAI AC => PORTA | 2
        | PARA | 0
        """,
    )

    app._acao_run()
    app.painel_terminal.campo_entrada.insert(0, "3")
    app.painel_terminal._enviar_entrada()
    app.update()

    log = texto_terminal()
    mensagem_pausa = "Programa pausado. Aguardando valor de entrada."
    primeira_pausa = log.index(mensagem_pausa)
    entrada = log.index("Entrada definida: 3")
    segunda_pausa = log.index(mensagem_pausa, primeira_pausa + 1)
    assert primeira_pausa < entrada < segunda_pausa
    assert app._modo_entrada_pendente == "run"

    app.painel_terminal.campo_entrada.insert(0, "4")
    app.painel_terminal._enviar_entrada()
    app.update()

    log = texto_terminal()
    assert log.index("Entrada definida: 4") < log.index("Saída: 7")
    assert log.index("Saída: 7") < log.index("Programa finalizado")
    assert app.minha_cpu.finalizado is True


def teste_entrada_invalida_e_preservada():
    preparar_app()
    montar("| ENT PORTA => AC | 0\n| PARA | 0")
    app._acao_run()

    app.painel_terminal.campo_entrada.insert(0, "abc")
    app.painel_terminal._enviar_entrada()
    app.update()

    log = texto_terminal()
    assert app.painel_terminal.campo_entrada.get() == "abc"
    assert "Entrada definida: abc" not in log
    assert "Operando inválido" in log
    assert app._modo_entrada_pendente == "run"


def teste_erro_de_execucao_bloqueia_run_e_step():
    preparar_app()
    montar("| COP VAL => AC | ABC\n| PARA | 0")

    app._acao_run()

    assert app._erro_execucao is True
    assert app.botao_run.cget("state") == "disabled"
    assert app.botao_step.cget("state") == "disabled"
    assert app.botao_reset.cget("state") == "normal"


def teste_troca_de_texto_limpa_historico_undo():
    preparar_app()
    app.painel_editor.set_texto("arquivo antigo")
    app.painel_editor.set_texto("arquivo novo")

    try:
        app.painel_editor.editor.edit_undo()
    except tk.TclError:
        pass

    assert app.painel_editor.get_texto() == "arquivo novo"


def teste_numeracao_permanece_alinhada():
    preparar_app()
    app.painel_editor.set_texto("\n".join(f"linha {i}" for i in range(1, 41)))
    app.painel_editor.editor.see("20.0")
    app.painel_editor.nums.see("20.0")
    app.update()

    info_editor = app.painel_editor.editor.dlineinfo("20.0")
    info_nums = app.painel_editor.nums.dlineinfo("20.0")

    assert info_editor is not None
    assert info_nums is not None
    assert abs(info_editor[1] - info_nums[1]) <= 1


def teste_scroll_pequeno_e_simetrico():
    preparar_app()
    app.painel_editor.set_texto("\n".join(f"linha {i}" for i in range(1, 101)))
    app.update()

    app.painel_editor.editor.yview_moveto(0.5)
    app.painel_editor.nums.yview_moveto(0.5)
    app.update()
    origem = app.painel_editor.editor.yview()[0]

    app.painel_editor._on_scroll_mouse(SimpleNamespace(delta=1, num=None))
    app.update()
    posicao_positiva = app.painel_editor.editor.yview()[0]

    app.painel_editor.editor.yview_moveto(0.5)
    app.painel_editor.nums.yview_moveto(0.5)
    app.update()
    app.painel_editor._on_scroll_mouse(SimpleNamespace(delta=-1, num=None))
    app.update()
    posicao_negativa = app.painel_editor.editor.yview()[0]

    assert posicao_positiva < origem
    assert posicao_negativa > origem


def teste_finalizacao_remove_destaque_da_instrucao():
    preparar_app()
    montar("| PARA | 0")
    app._acao_run()
    app.update()

    assert not app.painel_instrucoes.tree.item("0", "tags")


def teste_montagem_inicial_nao_destaca_registradores():
    preparar_app()
    montar("| PARA | 0")

    for _, _, card in app.painel_registradores._labels.values():
        assert card.cget("fg_color") == app.painel_registradores.COR_CARD


def teste_ciclos_repetidos_de_montagem_e_invalidacao():
    preparar_app()

    for valor in range(25):
        montar(
            f"""
            | COP VAL => AC | {valor}
            | SAI AC => PORTA | 2
            | PARA | 0
            """
        )
        app._acao_run()
        app.update()

        assert app.minha_cpu.finalizado is True
        assert app.painel_terminal.valor_saida.cget("text") == str(valor)

        app.painel_editor.editor.insert("end", "\n# alteração")
        app.update()

        assert app._instrucoes_montadas is None
        assert app.botao_run.cget("state") == "disabled"


TESTES = [
    ("teste_abrir_com_erro_preserva_arquivo_e_editor", teste_abrir_com_erro_preserva_arquivo_e_editor),
    ("teste_salvar_com_erro_nao_atualiza_caminho", teste_salvar_com_erro_nao_atualiza_caminho),
    ("teste_salvar_grava_utf8_e_atualiza_caminho", teste_salvar_grava_utf8_e_atualiza_caminho),
    ("teste_falha_ao_substituir_preserva_arquivo_original", teste_falha_ao_substituir_preserva_arquivo_original),
    ("teste_falha_na_escrita_remove_temporario_de_salvamento", teste_falha_na_escrita_remove_temporario_de_salvamento),
    ("teste_falha_na_escrita_remove_temporario_de_montagem", teste_falha_na_escrita_remove_temporario_de_montagem),
    ("teste_edicao_invalida_montagem", teste_edicao_invalida_montagem),
    ("teste_remontagem_invalida_limpa_estado_anterior", teste_remontagem_invalida_limpa_estado_anterior),
    ("teste_programa_sem_instrucoes_nao_monta", teste_programa_sem_instrucoes_nao_monta),
    ("teste_run_mostra_todas_as_saidas", teste_run_mostra_todas_as_saidas),
    ("teste_entrada_retorna_execucao_run", teste_entrada_retorna_execucao_run),
    ("teste_entrada_no_step_executa_somente_ent", teste_entrada_no_step_executa_somente_ent),
    ("teste_entradas_consecutivas_mantem_ordem_do_terminal", teste_entradas_consecutivas_mantem_ordem_do_terminal),
    ("teste_entrada_invalida_e_preservada", teste_entrada_invalida_e_preservada),
    ("teste_erro_de_execucao_bloqueia_run_e_step", teste_erro_de_execucao_bloqueia_run_e_step),
    ("teste_troca_de_texto_limpa_historico_undo", teste_troca_de_texto_limpa_historico_undo),
    ("teste_numeracao_permanece_alinhada", teste_numeracao_permanece_alinhada),
    ("teste_scroll_pequeno_e_simetrico", teste_scroll_pequeno_e_simetrico),
    ("teste_finalizacao_remove_destaque_da_instrucao", teste_finalizacao_remove_destaque_da_instrucao),
    ("teste_montagem_inicial_nao_destaca_registradores", teste_montagem_inicial_nao_destaca_registradores),
    ("teste_ciclos_repetidos_de_montagem_e_invalidacao", teste_ciclos_repetidos_de_montagem_e_invalidacao),
]


def setup_module():
    global app
    app = App(CPU())
    app.geometry("1180x700+10000+10000")

    try:
        app.attributes("-alpha", 0.0)
    except tk.TclError:
        pass

    app.update()


def teardown_module():
    global app
    if app is not None:
        app.destroy()
        app = None


if __name__ == "__main__":
    setup_module()

    try:
        for nome, teste in TESTES:
            teste()
            print(f"{nome} passou")

        print("Todos os testes da interface passaram.")
    finally:
        teardown_module()
