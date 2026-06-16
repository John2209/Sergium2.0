# lê arquivos de código Sergium e transforma o texto em instruções iterpretáveis pela CPU
from .errors import ParserError
from .instruction_set import INSTRUCOES_VALIDAS, normalizar_mnemonico


class Parser:
    def __init__(self, caminho_arquivo: str):       ## inicializa o parser com o caminho do arquivo

        self.caminho_arquivo = caminho_arquivo      # armazena o caminho do arquivo
        self.instrucoes = {}                        # dicionário para armazenar as instruções

    def parsear(self):          ## função para realizar o parsing do arquivo
        self.instrucoes = {}    # limpa instruções anteriores caso o mesmo Parser seja reutilizado

        with open(self.caminho_arquivo, 'r') as arquivo:    # abre o arquivo no modo leitura
            conteudo = arquivo.read()                       # transforma o conteúdo do arquivo em uma string
            linhas = conteudo.splitlines()                  # transforma a string em uma lista de linhas

            linhas_validas = []                             # lista com as linhas válidas e seus números originais no arquivo

            for numero_linha, linha in enumerate(linhas, start=1):      # percorre as linhas do arquivo começando em 1
                if '|' in linha:                                        # se houver '|', a linha tem formato de instrução
                    linhas_validas.append((numero_linha, linha))        # guarda o número real da linha junto com o texto

            for i, (numero_linha, linha) in enumerate(linhas_validas):  # percorre as instruções válidas em ordem
                partes = linha.split('|')                               # separa em: rótulo | mnemônico | operando

                if len(partes) != 3:                                    # uma instrução precisa ter exatamente 3 partes
                    raise ParserError(f"Linha {numero_linha} inválida: {linha}")

                rotulo = partes[0].strip().upper()              # remove espaços e padroniza o rótulo
                mnemonico = normalizar_mnemonico(partes[1])     # padroniza o mnemônico para o formato oficial
                operando = partes[2].strip().upper()            # remove espaços e padroniza o operando

                if mnemonico not in INSTRUCOES_VALIDAS:  # verifica se a instrução existe no Sergium
                    raise ParserError(f"Linha {numero_linha}: instrução desconhecida: {mnemonico}")

                if rotulo == "":                # se não houver rótulo escrito no arquivo,
                    rotulo = str(i)             # usa o índice da instrução como rótulo automático

                if rotulo in self.instrucoes:  # impede que um rótulo sobrescreva outro
                    raise ParserError(f"Linha {numero_linha}: rótulo duplicado: {rotulo}")

                self.instrucoes[rotulo] = (mnemonico, operando)  # guarda a instrução no formato usado pela CPU

        return self.instrucoes
