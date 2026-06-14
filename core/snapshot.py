from dataclasses import dataclass


@dataclass
class Snapshot:
    # Estado dos registradores e memória no momento do snapshot
    pc: int                  # Program Counter: posição da próxima instrução a executar
    ac: int                  # Acumulador
    auxs: list[int]          # Cópia dos registradores auxiliares AUX0 até AUX3
    mem: list[int]           # Cópia da memória principal

    # Flags da CPU
    z: int                   # 1 se o último resultado aritmético foi zero
    p: int                   # 1 se o último resultado aritmético foi positivo

    # Estado de entrada e saída
    entrada: int | None      # Valor de entrada aguardando leitura; None se não houver entrada disponível
    saida: int | None        # Último valor enviado para a porta de saída; None se nada foi enviado

    # Estado de execução
    finalizado: bool         # True se o programa já terminou

    # Instrução atual apontada pelo PC
    rotulo_atual: str | None
    mnemonico_atual: str | None
    operando_atual: str | None