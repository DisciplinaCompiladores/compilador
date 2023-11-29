from analisador_lexico import carregar_tokens
from carregar_codigo import carregar_codigo
from carregar_palavras_reservadas import carregar_palavras_reservadas

codigo = 'codigo.txt'
palavras = 'palavras_reservadas.txt'

# Carrega o código de um TXT
programa_exemplo = carregar_codigo(codigo)

# Carrega o código de um TXT
palavras_reservadas = carregar_palavras_reservadas(palavras)

tokens_encontrados = carregar_tokens(programa_exemplo, palavras_reservadas)

for token in tokens_encontrados:
    print(token)