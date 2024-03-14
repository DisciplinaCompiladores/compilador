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


        with open(nome_arquivo, 'w') as arquivo:
            for posicao, token in enumerate(self.tokens):

                # Verifica inicialização de variável
                if self.tokens[posicao]['tipo'] in ['INT', 'BOOLEAN']:
                    if self.tokens[posicao + 1]['tipo'] == 'IDENTIFICADOR' and self.tokens[posicao + 2]['tipo'] == '(':
                        arquivo.write(str(self.tokens[posicao + 1]['valor']) + '\n')
                    elif self.tokens[posicao + 1]['tipo'] == 'FUNC':
                        if self.tokens[posicao + 2]['tipo'] == 'IDENTIFICADOR':
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
                                        break



                # Verifica atribuição de variável
                elif self.tokens[posicao]['tipo'] == 'IDENTIFICADOR':
                    if self.tokens[posicao + 1]['valor'] == '=':
                        if self.tokens[posicao + 2]['tipo'] in  ['NUMERO', 'IDENTIFICADOR']:
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