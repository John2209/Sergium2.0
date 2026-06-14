from dataclasses import dataclass

@dataclass
class Snapshot:
    pc: int
    ac: int
    auxs: list[int]
    mem: list[int]

    # Flags da CPU
    z: int
    p: int

    # Estado de entrada e saída
    entrada: int | None
    saida: int | None

    # Estado de execução
    finalizado: bool

    # Instrução atual apontada pelo PC
    rotulo_atual: str | None
    mnemonico_atual: str | None
    operando_atual: str | None
