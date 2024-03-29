from analisador_lexico import *

class AnalisadorSintatico:
    def __init__(self, tokens, codigo):
        self.posicao = 0
        self.codigo = codigo
        self.tokens = tokens

    def analise_sintatica(self):
        try:
            self.programa()
        except Exception as e:
            print(f"{e}")

    def programa(self):
        self.match('PROGRAMA')
        self.identificador()
        self.match(';')
        self.bloco()

    def identificador(self):
        if self.tokens[self.posicao]['tipo'] == 'IDENTIFICADOR':
            self.avancar()
            return
        else:
            raise SyntaxError(f"Erro de sintaxe: Identificador inválido \"{self.tokens[self.posicao]['tipo']}\" na linha {self.tokens[self.posicao]['linha']}")

    def match(self, terminal):
        if self.tokens[self.posicao]['tipo'] == terminal:
            self.avancar()
        else:
            raise SyntaxError(f"Erro de sintaxe: Esperado {terminal} na linha {self.tokens[self.posicao]['linha']}, mas encontrado {self.tokens[self.posicao]['tipo']}")

    def bloco(self):
        # Verifica se o bloco está vazio
        if self.tokens[self.posicao]['tipo'] == 'END' and self.tokens[self.posicao - 1]['tipo'] == 'BEGIN':
            raise SyntaxError(
                f"Erro de sintaxe: Bloco vazio {self.tokens[self.posicao]['linha']}")
        elif self.tokens[self.posicao]['tipo'] in ['BREAK', 'CONTINUE', 'RETURN']:
            raise SyntaxError(
                f"Erro de sintaxe: Uso invalido de {self.tokens[self.posicao]['valor']} na linha {self.tokens[self.posicao]['linha']}")
        while self.tokens[self.posicao]['tipo'] in ['INT', 'BOOLEAN']:
            if self.tokens[self.posicao + 1]['tipo'] == 'FUNC':
                self.declaracao_funcao()
            else:
                self.declaracao_variaveis()
        while self.tokens[self.posicao]['tipo'] in ['IDENTIFICADOR', 'IF', 'WHILE', 'PRINT']:
            self.comando()

        self.bloco()


    def declaracao_variaveis(self):
        self.tipo()
        if self.tokens[self.posicao + 1]['valor'] == ';':
            self.identificador()
            self.match(';')
        else:
            self.atribuicao()

    def tipo(self):
        if self.tokens[self.posicao]['tipo'] in ['INT', 'BOOLEAN']:
            self.avancar()
            return
        else:
            raise SyntaxError(f"Erro de sintaxe: Tipo inválido na linha {self.tokens[self.posicao]['linha']}")


    def declaracao_funcao(self):
        self.tipo()
        self.match('FUNC')
        self.identificador()
        self.match('(')
        if self.tokens[self.posicao]['tipo'] in ['INT', 'BOOLEAN']:
            self.parametro()
        self.match(')')
        self.match(';')
        self.bloco_funcao()

    def declaracao_procedimento(self):
        self.bloco_procedimento()

    def parametro(self):
        self.tipo()
        self.identificador()
        while self.tokens[self.posicao]['tipo'] == ',':
            self.avancar()
            self.tipo()
            self.identificador()

    def avancar(self):
        if self.posicao < len(self.tokens) - 1:
            self.posicao += 1
            return
        elif self.posicao == len(self.tokens) - 1 and self.tokens[self.posicao]['tipo'] == 'END' or self.tokens[self.posicao]['tipo'] == ';':
            raise SyntaxError("Nenhum Erro Sintático")
        else:
            raise SyntaxError(f"Erro Sintático: Faltando completar o código na linha {self.tokens[self.posicao]['linha']}")

    def bloco_funcao(self):
        self.match('BEGIN')
        # Verifica se o bloco está vazio
        if self.tokens[self.posicao]['tipo'] == 'END' and self.tokens[self.posicao - 1]['tipo'] == 'BEGIN':
            raise SyntaxError(
                f"Erro de sintaxe: Bloco vazio {self.tokens[self.posicao]['linha']}")
        if self.tokens[self.posicao]['tipo'] in ['BREAK', 'CONTINUE']:
            raise SyntaxError(
                f"Erro de sintaxe: Uso invalido de {self.tokens[self.posicao]['valor']} na linha {self.tokens[self.posicao]['linha']}")

        while self.tokens[self.posicao]['tipo'] in ['INT', 'BOOLEAN']:
            if self.tokens[self.posicao + 1]['tipo'] == 'FUNC':
                self.declaracao_funcao()
            else:
                self.declaracao_variaveis()
        while self.tokens[self.posicao]['tipo'] in ['IDENTIFICADOR', 'IF', 'WHILE', 'RETURN', 'BREAK', 'CONTINUE',                                                'PRINT']:
            self.comando()
        if self.tokens[self.posicao]['tipo'] == 'END':
            self.match('END')
        else:
            self.bloco_funcao()

    def expressao(self):
        self.expressao_simples()
        if self.tokens[self.posicao]['tipo'] in ['IDENTIFICADOR']:
            self.identificador()
        elif self.tokens[self.posicao]['valor'] in ['==', '!=', '>', '>=', '<', '<=']:
            self.op_relacional()
            if self.tokens[self.posicao]['tipo'] in ['IDENTIFICADOR']:
                self.expressao_simples()
        elif self.tokens[self.posicao]['valor'] in ['+', '-', '*', '/']:
            self.expressao_simples()

    def expressao_simples(self):
        if self.tokens[self.posicao]['valor'] in ['+', '-']:
            self.op_aditivo()
        self.termo()
        while self.tokens[self.posicao]['tipo'] in ['+', '-']:
            self.op_aditivo()
            self.termo()

    def atribuicao(self):
        self.identificador()
        self.match('OP_RELACIONAL')
        if self.tokens[self.posicao]['tipo'] == 'NUMERO':
            self.match('NUMERO')
            if self.tokens[self.posicao]['tipo'] != ';':
                self.expressao()
        elif self.tokens[self.posicao]['tipo'] == 'IDENTIFICADOR':
            self.identificador()
            if self.tokens[self.posicao]['tipo'] != ';' and self.tokens[self.posicao]['tipo'] != '(':
                self.expressao()
            elif self.tokens[self.posicao]['tipo'] == '(':
                self.match('(')
                if self.tokens[self.posicao]['tipo'] in ['INT', 'BOOLEAN']:
                    self.parametro()
                self.match(')')
        elif self.tokens[self.posicao]['tipo'] == 'BOOLEAN':
            self.match('BOOLEAN')
        else:
            self.expressao()
        self.match(';')

    def comando(self):
        if self.tokens[self.posicao]['tipo'] == 'IDENTIFICADOR':
            if self.posicao + 1 < len(self.tokens) and self.tokens[self.posicao + 1]['valor'] == '(':
                self.chamada_procedimento_funcao()
            else:
                self.atribuicao()
        elif self.tokens[self.posicao]['tipo'] == 'IF':
            self.condicional()
        elif self.tokens[self.posicao]['tipo'] == 'WHILE':
            self.enquanto()
        elif self.tokens[self.posicao]['tipo'] == 'RETURN':
            self.comando_retorno()
        elif self.tokens[self.posicao]['tipo'] == 'PRINT':
            self.escrita()
        else:
            raise SyntaxError("Erro de sintaxe: Comando inválido")

    def enquanto(self):
        self.match('WHILE')
        self.match('(')
        self.expressao()
        self.match(')')
        self.match(';')
        self.bloco_enquanto()


    def termo(self):
        if self.tokens[self.posicao]['valor'] in ['*', '/']:
            self.op_multiplicativo()
            self.fator()
        else:
            self.fator()
        while self.tokens[self.posicao]['valor'] in ['*', '/']:
            self.op_multiplicativo()
            self.fator()

    def fator(self):
        if self.tokens[self.posicao]['tipo'] == 'IDENTIFICADOR':
            self.identificador()
        elif self.tokens[self.posicao]['tipo'] == 'NUMERO':
            self.avancar()
        elif self.tokens[self.posicao]['tipo'] == '(':
            self.avancar()
            self.expressao()
            self.match(')')
        elif self.tokens[self.posicao]['tipo'] in ['TRUE', 'FALSE']:
            self.avancar()
        elif self.tokens[self.posicao]['tipo'] == 'NAO':
            self.avancar()
            self.fator()
        else:
            raise SyntaxError(f"Erro de sintaxe: Fator {self.tokens[self.posicao]['tipo']} inválido na linha {self.tokens[self.posicao]['linha']}")

    def bloco_enquanto(self):
        self.match('BEGIN')
        # Verifica se o bloco está vazio
        if self.tokens[self.posicao]['tipo'] == 'END' and self.tokens[self.posicao - 1]['tipo'] == 'BEGIN':
            raise SyntaxError(
                f"Erro de sintaxe: Bloco vazio {self.tokens[self.posicao]['linha']}")
        elif self.tokens[self.posicao]['tipo'] in ['BREAK', 'CONTINUE']:
            self.comando_desvio_incondicional()
        elif self.tokens[self.posicao]['tipo'] == 'RETURN':
            raise SyntaxError(
                f"Erro de sintaxe: Uso invalido de {self.tokens[self.posicao]['valor']} na linha {self.tokens[self.posicao]['linha']}")
        while self.tokens[self.posicao]['tipo'] in ['INT', 'BOOLEAN']:
            if self.tokens[self.posicao + 1]['tipo'] == 'FUNC':
                self.declaracao_funcao()
            else:
                self.declaracao_variaveis()
        while self.tokens[self.posicao]['tipo'] in ['IDENTIFICADOR', 'IF', 'WHILE',
                                                    'PRINT']:
            self.comando()
        if self.tokens[self.posicao]['tipo'] == 'END':
            self.match('END')
        else:
            self.bloco_enquanto()

    def comando_desvio_incondicional(self):

        if self.tokens[self.posicao]['tipo'] in ['BREAK', 'CONTINUE']:
            self.avancar()
            self.match(';')
        else:
            raise SyntaxError("Erro de sintaxe: Comando de desvio incondicional inválido")

    def escrita(self):
        self.match('PRINT')
        self.match('(')
        if self.tokens[self.posicao]['tipo'] == 'NUMERO':
            self.fator()
            self.match(')')
            self.match(';')
        else:
            self.expressao()
        self.match(')')
        self.match(';')

    def condicional(self):
        self.match('IF')
        self.match('(')
        self.expressao()
        self.match(')')
        self.match(';')
        self.bloco_condicional()
        if(self.tokens[self.posicao]['tipo'] == 'ELSE'):
            self.avancar()
            self.match(';')
            self.bloco_condicional()



    def bloco_condicional(self):
        self.match('BEGIN')
        # Verifica se o bloco está vazio
        if self.tokens[self.posicao]['tipo'] == 'END' and self.tokens[self.posicao - 1]['tipo'] == 'BEGIN':
            raise SyntaxError(
                f"Erro de sintaxe: Bloco vazio {self.tokens[self.posicao]['linha']}")
        elif self.tokens[self.posicao]['tipo'] in ['BREAK', 'CONTINUE', 'RETURN']:
            raise SyntaxError(
                f"Erro de sintaxe: Uso invalido de {self.tokens[self.posicao]['valor']} na linha {self.tokens[self.posicao]['linha']}")
        while self.tokens[self.posicao]['tipo'] in ['INT', 'BOOLEAN']:
            if self.tokens[self.posicao + 1]['tipo'] == 'FUNC':
                self.declaracao_funcao()
            else:
                self.declaracao_variaveis()
        while self.tokens[self.posicao]['tipo'] in ['IDENTIFICADOR', 'IF', 'WHILE',
                                                    'PRINT']:
            self.comando()
        if self.tokens[self.posicao]['tipo'] == 'END':
            self.match('END')
        else:
            self.bloco_condicional()

    def op_relacional(self):
        if self.tokens[self.posicao]['valor'] in ['==', '!=', '>', '>=', '<', '<=']:
            self.avancar()
        else:
            raise SyntaxError("Erro de sintaxe: Operador relacional inválido")

    def op_aditivo(self):
        if self.tokens[self.posicao]['valor'] in ['+', '-']:
            self.avancar()
        else:
            raise SyntaxError("Erro de sintaxe: Operador aditivo inválido")

    def comando_retorno(self):
        self.match('RETURN')
        self.expressao()
        self.match(';')


    def chamada_procedimento_funcao(self):
        self.identificador()
        self.match('(')
        if self.tokens[self.posicao]['tipo'] in ['INT', 'BOOLEAN']:
            self.parametro()
        self.match(')')
        self.match(';')
        if self.tokens[self.posicao]['tipo'] in ['BEGIN']:
            self.declaracao_procedimento()

    def op_multiplicativo(self):
        if self.tokens[self.posicao]['valor'] in ['*', '/']:
            self.avancar()
        else:
            raise SyntaxError("Erro de sintaxe: Operador multiplicativo inválido")


    def bloco_procedimento(self):
        self.match('BEGIN')
        # Verifica se o bloco está vazio
        if self.tokens[self.posicao]['tipo'] == 'END' and self.tokens[self.posicao - 1]['tipo'] == 'BEGIN':
            raise SyntaxError(
                f"Erro de sintaxe: Bloco vazio {self.tokens[self.posicao]['linha']}")
        elif self.tokens[self.posicao]['tipo'] in ['BREAK', 'CONTINUE', 'RETURN']:
            raise SyntaxError(
                f"Erro de sintaxe: Uso invalido de {self.tokens[self.posicao]['valor']} na linha {self.tokens[self.posicao]['linha']}")

        while self.tokens[self.posicao]['tipo'] in ['INT', 'BOOLEAN']:
            if self.tokens[self.posicao + 1]['tipo'] == 'FUNC':
                self.declaracao_funcao()
            else:
                self.declaracao_variaveis()
        while self.tokens[self.posicao]['tipo'] in ['IDENTIFICADOR', 'IF', 'WHILE',
                                                    'PRINT']:
            self.comando()
        if self.tokens[self.posicao]['tipo'] == 'END':
            self.match('END')
        else:
            self.bloco_procedimento()

