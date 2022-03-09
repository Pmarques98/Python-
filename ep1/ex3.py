from pickle import FALSE, TRUE
import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from metodos import *
from ex1 import *

erro = 10**(-15)
erro_atvalor = 10**(-15)
interacao_max = 30


def devolve_m_identidade(z):
   """
   Devolve uma M identidade de ordem z
        ->
        --> para z ordem da M
        --> Devolve a  Matriz identidade
   """

   I = [[0 for x in range(z)] for y in range(z)]
   g = 0

   while g < z:
       I[g][g] = 1
       g += 1


   return I


def atvetor_calc(az):
   """
   calcula atvetor a partir de An
        ->
        --> para az vetor An
        --> Devolve atvetor
   """

   ez =  [0 for x in range(int(numpy.size(az)))]

   k =  [0 for x in range(int(numpy.size(az)))]

   g = 0

   while az[g] == 0:
       g = g + 1

   ez[g] = 1

   g = 0

   for numero in az:
       k[g] = az[g] + Devolve_sinal(az)*ez[g]*numpy.linalg.norm(az)/numpy.linalg.norm(ez)
       g = g + 1


   return k


def produto_escalar_calc(transposta, vetor):
   """
   Calcula o produto tensorial (ou escalar) de uma M
        ->
        --> para transposta Matriz nXn que será transposta
        --> para M Matriz nXn sem transpor
        --> Devolve o Produto escalar das matrizes
   """

   soma = 0
   g = 0

   for numero in vetor:
       soma = soma + numero * transposta[g]
       g = g + 1


   return float(soma)


def Devolve_vet_az(M, z):
   """
   Mensura os atvetores e atvalores de ima M usando o método de fatoração QR
        ->
        --> para M M analisada
        --> para z      Indice do vetor
        --> Devolve vetor Az
   """

   tam_vetor = numpy.sqrt(numpy.size(M))
   vetor = [0 for x in range(int(tam_vetor))]

   g = z - 1

   while g < tam_vetor:
       vetor[g] = M[g][z-1]
       g = g + 1

   return vetor


def norma_atvalor_calc(M, indice):
   """
   Calcula a norma de um atvetor e de indice 'indice'
        ->
        --> para M Matriz de atvetores
        --> para indice Indice do atvetor
        --> Devolve a norma do atvetor
   """
   
   tam_matriz = numpy.sqrt(numpy.size(M))

   soma = 0
   g = 0

   while g < tam_matriz:
       soma += (M[g][indice-1])**2
       g += 1

   # return float(numpy.sqrt(soma))
   return numpy.sqrt(soma)


def Devolve_sinal(az):
   """
   Pega o sinal do primeiro número não nulo do vetor An
        ->
        --> para az vetor analisado
        --> Devolve o sinal do primeiro número não nulo
   """

   g = 0

   while az[g] < erro and g != numpy.size(az) -1:
       g = g + 1


   return 1 if (az[g] >= 0) else -1


def calc_Q_e_R(M):
   """
   Mátodo para o cálculo de das matrizes Q e R
        ->
        --> para M M analisada
        --> return Q e R
   """

   tam_matriz = numpy.sqrt(numpy.size(M))

   R = M

   # print("M inicial =\z", M)
   z = 1

   while z < tam_matriz:
       az = Devolve_vet_az(R, z)
       # print("az =", az)
       vn = atvetor_calc(az)
       Hn = transformacao_householder_calc(vn)
       R = numpy.dot(Hn, R)
       # print("R intermediario = \z", R)
       z = z + 1


   Q = numpy.dot(M, numpy.linalg.inv(R))

   return Q, R


def analisa_erro_diagonal(M, atvalores):
   """
   Compara todos os atvalores da M com os atvalores orginais
        ->
        --> para M M analisada
        --> para atvalores Lista de atvalores originais
        --> Devolve TRUE caso exista um autovalor onde o erro é menor que erro_atvalor
   """

   g = 0

   while g < numpy.sqrt(numpy.size(M)):
       if abs(M[g][g] - atvalores[g]) < erro_atvalor:
           return TRUE

       g = g + 1


   return FALSE


