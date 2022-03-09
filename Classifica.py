"""
# Atividade 3 – MAC 122 – PDA
# Patrick Marques de Barros Costa
# NUSP: 11257550
"""

from datetime import datetime

def Classifica(TAB, ordem):
    lista_convertida = []
    for sublista in TAB:
       sublista[2] = datetime.strptime(sublista[2], '%d/%m/%Y').date()
       lista_convertida.append(sublista)
    
    if len(ordem) == 1:
        i1 = ordem[0]
        TAB.sort(key=lambda x: x[i1])
    
    elif len(ordem) == 2:
        i1, i2 = tuple(ordem)
        TAB.sort(key=lambda x: (x[i1], x[i2]))
        ...
    elif len(ordem) == 3:
        i1, i2, i3 = tuple(ordem)
        TAB.sort(key=lambda x: (x[i1], x[i2], x[i3]))
        ...
    else:
        print("Não é possível ordenar por essa quantidade de elementos")
        
    for sublista in TAB:
       sublista[2] = sublista[2].strftime('%d/%m/%Y')
       
    return lista_convertida


