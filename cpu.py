class CPU:
    def __init__(self):
        self.auxs = [0] * 4             ## Array de auxiliares
        self.mem = [0] * 256            ## Memória principal
        self.instrucoes = {}            ## Dicionário de instruções
        self.entrada = 0                ## Valor de entrada fornecido externamente (I/O)
        self.flag_entrada = False       ## Indica se há um valor de entrada aguardando leitura
        self.ac = 0                     ## Acumulador
        self.z = 0                      ## 0 - resultado nulo | 1 - resultado positivo
        self.p = 0                      ## 0 - resultado negativo | 1 - resultado positivo
        self.pc = 0                     ## Program Counter
