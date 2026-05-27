from core.cpu import CPU
from core.parser import Parser
from app import App

if __name__ == "__main__":
    minha_cpu = CPU()
    app = App(minha_cpu)
    app.mainloop()