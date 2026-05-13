class Parser:
    def __init__(self, caminho_arquivo: str):       ## Inicializa o parser com o caminho do arquivo

        self.caminho_arquivo = caminho_arquivo      # Armazena o caminho do arquivo
        self.instrucoes = {}                        # Dicionário para armazenar as instruções

    def parsear(self):  ## Função para realizar o parsing do arquivo

        with open(self.caminho_arquivo, 'r') as arquivo:    # abre o arquivo no caminho no modo read. conteudo é objeto
            conteudo = arquivo.read()                       # tranforma o conteúdo do arquivo em uma string. conteudo passa a ser string
            linhas = conteudo.splitlines()                  # trasfomar a string em uma lista de strings, cada uma representando uma linha do arquivo

            linhas_validas = []  # lista de linhas válidas do codigo

            # todo: juntar os dois for em um
            for linha in linhas:                    # para cada linha em linhas
                if '|' in linha:                    # se houver '|'
                    linhas_validas.append(linha)    # adiciona em linhas_validas

            for i, linha in enumerate(linhas_validas):      # para cada linha em linhas_validas
                partes = linha.split('|')                   # .split() retorna uma lista

                rotulo = partes[0].strip().upper()      # transforma o elemento 0 da lista em rotulo, deixa em maiúsculo e retira os espaços
                mnemonico = partes[1].strip().upper()   # transforma o elemento 1 da lista em menemônico, deixa em maiúsculo e retira os espaços
                operando = partes[2].strip().upper()    # transforma o elemento 2 da lista em operando, deixa em maiúsculo e retira os espaços

                if rotulo == "":        # se não houver rótulo,
                    rotulo = str(i)     # o rótulo passa a ser o índice em formato de string

                self.instrucoes[rotulo] = (mnemonico, operando) # instrucoes recebe o dicionário com o rotulo e a tupla de mnemonico e operando

        return self.instrucoes

## PARA TESTES ##
parser = Parser(r"C:\dev\mSergium\codigos\EX3.txt")
resultado = parser.parsear()
print(resultado)
