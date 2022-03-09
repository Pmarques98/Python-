from math import log
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from metodos import *


Nerro = 10**(-15)
int_max = 40


def calcMI(matriz, xk):
    
   """
   Operação para calcular o valor de mi
   :matriz = Matriz base 
   :Xk = Matriz de autovetores estimados
   """
   m_matriz = np.dot(matriz, xk)

   return calcProd(xk, m_matriz)/calcProd(xk, xk)


def calcX(matriz, x_anterior):
    
   """
   Operação para calcular o próximo valor da sequência de possíveis autovetores X
   """
   
   m_matriz = np.dot(matriz, x_anterior)
   norma = np.linalg.norm(m_matriz)  #calculo da norma
   
   return np.dot(m_matriz, 1/norma)


def calcProd(transp, matriz):
    
   """
   Operação para calcular o produto tensorial de uma matriz
   :transp = matriz transposta que vai somar
   :matriz = matriz base para a soma
   """
   soma = 0
   i = 0
   for lin in matriz:
       j = 0
       for num in lin:
           soma = soma + num * transp[i][j]
           j += 1
       i += 1
       
   return float(soma)

def arrayMatCol(array):

   """
   Operação para transformar um vetor para uma matriz nX1
   :array = vetor a ser transposto
   """
   
   mat_col = [[0 for x in range(1)] for y in range(np.size(array))]
   i = 0

   for num in array:

       mat_col[i][0] = num
       i += 1

   return mat_col

def calcOrd(M, X, erro, autovet):
  
   """
   Operação para calcular a ordem de convergencia de matriz a partir da matriz inicial X da última interação, o erro assintótico e o autovetor
   :M = Matriz base
   :X = Autovetores da ultima interação
   :erro =  erro assintótico
   :autovetor = autovetor da matriz M
   """
   a = calcModDaDif(calcX(M, X), autovet)/erro
   b = calcModDaDif(X, autovet) 

   return log(a, b)


def calcModDaDif(mat1, mat2):

   """
   Operação para calcular o módulo do vetor da diferença de dois vetores
   :mat1 = matriz base
   :mat2 = matriz para subtração
   """
   soma = 0
   i = 0
   for lin in mat1:
       soma = soma + (mat1[i][0] - mat2[i][0])**2
       i += 1

   return float(np.sqrt(soma))


def pegaAutovet(autovets, ind):

   """
   Operação para pegar determinado autovetor
    :autovets = matriz de autovetores
    :ind = indice da matriz
   """
   matriz_tam = int(np.sqrt(np.size(autovets)))
   autovet = [[0 for x in range(1)] for x in range(matriz_tam)]

   i = 0
   
   while i < matriz_tam:
       autovet[i][0] = autovets[i][ind-1]
       i += 1

   return autovet


def Grafico(val):

   """
    Gráfico com 4 valores fornecidos
     val[0] = Erro correspondente ao autovetor
     val[1] = Erro correspondente ao autovalor
     val[2] = Erro assintótico
     val[3] = Erro assintótico ao quadrado
   """
   
   fig, ax = plt.subplots() # Inicia gráfico
   plt.grid(True) # Adiciona grade

   plt.xlabel("Interação", size = 18)# Adiciona nome do eixo X
   plt.ylabel("Erro L2", size = 18)# Adiciona nome do eixo Y


   plt.yscale("log")# Ajusta para log

   ax.plot(val[0], label='Erro Autovalor')
   ax.plot(val[1], label='Erro Autovetor')
   ax.plot(val[2], label='Erro Assintótico')
   ax.plot(val[3], label='Erro Assintótico ao quadrado')

   #legendas
   
   handles, labels = ax.get_legend_handles_labels()
   ax.legend(handles[::-1], labels[::-1])

   # mostra o gráfico
   plt.show()

   return


def metDasPotencias(M, n):

   """
   Operação para a execução do método das potências
   :M = matriz base
   :n = dimensão da matriz
   """

   grafico = [[0 for x in range(int_max)] for y in range(4)] # Matriz que armazena os dados para plotar o gráfico
   X = [[0 for x in range(1)] for y in range(n)]# primeiro X da sequência com valores aleatorios
   i = 0

   for lin in X:
       for num in lin:
           X[i][0] = np.random.rand()
       i += 1


   autovalores, autovetores = atvalor_e_atvetor(M)# Captura de autovalores e autovetor precisos
   autovetor = pegaAutovet(autovetores, 1)
   lamb1 = autovalores[0]
   lamb2 = autovalores[1]
   erro_assintotico = abs(lamb2/lamb1)
  
   mod = calcModDaDif(X, autovetor) # Calcula o primeiro módulo da diferênça de X com o autovetor antes do loop
   i = 0
   
   while mod > Nerro and i < int_max:# ciclo para a execução do método que termina 
   #o valor de precisão fica menor que o Nerro ou quando atinge o numero maximo de interações
       
       mi = calcMI(M, X) # Calcula mi

       # Armazena as informações pertinentes ao gráfico na matriz

       grafico[0][i] = abs(mi - lamb1) # Erro do autovalor
       grafico[1][i] = mod # Erro do autovetor
       grafico[2][i] = erro_assintotico**(i) # Erro assintótico elevado à número da interação
       grafico[3][i] = erro_assintotico**(2*i) # Erro assintótico elevado ao quadrado do número da interação
       

       X = calcX(M, X)# Calcula o próximo X
       mod = calcModDaDif(X, autovetor)  # Calcula novo módulo
       i += 1 # Incrementa interação
   # calcula alfa e mostra seu valor e o do erro assintótico no terminal

   alfa = calcOrd(M, X, erro_assintotico, autovetor)

   print("n = ", erro_assintotico)
   print("alfa = ", alfa)
  

   Grafico(grafico)
   return X

