# Conjunto de instruções do Segium
import re

CODIGOS_INSTRUCOES = {
    "ENT PORTA => AC": 0,
    "SAI AC => PORTA": 1,

    "COP AUX => AC": 2,
    "COP AC => AUX": 3,
    "COP MEM => AC": 4,
    "COP AC => MEM": 5,
    "COP VAL => AC": 6,

    "SOM AC + AUX => AC": 10,
    "SUB AC - AUX => AC": 11,
    "SOM AC + VAL => AC": 12,
    "SUB AC - VAL => AC": 13,

    "VAI": 20,
    "VAI SE Z = 1": 21,
    "VAI SE P = 1": 22,

    "PARA": 23,
}


INSTRUCOES_VALIDAS = set(CODIGOS_INSTRUCOES.keys())


def normalizar_mnemonico(mnemonico: str) -> str:
    """
    Padroniza o texto de um mnemônico.

    Exemplos:
    'cop ac=>mem' vira 'COP AC => MEM'
    'SOM AC+VAL=>AC' vira 'SOM AC + VAL => AC'
    'vai se z=1' vira 'VAI SE Z = 1'
    """

    texto = mnemonico.strip().upper()

    texto = re.sub(r"\s+", " ", texto)

    # Primeiro normaliza a seta =>.
    texto = re.sub(r"\s*=>\s*", " => ", texto)

    # Normaliza operadores aritméticos.
    texto = re.sub(r"\s*\+\s*", " + ", texto)
    texto = re.sub(r"\s*-\s*", " - ", texto)

    # Normaliza apenas o sinal = que NÃO faz parte de =>.
    texto = re.sub(r"\s*=(?!>)\s*", " = ", texto)

    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


def instrucao_existe(mnemonico: str) -> bool:
    return normalizar_mnemonico(mnemonico) in INSTRUCOES_VALIDAS