from app import App
from cpu import CPU
from leitor import Parser

if __name__ == "__main__":              ## Ponto de entrada do programa

        minha_cpu = CPU()               # Cria instância da CPU
        meu_parser = Parser("")         # Cria instância do parser
        meu_app = App(minha_cpu)        # Cria instância da aplicação

        meu_app.mainloop()              # Inicia o loop principal da interface
