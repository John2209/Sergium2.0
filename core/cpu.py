# implementa a CPU do Sergium

from .snapshot import Snapshot
from .errors import (
    InstrucaoInvalidaError,
    OperandoInvalidoError,
    RotuloInvalidoError,
    AuxiliarInvalidoError,
    MemoriaInvalidaError,
    PortaInvalidaError,
    LoopInfinitoError,
    EntradaNecessariaError,
)


class CPU:
    def __init__(self):     ## inicializa a CPU com valores padrão
        self.dispatch_table = self._criar_dispatch_table()
        self.resetar()


    def _criar_dispatch_table(self):    ## cria a tabela que liga cada mnemônico à função que o executa
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

            "MUL AC * VAL => AC" : self._exec_mul_ac_val_ac,
            "MUL AC / VAL => AC": self._exec_div_ac_val_ac,
            "MUL AC * AUX => AC": self._exec_mul_ac_aux_ac,
            "MUL AC / AUX => AC": self._exec_mul_ac_aux_ac,

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
        self.entrada = None             # valor de entrada aguardando leitura; None significa que não há entrada disponível
        self.flag_entrada = False       # indica se há um valor pronto para a próxima instrução ENT
        self.saida = None               # valor de saida do Sergium
        self._saidas_pendentes = []     # saídas ainda não entregues à interface, na ordem em que foram geradas
        self.ac = 0                     # acumulador
        self.z = 0                      # 1 se o último resultado aritmético foi zero
        self.p = 0                      # 1 se o último resultado aritmético foi positivo
        self.pc = 0                     # program counter
        self.finalizado = False


    def carregar_programa(self, instrucoes):    ## carrega as instruções prontas para a CPU do parser.py
        self.resetar()
        self.instrucoes = instrucoes
        self.indices_rotulos = {                # cria uma tabela auxiliar com os índices dos rótulos
            rotulo: indice                      # cada chave será um rótulo, e o valor será a posição dele no programa
            for indice, rotulo in enumerate(self.instrucoes.keys())     # self.instrucoes.keys() pega os rótulos/chaves do programa
                                                                        # enumerate() numera rótulos em ordem: 0, 1, ...
        }


    def definir_entrada(self, valor):
        # recebe um valor externo para ser usado pela próxima instrução ENT
        self.entrada = self._converter_operando_para_int(valor)
        self.flag_entrada = True


    def consumir_saida(self):
        # mantém a API antiga: entrega a saída mais recente e limpa todas as pendências
        saida = self.saida
        self._saidas_pendentes.clear()
        self.saida = None
        return saida


    def consumir_saidas(self):
        # entrega todas as saídas na ordem em que foram geradas e limpa para não imprimir de novo
        saidas = self._saidas_pendentes.copy()
        self._saidas_pendentes.clear()
        self.saida = None
        return saidas


    def snapshot(self):
        # cria um snapshot do estado atual da CPU para a interface
        chaves = list(self.instrucoes.keys())

        rotulo_atual = None
        mnemonico_atual = None
        operando_atual = None

        # se o PC aponta para uma instrução válida, identifica a instrução atual
        if 0 <= self.pc < len(chaves):
            rotulo_atual = chaves[self.pc]
            mnemonico_atual = self.instrucoes[rotulo_atual][0]
            operando_atual = self.instrucoes[rotulo_atual][1]

        return Snapshot(
            auxs=self.auxs.copy(),  # cópia para impedir alteração direta dos auxiliares
            mem=self.mem.copy(),  # cópia para impedir alteração direta da memória
            entrada=self.entrada,
            saida=self.saida,
            ac=self.ac,
            z=self.z,
            p=self.p,
            pc=self.pc,
            finalizado=self.finalizado,
            rotulo_atual=rotulo_atual,
            mnemonico_atual=mnemonico_atual,
            operando_atual=operando_atual,
        )


    def atualizar_flags(self):      ## atualiza as flags z e p
        self.z = 1 if self.ac == 0 else 0      # se ac == 0, Z = 1
        self.p = 1 if self.ac > 0 else 0       # se ac > 0, P = 1


    def _converter_operando_para_int(self, operando):
        # converte operandos textuais para inteiro antes de usar em registradores, memória ou portas
        try:
            return int(operando)
        except ValueError:
            raise OperandoInvalidoError(f"Operando inválido: {operando}. Esperado um número inteiro.")


    def _validar_auxiliar(self, operando):
        # garante que o operando aponta para um registrador auxiliar existente
        indice = self._converter_operando_para_int(operando)

        if indice < 0 or indice >= len(self.auxs):
            raise AuxiliarInvalidoError(
                f"Auxiliar inválido: AUX{indice}. Use AUX0 até AUX{len(self.auxs) - 1}."
            )

        return indice


    def _validar_memoria(self, operando):
        # garante que o endereço está dentro da memória disponível
        endereco = self._converter_operando_para_int(operando)

        if endereco < 0 or endereco >= len(self.mem):
            raise MemoriaInvalidaError(
                f"Endereço de memória inválido: {endereco}. Use valores de 0 até {len(self.mem) - 1}."
            )

        return endereco


    def _validar_porta_entrada(self, operando):
        porta = self._converter_operando_para_int(operando)

        if porta != 0:
            raise PortaInvalidaError(f"Porta de entrada inválida: {porta}. Use porta 0.")

        return porta


    def _validar_porta_saida(self, operando):
        porta = self._converter_operando_para_int(operando)

        if porta != 2:
            raise PortaInvalidaError(f"Porta de saída inválida: {porta}. Use porta 2.")

        return porta


    def executar_instrucao(self):      ## executa uma instrução
        if self.finalizado:
            return True

        chaves = list(self.instrucoes.keys())        # transforma as chaves do dicionário em uma lista ordenada

        if self.pc >= len(chaves):      # se o pc for maior ou igual ao número de chaves
            self.finalizado = True
            return True                 # o programa acabou

        chave_atual = chaves[self.pc]       # chave da instrução atual
        mnemonico = self.instrucoes[chave_atual][0]     # primeiro ítem da tupla: mnemonico
        operando = self.instrucoes[chave_atual][1]      # segundo ítem da tupla: operando

        funcao = self.dispatch_table.get(mnemonico)     # procura na dispatch table qual função exectua esse mnemonico

        if funcao is None:      # se o .get() não o achar, reterona None
            raise InstrucaoInvalidaError(f"Instrução inválida: {mnemonico} | {operando}")

        resultado = funcao(operando)    # executa a função, passando o operando

        if resultado is True:       # se for uma instrução para encerrar o programa
            self.finalizado = True
            return True

        if resultado is False:  # se a instrução já alterou o pc (VAI SE)
            return False        # programa ainda não terminou, mas a CPU não deve incrementar o PC

        self.pc += 1    # se for uma instrução comum (valor None), vai para a próxima

        if self.pc >= len(chaves):
            self.finalizado = True
            return True                 # a instrução executada era a última do programa

        return False    # programa ainda não acabou


    def executar_tudo(self, limite_instrucoes=1000):
        instrucoes_executadas = 0

        while not self.finalizado:
            if instrucoes_executadas >= limite_instrucoes:
                raise LoopInfinitoError(
                    f"Limite de {limite_instrucoes} instruções atingido. Possível loop infinito."
                )

            try:
                self.executar_instrucao()
            except EntradaNecessariaError:
                return False  # pausou esperando entrada

            instrucoes_executadas += 1

        return True  # terminou de verdade


    # ==============================
    # FUNÇÕES PARA A DISPATCH TABLE
    # ==============================
    # =====================
    # OPERAÇÕES DE MEMÓRIA
    # =====================
    def _exec_cop_val_ac(self, operando):
        self.ac = self._converter_operando_para_int(operando)

    def _exec_cop_ac_aux(self, operando):
        indice = self._validar_auxiliar(operando)
        self.auxs[indice] = self.ac

    def _exec_cop_aux_ac(self, operando):
        indice = self._validar_auxiliar(operando)
        self.ac = self.auxs[indice]

    def _exec_cop_ac_mem(self, operando):
        endereco = self._validar_memoria(operando)
        self.mem[endereco] = self.ac

    def _exec_cop_mem_ac(self, operando):
        endereco = self._validar_memoria(operando)
        self.ac = self.mem[endereco]


    # ======================
    # OPERAÇÕES ARITMÉTICAS
    # ======================
    def _exec_som_ac_val_ac(self, operando):
        valor = self._converter_operando_para_int(operando)
        self.ac = self.ac + valor
        self.atualizar_flags()

    def _exec_sub_ac_val_ac(self, operando):
        valor = self._converter_operando_para_int(operando)
        self.ac = self.ac - valor
        self.atualizar_flags()

    def _exec_som_ac_aux_ac(self, operando):
        indice = self._validar_auxiliar(operando)
        self.ac = self.ac + self.auxs[indice]
        self.atualizar_flags()

    def _exec_sub_ac_aux_ac(self, operando):
        indice = self._validar_auxiliar(operando)
        self.ac = self.ac - self.auxs[indice]
        self.atualizar_flags()

    def _exec_mul_ac_val_ac(self, operando):
        valor = self._converter_operando_para_int(operando)
        self.ac = self.ac * valor
        self.atualizar_flags()

    def _executar_mul_ac_aux_ac(self, operando):
        indice = self._validar_auxiliar(operando)
        self.ac = self.ac * self.auxs[indice]
        self.atualizar_flags()


    # ====================
    # OPERAÇÕES DE DESVIO
    # ====================
    def _exec_vai(self, operando):
        if operando in self.indices_rotulos:
            self.pc = self.indices_rotulos[operando]
            return False

        raise RotuloInvalidoError(f"Rótulo inválido: {operando}")

    def _exec_vai_se_z(self, operando):
        if self.z == 1:
            return self._exec_vai(operando)

        return None

    def _exec_vai_se_p(self, operando):
        if self.p == 1:
            return self._exec_vai(operando)

        return None


    # ====================
    # OPERAÇÕES DE I/O
    # ====================
    def _exec_ent_porta_ac(self, operando):
        self._validar_porta_entrada(operando)

        if not self.flag_entrada:
            raise EntradaNecessariaError("A instrução ENT precisa de um valor de entrada.")

        self.ac = self.entrada
        self.entrada = None
        self.flag_entrada = False

    def _exec_sai_ac_porta(self, operando):
        self._validar_porta_saida(operando)
        self.saida = self.ac
        self._saidas_pendentes.append(self.ac)

    def _exec_para(self, operando):
        return True
