# Implementa a CPU do Sergium

class CPU:
    def __init__(self):     ## inicializa a CPU com valores padrão
        self.resetar()

    def resetar(self):      ##
        self.auxs = [0] * 4             # array de auxiliares
        self.mem = [0] * 256            # memória principal
        self.instrucoes = {}            # dicionário de instruções
        self.entrada = 0                # valor de entrada fornecido externamente (I/O)
        self.saida = None               # valor de saida do Sergium
        self.flag_entrada = False       # indica se há um valor de entrada aguardando leitura
        self.ac = 0                     # acumulador
        self.z = 0                      # 1 se o último resultado aritmético foi zero
        self.p = 0                      # 1 se o último resultado aritmético foi positivo
        self.pc = 0                     # program counter

    def carregar_programa(self, instrucoes):        ## carrega as instruções prontas para a CPU do parser.py
        self.resetar()
        self.instrucoes = instrucoes

    def atualizar_flags(self):
        self.z = 1 if self.ac == 0 else 0      # se ac == 0, Z = 1
        self.p = 1 if self.ac > 0 else 0       # se ac > 0, P = 1

    def executar_instrucao(self):      ## executa uma instrução
        chaves = list(self.instrucoes.keys())        # transforma as chaves do dicionário em uma lista ordenada

        if self.pc >= len(chaves):      # se o pc for maior ou igual ao número de chaves
            return True     # o programa acabou

        chave_atual = chaves[self.pc]       # chave da instrução atual
        mnemonico = self.instrucoes[chave_atual][0]     # primeiro ítem da tupla: mnemonico
        operando = self.instrucoes[chave_atual][1]      # segundo ítem da tupla: operando

        # todo: fazer um dispatch table
        # operando vem como string

        # =====================
        # OPERAÇÕES DE MEMÓRIA
        # =====================
        if mnemonico == "COP VAL => AC":
            self.ac = int(operando)

        elif mnemonico == "COP AC => AUX":
            self.auxs[int(operando)] = self.ac

        elif mnemonico == "COP AUX => AC":
            self.ac = self.auxs[int(operando)]

        elif mnemonico == "COP AC => MEM":
            self.mem[int(operando)] = self.ac

        elif mnemonico == "COP MEM => AC":
            self.ac = self.mem[int(operando)]

        # ======================
        # OPERAÇÕES ARITMÉTICAS
        # ======================
        elif mnemonico == "SOM AC + VAL => AC":
            self.ac = self.ac + int(operando)
            self.atualizar_flags()

        elif mnemonico == "SUB AC - VAL => AC":
            self.ac = self.ac - int(operando)
            self.atualizar_flags()

        elif mnemonico == "SOM AC + AUX => AC":
            self.ac = self.ac + self.auxs[int(operando)]
            self.atualizar_flags()

        elif mnemonico == "SUB AC - AUX => AC":
            self.ac = self.ac - self.auxs[int(operando)]
            self.atualizar_flags()

        # ====================
        # OPERAÇÕES DE DESVIO
        # ====================

        # .index() retorna o índice da primeira ocorrência
        # todo: substituir busca sequencial em chaves por dicionário de rótulos para índices
        elif mnemonico == "VAI":
            if operando in chaves:                  # se o operando (rótulo) estiver em chaves
                self.pc = chaves.index(operando)    # pc aponta para ele
                return False                        # o programa não acabou
            else:
                raise Exception(f"Rótulo inválido: {operando}")

        elif mnemonico == "VAI SE Z = 1":
            if self.z == 1:
                if operando in chaves:
                    self.pc = chaves.index(operando)
                    return False
                else:
                    raise Exception(f"Rótulo inválido: {operando}")

        elif mnemonico == "VAI SE P = 1":
            if self.p == 1:
                if operando in chaves:
                    self.pc = chaves.index(operando)
                    return False
                else:
                    raise Exception(f"Rótulo inválido: {operando}")

        # =============================
        # OPERAÇÕES DE ENTRADA E SAÍDA
        # =============================
        elif mnemonico == "ENT PORTA => AC":
            if operando != "0":
                raise ValueError(f"Porta de entrada inválida: {operando}. Use porta 0.")
            self.ac = self.entrada

        elif mnemonico == "SAI AC => PORTA":
            if operando != "2":
                raise ValueError(f"Porta de saída inválida: {operando}. Use porta 2.")
            self.saida = self.ac

        # =============================
        # OPERAÇÕES INCONDICIONAIS
        # =============================
        elif mnemonico == 'PARA':
            return True

        else:
            raise Exception(f"Instrução inválida: {mnemonico} | {operando}")

        self.pc += 1    # próxima instrução
        return False    # o programa ainda não acabou
