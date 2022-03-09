# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 13:04:12 2022

@author: Samsung
"""

import numpy



def calculaTransposta(matriz, n):
    
   transposta = [[0 for x in range(n)] for y in range(n)]
   l = 0

   for lin in matriz:
       c = 0
       for num in lin:
           transposta[c][l] = num # Inverte linha e coluna
           c += 1
       l += 1

   return transposta


def somaMatriz(matriz1, matriz2):
    
   l = 0
   for lin in matriz1:
       c = 0
       for num in lin:
           matriz2[l][c] += num # É adicionado o valor da matriz1 na célula correspondente da matriz 2
           c = c + 1
       l = l + 1


   return matriz2



def ordenaAutovaloresEAutovetores(autovalores, autovetores):



   vector_size = numpy.size(autovalores)
   autovalores_novos = [0 for x in range(vector_size)]
   autovetores_novos = [[0 for x in range(vector_size)] for y in range(vector_size)]
   maior = 0
   i = 0
   while i < vector_size:
       j = 0
       max_index = 0

       for num in autovalores:
           if(abs(num) > abs(maior)):
               maior = num
               max_index = j # ìndice do maior valor
           j += 1
       autovalores_novos[i] = maior # Adiciona o valor no novo vetor
       indice = 0
       while indice < vector_size:
           autovetores_novos[indice][i] = autovetores[indice][max_index]
           indice += 1
       autovalores[max_index] = 0 # Zera o valor no vetor original para que ele não seja mais adicionado
       maior = 0
       i += 1

   return autovalores_novos, autovetores_novos



def AutovalorEAutovetor(matriz):


   autovalores, autovetores = numpy.linalg.eig(matriz) # Obtém autovalores e autovetores da matriz


   return ordenaAutovaloresEAutovetores(autovalores, autovetores)


