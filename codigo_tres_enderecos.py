from analisador_lexico import AnalisadorLexico
from analisador_sintatico import *
from analisador_semantico import *
from tabela_simbolos import *

class CodigoTresEnderecos:
    def __init__(self, tokens_encontrados, tabela_simbolos):
        self.temporarios = []
        self.tokens = tokens_encontrados
        self.tabela_simbolos = tabela_simbolos
        self.nome_arquivo = "codigo_enderecos.txt"
        self.posicao = 0

    def salvar_codigo_tres_enderecos(self, nome_arquivo):

        contador = 0;
        rotulo_count = 0


        with open(nome_arquivo, 'w') as arquivo:
            for posicao, token in enumerate(self.tokens):

                # Verifica inicialização de variável
                if self.tokens[posicao]['tipo'] in ['INT', 'BOOLEAN'] and self.tokens[posicao - 1]['valor'] not in ['(', ',']:
                    if self.tokens[posicao + 1]['tipo'] == 'IDENTIFICADOR' and self.tokens[posicao + 2]['valor'] not in ['(', '=']:
                        arquivo.write(str(self.tokens[posicao + 1]['valor']) + '\n')
                    # Chamada de Funcão
                    elif self.tokens[posicao + 2]['valor'] == '=':
                        if self.tokens[posicao + 3]['tipo'] == 'IDENTIFICADOR':
                            nome_funcao = self.tokens[posicao + 3]['valor']
                            if self.tokens[posicao + 4]['tipo'] == '(':
                                for posicao, token in enumerate(self.tokens[posicao + 4:], start=posicao + 4):
                                    if self.tokens[posicao]['tipo'] != ')':
                                        if self.tokens[posicao]['tipo'] == 'IDENTIFICADOR':
                                            # Adiciona uma variavel no contador
                                            contador += 1
                                            arquivo.write('param ' + str(self.tokens[posicao]['valor']) + '\n')
                                    else:
                                        arquivo.write(f'call {nome_funcao}, {contador}  \n')
                                        contador = 0
                                        break

                    elif self.tokens[posicao + 1]['tipo'] == 'FUNC':
                        if self.tokens[posicao + 2]['tipo'] == 'IDENTIFICADOR':
                            nome_funcao = self.tokens[posicao + 2]['valor']
                            arquivo.write(f'{nome_funcao}: \n')
                            if self.tokens[posicao + 3]['tipo'] == '(':
                                for posicao, token in enumerate(self.tokens[posicao + 3:], start=posicao + 3):
                                    if self.tokens[posicao]['tipo'] != ')':
                                        if self.tokens[posicao]['tipo'] == 'IDENTIFICADOR' and self.tokens[posicao - 1]['tipo'] != 'RETURN':
                                            # Adiciona uma variavel no contador
                                            contador += 1
                                            arquivo.write('param ' + str(self.tokens[posicao]['valor']) + '\n')

                                    else:
                                        print(self.tokens[posicao]['valor'])
                                        for posicao, token in enumerate(self.tokens[posicao:], start=posicao):


                                            if self.tokens[posicao]['tipo'] != 'RETURN':
                                                print(token['valor'])
                                            elif self.tokens[posicao]['tipo'] == 'RETURN':
                                                arquivo.write('return ')
                                                for posicao, token in enumerate(self.tokens[posicao:], start=posicao):
                                                    if self.tokens[posicao]['tipo'] != ';':
                                                        if self.tokens[posicao]['tipo'] == 'IDENTIFICADOR':
                                                            arquivo.write(str(self.tokens[posicao]['valor']+ '\n'))
                                                    else:
                                                        break




                # Verifica atribuição de variável
                elif self.tokens[posicao]['tipo'] == 'IDENTIFICADOR' and self.tokens[posicao - 1]['valor'] != '':
                    if self.tokens[posicao + 1]['valor'] == '=':
                        if self.tokens[posicao + 2]['tipo'] in  ['NUMERO', 'IDENTIFICADOR'] and self.tokens[posicao + 3]['valor'] != '(':
                            if self.tokens[posicao + 3]['tipo'] == ';':
                                arquivo.write(str(self.tokens[posicao]['valor']) + ' = ' + str(self.tokens[posicao + 2]['valor']) + '\n')
                            # Verifica atribuição de variável
                            elif self.tokens[posicao + 3]['tipo'] == 'OP_ARITMETICO':
                                # Adiciona as variaveis ao vetor
                                self.temporarios.append(self.tokens[posicao + 2]['valor'])
                                self.temporarios.append(self.tokens[posicao + 3]['valor'])
                                arquivo.write(str(self.tokens[posicao]['valor']) + ' = ' + str(
                                                self.tokens[posicao + 2]['valor']) + ' ' + str(self.tokens[posicao + 3]['valor']))
                                for posicao, token in enumerate(self.tokens[posicao + 4:], start=posicao + 4):

                                    if self.tokens[posicao]['tipo'] != ';':
                                        # Adiciona as variaveis ao vetor
                                        self.temporarios.append(self.tokens[posicao]['valor'])
                                        arquivo.write(' ' + str(self.tokens[posicao]['valor']))
                                    else:
                                        valor_temp = 1
                                        self.temporarios.reverse()
                                        print(self.temporarios)
                                        while len(self.temporarios) > 0:

                                            if valor_temp == 1:
                                               arquivo.write('\n'+f'temp{valor_temp} = {self.temporarios[2]} {self.temporarios[1]} {self.temporarios[0]}')
                                               self.temporarios.remove(self.temporarios[2])
                                               self.temporarios.remove(self.temporarios[1])
                                               self.temporarios.remove(self.temporarios[0])

                                            else:
                                                arquivo.write(
                                                    '\n' + f'temp{valor_temp} = {self.temporarios[1]} {self.temporarios[0]} temp{valor_temp - 1}')
                                                self.temporarios.remove(self.temporarios[1])
                                                self.temporarios.remove(self.temporarios[0])
                                            print(self.temporarios)
                                            valor_temp += 1
                                        self.temporarios = []
                                        arquivo.write('\n')

                                        break

                # Chamada de Funcão
                elif posicao + 2 < len(self.tokens) and self.tokens[posicao + 2]['tipo'] == 'IDENTIFICADOR' and self.tokens[posicao - 1]['tipo'] not in ['INT', 'BOOLEAN']:
                    nome_funcao = self.tokens[posicao + 2]['valor']
                    if self.tokens[posicao + 3]['tipo'] == '(':
                        for posicao, token in enumerate(self.tokens[posicao + 3:], start=posicao + 3):
                            if self.tokens[posicao]['tipo'] != ')':
                                if self.tokens[posicao]['tipo'] == 'IDENTIFICADOR':
                                    # Adiciona uma variavel no contador
                                    contador += 1
                                    arquivo.write('param ' + str(self.tokens[posicao]['valor']) + '\n')
                            else:
                                arquivo.write(f'call {nome_funcao}, {contador}  \n')
                                contador = 0
                                break
                # Verifica comando condicional (if ou while)F
                elif self.tokens[posicao]['tipo'] in ['IF', 'WHILE']:
                    if self.tokens[posicao]['tipo'] == 'IF':
                        posicao = self.processa_condicional(
                            posicao, arquivo, rotulo_count)
                    elif self.tokens[posicao]['tipo'] == 'WHILE':
                        posicao = self.processa_while(
                            posicao, arquivo, rotulo_count)
                    rotulo_count += 2

                # Verifica comando de impressão (print)
                elif self.tokens[posicao]['tipo'] == 'PRINT':
                    arquivo.write("\n" + "print " +
                                  self.tokens[posicao + 2]['valor'] + "\n")

                # Verifica chamada de procedimento
                elif self.tokens[posicao]['tipo'] == 'CHAMADA_PROCEDIMENTO':
                    self.chamada_de_procedimento(arquivo)

                # Verifica declaração de procedimento
                elif self.tokens[posicao]['tipo'] == 'DECLARACAO_PROCEDIMENTO':
                    self.declaracao_procedimento(posicao, arquivo)

                # Avança para o próximo token
                posicao += 1

    def processa_condicional(self, posicao, arquivo, rotulo_count):
        # Lê o token "if"
        posicao += 1
        token = self.tokens[posicao]

        # Lê a condição do "if"
        condicao = ""
        while self.tokens[posicao]['valor'] != ";":
            condicao += self.tokens[posicao]['valor'] + " "
            posicao += 1

        # Remove o último espaço extra
        condicao = condicao[:-1]

        # Escreve a condição do "if"
        arquivo.write("if " + condicao + " goto L" + str(rotulo_count) + "\n")
        arquivo.write("goto L" + str(rotulo_count + 1) + "\n")
        arquivo.write("L" + str(rotulo_count) + ":\n")

        # Encontra o início do bloco do "if" ou "while"
        while self.tokens[posicao]['valor'] != "begin":
            posicao += 1

        # Processa o bloco do "if" ou "while"
        self.processa_bloco(posicao, arquivo)

        arquivo.write("L" + str(rotulo_count + 1) + ":\n")

        return posicao

    def processa_while(self, posicao, arquivo, rotulo_count):
        # Lê o token "while"
        posicao += 1

        # Lê a condição do "while"
        condicao = ""
        while self.tokens[posicao]['valor'] != ";":
            condicao += self.tokens[posicao]['valor'] + " "
            posicao += 1

        # Remove o último espaço extra
        condicao = condicao[:-1]

        # Escreve a condição do "while"
        arquivo.write("L" + str(rotulo_count) + ":\n")
        arquivo.write("if " + condicao + " goto L" +
                      str(rotulo_count + 1) + "\n")
        arquivo.write("goto L" + str(rotulo_count + 1) + "\n")
        arquivo.write("L" + str(rotulo_count + 1) + ":\n")

        # Encontra o início do bloco do "while"
        while self.tokens[posicao]['valor'] != "begin":
            posicao += 1

        # Processa o bloco do "while"
        self.processa_bloco(posicao, arquivo)

        arquivo.write("goto L" + str(rotulo_count) + "\n")

        return posicao

    def declaracao_procedimento(self, posicao, arquivo):
        arquivo.write('proc ' + str(self.tokens[posicao]['valor']) + ' ')
        posicao += 1
        while self.tokens[posicao]['tipo'] != 'BEGIN':
            if self.tokens[posicao]['tipo'] in ['NUMERO', 'IDENTIFICADOR']:
                arquivo.write(str(self.tokens[posicao]['valor']) + ' ')
            posicao += 1
        arquivo.write('\n')

    def chamada_de_procedimento(self, posicao, arquivo):
        arquivo.write('call ' + str(self.tokens[posicao]['valor']) + ' ')
        posicao += 1
        while self.tokens[posicao]['tipo'] != ';':
            if self.tokens[posicao]['tipo'] in ['NUMERO', 'IDENTIFICADOR']:
                arquivo.write(str(self.tokens[posicao]['valor']) + ' ')
            posicao += 1
        arquivo.write('\n')

    def processa_bloco(self, posicao, arquivo):
        # Lê tokens até encontrar o fim do bloco
        while self.tokens[posicao]['valor'] != "end":
            # Se encontrar uma variável, escreve seu nome
            if self.tokens[posicao]['tipo'] == 'IDENTIFICADOR':
                arquivo.write(self.tokens[posicao]['valor'])
            posicao += 1

    def carrega_codigo(self):
        self.salvar_codigo_tres_enderecos(self.nome_arquivo)


    def cria_codigo_3_endereco(self):
        self.carrega_codigo()
        for token in self.tokens:
            print(token)




codigo = "exemplo_codigo/atribuicao.txt"

# Carrega o código de um arquivo TXT
programa_exemplo = AnalisadorLexico(codigo)

# Obtém os tokens do programa
tokens_encontrados, tabela_simbolos = programa_exemplo.carregar_tokens()


# Crie uma instância do analisador sintático e realize a análise
analisador = AnalisadorSintatico(tokens_encontrados, codigo)
analisador.analise_sintatica()

# Crie uma instância do analisador semântico e realize a análise
analisador_semantico = AnalisadorSemantico(tabela_simbolos, tokens_encontrados)
analisador_semantico.realizar_analise_semantica(tokens_encontrados)

codigo_3_enderecos = CodigoTresEnderecos(tokens_encontrados, tabela_simbolos)
codigo_3_enderecos.cria_codigo_3_endereco()