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

## Heuristica Rigth, Up, Best
## Consiste em: dirigir-se para direita sempre que possível, em caso de obstáculo, sobe (independente se haverá obstáculo ou não).
## Ao concluir ao atingir o limite do tabuleiro, irá subir até o destino.

def heuristicaRUB():
    posicao = inicio[:];
    coordenadaDistino = inicio[:];
    rota = [posicao[:]];
    while(posicao != objetivo):
        if posicao[0] != objetivo[0]:
            movX, movY = movimentos[2];
            coordenadaDistino[0] += movX;
            coordenadaDistino[1] += movY;
            if (tuple(coordenadaDistino) in obstaculos):
                    coordenadaDistino = posicao[:];
                    movX, movY = movimentos[1];
                    coordenadaDistino[0] += movX;
                    coordenadaDistino[1] += movY;
        else:
            movX, movY = movimentos[1];
            coordenadaDistino[0] += movX;
            coordenadaDistino[1] += movY;
        posicao = coordenadaDistino[:];
        rota.append(posicao[:]);
    return rota;
            
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

rota = heuristicaRUB();
imprimeGrafico(rota);
print("Melhor custo: ",calculaCusto(rota));