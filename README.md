# mSergium

mSergium é um simulador em Python para a linguagem de montagem do computador fictício Sergium, usado em Arquitetura de Computadores para representar conceitos básicos da arquitetura de von Neumann, ciclo de busca, ciclo de execução, registradores, memória, entrada, saída e desvios.

O projeto foi desenvolvido a partir de uma versão inicial do simulador e reorganizado com foco em separação entre núcleo de execução, parser e interface gráfica.

## Objetivo

O objetivo do projeto é permitir que programas escritos na linguagem do Sergium sejam carregados, interpretados e executados de forma visual.

A aplicação permite acompanhar o estado do processador durante a execução, incluindo acumulador, registradores auxiliares, flags, memória, entrada, saída e instrução atual.

## Funcionalidades

O simulador possui:

- Leitura de arquivos com instruções do Sergium.
- Parser para transformar o código textual em instruções executáveis.
- Execução completa do programa.
- Execução passo a passo.
- Visualização dos registradores.
- Visualização da memória.
- Entrada de dados pela porta de entrada.
- Saída de dados pela porta de saída.
- Tratamento de erros de sintaxe, instruções inválidas e rótulos inválidos.
- Interface gráfica feita em Python com CustomTkinter.

## Estrutura do projeto

A estrutura principal do projeto é organizada da seguinte forma:

```text
mSergium/
├── core/
│   ├── __init__.py
│   ├── cpu.py
│   ├── errors.py
│   ├── instruction_set.py
│   ├── parser.py
│   └── snapshot.py
│
├── ui/
│   ├── __init__.py
│   └── app.py
│
├── codigos/
│   └── exemplos de programas Sergium
│
├── main.py
├── test_core.py
└── README.md