"""
# Exercício Programa III – MAC 122 – PDA
# Patrick Marques de Barros Costa
# NUSP: 11257550
"""

def aplica_funcao_hash(string_nome, tabela_hash_tam):
    '''
    Função de hash que vamos aplicar
    Ideia: fazer a soma dos valores ASCII das letras e dps fazer o módulo
    '''
    soma_das_letras = 0
    for letra in string_nome:
        soma_das_letras += ord(letra)
    primeiro_hash = (soma_das_letras + 1) % (tabela_hash_tam * 2)
    segundo_hash = (primeiro_hash + len(string_nome)) % tabela_hash_tam
    return segundo_hash

def cria_hash(TAB):
    # Defini como tamanho da tabela de hash um terço do tamanho da tabela que
    # li do arquivo
    tabela_hash_tam = int(len(TAB)/3)

    # Crio uma tabela hash
    # É basicamente um dict de listas
    tabela_hash = {i: [] for i in range(tabela_hash_tam)}

    for i, item in enumerate(TAB):
        # Itero por cada linha da tabela que li so arquivo
        # Se é uma linha válida, com mais de 1 item eu splito ela
        if len(item) > 0:
            TAB_splited = item.split(",")

            # Aqui pego cada uma das palavras do nome da pessoas por isso
            # faço split por espaço: TAB_splited[1].split(' ')
            for palavra in TAB_splited[1].split(' '):

                # Calculo o valor do indice da tabela hash onde vou colocar essa
                # palavra
                hash_indice = aplica_funcao_hash(palavra.lower(), tabela_hash_tam)
                
                # Adiciono na tabela hash
                tabela_hash[hash_indice].append((palavra.lower(), i))
    
    return tabela_hash, tabela_hash_tam

nome_arq= input("Entre com um nome de arquivo:")

with open (nome_arq, "r") as f:
    TAB = f.read().split("\n")

tabela_hash, tabela_hash_tam = cria_hash(TAB)

print(tabela_hash)

while True:      
    nom = input("Entre com um valor:")
    print()
    if nom == 'fim':
        break

    # Quando li a palavra do usuário, aplico a função de hash pra saber o 
    # indice de onde pode estar aquela palavra
    indice = aplica_funcao_hash(nom, tabela_hash_tam)

    # Pego a lista referente àquele índice
    lista_nomes = tabela_hash[indice]

    # Itero e vejo se tem algum cara que é a palavra que quero
    for nome, indice in lista_nomes:
        if nome == nom.lower():
            # Se tem a palavra, imprimo a linha da tabela original: TAB[indice]
            print(TAB[indice])
    
    print()

    # A quantidade de comparações que fiz nada mais é do que o tamanho da 
    # da lista que peguei da tabela hash
    print(f'* * * {len(lista_nomes)} comparações para localizar os nomes\n')


    