import numpy



def matriz_soma(m1, m2):
   """
    Somando a m1 com m2
        ->
        --> para m1 - matriz1
        --> para m2 - matriz2
        --> retorna a matriz de acordo com a soma das entradas
   """

   f = 0

   for linha_m in m1:
       g = 0
       for numero in linha_m:
           m2[f][g] = m2[f][g] + numero                                     # adicionando o valor da m1 na celula de acordo com m2
           g = g + 1
       f = f + 1

   return m2

def ordena_atvetores_e_atvalores(atvalores, atvetores):
   """
    O vetor é ordenado em ordem decrescente e modifica 
        ->
        --> para atvalores - vetor vai ser ordenado
        --> retorna um novo vetor ordenado e matriz de atvalores organizada
   """

   tamanho_vetor = numpy.size(atvalores)

   novos_atvalores = [0 for x in range(tamanho_vetor)]
   novos_atvetores = [[0 for x in range(tamanho_vetor)] for y in range(tamanho_vetor)]

   i = 0
   maior = 0

   while i < tamanho_vetor:
       j = 0
       maximo_index = 0

                                                                            # laço de repetição para encontrar maior valor absoluto
       for numero in atvalores:
           if(abs(numero) > abs(maior)):
               maior = numero
               maximo_index = j                                             # Pegando o maior valor do indice
           j = j + 1
       novos_atvalores[i] = maior                                           # incrementando o valor no novo vetor
       indice = 0
       while indice < tamanho_vetor:
           novos_atvetores[indice][i] = atvetores[indice][maximo_index]
           indice = indice + 1
       atvalores[maximo_index] = 0                                          # deixa em zero o valor do vetor original para nao ser incrementado
       maior = 0
       i = i + 1
   return novos_atvalores, novos_atvetores

def transposta_calc(m, s):
   """
   Calcula transposta de uma m
   :param m m em análise
   :param s      Dimensão da m
   :return Matriz transposta
   """



   matriz_transposta = [[0 for x in range(s)] for y in range(s)]



   f = 0
   for lin in m:
       g = 0
       for numero in lin:
           matriz_transposta[g][f] = numero # Inverte linha e coluna
           g += 1
       f += 1



   return matriz_transposta

def atvalor_e_atvetor(m):
   """
   Partindo de uma matriz, obtém atravéz de bibliotecas externas, os atvalores e atvetores correspondentes
        ->
        --> para matriz-  matriz analisada
        --> para n - dimensão da matriz
        --> retorna Lista de atvetores e matriz de atvetores
   """

   atvalores, atvetores = numpy.linalg.eig(m)                               # pega atvalores e atvetores da matriz

   return ordena_atvetores_e_atvalores(atvalores, atvetores)

