# para imports diretos
# from core import CPU, Parser, Snapshot em vez de importar cada um pelo arquivo específico

from .cpu import CPU
from .parser import Parser
from .snapshot import Snapshot

from .errors import (
    SergiumError,
    ParserError,
    CPUError,
    InstrucaoInvalidaError,
    OperandoInvalidoError,
    RotuloInvalidoError,
    AuxiliarInvalidoError,
    MemoriaInvalidaError,
    PortaInvalidaError,
    EntradaNecessariaError,
    LoopInfinitoError,
)

from .instruction_set import (
    CODIGOS_INSTRUCOES,
    INSTRUCOES_VALIDAS,
    normalizar_mnemonico,
    instrucao_existe,
)
