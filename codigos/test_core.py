import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.cpu import CPU
from core.parser import Parser
from core.instruction_set import normalizar_mnemonico, instrucao_existe
from core.errors import (
    ParserError,
    OperandoInvalidoError,
    AuxiliarInvalidoError,
    MemoriaInvalidaError,
    PortaInvalidaError,
    LoopInfinitoError,
    EntradaNecessariaError,
)


# =========================
# FUNÇÕES AUXILIARES
# =========================

def assert_lanca(erro_esperado, funcao, *args, **kwargs):
    try:
        funcao(*args, **kwargs)
    except erro_esperado:
        return

    assert False, f"Era esperado {erro_esperado.__name__}"


def criar_arquivo_teste(nome_arquivo, conteudo):
    pasta = Path("codigos")
    pasta.mkdir(exist_ok=True)

    caminho = pasta / nome_arquivo
    caminho.write_text(conteudo, encoding="utf-8")

    return caminho


# =========================
# TESTES DA CPU
# =========================

def teste_copia_aritmetica_saida():
    cpu = CPU()

    programa = {
        "0": ("COP VAL => AC", "10"),
        "1": ("SOM AC + VAL => AC", "5"),
        "2": ("SAI AC => PORTA", "2"),
        "3": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)
    cpu.executar_tudo()

    assert cpu.ac == 15
    assert cpu.saida == 15
    assert cpu.finalizado is True


def teste_flags_zero():
    cpu = CPU()

    programa = {
        "0": ("COP VAL => AC", "10"),
        "1": ("SUB AC - VAL => AC", "10"),
        "2": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)
    cpu.executar_tudo()

    assert cpu.ac == 0
    assert cpu.z == 1
    assert cpu.p == 0
    assert cpu.finalizado is True


def teste_desvio_condicional():
    cpu = CPU()

    programa = {
        "0": ("COP VAL => AC", "0"),
        "1": ("SOM AC + VAL => AC", "0"),
        "2": ("VAI SE Z = 1", "CASO2"),
        "CASO1": ("COP VAL => AC", "111"),
        "4": ("VAI", "FIM"),
        "CASO2": ("COP VAL => AC", "999"),
        "FIM": ("SAI AC => PORTA", "2"),
        "7": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)
    cpu.executar_tudo()

    assert cpu.ac == 999
    assert cpu.saida == 999
    assert cpu.finalizado is True


def teste_entrada_saida():
    cpu = CPU()

    programa = {
        "0": ("ENT PORTA => AC", "0"),
        "1": ("SAI AC => PORTA", "2"),
        "2": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)
    cpu.definir_entrada(42)
    cpu.executar_tudo()

    assert cpu.ac == 42
    assert cpu.saida == 42
    assert cpu.finalizado is True


def teste_duas_entradas_step_by_step():
    cpu = CPU()

    programa = {
        "0": ("ENT PORTA => AC", "0"),
        "1": ("COP AC => AUX", "0"),
        "2": ("ENT PORTA => AC", "0"),
        "3": ("SOM AC + AUX => AC", "0"),
        "4": ("SAI AC => PORTA", "2"),
        "5": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)

    cpu.definir_entrada(10)
    terminou = cpu.executar_instrucao()
    assert terminou is False
    assert cpu.ac == 10

    terminou = cpu.executar_instrucao()
    assert terminou is False
    assert cpu.auxs[0] == 10

    cpu.definir_entrada(7)
    terminou = cpu.executar_instrucao()
    assert terminou is False
    assert cpu.ac == 7

    cpu.executar_tudo()

    assert cpu.ac == 17
    assert cpu.saida == 17
    assert cpu.finalizado is True


def teste_executar_tudo():
    cpu = CPU()

    programa = {
        "0": ("COP VAL => AC", "10"),
        "1": ("SOM AC + VAL => AC", "5"),
        "2": ("SAI AC => PORTA", "2"),
        "3": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)

    terminou = cpu.executar_tudo()

    assert terminou is True
    assert cpu.finalizado is True
    assert cpu.ac == 15
    assert cpu.saida == 15


