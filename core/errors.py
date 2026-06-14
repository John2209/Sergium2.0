# Erros próprios do core do Sergium

class SergiumError(Exception):
    """Erro base de todo o simulador Sergium."""
    pass


class ParserError(SergiumError):
    """Erro gerado durante a leitura ou interpretação do código."""
    pass


class CPUError(SergiumError):
    """Erro gerado durante a execução do programa pela CPU."""
    pass


class InstrucaoInvalidaError(CPUError):
    """Erro para mnemônicos que não existem no Sergium."""
    pass


class OperandoInvalidoError(CPUError):
    """Erro para operandos inválidos."""
    pass


class RotuloInvalidoError(CPUError):
    """Erro para desvios para rótulos inexistentes."""
    pass


class AuxiliarInvalidoError(OperandoInvalidoError):
    """Erro para acesso inválido aos registradores AUX0 até AUX3."""
    pass


class MemoriaInvalidaError(OperandoInvalidoError):
    """Erro para acesso inválido à memória."""
    pass


class PortaInvalidaError(OperandoInvalidoError):
    """Erro para acesso inválido às portas de entrada/saída."""
    pass


class EntradaNecessariaError(CPUError):
    """Erro para quando a CPU precisa de entrada, mas ela não foi fornecida."""
    pass