# instruções reconhecidas pelo simulador Sergium

import re

INSTRUCOES_VALIDAS = {
    "ENT PORTA => AC",
    "SAI AC => PORTA",

    "COP AUX => AC",
    "COP AC => AUX",
    "COP MEM => AC",
    "COP AC => MEM",
    "COP VAL => AC",

    "SOM AC + AUX => AC",
    "SUB AC - AUX => AC",
    "SOM AC + VAL => AC",
    "SUB AC - VAL => AC",

    "MUL AC * AUX => AC",
    "DIV AC / AUX => AC"
    "MUL AC * VAL => AC"
    "DIV AC / VAL => AC"

    "VAI",
    "VAI SE Z = 1",
    "VAI SE P = 1",

    "PARA",
}


def normalizar_mnemonico(mnemonico: str) -> str:
    texto = mnemonico.strip().upper()

    texto = re.sub(r"\s+", " ", texto)
    texto = re.sub(r"\s*=>\s*", " => ", texto)
    texto = re.sub(r"\s*\+\s*", " + ", texto)
    texto = re.sub(r"\s*-\s*", " - ", texto)
    texto = re.sub(r"\s*=(?!>)\s*", " = ", texto)
    texto = re.sub(r"\s*\*\s*", " * ", texto)
    texto = re.sub(r"\s*/\s*", " / ", texto)
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


def instrucao_existe(mnemonico: str) -> bool:
    return normalizar_mnemonico(mnemonico) in INSTRUCOES_VALIDAS
