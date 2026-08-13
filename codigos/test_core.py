import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.cpu import CPU
from core.parser import Parser
from core.instruction_set import (
    INSTRUCOES_VALIDAS,
    instrucao_existe,
    normalizar_mnemonico,
)
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

PASTA_TEMPORARIA = TemporaryDirectory(prefix="msergium_testes_")
PASTA_TESTES = Path(PASTA_TEMPORARIA.name)


def assert_lanca(erro_esperado, funcao, *args, **kwargs):
    try:
        funcao(*args, **kwargs)
    except erro_esperado:
        return

    assert False, f"Era esperado {erro_esperado.__name__}"


def criar_arquivo_teste(nome_arquivo, conteudo, encoding="utf-8"):
    caminho = PASTA_TESTES / nome_arquivo
    caminho.write_text(conteudo, encoding=encoding)

    return caminho


def divisao_truncada_esperada(dividendo, divisor):
    quociente = abs(dividendo) // abs(divisor)

    if (dividendo < 0) != (divisor < 0):
        quociente = -quociente

    return quociente


def modulo_truncado_esperado(dividendo, divisor):
    quociente = divisao_truncada_esperada(dividendo, divisor)
    return dividendo - divisor * quociente


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


def teste_matriz_multiplicacao_divisao_e_flags():
    for ac in range(-10, 11):
        for valor in range(-5, 6):
            casos_multiplicacao = (
                ("MUL AC * VAL => AC", str(valor), None),
                ("MUL AC * AUX => AC", "2", valor),
            )

            for mnemonico, operando, valor_auxiliar in casos_multiplicacao:
                cpu = CPU()
                cpu.carregar_programa({"0": (mnemonico, operando)})
                cpu.ac = ac

                if valor_auxiliar is not None:
                    cpu.auxs[2] = valor_auxiliar

                cpu.executar_instrucao()
                esperado = ac * valor

                assert cpu.ac == esperado
                assert cpu.z == int(esperado == 0)
                assert cpu.p == int(esperado > 0)
                assert cpu.finalizado is True

        for divisor in range(-5, 6):
            if divisor == 0:
                continue

            casos_divisao = (
                ("DIV AC / VAL => AC", str(divisor), None),
                ("DIV AC / AUX => AC", "3", divisor),
            )

            for mnemonico, operando, valor_auxiliar in casos_divisao:
                cpu = CPU()
                cpu.carregar_programa({"0": (mnemonico, operando)})
                cpu.ac = ac

                if valor_auxiliar is not None:
                    cpu.auxs[3] = valor_auxiliar

                cpu.executar_instrucao()
                esperado = divisao_truncada_esperada(ac, divisor)

                assert cpu.ac == esperado
                assert cpu.z == int(esperado == 0)
                assert cpu.p == int(esperado > 0)
                assert cpu.finalizado is True


def teste_matriz_modulo_e_flags():
    for ac in range(-20, 21):
        for divisor in range(-10, 11):
            if divisor == 0:
                continue

            casos = (
                ("MOD AC % VAL => AC", str(divisor), None),
                ("MOD AC % AUX => AC", "2", divisor),
            )

            for mnemonico, operando, valor_auxiliar in casos:
                cpu = CPU()
                cpu.carregar_programa({"0": (mnemonico, operando)})
                cpu.ac = ac

                if valor_auxiliar is not None:
                    cpu.auxs[2] = valor_auxiliar

                cpu.executar_instrucao()
                esperado = modulo_truncado_esperado(ac, divisor)

                assert cpu.ac == esperado
                assert cpu.z == int(esperado == 0)
                assert cpu.p == int(esperado > 0)
                assert abs(cpu.ac) < abs(divisor)

                if cpu.ac != 0:
                    assert (cpu.ac > 0) == (ac > 0)

                assert ac == divisor * divisao_truncada_esperada(ac, divisor) + cpu.ac
                assert cpu.finalizado is True


def teste_divisao_inteiros_muito_grandes():
    valor = 10 ** 500 + 123
    quociente = valor // 7

    casos = (
        (valor, "7", quociente),
        (-valor, "7", -quociente),
        (valor, "-7", -quociente),
        (-valor, "-7", quociente),
    )

    for dividendo, divisor, esperado in casos:
        cpu = CPU()
        cpu.carregar_programa({"0": ("DIV AC / VAL => AC", divisor)})
        cpu.ac = dividendo
        cpu.executar_instrucao()

        assert cpu.ac == esperado


