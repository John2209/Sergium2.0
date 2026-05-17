from cpu import CPU
from leitor import Parser

if __name__ == "__main__":
    minha_cpu = CPU()

    parser = Parser(r"C:\dev\mSergium\codigos\pTestCompleto.txt")
    instrucoes = parser.parsear()

    minha_cpu.carregar_programa(instrucoes)

    acabou = False

    while not acabou:
        acabou = minha_cpu.executar_instrucao()
        print("AC:", minha_cpu.ac)
        print("AUX:", minha_cpu.auxs)
        print("Z:", minha_cpu.z)
        print("P:", minha_cpu.p)
        print("PC:", minha_cpu.pc)
        print("---")
