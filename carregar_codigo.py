def carregar_codigo(codigo):
    # Ler o txt com o código
    with open(codigo, 'r') as arquivo:
        linha = arquivo.read()
        return linha