def teste_modulo_inteiros_muito_grandes():
    valor = 10 ** 1000 + 987654321
    casos = (
        (valor, 97),
        (-valor, 97),
        (valor, -97),
        (-valor, -97),
    )

    for dividendo, divisor in casos:
        cpu = CPU()
        cpu.carregar_programa({"0": ("MOD AC % VAL => AC", str(divisor))})
        cpu.ac = dividendo
        cpu.executar_instrucao()

        esperado = modulo_truncado_esperado(dividendo, divisor)
        assert cpu.ac == esperado
        assert abs(cpu.ac) < abs(divisor)


def teste_divisao_por_zero_val_e_aux():
    casos = (
        ("DIV AC / VAL => AC", "0", None),
        ("DIV AC / AUX => AC", "1", 0),
    )

    for mnemonico, operando, valor_auxiliar in casos:
        cpu = CPU()
        cpu.carregar_programa({"0": (mnemonico, operando)})
        cpu.ac = 99

        if valor_auxiliar is not None:
            cpu.auxs[1] = valor_auxiliar

        assert_lanca(OperandoInvalidoError, cpu.executar_instrucao)
        assert cpu.ac == 99
        assert cpu.pc == 0
        assert cpu.finalizado is False


def teste_modulo_por_zero_val_e_aux():
    casos = (
        ("MOD AC % VAL => AC", "0", None),
        ("MOD AC % AUX => AC", "1", 0),
    )

    for mnemonico, operando, valor_auxiliar in casos:
        cpu = CPU()
        cpu.carregar_programa({"0": (mnemonico, operando)})
        cpu.ac = 99

        if valor_auxiliar is not None:
            cpu.auxs[1] = valor_auxiliar

        assert_lanca(OperandoInvalidoError, cpu.executar_instrucao)
        assert cpu.ac == 99
        assert cpu.pc == 0
        assert cpu.finalizado is False


def teste_novas_operacoes_rejeitam_operandos_invalidos():
    for mnemonico in (
        "MUL AC * VAL => AC",
        "DIV AC / VAL => AC",
        "MOD AC % VAL => AC",
    ):
        cpu = CPU()
        cpu.carregar_programa({"0": (mnemonico, "ABC")})
        assert_lanca(OperandoInvalidoError, cpu.executar_instrucao)

    for mnemonico in (
        "MUL AC * AUX => AC",
        "DIV AC / AUX => AC",
        "MOD AC % AUX => AC",
    ):
        for indice in ("-1", "4"):
            cpu = CPU()
            cpu.carregar_programa({"0": (mnemonico, indice)})
            assert_lanca(AuxiliarInvalidoError, cpu.executar_instrucao)

        cpu = CPU()
        cpu.carregar_programa({"0": (mnemonico, "ABC")})
        assert_lanca(OperandoInvalidoError, cpu.executar_instrucao)


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


def teste_termino_natural_na_ultima_instrucao():
    cpu = CPU()

    programa = {
        "0": ("COP VAL => AC", "10"),
    }

    cpu.carregar_programa(programa)

    terminou = cpu.executar_instrucao()

    assert terminou is True
    assert cpu.finalizado is True
    assert cpu.pc == 1


def teste_limite_exato_nao_e_loop_infinito():
    cpu = CPU()
    programa = {
        str(indice): ("COP VAL => AC", str(indice))
        for indice in range(1000)
    }

    cpu.carregar_programa(programa)

    terminou = cpu.executar_tudo(limite_instrucoes=1000)

    assert terminou is True
    assert cpu.finalizado is True
    assert cpu.pc == 1000
    assert cpu.ac == 999


def teste_preserva_todas_as_saidas():
    cpu = CPU()

    programa = {
        "0": ("COP VAL => AC", "1"),
        "1": ("SAI AC => PORTA", "2"),
        "2": ("COP VAL => AC", "2"),
        "3": ("SAI AC => PORTA", "2"),
        "4": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)
    cpu.executar_tudo()

    assert cpu.saida == 2
    assert cpu.consumir_saidas() == [1, 2]
    assert cpu.saida is None
    assert cpu.consumir_saidas() == []


