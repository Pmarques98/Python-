# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 13:00:48 2022

@author: Samsung
"""


from math import log
import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from metodos import *


erro = 10**(-15)
interacao_max = 30



def calculaNorma(vetor):
    
   """
   Calcula a norma do vetor
   :param vetor matriz nX1
   :return Norma do vetor
   """
   soma = 0
   for num in vetor:
       soma += num**2
   return numpy.sqrt(float(soma))


def calculaX(matriz, x_antigo):
    
   """
   Calcula o próximo valor da sequência de possíveis autovetores X
   :param matriz   Matriz nXn que está sendo analizada
   :param x_antigo Matriz nX1 do valor de X anterior
   :return Póxima matriz X da sequência
   """
   mult_matriz = numpy.dot(matriz, x_antigo)
   norma = calculaNorma(mult_matriz)
   return numpy.dot(mult_matriz, 1/norma)


def calculaProdutoTensorial(transposta, matriz):
    
   """
   Calcula o produto tensorial (ou escalar) de uma matriz
   :param transposta Matriz nXn que será transposta
   :param matriz     Matriz nXn sem transpor
   :return Produto escalar das matrizes
   """
   soma = 0
   i = 0
   for lin in matriz:
       j = 0
       for num in lin:
           soma = soma + num * transposta[i][j]
           j += 1
       i += 1
   return float(soma)


def calculaMi(matriz, Xk):
    
   """
   Calcula o valor de mi, estimativa do autovalor 1
   :param matriz Matriz nXn analisada
   :param Xk     Matriz nX1 de autovetores estimados
   :return Valor de mi
   """
   mult_matriz = numpy.dot(matriz, Xk)


   return calculaProdutoTensorial(Xk, mult_matriz)/calculaProdutoTensorial(Xk, Xk)

def calculaModuloDaDiferenca(matriz1, matriz2):

   """
   Calcula o módulo do vetor correspondente a diferença de dois vetores
   :param matriz1 Matriz nX1 primeiro vetor
   :param matriz2 Matriz nX1 vetor subitraído
   :return Norma do vetor resultante
   """
   soma = 0
   i = 0
   for lin in matriz1:
       soma = soma + (matriz1[i][0] - matriz2[i][0])**2
       i += 1

   return float(numpy.sqrt(soma))

def arrayParaMatrizColuna(array):

   """
   Transpõe um vetor para uma matriz nX1
   :param array Vetor a ser transposto
   :return Matriz nX1 correspondente ao vetor
   """
   
   matriz_coluna = [[0 for x in range(1)] for y in range(numpy.size(array))]
   i = 0

   for num in array:

       matriz_coluna[i][0] = num
       i += 1

   return matriz_coluna


def criaGrafico(valores):

   """
   Cria um gráfico a partir dos valores fornecidos

   :param valores matriz 4Xn com as informações a serem plotadas


       valores[0] -> Erro correspondente ao autovetor


       valores[1] -> Erro correspondente ao autovalor


       valores[2] -> Erro assintótico


       valores[3] -> Erro assintótico ao quadrado


   """

   fig, ax = plt.subplots() # Inicia gráfico

   plt.grid(True) # Adiciona grade

   # Adiciona nome do eixos


   plt.xlabel("Interação", size = 16)


   plt.ylabel("Erro L2", size = 16)

   # Ajusta para escala logarítmica no eixo y


   plt.yscale("log")

   # Acrescenta as informações ao gráfico


   ax.plot(valores[0], label='Erro autovalor')


   ax.plot(valores[1], label='Erro autovetor')


   ax.plot(valores[2], label='erro assintótico')


   ax.plot(valores[3], label='erro assintótico ao quadrado')

   # Configura legendas


   handles, labels = ax.get_legend_handles_labels()


   ax.legend(handles[::-1], labels[::-1])

   # Apresenta gráfico

   plt.show()

   return


def calculaOrdem(A, X, autovetor, erro_assint):

   """
   Calcula ordem de converg~encia de matriz a partir da matriz inicial, X da última interação, o autovetor e o erro assintótico

   :param A           Matriz analisada


   :param X           Autovetores da ultima interação


   :param autovetor   Autovetor da matriz A


   :param erro_assint Erro assintótico

   :return Ordem de convergência


   """
   return log(calculaModuloDaDiferenca(calculaX(A, X), autovetor)/erro_assint, calculaModuloDaDiferenca(X, autovetor))


def pegaAutovetor(autovetores, indice):

   tamanho_matriz = int(numpy.sqrt(numpy.size(autovetores)))
   autovetor = [[0 for x in range(1)] for x in range(tamanho_matriz)]

   i = 0


   while i < tamanho_matriz:

       autovetor[i][0] = autovetores[i][indice-1]

       i += 1


   return autovetor


def metodoDasPotencias(A, n):

   """
   Cálculo interativo para estimação do autovalor 1 e autovetor correspondente por meio do método das potências
   :param A matriz nXn analisada


   :param n Dimensão da matriz

   :return autovetor estimado

   """

   # Matriz que armazena os dados necessários para plotar o gráfico


   grafico = [[0 for x in range(interacao_max)] for y in range(4)]

   # Inicializa e atribui valores aleatórios de 0 a 1 para o primeiro X da sequência

   X = [[0 for x in range(1)] for y in range(n)]

   i = 0

   for lin in X:
       for num in lin:
           X[i][0] = numpy.random.rand()
       i += 1

   # Captura autovalores e autovetor precisos

   autovalores, autovetores = AutovalorEAutovetor(A)
   autovetor = pegaAutovetor(autovetores, 1)
   lamb1 = autovalores[0]
   lamb2 = autovalores[1]
   erro_assintotico = abs(lamb2/lamb1)
   # Calcula o primeiro módulo da diferênça de X com o autovetor antes do loop
   modulo = calculaModuloDaDiferenca(X, autovetor)
   i = 0
   # Loop para o método das potências que ocorre até que o módulo fique abaixo da precisão de máquina
   # ou que atinja o número máximo de interações

   while modulo > erro and i < interacao_max:

       # Calcula mi da interação atual

       mi = calculaMi(A, X)

       # Armazena as informações pertinentes ao gráfico na matriz

       grafico[0][i] = abs(mi - lamb1) # Erro do autovalor


       grafico[1][i] = modulo # Erro do autovetor


       grafico[2][i] = erro_assintotico**(i) # Erro assintótico elevado à número da interação


       grafico[3][i] = erro_assintotico**(2*i) # Erro assintótico elevado ao quadrado do número da interação
       # Calcula o próximo X

       X = calculaX(A, X)
       # Calcula novo módulo


       modulo = calculaModuloDaDiferenca(X, autovetor)
       i += 1 # Incrementa interação
   # calcula alfa e mostra seu valor e o do erro assintótico no terminal


   alfa = calculaOrdem(A, X, autovetor, erro_assintotico)

   print("alfa = ", alfa)
   print("n = ", erro_assintotico)
   # cria o gráfico

   criaGrafico(grafico)
   return X


def ordenaVetorDeAutovalores(autovalores):

   """
   Ordena em ordem decrescente um vetor
   :param autovalores Vetor a ser ordenado
   :return Novo vetor ordenado
   """
   vector_size = numpy.size(autovalores)
   autovalores_novos = [0 for x in range(vector_size)]
   maior = 0
   i = 0


   while i < vector_size:
       j = 0
       max_index = 0
       # Loop para achar o maior valor absoluto


       for num in autovalores:
           if(abs(num) > abs(maior)):
               maior = num
               max_index = j # ìndice do maior valor
           j += 1
       autovalores_novos[i] = maior # Adiciona o valor no novo vetor
       autovalores[max_index] = 0 # Zera o valor no vetor original para que ele não seja mais adicionado
       maior = 0
       i += 1


   return autovalores_novos



def ex1Q1():
   """
   Inicia e executa as operações para a resposta do item 1 da questão 1
   """

   print("Iniciando exercício 1, item 1...")


   n = 10 # Dimensão da matriz


   A = [[0 for x in range(n)] for y in range(n)]
   B = [[0 for x in range(n)] for y in range(n)]

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

   A = somaMatriz(B, calculaTransposta(B, n))
   metodoDasPotencias(A, n)

   return


def ex1Q2():


   """
   Inicia e executa as operações para a resposta do item 2 da questão 1
   """
   print("Iniciando exercício 1, item 2...")
   n = 10

   A = [[0 for x in range(n)] for y in range(n)]
   B = [[0 for x in range(n)] for y in range(n)]
   D = [[0 for x in range(n)] for y in range(n)]


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


   print("TESTE1: Lâmbidas próximos")
   
   D[0][0] = 20
   D[1][1] = 19
   D[2][2] = 8
   D[3][3] = 7
   D[4][4] = 6
   D[5][5] = 5
   D[6][6] = 4
   D[7][7] = 3
   D[8][8] = 2
   D[9][8] = 1


   A = numpy.dot(numpy.dot(B, D), numpy.linalg.inv(B))
   metodoDasPotencias(A, n)

   print("TESTE2: Lâmbidas distantes")

   D[0][0] = 20
   D[1][1] = 9
   D[2][2] = 8
   D[3][3] = 7
   D[4][4] = 6
   D[5][5] = 5
   D[6][6] = 4
   D[7][7] = 3
   D[8][8] = 2
   D[9][9] = 1

   A = numpy.dot(numpy.dot(B, D), numpy.linalg.inv(B))
   metodoDasPotencias(A, n)

   return

def main():


   print("BOT")

   ex1Q1()

   ex1Q2()

   print("EOT")


if __name__ == "__main__":

   main()