def teste_loop_infinito():
    cpu = CPU()

    programa = {
        "inicio": ("VAI", "inicio"),
    }

    cpu.carregar_programa(programa)

    assert_lanca(LoopInfinitoError, cpu.executar_tudo, limite_instrucoes=10)


def teste_entrada_necessaria():
    cpu = CPU()

    programa = {
        "0": ("ENT PORTA => AC", "0"),
        "1": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)

    assert_lanca(EntradaNecessariaError, cpu.executar_instrucao)


def teste_definir_entrada():
    cpu = CPU()

    programa = {
        "0": ("ENT PORTA => AC", "0"),
        "1": ("SAI AC => PORTA", "2"),
        "2": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)

    cpu.definir_entrada(42)
    cpu.executar_tudo()

    assert cpu.ac == 42
    assert cpu.saida == 42
    assert cpu.finalizado is True


# =========================
# TESTES DE SNAPSHOT
# =========================

def teste_snapshot_basico():
    cpu = CPU()

    programa = {
        "0": ("COP VAL => AC", "7"),
        "1": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)

    estado = cpu.snapshot()

    assert estado.pc == 0
    assert estado.ac == 0
    assert estado.finalizado is False
    assert estado.rotulo_atual == "0"
    assert estado.mnemonico_atual == "COP VAL => AC"
    assert estado.operando_atual == "7"

    cpu.executar_instrucao()
    estado = cpu.snapshot()

    assert estado.pc == 1
    assert estado.ac == 7
    assert estado.finalizado is False
    assert estado.rotulo_atual == "1"
    assert estado.mnemonico_atual == "PARA"
    assert estado.operando_atual == "0"

    cpu.executar_instrucao()
    estado = cpu.snapshot()

    assert estado.finalizado is True


# =========================
# TESTES DO PARSER
# =========================

def teste_parser_com_cpu():
    caminho = criar_arquivo_teste(
        "test_parser_cpu.txt",
        """
        | COP VAL => AC | 10
        | SOM AC + VAL => AC | 5
        | SAI AC => PORTA | 2
        | PARA | 0
        """,
    )

    parser = Parser(str(caminho))
    programa = parser.parsear()

    cpu = CPU()
    cpu.carregar_programa(programa)
    cpu.executar_tudo()

    assert cpu.ac == 15
    assert cpu.saida == 15
    assert cpu.finalizado is True


def teste_parser_aceita_linha_sem_rotulo():
    caminho = criar_arquivo_teste(
        "test_parser_sem_rotulo.txt",
        """
        COP VAL => AC | 10
        PARA | 0
        """,
    )

    try:
        parser = Parser(str(caminho))
        programa = parser.parsear()

        assert programa == {
            "0": ("COP VAL => AC", "10"),
            "1": ("PARA", "0"),
        }
    finally:
        caminho.unlink(missing_ok=True)


def teste_parser_mapeia_linhas_originais():
    caminho = criar_arquivo_teste(
        "test_parser_linhas_originais.txt",
        """
        # comentario

        inicio | COP VAL => AC | 10

        SAI AC => PORTA | 2
        """,
    )

    try:
        parser = Parser(str(caminho))
        parser.parsear()

        assert parser.linhas_origem == {
            "INICIO": 4,
            "1": 6,
        }
    finally:
        caminho.unlink(missing_ok=True)


def teste_parser_rejeita_instrucao_desconhecida():
    caminho = criar_arquivo_teste(
        "test_instrucao_invalida.txt",
        """
        | BANANA | 0
        """,
    )

    parser = Parser(str(caminho))

    assert_lanca(ParserError, parser.parsear)


def teste_parser_rejeita_linha_com_formato_invalido():
    caminho = criar_arquivo_teste(
        "test_linha_invalida.txt",
        """
        | COP VAL => AC
        """,
    )

    parser = Parser(str(caminho))

    assert_lanca(ParserError, parser.parsear)


