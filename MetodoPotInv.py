import numpy as np
import matplotlib.pyplot as plt

Nerro = 10**(-15)
int_max = 50


def SOR(M, b, vetInicial, w):
    """
    Operação para a execução do método SOR
    """
    k = 0
    xk_sor = np.copy(vetInicial)
    
    resi = np.linalg.norm(np.matmul(M, xk_sor) - b)# residuo
    while resi > Nerro and k < int_max:
        for i in range(M.shape[0]):
            sigma = 0
            for j in range(M.shape[1]):
                if j != i:
                    sigma += M[i, j] * xk_sor[j]
            xk_sor[i] = (1-w) * xk_sor[i] + (w /M[i, i]) * (b[i] - sigma)
            resi = np.linalg.norm( np.matmul(M, xk_sor) - b)
            k += 1
           
    return xk_sor


def calcXMaior(autoVal):
    """
    Operação para calcular o autovetor associado ao maior autovalor de uma matriz
    """
    V = np.linalg.eig(autoVal)
    lambdaN = np.min(V[0])#maior autovalor
    l = 0
    for mi_k in V[0]:
        if mi_k == lambdaN:
            matriz_result = V[1].T 
            return (matriz_result[l,:]) 
        l = l + 1


def criterio(M):
   """
   Operação para executar o criterio. Realiza-se uma Iteracao pelas linhas da matriz, 
   fazendo a soma dos termos delas em módulo
   """
   i = 0
   while i < M.shape[0]:
        soma = 0
        j = 0
        while j < M.shape[1]:   
            if i != j: # Se o elemento for diferente da diagonal principal, soma seu módulo
                soma = soma + abs(M[i][j])
            j = j + 1
        if soma >= abs(M[i][i]):#verifica se o criterio das linhas esta satisfeito
            print("linha" , i , "não satisfaz o criterio")#linha da qual o criterio deu erro
            return False
        i = i + 1
    # se esta satisfeito, retorna true
   return True


def pAutoVal(xk, A1xk):
    """    
    Operação para calcular o proximo autovalor
    """
    if np.all( (xk == 0) ):
        return 0
    den = np.inner(xk.T, xk)
    num = np.inner(xk.T, A1xk)
    if den != 0:
        return num/den
    

def critPara(x_k, X):
    """
    Operação para verificar se o citerio de parada foi satisfeito(True) ou não(False)
    """
    verifica = min(np.linalg.norm(x_k - X), np.linalg.norm(x_k + X))
    if verifica >= Nerro:
        return True
    return False


def metPotInv(A, Val , inicio, w):
    """
    Operação para a execução do método das potências inversas
    Retorna o menor autovalor de A, com seu autovetor associado, ou False caso o criterio não seja satisfeito
    """
    #variaveis de arrays iniciais
    x_k = np.copy(inicio)
    x_k1 = np.copy(inicio)
    
    #variaveis de array de erro
    erroAutoval = np.array([])
    erroAutovet = np.array([])
    erroAssintotico = np.array([])
    erroAssintoticoAoQuadrado= np.array([])
    
    
    X = calcXMaior(A)
    #Seleciona os autovalores e autovetores dominantes para comparacao
    autovals = np.sort(Val[0])
    lambn = autovals[0]
    lamb1 = autovals[1]
   
   
    if not criterio(A): #checa o criterio, se verdadeiro o ciclo das interações começa
        print("Criterio das linhas nao foi satisfeito")
        return False

    cont=1
    while critPara(x_k1, X) and cont <= int_max:
        x_k = np.copy(x_k1)
        x_t = np.empty_like(x_k)
        
        x_t = SOR(A, np.copy(x_k), np.random.random(A.shape[0]), w)# com o metodo sor, a cada interação acha o x_t
        
        if np.all( (x_t == 0) ):
             x_k1 = np.zeros(A.shape[0])
        else:
            x_k1 = (x_t) / (np.linalg.norm(x_t))
        
        mi_k = pAutoVal(x_k, x_t)#calcula-se a proxima iteracao do autovalor
        
        #atualização dos arrays de erro
        erroAutoval = np.append(erroAutoval, [abs(1/mi_k - lambn)] )
        erroAutovet = np.append(erroAutovet, [ min(np.linalg.norm(x_k1 - X), np.linalg.norm(x_k1 + X)) ] )
        erroAssintotico = np.append(erroAssintotico, (lambn/lamb1)**(cont))
        erroAssintoticoAoQuadrado = np.append(erroAssintoticoAoQuadrado, (lambn/lamb1)**(2*cont)) 
       
        cont += 1 
        
     
    result = np.array( [1/mi_k, x_k1], dtype=object )#resultado final
    plot (erroAutoval, erroAutovet, erroAssintotico, erroAssintoticoAoQuadrado, cont)

    print(result)
    
    return result


def plot (erroAutovalor, erroAutovetor, erroAssintotico, erroAssintoticoQuadrado, k):
    """
    Gráfico com 4 valores fornecidos
    """
    plt.title('Exercicio 2')
    plt.plot(erroAutovalor, 'k', erroAutovetor, 'g', erroAssintotico, 'b', erroAssintoticoQuadrado, 'r')
    plt.xlabel('Interações')
    plt.ylabel('Erro (log)')
    plt.yscale('log')
   
    plt.axis([1, k,  10**(-15), 1])

    plt.show()
    
    return


def ex2Q1():   
    """
    Questão 1
    """
    
    print("Iniciando exercício 1")
    
    B = np.random.random((10, 10))
    I = np.identity(10)
    A = B + B.T + 10*I
    V = np.linalg.eig(A)

    metPotInv(A, V, np.random.random(10), 1.15)

    return 


def ex2Q2():  
    """
    Questão 2
    """
    
    print("Iniciando exercício 2")
    
    #primeiro teste
    ConstIden1 = 100 * np.identity(8)

    B0_1 = np.random.random((8, 8))
    B1 = B0_1 + ConstIden1
    B_1 = np.linalg.inv(B1)
    Diag1 = np.diag(np.arange(1,9))
    A = np.dot(np.dot(B1, Diag1), B_1)
    V1 = np.linalg.eig(A)
    
    metPotInv(A, V1 ,np.random.random(8), 1)

    
    #segundo teste
    ConstIden2 = 100000 * np.identity(9)
    
    Diag2 = np.array([[1, 0, 0, 0,  0,  0, 0, 0, 0],
                      [0, 200, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 300, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 400, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 500, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 600, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 700, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 800, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 900]
                      ])
    
    B0_2 = np.random.random((9, 9))
    B2 = B0_2 + ConstIden2
    B_2 = np.linalg.inv(B2)
    A = np.dot(np.dot(B2, Diag2), B_2)
    V2 = np.linalg.eig(A)
    
    metPotInv(A, V2,np.random.random(9), 1)
    
    return


def main():
   
   ex2Q1()
   ex2Q2()
   
    
    
if __name__ == "__main__":

   main()