def teste_consumir_saida_mantem_compatibilidade():
    cpu = CPU()

    programa = {
        "0": ("COP VAL => AC", "1"),
        "1": ("SAI AC => PORTA", "2"),
        "2": ("COP VAL => AC", "2"),
        "3": ("SAI AC => PORTA", "2"),
        "4": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)
    cpu.executar_tudo()

    assert cpu.consumir_saida() == 2
    assert cpu.saida is None
    assert cpu.consumir_saidas() == []


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


def teste_parser_executa_todas_novas_instrucoes():
    caminho = criar_arquivo_teste(
        "test_parser_mul_div_mod.txt",
        """
        | COP VAL => AC | 7
        | MUL AC*VAL=>AC | -3
        | COP AC => AUX | 0
        | COP VAL => AC | 100
        | DIV AC/AUX=>AC | 0
        | MUL AC*AUX=>AC | 0
        | DIV AC/VAL=>AC | 5
        | MOD AC%VAL=>AC | 7
        | MOD AC%AUX=>AC | 0
        | SAI AC => PORTA | 2
        | PARA | 0
        """,
    )

    programa = Parser(str(caminho)).parsear()
    mnemonicos = {mnemonico for mnemonico, _ in programa.values()}

    assert {
        "MUL AC * AUX => AC",
        "DIV AC / AUX => AC",
        "MUL AC * VAL => AC",
        "DIV AC / VAL => AC",
        "MOD AC % AUX => AC",
        "MOD AC % VAL => AC",
    } <= mnemonicos

    cpu = CPU()
    cpu.carregar_programa(programa)
    cpu.executar_tudo()

    assert cpu.ac == 2
    assert cpu.consumir_saidas() == [2]
    assert cpu.z == 0
    assert cpu.p == 1
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


def teste_parser_le_utf8_com_bom():
    caminho = criar_arquivo_teste(
        "test_parser_utf8_bom.txt",
        """início | COP VAL => AC | 7
        # comentário com acentuação
        fim | PARA | 0
        """,
        encoding="utf-8-sig",
    )

    parser = Parser(str(caminho))
    programa = parser.parsear()

    assert programa == {
        "INÍCIO": ("COP VAL => AC", "7"),
        "FIM": ("PARA", "0"),
    }


def teste_parser_ignora_comentario_com_separador():
    caminho = criar_arquivo_teste(
        "test_parser_comentario_separador.txt",
        """
        # formato: rótulo | mnemônico | operando
        # | isto também é apenas um comentário | mesmo com separadores

        | COP VAL => AC | 10
        | PARA | 0
        """,
    )

    parser = Parser(str(caminho))
    programa = parser.parsear()

    assert programa == {
        "0": ("COP VAL => AC", "10"),
        "1": ("PARA", "0"),
    }


def teste_parser_rejeita_linha_sem_separador():
    caminho = criar_arquivo_teste(
        "test_parser_sem_separador.txt",
        """
        | COP VAL => AC | 10
        esta linha não é uma instrução válida
        | PARA | 0
        """,
    )

    parser = Parser(str(caminho))

    assert_lanca(ParserError, parser.parsear)


def teste_parser_rejeita_programa_sem_instrucoes():
    caminho = criar_arquivo_teste(
        "test_parser_sem_instrucoes.txt",
        """

        # arquivo apenas com comentários
        # formato: rótulo | mnemônico | operando

        """,
    )

    parser = Parser(str(caminho))

    assert_lanca(ParserError, parser.parsear)


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
    assert normalizar_mnemonico("mul ac*aux=>ac") == "MUL AC * AUX => AC"
    assert normalizar_mnemonico("DIV AC/VAL=>AC") == "DIV AC / VAL => AC"
    assert normalizar_mnemonico("mod ac%aux=>ac") == "MOD AC % AUX => AC"
    assert normalizar_mnemonico("MOD AC%VAL=>AC") == "MOD AC % VAL => AC"
    assert normalizar_mnemonico("vai se z=1") == "VAI SE Z = 1"


def teste_instrucao_existe():
    assert instrucao_existe("COP AC=>MEM") is True
    assert instrucao_existe("SOM AC+VAL=>AC") is True
    assert instrucao_existe("MUL AC*AUX=>AC") is True
    assert instrucao_existe("DIV AC/VAL=>AC") is True
    assert instrucao_existe("MOD AC%AUX=>AC") is True
    assert instrucao_existe("MOD AC%VAL=>AC") is True
    assert instrucao_existe("banana") is False