def transformacao_householder_calc(k):
   """
   Calcula a tranformação de Householder para um atvetor k
        ->
        --> param k atvetor
        --> return Matriz de Householder
   """

   tam_matriz = numpy.size(k)

   I = devolve_m_identidade(tam_matriz)

   h = [[0 for x in range(tam_matriz)] for y in range(tam_matriz)]

   produto_escalar = produto_escalar_calc(k, k)

   linha = 0

   while linha < tam_matriz:
       col = 0
       while col < tam_matriz:
           h[linha][col] = I[linha][col] - (2/produto_escalar) * k[linha] * k[col]
           col = col + 1
       linha = linha + 1


   return h


def Q_R_fat(M, atvalores, atvetores):
   """
   Mensura os atvetores e atvalores de ima M usando o método de fatoração QR
        ->
        --> para M - M analisada
        --> para atvalores Lista de atvalores orginais
        --> para atvetores Matriz de atvetores orginais
        --> retorna aMatriz resultante, M com o histórico de erros dos v, M de atvetores calculados
   """

   tam_matriz = int(numpy.sqrt(numpy.size(M)))

   V = [[0 for x in range(interacao_max)] for y in range(tam_matriz)]

   grafico = [[0 for x in range(interacao_max)] for y in range(tam_matriz * 2)]

   Q, R = calc_Q_e_R(M)
   V = Q
   A = numpy.dot(R,Q)

   # Atualiza v do grafico
   numero_atvalor = 1

   while numero_atvalor <= tam_matriz:
       grafico[numero_atvalor-1][0] = abs(A[numero_atvalor-1][numero_atvalor-1] - atvalores[numero_atvalor-1])
       numero_atvalor += 1

   numero_atvetor = 1

   while numero_atvetor <= tam_matriz:
       grafico[numero_atvetor + tam_matriz - 1][0] = retorna_dif_modulo_atvetores(V, atvetores, numero_atvetor)
       numero_atvetor += 1

   g = 1

   while analisa_erro_diagonal(R, atvalores) == FALSE and g < interacao_max:
       Q, R = calc_Q_e_R(A)
       V = numpy.dot(V, Q)
       A = numpy.dot(R,Q)

       # Atualiza v do grafico
       numero_atvalor = 1

       while numero_atvalor <= tam_matriz:
           grafico[numero_atvalor-1][g] = abs(A[numero_atvalor-1][numero_atvalor-1] - atvalores[numero_atvalor-1])
           numero_atvalor += 1


       numero_atvetor = 1

       while numero_atvetor <= tam_matriz:
           grafico[numero_atvetor + tam_matriz - 1][g] = retorna_dif_modulo_atvetores(V, atvetores, numero_atvetor)
           numero_atvetor += 1


       g += 1


   return A, grafico, V


def retorna_dif_modulo_atvetores(atvetor_calculado, atvetores, indice):
   """
   Devolve a norma da diferença entre um atvetor calculado e oficial de indice 'indice'. Os vetores são normalizados no cálculo
        ->
        --> para atvetor_calculado Matriz de atvetores calculados
        --> para atvetores - Matriz de atvetores orginais
        --> para indice - Indice do atvetor analizado
        --> Devolve a norma da diferença
        """

   tam_matriz = numpy.sqrt(numpy.size(atvetor_calculado))

   soma = 0

   sinal = -1 if atvetor_calculado[0][indice-1] < 0 else 1
   sinal2 = -1 if atvetores[0][indice-1] < 0 else 1

   norma_calculada = norma_atvalor_calc(atvetor_calculado, indice)          #calcula a nomra
   norma = norma_atvalor_calc(atvetores, indice)                            # pega a norma

   g = 0

   while g < tam_matriz:
       soma = soma + (sinal*atvetor_calculado[g][indice-1]/norma_calculada - sinal2*atvetores[g][indice-1]/norma)**2
       g = g + 1


   return numpy.sqrt(soma)


