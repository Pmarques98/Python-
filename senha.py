# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 20:37:00 2022

@author: Samsung
"""

import random

def senha():
        numeros = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        caractere_especial = ['!', '@', '#', '$', '%', '¨', '&', '*']
        senha = []

        for i in range (3):
            num1 = random.choice(numeros)
            senha.append(num1)
            letra1 = random.choice(letras)
            senha.append(letra1)
            carac1 = random.choice(caractere_especial)
            senha.append(carac1)

        
        numfinal = random.choice(numeros)
        senha.append(numfinal)
      

        return senha


print(senha())