# =========================
# TESTES DO INSTRUCTION SET
# =========================

def teste_normalizar_mnemonico():
    assert normalizar_mnemonico("cop ac=>mem") == "COP AC => MEM"
    assert normalizar_mnemonico("SOM AC+VAL=>AC") == "SOM AC + VAL => AC"
    assert normalizar_mnemonico("vai se z=1") == "VAI SE Z = 1"


def teste_instrucao_existe():
    assert instrucao_existe("COP AC=>MEM") is True
    assert instrucao_existe("SOM AC+VAL=>AC") is True
    assert instrucao_existe("banana") is False


# =========================
# TESTES DE ERROS DA CPU
# =========================

def teste_auxiliar_invalido():
    cpu = CPU()

    programa = {
        "0": ("COP AC => AUX", "4"),
        "1": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)

    assert_lanca(AuxiliarInvalidoError, cpu.executar_instrucao)


def teste_memoria_invalida():
    cpu = CPU()

    programa = {
        "0": ("COP AC => MEM", "256"),
        "1": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)

    assert_lanca(MemoriaInvalidaError, cpu.executar_instrucao)


def teste_operando_nao_numerico():
    cpu = CPU()

    programa = {
        "0": ("COP VAL => AC", "ABC"),
        "1": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)

    assert_lanca(OperandoInvalidoError, cpu.executar_instrucao)


def teste_porta_saida_invalida():
    cpu = CPU()

    programa = {
        "0": ("SAI AC => PORTA", "1"),
        "1": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)

    assert_lanca(PortaInvalidaError, cpu.executar_instrucao)


def teste_parser_rotulo_duplicado():
    caminho = Path("codigos/test_rotulo_duplicado.txt")

    caminho.write_text(
        """
        inicio | COP VAL => AC | 10
        inicio | SAI AC => PORTA | 2
        | PARA | 0
        """,
        encoding="utf-8"
    )

    parser = Parser(str(caminho))

    assert_lanca(ParserError, parser.parsear)


def teste_imports_publicos_do_core():
    from core import CPU, Parser, EntradaNecessariaError, Snapshot

    assert CPU is not None
    assert Parser is not None
    assert EntradaNecessariaError is not None
    assert Snapshot is not None


# =========================
# EXECUÇÃO DOS TESTES
# =========================

TESTES = [
    ("teste_copia_aritmetica_saida", teste_copia_aritmetica_saida),
    ("teste_flags_zero", teste_flags_zero),
    ("teste_desvio_condicional", teste_desvio_condicional),
    ("teste_entrada_saida", teste_entrada_saida),
    ("teste_parser_com_cpu", teste_parser_com_cpu),
    ("teste_parser_aceita_linha_sem_rotulo", teste_parser_aceita_linha_sem_rotulo),
    ("teste_parser_mapeia_linhas_originais", teste_parser_mapeia_linhas_originais),
    ("teste_duas_entradas_step_by_step", teste_duas_entradas_step_by_step),
    ("teste_snapshot_basico", teste_snapshot_basico),
    ("teste_normalizar_mnemonico", teste_normalizar_mnemonico),
    ("teste_instrucao_existe", teste_instrucao_existe),
    ("teste_auxiliar_invalido", teste_auxiliar_invalido),
    ("teste_memoria_invalida", teste_memoria_invalida),
    ("teste_operando_nao_numerico", teste_operando_nao_numerico),
    ("teste_porta_saida_invalida", teste_porta_saida_invalida),
    ("teste_executar_tudo", teste_executar_tudo),
    ("teste_loop_infinito", teste_loop_infinito),
    ("teste_entrada_necessaria", teste_entrada_necessaria),
    ("teste_definir_entrada", teste_definir_entrada),
    ("teste_parser_rotulo_duplicado", teste_parser_rotulo_duplicado),
    ("teste_imports_publicos_do_core", teste_imports_publicos_do_core),
]


if __name__ == "__main__":
    for nome, teste in TESTES:
        teste()
        print(f"{nome} passou")

    print("Todos os testes passaram.")
