class Parser:
    def __init__(self, caminho_arquivo: str):       ## Inicializa o parser com o caminho do arquivo

        self.caminho_arquivo = caminho_arquivo      # Armazena o caminho do arquivo
        self.instrucoes = {}                        # Dicionário para armazenar as instruções

    def parsear(self):                  ## Função para realizar o parsing do arquivo

        with open(self.caminho_arquivo, 'r') as file:                                       # abre o arquivo no caminho no modo read

            conteudo = file.read()                                                          # tranforma todo o conteúdo do arquivo em uma string
            conteudo = "\n".join(linha for linha in conteudo.splitlines() if "|" in linha)  # Remove as linhas em branco do conteúdo do arquivo





        return self.instrucoes
