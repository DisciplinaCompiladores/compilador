def carregar_palavras_reservadas(palavras):
    palavras_reservadas = []

    # Ler o txt com o código
    with open(palavras, 'r') as arquivo:
        linhas = arquivo.read()
        # Dividir a string em uma lista de palavras
        palavras_divididas = linhas.split()

        # Adicionar cada palavra ao vetor
        for palavra in palavras_divididas:
            palavras_reservadas.append(palavra.strip())

    return palavras_reservadas

