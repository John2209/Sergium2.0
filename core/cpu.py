# Implementa a CPU do Sergium

class CPU:
    def __init__(self):     ## inicializa a CPU com valores padrão
        self.dispatch_table = self._criar_dispatch_table()
        self.resetar()


    def _criar_dispatch_table(self):    ##
        return {
            "COP VAL => AC": self._exec_cop_val_ac,
            "COP AC => AUX": self._exec_cop_ac_aux,
            "COP AUX => AC": self._exec_cop_aux_ac,
            "COP AC => MEM": self._exec_cop_ac_mem,
            "COP MEM => AC": self._exec_cop_mem_ac,

            "SOM AC + VAL => AC": self._exec_som_ac_val_ac,
            "SUB AC - VAL => AC": self._exec_sub_ac_val_ac,
            "SOM AC + AUX => AC": self._exec_som_ac_aux_ac,
            "SUB AC - AUX => AC": self._exec_sub_ac_aux_ac,

            "VAI": self._exec_vai,
            "VAI SE Z = 1": self._exec_vai_se_z,
            "VAI SE P = 1": self._exec_vai_se_p,

            "ENT PORTA => AC": self._exec_ent_porta_ac,
            "SAI AC => PORTA": self._exec_sai_ac_porta,

            "PARA": self._exec_para,
        }


    def resetar(self):
        self.auxs = [0] * 4             # array de auxiliares
        self.mem = [0] * 256            # memória principal
        self.instrucoes = {}            # dicionário de instruções
        self.indices_rotulos = {}       # dicionário de rótulos
        self.entrada = 0                # valor de entrada fornecido externamente (I/O)
        self.saida = None               # valor de saida do Sergium
        self.flag_entrada = False       # indica se há um valor de entrada aguardando leitura
        self.ac = 0                     # acumulador
        self.z = 0                      # 1 se o último resultado aritmético foi zero
        self.p = 0                      # 1 se o último resultado aritmético foi positivo
        self.pc = 0                     # program counter


    def carregar_programa(self, instrucoes):    ## carrega as instruções prontas para a CPU do parser.py
        self.resetar()
        self.instrucoes = instrucoes
        self.indices_rotulos = {                # cria uma tabela auxiliar com os índices dos rótulos
            rotulo: indice                      # cada chave será um rótulo, e o valor será a posição dele no programa
            for indice, rotulo in enumerate(self.instrucoes.keys())     # self.instrucoes.keys() pega os rótulos/chaves do programa
                                                                        # enumerate() numera rótulos em ordem: 0, 1, ...
        }


    def atualizar_flags(self):      ## atualiza as flags z e p
        self.z = 1 if self.ac == 0 else 0      # se ac == 0, Z = 1
        self.p = 1 if self.ac > 0 else 0       # se ac > 0, P = 1


    def executar_instrucao(self):      ## executa uma instrução
        chaves = list(self.instrucoes.keys())        # transforma as chaves do dicionário em uma lista ordenada

        if self.pc >= len(chaves):      # se o pc for maior ou igual ao número de chaves
            return True     # o programa acabou

        chave_atual = chaves[self.pc]       # chave da instrução atual
        mnemonico = self.instrucoes[chave_atual][0]     # primeiro ítem da tupla: mnemonico
        operando = self.instrucoes[chave_atual][1]      # segundo ítem da tupla: operando

        funcao = self.dispatch_table.get(mnemonico)     # procura na dispatch table qual função exectua esse mnemonico

        if funcao is None:      # se o .get() não o achar, reterona None
            raise Exception(f"Instrução inválida: {mnemonico} | {operando}")

        resultado = funcao(operando)    # executa a função, passando o operando

        if resultado is True:   # se for uma instrução para encerrar o programa
            return True

        if resultado is False:  # se a instrução já alterou o pc (VAI SE)
            return False        # programa ainda não terminou, mas a CPU não deve incrementar o PC

        self.pc += 1    # se for uma instrução comum (valor None), vai para a próxima
        return False    # programa ainda não acabou


    # ==============================
    # FUNÇÕES PARA A DISPATCH TABLE
    # ==============================
    # =====================
    # OPERAÇÕES DE MEMÓRIA
    # =====================
    def _exec_cop_val_ac(self, operando):
        self.ac = int(operando)

    def _exec_cop_ac_aux(self, operando):
        self.auxs[int(operando)] = self.ac

    def _exec_cop_aux_ac(self, operando):
        self.ac = self.auxs[int(operando)]

    def _exec_cop_ac_mem(self, operando):
        self.mem[int(operando)] = self.ac

    def _exec_cop_mem_ac(self, operando):
        self.ac = self.mem[int(operando)]

    # ======================
    # OPERAÇÕES ARITMÉTICAS
    # ======================
    def _exec_som_ac_val_ac(self, operando):
        self.ac = self.ac + int(operando)
        self.atualizar_flags()

    def _exec_sub_ac_val_ac(self, operando):
        self.ac = self.ac - int(operando)
        self.atualizar_flags()

    def _exec_som_ac_aux_ac(self, operando):
        self.ac = self.ac + self.auxs[int(operando)]
        self.atualizar_flags()

    def _exec_sub_ac_aux_ac(self, operando):
        self.ac = self.ac - self.auxs[int(operando)]
        self.atualizar_flags()

    # ====================
    # OPERAÇÕES DE DESVIO
    # ====================
    def _exec_vai(self, operando):
        if operando in self.indices_rotulos:
            self.pc = self.indices_rotulos[operando]
            return False

        raise Exception(f"Rótulo inválido: {operando}")

    def _exec_vai_se_z(self, operando):
        if self.z == 1:
            return self._exec_vai(operando)

        return None

    def _exec_vai_se_p(self, operando):
        if self.p == 1:
            return self._exec_vai(operando)

        return None

    def _exec_ent_porta_ac(self, operando):
        if operando != "0":
            raise ValueError(f"Porta de entrada inválida: {operando}. Use porta 0.")

        self.ac = self.entrada

    def _exec_sai_ac_porta(self, operando):
        if operando != "2":
            raise ValueError(f"Porta de saída inválida: {operando}. Use porta 2.")

        self.saida = self.ac

    def _exec_para(self, operando):
        return True
    