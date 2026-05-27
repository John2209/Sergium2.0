if __name__ == "__main__":
    # =============================================================================================================================
    # Simulador para a Linguagem de Montagem do Sergium
    # =============================================================================================================================
    # Todo o simulador está implementado utilizando uma interface gráfica na linguagem Python
    # Cada botão que o usuário pressiona está relacionado a recursos do simulador, sendo que os botões estão atrelados a funções

    # Utilizar o pyinstaller para gerar um executável que não precisa do Python instalado para executar
    #   pyinstaller --onefile --windowed sergium.py

    import sys
    import tkinter as tk
    from tkinter import ttk, filedialog

    # ==================================================================================================
    # Variaveis Globais de Estado
    # ==================================================================================================

    # Registradores Auxiliares (AUX0, AUX1, AUX2, AUX3)
    auxs = [0] * 4

    # Acumulador
    ac = 0

    # Memória
    mem = [0] * 256

    # Indicadores (z - resultado nulo | p - resultado positivo)
    z = 0
    p = 0

    # Dicionario que irá armazenar as instruções que serão executadas
    instrucoes = {}

    # Program Counter - Iterador das insctruções do dicionário
    pc = 0

    # Valor fornecido na porta de entrada do Sergium
    entrada = 0

    # Flag indicando um novo número para ler na porta de entrada do Sergium
    flag_entrada = False

    # ==================================================================================================
    # Criação da Interface Gráfica
    # ==================================================================================================

    def criar_interface():
        global root                                                                                             # Interface gráfica
        global tabela_registradores, tabela_memoria, registradores_ids, memoria_ids                             # Tabelas
        global botao_selecionar_arquivo, botao_simular, botao_simular_parcial, botao_processar, botao_reiniciar # Botoes
        global text_box, log_text, entry_numero, text_saida                                                     # Caixas de texto

        # Cria a interface gráfica
        root = tk.Tk()
        root.title("Simulador Sergium")
        root.protocol("WM_DELETE_WINDOW", fechar)

        # =================================================================================
        # Cria uma frame para o arquivo de instruções
        # =================================================================================
        # X |  |
        #   |  |
        frame_arquivo = tk.LabelFrame(root, text="Instruções", padx=10, pady=10)
        frame_arquivo.grid(row=0, column=0, padx=10, pady=10, rowspan=2)

        # Cria a caixa de texto para mostrar o conteúdo do arquivo com escrita desabilitada
        text_box = tk.Text(frame_arquivo, width=50, height=20, wrap="word", state=tk.DISABLED)
        text_box.grid(row=0, column=0)

        # Adiciona uma barra de rolagem para o arquivo de instruções
        scrollbar_arquivo = tk.Scrollbar(frame_arquivo, orient="vertical", command=text_box.yview)
        scrollbar_arquivo.grid(row=0, column=1, sticky="ns")  # Barra de rolagem ao lado da caixa de texto
        text_box.config(yscrollcommand=scrollbar_arquivo.set)

        # Cria o botão "Selecionar Arquivo" dentro da frame_arquivo
        botao_selecionar_arquivo = tk.Button(frame_arquivo, text="Selecionar Arquivo", command=selecionar_arquivo)
        botao_selecionar_arquivo.grid(row=1, column=0, columnspan=2, padx=10, pady=5)  # Colocando abaixo da caixa de texto
        # =================================================================================

        # =================================================================================
        # Cria uma frame para o conteúdo dos registradores
        # =================================================================================
        #   | X |
        #   |   |
        frame_registradores = tk.LabelFrame(root, text="Registradores", padx=10, pady=10)
        frame_registradores.grid(row=0, column=1, padx=10, pady=10)

        # Cria a tabela de registradores
        tabela_registradores = ttk.Treeview(frame_registradores, columns=("col1", "col2"), show="headings")
        tabela_registradores.heading("col1", text="Registrador")
        tabela_registradores.heading("col2", text="Valor")
        tabela_registradores.grid(row=0, column=0)

        # Preenche a tabela de registradores com valores iniciais e salvar os IDs para atualização posterior
        registradores_ids = []

        registradores_ids.append(tabela_registradores.insert("", "end", values=("AUX0", auxs[0])))
        registradores_ids.append(tabela_registradores.insert("", "end", values=("AUX1", auxs[1])))
        registradores_ids.append(tabela_registradores.insert("", "end", values=("AUX2", auxs[2])))
        registradores_ids.append(tabela_registradores.insert("", "end", values=("AUX3", auxs[3])))
        registradores_ids.append(tabela_registradores.insert("", "end", values=("AC", ac)))
        registradores_ids.append(tabela_registradores.insert("", "end", values=("Z", z)))
        registradores_ids.append(tabela_registradores.insert("", "end", values=("P", p)))
        # =================================================================================

        # =================================================================================
        # Cria um frame para o conteúdo da memória
        # =================================================================================
        #   |   | X
        #   |   |
        frame_memoria = tk.LabelFrame(root, text="Memória", padx=10, pady=10)
        frame_memoria.grid(row=0, column=2, padx=10, pady=10)

        # Cria a tabela de memória
        tabela_memoria = ttk.Treeview(frame_memoria, columns=("col1", "col2"), show="headings")
        tabela_memoria.heading("col1", text="Endereço")
        tabela_memoria.heading("col2", text="Valor")
        tabela_memoria.grid(row=0, column=0)

        # Preenche a tabela de memória com valores iniciais e salvar os IDs para atualização posterior
        memoria_ids = []
        for i in range(256):
            id_mem = tabela_memoria.insert("", "end", values=(i, mem[i]))
            memoria_ids.append(id_mem)

        # Adiciona uma barra de rolagem vertical para a memória
        scrollbar_memoria = tk.Scrollbar(frame_memoria, orient="vertical", command=tabela_memoria.yview)
        scrollbar_memoria.grid(row=0, column=1, sticky="ns")  # A barra de rolagem será posicionada ao lado da tabela
        tabela_memoria.config(yscrollcommand=scrollbar_memoria.set)
        # =================================================================================

        # =================================================================================
        # Cria um frame para a simulação das instruções
        # =================================================================================
        #   |   |
        # X |   |
        frame_simulacao = tk.LabelFrame(root, text="Simulação", padx=10, pady=10)
        frame_simulacao.grid(row=3, column=0, padx=10, pady=10)

        # Cria o botão "Completa"
        botao_simular = tk.Button(frame_simulacao, text="Completa", command=executa_tudo, state=tk.DISABLED)
        botao_simular.grid(row=0, column=0, pady=5)

        # Cria o botão "Próxima Instrução" a direita de "Completa"
        botao_simular_parcial = tk.Button(frame_simulacao, text="Próxima Instrução", command=executa_instrucao, state=tk.DISABLED)
        botao_simular_parcial.grid(row=0, column=1, pady=5)

        # Cria o botão "Reiniciar" abaixo de "Completa"
        botao_reiniciar = tk.Button(frame_simulacao, text="Reiniciar Simulação", command=reiniciar, state=tk.DISABLED)
        botao_reiniciar.grid(row=1, column=0, pady=5)
        # =================================================================================

        # =================================================================================
        # Cria um frame de interface Entrada/Saída
        # =================================================================================
        #   |   |
        #   | X |
        frame_entrada = tk.LabelFrame(root, text="Porta", padx=10, pady=10)
        frame_entrada.grid(row=3, column=1, padx=10, pady=10)

        # Cria rótulo "Entrada"
        label_entrada = tk.Label(frame_entrada, text="Entrada:")
        label_entrada.grid(row=0, column=0, padx=10, pady=10)

        # Caixa de texto para entrada
        entry_numero = tk.Entry(frame_entrada, width=10)
        entry_numero.grid(row=0, column=1, padx=10, pady=10)

        # Cria um botão para enviar o número fornecido na entrada
        botao_processar = tk.Button(frame_entrada, text="Enviar", command=le_entrada, state=tk.DISABLED)
        botao_processar.grid(row=0, column=2, padx=10, pady=10)

        # Cria rótulo "Saída"
        label_saida = tk.Label(frame_entrada, text="Saída:")
        label_saida.grid(row=1, column=0, padx=10, pady=10)

        # Caixa de texto para saida com escrita desabilitada
        text_saida = tk.Text(frame_entrada, width=10, height=1)
        text_saida.grid(row=1, column=1, padx=10, pady=10)
        text_saida.config(state=tk.DISABLED)

        # =================================================================================

        # =================================================================================
        # Cria um frame para o log do simulador
        # =================================================================================
        #   |   |
        #   |   | X
        frame_log = tk.LabelFrame(root, text="Log", padx=10, pady=10)
        frame_log.grid(row=3, column=2, padx=10, pady=10)

        # Cria a caixa de texto para o log
        log_text = tk.Text(frame_log, width=70, height=10, wrap="word", state=tk.DISABLED)
        log_text.grid(row=0, column=0)

        # Adiciona uma barra de rolagem vertical para o log
        scrollbar_log = tk.Scrollbar(frame_log, orient="vertical", command=log_text.yview)
        scrollbar_log.grid(row=0, column=1, sticky="ns")  # Barra de rolagem do lado direito da caixa de texto
        log_text.config(yscrollcommand=scrollbar_log.set)
        # =================================================================================

        # Iniciar a interface gráfica
        root.mainloop()


    # ==================================================================================================
    # Funções de Suporte
    # ==================================================================================================

    # Função para atualizar os valores das tabelas "Registradores" e "Memorias"
    def atualiza_tabela():
        global auxs, ac, z, p, mem
        global tabela_registradores, tabela_memoria

        # Atualiza os valores da tabela dos registradores
        tabela_registradores.item(registradores_ids[0], values=("AUX0", auxs[0]))
        tabela_registradores.item(registradores_ids[1], values=("AUX1", auxs[1]))
        tabela_registradores.item(registradores_ids[2], values=("AUX2", auxs[2]))
        tabela_registradores.item(registradores_ids[3], values=("AUX3", auxs[3]))
        tabela_registradores.item(registradores_ids[4], values=("AC", ac))
        tabela_registradores.item(registradores_ids[5], values=("Z", z))
        tabela_registradores.item(registradores_ids[6], values=("P", p))

        # Atualiza os valores da tabela de memória
        for i in range(256):
            tabela_memoria.item(memoria_ids[i], values=(i, mem[i]))

    # Função para reiniciar o estado do simulador
    # Essa função é chamada sempre que um novo arquivo é carregado
    def reiniciar(newfile=False):
        global auxs, ac, mem, z, p, instrucoes, pc
        global text_saida, log_text, text_box
        global botao_simular, botao_simular_parcial, botao_reiniciar

        auxs = [0] * 4
        ac = 0
        mem = [0] * 256
        z = 0
        p = 0

        # Se um novo arquivo com instruções foi carregado
        if (newfile==True):
            instrucoes = {}
        # Se o botão "Reiniciar Simulação" foi pressionado
        else:
            adicionar_log("Reiniciando simulacao")
            text_box.config(state=tk.NORMAL)  # Habilitar edição para aplicar a tag
            text_box.tag_remove("executando", 1.0, tk.END)  # Remove qualquer tag anterior
            text_box.config(state=tk.DISABLED)  # Desabilita edição

        pc = 0

        atualiza_tabela()

        text_saida.config(state=tk.NORMAL)      # Habilita a escrita na caixa de texto "Saída"
        text_saida.delete(1.0, tk.END)          # Limpa a caixa de texto "Saída" (nesse caso utiliza-se o 1.0 como indicação)
        text_saida.config(state=tk.DISABLED)    # Desabilita a escrita na caixa de texto "Saída"

        entry_numero.delete(0, tk.END)          # Limpa a caixa de texto "Entrada" (nesse caso utiliza-se o 0 como indicação)

        # Habilita os botões de simulação da interface
        botao_simular.config(state=tk.NORMAL)
        botao_simular_parcial.config(state=tk.NORMAL)

        # Desabilita o botão de reiniciar a simulação
        botao_reiniciar.config(state=tk.DISABLED)

        # Coloca o fundo do log com a cor branca
        log_text.config(bg="white")

    # Função para adicionar mensagem ao log
    def adicionar_log(mensagem):
        global log_text

        log_text.config(state=tk.NORMAL)          # Habilita edição do log
        log_text.insert(tk.END, mensagem + "\n")  # Adiciona a nova mensagem
        log_text.yview(tk.END)                    # Move para a última linha do log
        log_text.config(state=tk.DISABLED)        # Desabilita edição do log

    # ==================================================================================================
    # Funções Atreladas aos Botões
    # ==================================================================================================

    # Função para selecionar o arquivo e exibir seu conteúdo na caixa de texto
    def selecionar_arquivo():
        global instrucoes
        global text_box
        global botao_simular, botao_simular_parcial

        rotulos = []
        mnemonicos = []
        operandos = []

        # Abrir o diálogo para selecionar o arquivo
        caminho_arquivo = filedialog.askopenfilename(title="Selecionar Arquivo", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))

        # Verifica se o caminho não está vazio
        if caminho_arquivo:

            # Reinicia o estado do simulador
            reiniciar(newfile=True)

            # Abrir o arquivo e exibir o conteúdo na caixa de texto
            with open(caminho_arquivo, 'r') as file:
                text_box.config(state=tk.NORMAL)    # Habilita a escrita na caixa de texto
                conteudo = file.read()
                conteudo = "\n".join(linha for linha in conteudo.splitlines() if "|" in linha)  # Remove as linhas em branco do conteúdo do arquivo
                linhas = conteudo.splitlines()
                text_box.delete(1.0, tk.END)        # Limpar o conteúdo atual
                text_box.insert(tk.END, conteudo)   # Inserir o conteúdo do arquivo
                text_box.config(state=tk.DISABLED)  # Desabilita a escrita na caixa de texto

                # Este simulador considera que cada instrucao presente no arquivo TXT possui o seguinte formato:
                #       rotulo | mnemonico | operando
                #       Ex: inicio | SOM AC+VAL => AC | 10
                # O rótulo pode estar vazio, fazendo com que o seja atribuido o índice da instrução como seu valor
                i = 0
                for instrucao in linhas:

                    # Deixa todas as letras em maiusculo
                    instrucao = instrucao.upper()

                    # Separa o rotulo da instrucao
                    rotulo = instrucao.split("|")[0]
                    rotulo = rotulo.replace(" ", "")
                    if rotulo == "":
                        rotulo = str(i)
                    rotulos.append(rotulo)

                    # Separa o mnemonico da instrução
                    mnemonico = instrucao.split("|")[1]
                    mnemonico = mnemonico.replace(" ", "")
                    mnemonicos.append(mnemonico)

                    # Separa o operando da instrução
                    operando = instrucao.split("|")[2]
                    operando = operando.replace(" ", "")
                    operando = operando.replace("\n", "")
                    operandos.append(operando)

                    i = i + 1

                # Apos preencher as listas de rotulos, mnemonicos e operandos é criado um dicionário com esses valores
                # O dicionário segue o seguinte padrão:
                #   instrucoes[chave] = (mnemonico,operando)

                for i in range(len(rotulos)):
                    instrucoes[rotulos[i]] = (mnemonicos[i], operandos[i])

            adicionar_log(f"Arquivo selecionado: {caminho_arquivo}")
            #adicionar_log(f"Instrucoes lidas:")
            #adicionar_log(f"{instrucoes}")

        else:
            adicionar_log("Erro! Nenhum arquivo foi selecionado")

    # Função para capturar e utilizar o número digitado pelo usuário na porta de entrada
    def le_entrada():
        global entrada, flag_entrada
        try:
            entrada = int(entry_numero.get())
            adicionar_log(f"Valor inserido: {entrada}")
            flag_entrada = True
        except ValueError:
            adicionar_log("Por favor, insira um número válido.")  # Em caso de erro, exibe uma mensagem no log

    # Função para tratar casos de exceção durante a simulação
    def tratar_excecao(e):
        global botao_simular, botao_simular_parcial, botao_reiniciar, log_text

        adicionar_log(f" Excecao {e} gerada. Finalizando a simulacao")
        botao_simular.config(state=tk.DISABLED)
        botao_simular_parcial.config(state=tk.DISABLED)
        botao_reiniciar.config(state=tk.DISABLED)
        log_text.config(bg="lightcoral")
        return True

    # Função que executa uma instrução do Sergium
    # A função retorna True quando todas as instruções tiverem sido simuladas ou se uma instrução for inválida
    def executa_instrucao():
        global root
        global auxs, ac, mem, z, p
        global instrucoes, pc
        global entrada, flag_entrada
        global botao_simular, botao_simular_parcial, botao_reiniciar, botao_processar
        global text_box, text_saida, log_text

        chaves = list(instrucoes.keys())
        botao_reiniciar.config(state=tk.NORMAL)

        # Se todas as instruções já foram executadas, desabilita os botões de simulação e habilita o botao de reiniciar
        if pc == len(chaves):
            botao_simular.config(state=tk.DISABLED)
            botao_simular_parcial.config(state=tk.DISABLED)
            log_text.config(bg="lightgreen")
            return True

        # Caso contrário, simula uma instrução
        else:
            chave = chaves[pc]
            mnemonico = instrucoes[chave][0]
            operando = instrucoes[chave][1]

            # Destacar a linha da instrução executada
            text_box.config(state=tk.NORMAL)  # Habilitar edição para aplicar a tag
            text_box.tag_remove("executando", 1.0, tk.END)  # Remove qualquer tag anterior
            linha_inicio = f"{pc + 1}.0"  # A linha que será destacada, ajustada para o índice das linhas
            linha_fim = f"{pc + 1}.end"
            text_box.tag_add("executando", linha_inicio, linha_fim)  # Aplica a tag na linha atual
            text_box.tag_configure("executando", background="lightgreen")  # Define a cor de fundo da tag
            text_box.config(state=tk.DISABLED)  # Desabilita edição

            adicionar_log(f"Executando instrução {mnemonico} | {operando}")

            if (mnemonico == "ENTPORTA=>AC") and (operando == "0"):
                botao_processar.config(state=tk.NORMAL)  # Habilita botao de leitura da entrada
                while(flag_entrada == False):            # Enquanto o botão não for pressionado
                    root.update_idletasks()              # Espera o botão ser pressionado rodando funções para que a interface gráfica não congele
                    root.update()
                flag_entrada = False
                ac = entrada
                botao_processar.config(state=tk.DISABLED) # Desabilita botao de leitura da entrada

            elif (mnemonico == "SAIAC=>PORTA") and (operando == "2"):
                text_saida.config(state=tk.NORMAL)      # Habilita a escrita na caixa de texto "Saída"
                text_saida.delete(1.0, tk.END)          # Limpa a caixa de texto "Saída"
                text_saida.insert(tk.END, str(ac))      # Insere o valor do acumulador nela
                text_saida.config(state=tk.DISABLED)    # Desabilita a escrita na caixa de texto "Saída"
                adicionar_log(f"Valor impresso na saída: {ac}")

            elif (mnemonico == "COPAUX=>AC"):
                try:
                    ac = auxs[int(operando)]
                except Exception as e:
                    return tratar_excecao(e)

            elif (mnemonico == "COPAC=>AUX"):
                try:
                    auxs[int(operando)] = ac
                except Exception as e:
                    return tratar_excecao(e)

            elif (mnemonico == "COPMEM=>AC"):
                try:
                    ac = mem[int(operando)]
                except Exception as e:
                    return tratar_excecao(e)

            elif (mnemonico == "COPAC=>MEM"):
                try:
                    mem[int(operando)] = ac
                except Exception as e:
                    return tratar_excecao(e)

            elif (mnemonico == "COPVAL=>AC"):
                try:
                    ac = int(operando)
                except Exception as e:
                    return tratar_excecao(e)

            elif (mnemonico == "SOMAC+AUX=>AC"):
                try:
                    ac = ac + auxs[int(operando)]
                    z = 1 if ac == 0 else 0
                    p = 1 if ac > 0 else 0
                except Exception as e:
                    return tratar_excecao(e)

            elif (mnemonico == "SUBAC-AUX=>AC"):
                try:
                    ac = ac - auxs[int(operando)]
                    z = 1 if ac == 0 else 0
                    p = 1 if ac > 0 else 0
                except Exception as e:
                    return tratar_excecao(e)

            elif (mnemonico == "SOMAC+VAL=>AC"):
                try:
                    ac = ac + int(operando)
                    z = 1 if ac == 0 else 0
                    p = 1 if ac > 0 else 0
                except Exception as e:
                    return tratar_excecao(e)

            elif (mnemonico == "SUBAC-VAL=>AC"):
                try:
                    ac = ac - int(operando)
                    z = 1 if ac == 0 else 0
                    p = 1 if ac > 0 else 0
                except Exception as e:
                    return tratar_excecao(e)

            elif(mnemonico == "VAI"):
                if (operando in chaves):
                    pc = chaves.index(operando)
                    return False
                else:
                    adicionar_log(f" Rótulo {operando} invalido. Finalizando a simulacao")
                    botao_simular.config(state=tk.DISABLED)
                    botao_simular_parcial.config(state=tk.DISABLED)
                    log_text.config(bg="lightcoral")
                    return True

            elif(mnemonico == "VAISEZ=1"):
                if (z == 1):
                    if (operando in chaves):
                        pc = chaves.index(operando)
                        return False
                    else:
                        adicionar_log(f" Rótulo {operando} invalido. Finalizando a simulacao")
                        botao_simular.config(state=tk.DISABLED)
                        botao_simular_parcial.config(state=tk.DISABLED)
                        log_text.config(bg="lightcoral")
                        return True

            elif(mnemonico == "VAISEP=1"):
                if (p == 1):
                    if (operando in chaves):
                        pc = chaves.index(operando)
                        return False
                    else:
                        adicionar_log(f" Rótulo {operando} invalido. Finalizando a simulacao")
                        botao_simular.config(state=tk.DISABLED)
                        botao_simular_parcial.config(state=tk.DISABLED)
                        log_text.config(bg="lightcoral")
                        return True

            elif(mnemonico == "PARA"):
                botao_simular.config(state=tk.DISABLED)
                botao_simular_parcial.config(state=tk.DISABLED)
                log_text.config(bg="lightgreen")
                return True

            else:
                adicionar_log(f" Instrução {mnemonico} | {operando} invalida. Finalizando a simulacao")
                botao_simular.config(state=tk.DISABLED)
                botao_simular_parcial.config(state=tk.DISABLED)
                log_text.config(bg="lightcoral")
                return True

            pc = pc + 1
            atualiza_tabela()
            return False


    # Funcao que executa todas as instruções de uma vez
    def executa_tudo():
        while(executa_instrucao() == False):
            continue
        adicionar_log(f"Fim da Simulação")

    # Caso o botão de fechar da interface gráfica seja pressionado, fecha a interface e encerra o processo do simulador
    def fechar():
        global root
        print("Simulador encerrado")
        root.destroy()
        sys.exit(0)

    # ==================================================================================================
    # Main
    # ==================================================================================================
    criar_interface()