def resultado_printa(M, V, atvalores, atvetores):
   """
   Imprime os atvalores e atvetores obtidos e orginais
        ->
        --> para M - M analisada
        --> para V - tamanho da M
        --> para atvalores Lista de atvalores calculados pela função importada
        --> para atvetores Matriz de atvetores calculados pela função importada
   """

   tam_matriz = int(numpy.sqrt(numpy.size(M)))

   autovalores_encontrados = [0 for x in range(tam_matriz)]

   g = 0

   while(g < tam_matriz):
       autovalores_encontrados[g] = M[g][g]
       g += 1


   print("atvalores encontrados")
   print(autovalores_encontrados)
   print("atvalores esperados")
   print(atvalores)

   print("atvetores encontrados")
   print(V)
   print("atvetores esperados")
   print(atvetores)

   return


def gera_grafico(v, tam_matriz):
   """
   Gera um gráfico a partir dos v fornecidos
        ->
        --> para v M 4Xn com as informações a serem plotadas
            v[0 ao tam_matriz-1] -> Erro correspondente aos atvalores
            v[tam_matriz ao 2*tam_matriz-1] -> Erro correspondente aos atvetores
   """

   fig, ax = plt.subplots() # Inicia gráfico
   plt.grid(True) # Adiciona grade

   # Adiciona nome do eixos
   plt.xlabel("Interação", size = 16)
   plt.ylabel("Erro L2", size = 16)

   # Ajusta para escala logarítmica no eixo y
   plt.yscale("log")

   # Acrescenta as informações ao gráfico baseado na dimensão da M
   numero_atvalor = 1

   while numero_atvalor <= tam_matriz:
       ax.plot(v[numero_atvalor-1], label='Erro do atvalor' + str(numero_atvalor))
       numero_atvalor += 1


   numero_atvetor = 1

   while numero_atvetor <= tam_matriz:
       ax.plot(v[numero_atvetor+tam_matriz-1], label='Erro do atvetor' + str(numero_atvetor))
       numero_atvetor += 1

   # Configura legendas
   handles, labels = ax.get_legend_handles_labels()
   ax.legend(handles[::-1], labels[::-1])

   # Apresenta gráfico
   plt.show()


   return


def ex3Q1():

   print("Exercicio 3 questão 1")

   tam_matriz = 3                                                                     # Tamanho da M

   A = [[0 for x in range(tam_matriz)] for y in range(tam_matriz)]
   A = [[6,-2,-1],[-2,6,-1],[-1,-1,5]]

   atvalores = [8,6,3]                                                                   # atvalores
   atvetores = [[1/numpy.sqrt(2), 1/(2*numpy.sqrt(3/2)), 1/numpy.sqrt(3)] , [-1/numpy.sqrt(2), -1/(2*numpy.sqrt(3/2)), 1/numpy.sqrt(3)] , [0,-numpy.sqrt(2/3), 1/numpy.sqrt(3)]]

   A, grafico, V = Q_R_fat(A, atvalores, atvetores)
   resultado_printa(A, V, atvalores, atvetores)
   gera_grafico(grafico, tam_matriz)
   Q, R = calc_Q_e_R(A)

   return


def ex3Q2():

   print("Exercicio 3 questão 2")

   tam_matriz = 2 # tamanho da M

   A = [[0 for x in range(tam_matriz)] for y in range(tam_matriz)]
   A = [[1,1],[-3,1]]

   atvalores = [1+numpy.sqrt(3)*1j, 1-numpy.sqrt(3)*1j]                                                     # Pegando atvalores
   atvetores = [[(1/numpy.sqrt(2))*1j, (1/numpy.sqrt(2))*1j] , [-(numpy.sqrt(3/2)), (numpy.sqrt(3/2))]]     # Pegando atvalores

   A, grafico, V = Q_R_fat(A, atvalores, atvetores)

   resultado_printa(A, V, atvalores, atvetores)

   gera_grafico(grafico, tam_matriz)

   return


def ex3Q3():

   print("Exercicio 3 questão 3")

   tam_matriz = 2 # tamanho da M

   A = [[0 for x in range(tam_matriz)] for y in range(tam_matriz)]
   A = [[3,-3],[0.33333,5]]

   atvalores = [(4000+numpy.sqrt(10))/1000 , (4000-numpy.sqrt(10))/1000]                                                                # Pegando atvalores
   atvetores = [[(100000-100*numpy.sqrt(10))/(33333*3.15) , -(100000+100*numpy.sqrt(10))/(33333*3.17)] , [-1/3.15 , 1/3.17]]            # Pegando atvetores

   A, grafico, V = Q_R_fat(A, atvalores, atvetores)
   resultado_printa(A, V, atvalores, atvetores)
   gera_grafico(grafico, tam_matriz)

   return


