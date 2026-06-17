# para imports diretos
# from core import CPU, Parser, Snapshot em vez de importar cada um pelo arquivo específico

from .cpu import CPU             # exporta a CPU principal do simulador
from .parser import Parser       # exporta o leitor de arquivos Sergium
from .snapshot import Snapshot   # exporta a estrutura de estado da CPU

from .errors import (            # exporta os erros próprios do core
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

from .instruction_set import (   # exporta definições das instruções válidas
    INSTRUCOES_VALIDAS,
    normalizar_mnemonico,
    instrucao_existe,
)
