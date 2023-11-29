from carregar_codigo import carregar_codigo

def carregar_tokens(programa, palavras_reservadas):
    tokens = []
    i = 0  # índice para percorrer o programa

    while i < len(programa):
        char = programa[i]

        # Ignorar espaços em branco e quebras de linha
        if char.isspace():
            i += 1
            continue

        # Identificadores e palavras-chave
        if char.isalpha() or char == '_':
            identificador = char
            i += 1
            while i < len(programa) and (programa[i].isalnum() or programa[i] == '_'):
                identificador += programa[i]
                i += 1

            # Roda o vetor de palavras reservads
            for palavra in palavras_reservadas:
                # Se palavra reservada é igual
                if identificador == palavra:
                    tokens.append({'tipo': palavra, 'valor': identificador})

        # Números
        elif char.isdigit():
            numero = char
            i += 1
            while i < len(programa) and programa[i].isdigit():
                numero += programa[i]
                i += 1
            tokens.append({'tipo': 'NUMERO', 'valor': numero})

        # Operadores relacionais
        elif char in "=!><":
            operador_relacional = char
            i += 1
            if i < len(programa) and programa[i] == '=':
                operador_relacional += '='
                i += 1
            tokens.append({'tipo': 'OP_RELACIONAL', 'valor': operador_relacional})

        # Operadores aritméticos
        elif char in "+-*/":
            tokens.append({'tipo': 'OP_ARITMETICO', 'valor': char})
            i += 1

        # Outros caracteres especiais
        else:
            tokens.append({'tipo': char, 'valor': char})
            i += 1

    return tokens