def ex3Q4():

   print("Exercicio 3 questão 4")

   # Primeira parte
   tam_matriz = 10 # tamanho da M

   A1 = [[0 for x in range(tam_matriz)] for y in range(tam_matriz)]

   B1 = [[0 for x in range(tam_matriz)] for y in range(tam_matriz)]

   B = [[0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.9 , 0.9],
        [0.2 , 0.6 , 0.3 , 0.8 , 0.5 , 0.9 , 0.5 , 0.1 , 0.7 , 0.1],
        [0.3 , 0.7 , 0.4 , 0.8 , 0.5 , 0.4 , 0.4 , 0.1 , 0.7 , 0.1],
        [0.4 , 0.6 , 0.4 , 0.8 , 0.1 , 0.5 , 0.5 , 0.3 , 0.6 , 0.2],
        [0.5 , 0.7 , 0.1 , 0.8 , 0.3 , 0.6 , 0.6 , 0.4 , 0.6 , 0.2],
        [0.6 , 0.6 , 0.2 , 0.8 , 0.2 , 0.7 , 0.8 , 0.5 , 0.3 , 0.3],
        [0.7 , 0.7 , 0.8 , 0.8 , 0.2 , 0.2 , 0.6 , 0.6 , 0.2 , 0.3],
        [0.8 , 0.6 , 0.3 , 0.8 , 0.5 , 0.2 , 0.6 , 0.6 , 0.3 , 0.4],
        [0.9 , 0.7 , 0.9 , 0.8 , 0.6 , 0.3 , 0.1 , 0.7 , 0.9 , 0.4],
        [0.9 , 0.6 , 0.7 , 0.8 , 0.7 , 0.1 , 0.7 , 0.8 , 0.8 , 0.5]]

   A1 = matriz_soma(B, transposta_calc(B, tam_matriz))

   atvalores, atvetores = atvalor_e_atvetor(A1)
   A1, grafico, V1 = Q_R_fat(A1, atvalores, atvetores)
   resultado_printa(A1, V1, atvalores, atvetores)
   gera_grafico(grafico, tam_matriz)

   # Segunda parte
   z = 10 # tamanho da M

   A2 = [[0 for x in range(z)] for y in range(z)]
   D2 = [[0 for x in range(z)] for y in range(z)]

   print("T1: Lâmbidas próximos")

   D2[0][0] = 20
   D2[1][1] = 19
   D2[2][2] = 8
   D2[3][3] = 7
   D2[4][4] = 6
   D2[5][5] = 5
   D2[6][6] = 4
   D2[7][7] = 3
   D2[8][8] = 2
   D2[9][8] = 1

   A2 = numpy.dot(numpy.dot(B, D2), numpy.linalg.inv(B))

   atvalores, atvetores = atvalor_e_atvetor(A2)

   print(atvalores)

   A2, grafico, V2 = Q_R_fat(A2, atvalores, atvetores)
   resultado_printa(A2, V2, atvalores, atvetores)
   gera_grafico(grafico, z)

   print("T2: Lâmbidas distantes")

   D2[0][0] = 20
   D2[1][1] = 19
   D2[2][2] = 8
   D2[3][3] = 7
   D2[4][4] = 6
   D2[5][5] = 5
   D2[6][6] = 4
   D2[7][7] = 3
   D2[8][8] = 2
   D2[9][8] = 1

   A2 = numpy.dot(numpy.dot(B, D2), numpy.linalg.inv(B))

   atvalores, atvetores = atvalor_e_atvetor(A2)
   A2, grafico, V2 = Q_R_fat(A2, atvalores, atvetores)
   resultado_printa(A2, V2, atvalores, atvetores)    
   gera_grafico(grafico, z)                                             #passado dados apra gerar grafico

   return


def main():               #func Principal (main)

   print("BOT")

   ex3Q1()
   ex3Q2()
   ex3Q3()
   ex3Q4()

   print("EOT")

if __name__ == "__main__":

   main()