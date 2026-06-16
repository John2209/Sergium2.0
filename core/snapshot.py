from dataclasses import dataclass

@dataclass
class Snapshot:
    pc: int
    ac: int
    auxs: list[int]
    mem: list[int]

    # flags da CPU
    z: int
    p: int

    # estado de entrada e saída
    entrada: int | None
    saida: int | None

    # estado de execução
    finalizado: bool

    # instrução atual apontada pelo pc
    rotulo_atual: str | None
    mnemonico_atual: str | None
    operando_atual: str | None
