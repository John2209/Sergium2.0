from app import App
from cpu import CPU
from leitor import Parser

if __name__ == "__main__":
        minha_cpu = CPU()
        meu_parser = Parser("")
        meu_app = App(minha_cpu)

        meu_app.mainloop()