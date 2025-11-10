'''
Projeto Grasp:                  Nadine Vasconcelos e Sophia Ferreira
Grasp na fase construtiva:      Ao colidir com um obstáculo, o novo movimento será realizado de modo randomizado;
Tam LCR:                        Considerou-se inicialmente uma LCR de tamanho 3 (excluindo o movimento que provoca colisão/sáda do tabuleiro)
Número de execuções (critério de parada): 30 sem atualização do best
Busca local =                   É realizado uma busca local em cima das coordenadas de colisão, buscando contorná-las, para tal, 
                                faz-se uma nova LCR evitando também os caminhos de colosão.
'''
## Heuristica Rigth, Up, Best
## Consiste em: dirigir-se para direita sempre que possível, em caso de obstáculo, sobe (independente se haverá obstáculo ou não).
## Ao concluir ao atingir o limite do tabuleiro, irá subir até o destino.

#Problema de Roteamento de Robo
import random
import matplotlib.pyplot as plt

#Ambiente
random.seed(3)  #para gerar as mesmas instâncias a partir da mesma semente
N = 30
Obs = N*10
inicio = [0, 0]
objetivo = [N-1, N-1]
obstaculos = set() #gera os obstáculos sem repetição de coordenadas
while len(obstaculos) < Obs:
    x = random.randint(0, N-1)
    y = random.randint(0, N-1)
    if (x, y) != inicio and (x, y) != objetivo:
        obstaculos.add((x, y))
obstaculos = list(obstaculos) #transformação em lista para facilitar o uso de métodos
obstaculos.sort()

#Coordenadas dos movimentos possíveis: 1=Cima, 2=Direita, 3=Baixo, 4=Esquerda
movimentos = {
    1: (0, 1),   # Cima
    2: (1, 0),   # Direita
    3: (0, -1),  # Baixo
    4: (-1, 0)   # Esquerda
}

pesoMovimentos = {
    1: 10,   # Cima
    2: 10,   # Direita
    3: 5,    # Baixo
    4: 5     # Esquerda
}

random.seed()
tamanhoLCR = 3;
condPlator = 50;
maxIteracao = 1000;

def geraMovimentoAleatorio():
    for movimento in movimentos:
        movX, movY = movimentos[movimento];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
        listaDestinos[movimento-1][1] = coordenadaDestino[:]
        if tuple(coordenadaDestino) in obstaculos or tuple(coordenadaDestino) in rota:
            listaDestinos[movimento-1][2] = pesoMovimentos[movimento] * 50;
        elif coordenadaDestino[0] < 0  or coordenadaDestino[0] >= N or coordenadaDestino[1] < 0 or coordenadaDestino[1] >= N:
            listaDestinos[movimento-1][2] = pesoMovimentos[movimento] * 100;
        else:
            listaDestinos[movimento-1][2] = pesoMovimentos[movimento];
    
    LCR = sorted(listaDestinos, key=lambda objDestino: objDestino[2])[0:tamanhoLCR];
    pesos = [];
    for objDestino in LCR:
        if tuple(objDestino[1]) in obstaculos:
            pesos.append(pesoMovimentos[objDestino[0]] / 10);
        elif objDestino[1][0] < 0  or objDestino[1][0] >= N or objDestino[1][1] < 0 or objDestino[1][0] >= N:
            pesos.append(0);
        else:
            pesos.append(pesoMovimentos[objDestino[0]]);
            
    return random.choices(LCR, weights=pesos, k=1)[0];


def calculaCusto(rota):
    custo = 0;
    for i in range(len(rota)-1):
        posicaoAtual = rota[i];
        if tuple(posicaoAtual) in obstaculos:
            custo += 50;
        else:
            custo += 1;        
    return custo;

def imprimeGrafico(melhorRota):
    x=[]
    y=[]
    for i in range(len(obstaculos)):
        x.append(obstaculos[i][0])
        y.append(obstaculos[i][1])
    plt.scatter(x, y, color='#fb5607')
    
    x=[]
    y=[]
    z=[]
    w=[]
    for coordenada in melhorRota:
        x.append(coordenada[0])
        y.append(coordenada[1])
        if tuple(coordenada) in obstaculos:
           z.append(coordenada[0])
           w.append(coordenada[1]) 
    plt.scatter(x, y, color='#90e0ef')
    plt.scatter(z, w, color='#d00000', marker='x')
    plt.show()


sentido = 0;
posicao = inicio[:];
rota = [inicio[:]];
rotaMov = [];
coordenadaDestino = posicao[:];
i = 0;
iP = 0;
melhorCusto = 99999;
melhorRota = [];

listaDestinos = [];
for movimento in movimentos:
    listaDestinos.append([movimento, inicio[:], 0]);

while (iP < condPlator) and (i < maxIteracao):
    while(posicao != objetivo):
        if (sentido == 0 and posicao[1] < N-1) or (sentido == 1 and posicao[1] < N-1 and posicao[0] == objetivo[0]):
            movX, movY = movimentos[1];
            coordenadaDestino[0] = movX + posicao[0];
            coordenadaDestino[1] = movY + posicao[1];
            if tuple(coordenadaDestino) in obstaculos:
                objCoordenadaDestino = geraMovimentoAleatorio();
                posicao = objCoordenadaDestino[1][:];
                rotaMov.append(objCoordenadaDestino[0]);
            else:
                sentido = 1;
                posicao = coordenadaDestino[:];
                rotaMov.append(1);
        elif (sentido == 1 and posicao[0] < N-1) or (sentido == 0 and posicao[0] < N-1 and posicao[1] == objetivo[1]):
            movX, movY = movimentos[2];
            coordenadaDestino[0] = movX + posicao[0];
            coordenadaDestino[1] = movY + posicao[1];
            if tuple(coordenadaDestino) in obstaculos:
                objCoordenadaDestino = geraMovimentoAleatorio();
                rotaMov.append(objCoordenadaDestino[0]);
                posicao = objCoordenadaDestino[1][:];
            else:
                sentido = 0;
                posicao = coordenadaDestino[:];
                rotaMov.append(2);
        rota.append(posicao[:]);
        custo = calculaCusto(rota);
        if(custo < melhorCusto):
            melhorCusto = custo;
            melhorRota = rota[:];
            iP = 0;
        else:
            iP += 1;
        i += 1;
    


imprimeGrafico(rota);
print("Melhor custo: ", custo);