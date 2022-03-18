# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 20:05:58 2022

@author: Samsung
"""

import string

def decifra (lista):
   a = []
   a = listAlphabet()
   novalista = []
   i = 0
   
   while i<28:
       for l in range (len(a)):
           if lista[i] in a[l]:
               l = l - 7
               if l < 0:
                   l = 26 + l
               novalista.append(a[l])
       i = i + 1       
        
        
   print(novalista)
        

def listAlphabet():
   a = list(string.ascii_uppercase)
   return a


lista = ['U','V','T','L','P','V','K','V','J','H','T','P','U','O','V','A','P','U','O','H','B','T','H','W','L','K','Y','H']
decifra(lista)




    

   