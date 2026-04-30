class Parser:
    def __init__(self, caminho_arquivo: str):       ## Inicializa o parser com o caminho do arquivo

        self.caminho_arquivo = caminho_arquivo      # Armazena o caminho do arquivo
        self.instrucoes = {}                        # Dicionário para armazenar as instruções

    def parsear(self):                  ## Função para realizar o parsing do arquivo

        conteudo = open(self.caminho_arquivo, 'r')  # abre o arquivo no caminho no modo read
        conteudo.read()                             # tranforma todo o conteúdo do arquivo em uma string




        return self.instrucoes
