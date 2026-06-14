from dataclasses import dataclass

@dataclass
class Snapshot:
    pc: int
    ac: int
    auxs: list[int]
    mem: list[int]
    z: int
    p: int
    entrada: int
    saida: int | None
    finalizado: bool

    rotulo_atual: str | None
    mnemonico_atual: str | None
    operando_atual: str | None