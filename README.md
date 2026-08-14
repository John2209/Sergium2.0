# Sergium 2.0

O Sergium 2.0 é um simulador do computador fictício Sergium, usado para estudar conceitos básicos de Arquitetura de Computadores.

O projeto permite carregar, visualizar e executar programas escritos na linguagem de montagem do Sergium. A ideia principal é facilitar o entendimento de como uma CPU simples executa instruções, altera registradores, usa memória e controla entrada e saída.

## Objetivo do projeto

Este projeto foi feito para melhorar o simulador original do Sergium.

A nova versão busca deixar o código mais organizado, mais fácil de manter e mais agradável de usar. Para isso, o projeto separa melhor a parte lógica da CPU, o parser dos arquivos e a interface gráfica.

## O que o simulador faz

O simulador permite:

- abrir arquivos de programa Sergium;
- visualizar o código carregado;
- executar o programa inteiro;
- executar uma instrução por vez;
- acompanhar os registradores;
- acompanhar a memória;
- enviar valores pela porta de entrada;
- visualizar valores enviados para a saída;
- reiniciar a simulação;
- mostrar mensagens de erro e execução no terminal da interface.

## Formato dos programas

Os programas devem ser salvos em UTF-8 e podem usar as extensões `.srg` ou `.txt`.
Cada instrução deve seguir um dos formatos abaixo:

```text
rotulo | MNEMONICO | operando
MNEMONICO | operando
```

Linhas vazias e comentários iniciados por `#` são ignorados. Qualquer outra linha
fora desse formato interrompe a montagem e mostra o erro com o número da linha.

## Fluxo de execução

1. Abra ou escreva um programa no editor.
2. Clique em **Montar** para validar e carregar o programa na CPU.
3. Use **Run** para executar até o fim ou **Step** para executar uma instrução.

Qualquer alteração no editor invalida a montagem atual. Nesse caso, Run e Step
permanecem desabilitados até que o programa seja montado novamente.

Quando Run encontra uma instrução de entrada, a execução pausa. Depois que um valor
válido é enviado pelo terminal, o programa continua automaticamente. Todas as
instruções de saída executadas são registradas no terminal, na ordem correta.