def teste_dispatch_cobre_todo_instruction_set():
    assert set(CPU().dispatch_table) == INSTRUCOES_VALIDAS


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
    caminho = criar_arquivo_teste(
        "test_rotulo_duplicado.txt",
        """
        inicio | COP VAL => AC | 10
        inicio | SAI AC => PORTA | 2
        | PARA | 0
        """,
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
    ("teste_matriz_multiplicacao_divisao_e_flags", teste_matriz_multiplicacao_divisao_e_flags),
    ("teste_matriz_modulo_e_flags", teste_matriz_modulo_e_flags),
    ("teste_divisao_inteiros_muito_grandes", teste_divisao_inteiros_muito_grandes),
    ("teste_modulo_inteiros_muito_grandes", teste_modulo_inteiros_muito_grandes),
    ("teste_divisao_por_zero_val_e_aux", teste_divisao_por_zero_val_e_aux),
    ("teste_modulo_por_zero_val_e_aux", teste_modulo_por_zero_val_e_aux),
    ("teste_novas_operacoes_rejeitam_operandos_invalidos", teste_novas_operacoes_rejeitam_operandos_invalidos),
    ("teste_desvio_condicional", teste_desvio_condicional),
    ("teste_entrada_saida", teste_entrada_saida),
    ("teste_parser_com_cpu", teste_parser_com_cpu),
    ("teste_parser_executa_todas_novas_instrucoes", teste_parser_executa_todas_novas_instrucoes),
    ("teste_parser_aceita_linha_sem_rotulo", teste_parser_aceita_linha_sem_rotulo),
    ("teste_parser_mapeia_linhas_originais", teste_parser_mapeia_linhas_originais),
    ("teste_duas_entradas_step_by_step", teste_duas_entradas_step_by_step),
    ("teste_snapshot_basico", teste_snapshot_basico),
    ("teste_normalizar_mnemonico", teste_normalizar_mnemonico),
    ("teste_instrucao_existe", teste_instrucao_existe),
    ("teste_dispatch_cobre_todo_instruction_set", teste_dispatch_cobre_todo_instruction_set),
    ("teste_auxiliar_invalido", teste_auxiliar_invalido),
    ("teste_memoria_invalida", teste_memoria_invalida),
    ("teste_operando_nao_numerico", teste_operando_nao_numerico),
    ("teste_porta_saida_invalida", teste_porta_saida_invalida),
    ("teste_executar_tudo", teste_executar_tudo),
    ("teste_termino_natural_na_ultima_instrucao", teste_termino_natural_na_ultima_instrucao),
    ("teste_limite_exato_nao_e_loop_infinito", teste_limite_exato_nao_e_loop_infinito),
    ("teste_preserva_todas_as_saidas", teste_preserva_todas_as_saidas),
    ("teste_consumir_saida_mantem_compatibilidade", teste_consumir_saida_mantem_compatibilidade),
    ("teste_loop_infinito", teste_loop_infinito),
    ("teste_entrada_necessaria", teste_entrada_necessaria),
    ("teste_definir_entrada", teste_definir_entrada),
    ("teste_parser_rotulo_duplicado", teste_parser_rotulo_duplicado),
    ("teste_parser_le_utf8_com_bom", teste_parser_le_utf8_com_bom),
    ("teste_parser_ignora_comentario_com_separador", teste_parser_ignora_comentario_com_separador),
    ("teste_parser_rejeita_linha_sem_separador", teste_parser_rejeita_linha_sem_separador),
    ("teste_parser_rejeita_programa_sem_instrucoes", teste_parser_rejeita_programa_sem_instrucoes),
    ("teste_parser_rejeita_instrucao_desconhecida", teste_parser_rejeita_instrucao_desconhecida),
    ("teste_parser_rejeita_linha_com_formato_invalido", teste_parser_rejeita_linha_com_formato_invalido),
    ("teste_imports_publicos_do_core", teste_imports_publicos_do_core),
]


if __name__ == "__main__":
    for nome, teste in TESTES:
        teste()
        print(f"{nome} passou")

    print("Todos os testes passaram.")
