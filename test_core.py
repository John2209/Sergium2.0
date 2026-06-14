from core.cpu import CPU
from pathlib import Path
from core.parser import Parser



def executar_ate_o_fim(cpu, limite=100):
    passos = 0
    terminou = False

    while not terminou:
        terminou = cpu.executar_instrucao()
        passos += 1

        if passos > limite:
            raise RuntimeError("Possível loop infinito. Limite de execução excedido.")

    return passos


def teste_copia_aritmetica_saida():
    cpu = CPU()

    programa = {
        "0": ("COP VAL => AC", "10"),
        "1": ("SOM AC + VAL => AC", "5"),
        "2": ("SAI AC => PORTA", "2"),
        "3": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)
    executar_ate_o_fim(cpu)

    assert cpu.ac == 15
    assert cpu.saida == 15

    print("teste_copia_aritmetica_saida passou")


def teste_flags_zero():
    cpu = CPU()

    programa = {
        "0": ("COP VAL => AC", "10"),
        "1": ("SUB AC - VAL => AC", "10"),
        "2": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)
    executar_ate_o_fim(cpu)

    assert cpu.ac == 0
    assert cpu.z == 1
    assert cpu.p == 0

    print("teste_flags_zero passou")


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
    executar_ate_o_fim(cpu)

    assert cpu.ac == 999
    assert cpu.saida == 999

    print("teste_desvio_condicional passou")

def teste_entrada_saida():
    cpu = CPU()

    programa = {
        "0": ("ENT PORTA => AC", "0"),
        "1": ("SAI AC => PORTA", "2"),
        "2": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)
    cpu.entrada = 42

    executar_ate_o_fim(cpu)

    assert cpu.ac == 42
    assert cpu.saida == 42

    print("teste_entrada_saida passou")


def teste_entrada_saida():
    cpu = CPU()

    programa = {
        "0": ("ENT PORTA => AC", "0"),
        "1": ("SAI AC => PORTA", "2"),
        "2": ("PARA", "0"),
    }

    cpu.carregar_programa(programa)
    cpu.entrada = 42

    executar_ate_o_fim(cpu)

    assert cpu.ac == 42
    assert cpu.saida == 42

    print("teste_entrada_saida passou")

def teste_parser_com_cpu():
    caminho = Path("codigos/test_parser_cpu.txt")

    caminho.write_text(
        """
        | COP VAL => AC | 10
        | SOM AC + VAL => AC | 5
        | SAI AC => PORTA | 2
        | PARA | 0
        """,
        encoding="utf-8"
    )

    parser = Parser(str(caminho))
    programa = parser.parsear()

    cpu = CPU()
    cpu.carregar_programa(programa)

    executar_ate_o_fim(cpu)

    assert cpu.ac == 15
    assert cpu.saida == 15

    print("teste_parser_com_cpu passou")


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

    cpu.entrada = 10
    terminou = cpu.executar_instrucao()
    assert terminou is False
    assert cpu.ac == 10

    terminou = cpu.executar_instrucao()
    assert terminou is False
    assert cpu.auxs[0] == 10

    cpu.entrada = 7
    terminou = cpu.executar_instrucao()
    assert terminou is False
    assert cpu.ac == 7

    executar_ate_o_fim(cpu)

    assert cpu.ac == 17
    assert cpu.saida == 17

    print("teste_duas_entradas_step_by_step passou")

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

    cpu.entrada = 10
    terminou = cpu.executar_instrucao()
    assert terminou is False
    assert cpu.ac == 10

    terminou = cpu.executar_instrucao()
    assert terminou is False
    assert cpu.auxs[0] == 10

    cpu.entrada = 7
    terminou = cpu.executar_instrucao()
    assert terminou is False
    assert cpu.ac == 7

    executar_ate_o_fim(cpu)

    assert cpu.ac == 17
    assert cpu.saida == 17

    print("teste_duas_entradas_step_by_step passou")

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

if __name__ == "__main__":
    teste_copia_aritmetica_saida()
    print("teste_copia_aritmetica_saida passou")

    teste_flags_zero()
    print("teste_flags_zero passou")

    teste_desvio_condicional()
    print("teste_desvio_condicional passou")

    teste_entrada_saida()
    print("teste_entrada_saida passou")

    teste_parser_com_cpu()
    print("teste_parser_com_cpu passou")

    teste_duas_entradas_step_by_step()
    print("teste_duas_entradas_step_by_step passou")

    teste_snapshot_basico()
    print("teste_snapshot_basico passou")

    print("Todos os testes passaram.")