def lambProxi(matriz):
   """
   Operação para devolver uma matriz do formato do teste1 da segunda questão 
   """
   matriz[0][0] = 20
   matriz[1][1] = 18
   matriz[2][2] = 9
   matriz[3][3] = 8
   matriz[4][4] = 7
   matriz[5][5] = 6
   matriz[6][6] = 5
   matriz[7][7] = 4
   matriz[8][8] = 3
   matriz[9][8] = 2
   
   return matriz

def lambDistant(matriz):
   """
   Operação para devolver uma matriz do formato do teste2 da segunda questão 
   """ 
   matriz[0][0] = 20
   matriz[1][1] = 10
   matriz[2][2] = 9
   matriz[3][3] = 8
   matriz[4][4] = 7
   matriz[5][5] = 6
   matriz[6][6] = 5
   matriz[7][7] = 4
   matriz[8][8] = 3
   matriz[9][8] = 2
   
   return matriz
   
def ex1Q1():
   """
   QUESTÃO 1
   """

   print("Iniciando exercício 1")

   n = 10 # Dimensão da matriz
   

   A = [[0 for x in range(n)] for y in range(n)]
   B = [[0 for x in range(n)] for y in range(n)]
   
   #matriz aleatoria 10x10
   B = [[0.2 , 0.2 , 0.8 , 0.4 , 0.1 , 0.6 , 0.7 , 0.3 , 0.8 , 0.2],
        [0.3 , 0.6 , 0.3 , 0.8 , 0.5 , 0.9 , 0.5 , 0.1 , 0.7 , 0.1],
        [0.3 , 0.2 , 0.4 , 0.6 , 0.5 , 0.4 , 0.4 , 0.3 , 0.7 , 0.1],
        [0.4 , 0.6 , 0.4 , 0.4 , 0.1 , 0.5 , 0.5 , 0.3 , 0.6 , 0.2],
        [0.5 , 0.7 , 0.1 , 0.8 , 0.3 , 0.6 , 0.6 , 0.4 , 0.3 , 0.9],
        [0.6 , 0.8 , 0.2 , 0.5 , 0.2 , 0.7 , 0.8 , 0.5 , 0.3 , 0.3],
        [0.7 , 0.2 , 0.8 , 0.7 , 0.2 , 0.2 , 0.6 , 0.6 , 0.2 , 0.3],
        [0.1 , 0.6 , 0.3 , 0.8 , 0.5 , 0.2 , 0.6 , 0.6 , 0.3 , 0.4],
        [0.3 , 0.7 , 0.9 , 0.2 , 0.7 , 0.3 , 0.1 , 0.9 , 0.9 , 0.4],
        [0.9 , 0.6 , 0.7 , 0.8 , 0.7 , 0.1 , 0.7 , 0.8 , 0.8 , 0.5]]

   Bt =  np.array(B) 
   A = matriz_soma(B, Bt.T)
   metDasPotencias(A, n)

   return


def ex1Q2():
   """
   QUESTÃO 2
   """
   n = 10 # Dimensão da matriz
     
   print("Iniciando exercício 2")
   

   A = [[0 for x in range(n)] for y in range(n)]
   B = [[0 for x in range(n)] for y in range(n)]
   D = [[0 for x in range(n)] for y in range(n)]
   
   #matriz aleatoria 10x10
   B = [[0.2 , 0.2 , 0.8 , 0.4 , 0.1 , 0.6 , 0.7 , 0.3 , 0.8 , 0.2],
        [0.3 , 0.6 , 0.3 , 0.8 , 0.5 , 0.9 , 0.5 , 0.1 , 0.7 , 0.1],
        [0.3 , 0.2 , 0.4 , 0.6 , 0.5 , 0.4 , 0.4 , 0.3 , 0.7 , 0.1],
        [0.4 , 0.6 , 0.4 , 0.4 , 0.1 , 0.5 , 0.5 , 0.3 , 0.6 , 0.2],
        [0.5 , 0.7 , 0.1 , 0.8 , 0.3 , 0.6 , 0.6 , 0.4 , 0.3 , 0.9],
        [0.6 , 0.8 , 0.2 , 0.5 , 0.2 , 0.7 , 0.8 , 0.5 , 0.3 , 0.3],
        [0.7 , 0.2 , 0.8 , 0.7 , 0.2 , 0.2 , 0.6 , 0.6 , 0.2 , 0.3],
        [0.1 , 0.6 , 0.3 , 0.8 , 0.5 , 0.2 , 0.6 , 0.6 , 0.3 , 0.4],
        [0.3 , 0.7 , 0.9 , 0.2 , 0.7 , 0.3 , 0.1 , 0.9 , 0.9 , 0.4],
        [0.9 , 0.6 , 0.7 , 0.8 , 0.7 , 0.1 , 0.7 , 0.8 , 0.8 , 0.5]]
  

   print("Teste 1:")
   

   A = np.dot(np.dot(B,lambProxi(D)), np.linalg.inv(B))
   metDasPotencias(A, n)

   print("Teste 2:")

   A = np.dot(np.dot(B, lambDistant(D)), np.linalg.inv(B))
   metDasPotencias(A, n)

   return

def main():
   
   ex1Q1()
   ex1Q2()



if __name__ == "__main__":

   main()


