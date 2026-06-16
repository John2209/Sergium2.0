# erros do Sergium

class SergiumError(Exception):
    """Erro base do simulador"""
    pass


class ParserError(SergiumError):
    """Erro gerado durante a leitura do código"""
    pass


class CPUError(SergiumError):
    """Erro gerado durante a execução do programa"""
    pass


class InstrucaoInvalidaError(CPUError):
    """Erro para mnemônicos não existentes"""
    pass


class OperandoInvalidoError(CPUError):
    """Erro de operandos inválidos"""
    pass


class RotuloInvalidoError(CPUError):
    """Erro de desvios para rótulos inexistentes"""
    pass


class AuxiliarInvalidoError(OperandoInvalidoError):
    """Erro de acesso inválido aos registradores AUX0 até AUX3"""
    pass


class MemoriaInvalidaError(OperandoInvalidoError):
    """Erro de acesso inválido à memória"""
    pass


class PortaInvalidaError(OperandoInvalidoError):
    """Erro de acesso inválido às portas"""
    pass


class EntradaNecessariaError(CPUError):
    """Erro de entrada não fornecida"""
    pass


class LoopInfinitoError(CPUError):
    """Erro de limite máximo de instruções executadas"""
    pass
