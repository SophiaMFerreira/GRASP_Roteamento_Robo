# 🤖 Projeto GRASP – Roteamento de Robô

**Autoras**: Nadine Vasconcellos e Sophia Ferreira

**Descrição Geral**: O projeto aplica a **meta-heurística** GRASP (Greedy Randomized Adaptive Search Procedure) ao problema de roteamento de um robô em um tabuleiro com obstáculos. O robô deve sair da posição inicial (0, 0) e alcançar o objetivo (N–1, N–1), movendo-se conforme a **heurística Right–Up**, isto é, priorizando direita e cima.
O processo combina uma fase construtiva (geração da rota) e uma fase de busca local (refinamento da rota), repetindo diversas execuções até estabilizar o melhor custo encontrado.

---

## 📝 Metaheurística Utilizada

- **Tipo:** GRASP (Greedy Randomized Adaptive Search Procedure)  
- **Fase ativa:** Construtiva e Busca Local
- **Tamanho da LCR:** 3
- **Número de execuções (critério de parada):** 50
- **Busca Local**: Remove ciclos e aplica um reparo de 1 passo para corrigir movimentos “problemáticos” (quando o robô pisa em obstáculo ou anda para trás, movimentos para esquerda ou para baixo), testando movimentos alternativos Right e Up e aceitando apenas se reduzirem o custo total.

---

## ⚙️ Sobre a Solução GRASP

### 🔧 Fase Construtiva

Na fase construtiva, o robô inicia sua trajetória movendo-se conforme a heurística Right–Up, ou seja, alternando os movimentos para cima (1) e direita (2) até alcançar o objetivo final `(while (posicao != objetivo):)`.
O algoritmo trabalha sobre um tabuleiro de dimensão N × N, contendo obstáculos gerados aleatoriamente, e em cada iteração o robô calcula o próximo movimento de acordo com as regras abaixo.

#### 🧩 1. Movimentação Principal
O comportamento da trajetória é controlado pelas condições de sentido:

```python
while (posicao != objetivo):
        if (sentido == 0 and posicao[1] < objetivo[1]) or (sentido == 1 and posicao[1] < objetivo[1] and posicao[0] == objetivo[0]):
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
        elif (sentido == 1 and posicao[0] < objetivo[0]) or (sentido == 0 and posicao[0] < objetivo[0] and posicao[1] == objetivo[1]):
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

```

#### 🚧 2. Tratamento de Obstáculos
Quando o próximo passo encontra um obstáculo `(if tuple(coordenadaDestino) in obstaculos:)`, a função `geraMovimentoAleatorio()` é chamada:

```python
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
        elif objDestino[1][0] < 0  or objDestino[1][0] >= N or objDestino[1][1] < 0 or objDestino[1][1] >= N:
            pesos.append(0);
        else:
            pesos.append(pesoMovimentos[objDestino[0]]);
            
    return random.choices(LCR, weights=pesos, k=1)[0];
```

Essa função gera uma Lista de Candidatos Restrita (LCR) contendo até 3 movimentos entre os 4 possíveis, excluindo aqueles que: 
- Colidem com obstáculos
- Saem dos limites do tabuleiro

#### 🎯 3. Cálculo da Qualidade (Pesos)
Dentro da função `geraMovimentoAleatorio()`, é feita a atribuição de pesos para cada direção, conforme a tabela abaixo:

| Movimento                       | Peso | Qualidade   |
|---------------------------------|------|-------------|
| 1 - Cima                        | 10   | Ótima       |
| 2 - Direita                     | 10   | Ótima       |
| 3 - Baixo                       | 5    | Média       |
| 4 - Esquerda                    | 5    | Média       |
| Cima + Obstáculo ou Retorno     | 1    | Ruim        |
| Direita + Obstáculo ou Retorno  | 1    | Ruim        |
| Baixo + Obstáculo ou Retorno    | 0.5  | Ruim        |
| Esquerda + Obstáculo ou Retorno | 0.5  | Ruim        |
| Cima fora do tabuleiro          | 0    | Descartada  |
| Direita fora do tabuleiro       | 0    | Descartada  |
| Baixo fora do tabuleiro         | 0    | Descartada  |
| Esquerda fora do tabuleiro      | 0    | Descartada  |

Após atribuir os pesos, o movimento é sorteado aleatoriamente, porém ponderado conforme esses valores. Movimentos com peso maior têm maior probabilidade de serem escolhidos.

Em seguida, um movimento é **sorteado entre os candidatos da LCR** com base nos pesos da tabela (quanto maior a qualidade, maior a probabilidade de escolha), e o robô **retoma sua movimentação diagonal** conforme o movimento que havia sido interrompido.

Para que o robô encontre corretamente seu objetivo, ao atingir as coordenadas *x* ou *y* correspondentes ao destino, ele passa a se mover apenas no sentido necessário até alcançá-lo.  
Quando encontra um novo obstáculo, é chamada a função `geraMovimentoAleatorio()` para decidir o próximo passo.

**Observações:**
- O robô **pode colidir com obstáculos**;  
- **Retornos a posições já visitadas** são possíveis, mas penalizados;  
- A **hierarquia de movimentos** orienta a busca sem eliminar a aleatoriedade do processo.

---

### 💰 Função de Cálculo de Custo

A função `calculaCusto(rota)` é responsável por avaliar a qualidade da trajetória do robô, atribuindo um custo total que representa o “esforço” da rota.
Ela é utilizada tanto na fase construtiva para acompanhar o desempenho parcial da rota quanto na busca local para verificar se uma alteração melhora a solução.

```python
def calculaCusto(rota):
    custo = 0;
    visitadas = set();

    for i in range(len(rota) - 1):
        posicaoAtual = rota[i];
        proxima = rota[i + 1];

        if tuple(posicaoAtual) in obstaculos:
            custo += 50;
        else:
            custo += 1;

        if tuple(posicaoAtual) in visitadas:
            custo += 10;

        dx = proxima[0] - posicaoAtual[0];
        dy = proxima[1] - posicaoAtual[1];
        if dx < 0 or dy < 0:
            custo += 10;

        visitadas.add(tuple(posicaoAtual));

    return custo
```


Cada célula visitada contribui com um custo base de 1 ponto. Entretanto, situações indesejáveis adicionam penalidades específicas que aumentam o custo total. Essas penalidades refletem o comportamento esperado da **heurística Right–Up**, que busca o trajeto em diagonal evitando revisitas e obstáculos.



#### ⚖️ Penalidades Consideradas

| Situação                            | Penalidade | 
|-------------------------------------|------------|
| Passo Normal                        | +1         | 
| Colisão com obstáculo               | +50        | 
| Movimento “para trás” (Left-Down)   | +10        | 
| Revisita de célula                  | +10        | 


- Quanto menor o custo, melhor a rota.
- Penalizações incentivam o robô a:
    - Evitar obstáculos
    - Evitar retornar a células já visitadas
    - Seguir consistentemente no sentido Right–Up.
- Em execuções iniciais, o custo tende a ser alto (por rota aleatória e colisões), **reduzindo gradualmente** conforme a busca local corrige desvios, até **estabilizar** próximo de 150.


---

### 🔎 Fase de Busca Local

Após a construção completa da rota, o algoritmo aplica uma busca local para refinar a solução e reduzir o custo total, corrigindo inconsistências que surgiram durante a fase construtiva.
A busca local é uma etapa clássica do GRASP (Greedy Randomized Adaptive Search Procedure) e tem como objetivo melhorar soluções viáveis já existentes, em vez de gerar novas do zero.

#### ⚙️ 1. Estrutura da Função

A função `buscaLocal(rota)` recebe uma rota já construída e realiza pequenas modificações para buscar versões com custo menor.
Ela atua em duas frentes principais:

**a) Remoção de Ciclos**

Se o robô retornar a uma célula já visitada, o trecho entre as duas ocorrências é eliminado, reduzindo revisitas e evitando loops desnecessários.

```python
def buscaLocal(rota):
    posicoesVisitadas = {} #Guarda cada posição já visitada e o índice onde ela apareceu pela primeira vez
    rotaSemCiclo = [] #Nova rota sem repetições, versão "limpa" da original

    for posicao in rota:
        coordenadaPosicao = tuple(posicao);
        if coordenadaPosicao in posicoesVisitadas:
            indiceRepetido = posicoesVisitadas[coordenadaPosicao]; 
            rotaSemCiclo = rotaSemCiclo[:indiceRepetido + 1]; #Remoção da parte intermediária
            posicoesVisitadas = {tuple(rotaSemCiclo[i]): i for i in range(len(rotaSemCiclo))}; #Reconstrói o dicionário de posições já visitadas
        else:
            posicoesVisitadas[coordenadaPosicao] = len(rotaSemCiclo);
            rotaSemCiclo.append(posicao); 

    melhorRota = rotaSemCiclo[:] 
    melhorCusto = calculaCusto(melhorRota)
```

➡️ Efeito: corta rotas redundantes, encurta o caminho e diminui o custo de revisitas.


**b) Reparo de Um Passo**

Depois da limpeza de ciclos, o algoritmo verifica cada ponto intermediário da rota.
Quando um ponto é **problemático**, ou seja, quando está em uma coordenada de obstáculo ou resulta de um movimento para trás (Left-Down), tenta substituir por um ponto vizinho melhor, mantendo a coerência do trajeto **diagonal** da heurística Right-Up


```python
i = 1;
    while i < len(melhorRota) - 1:
        anterior = melhorRota[i - 1];
        atual    = melhorRota[i];
        proxima  = melhorRota[i + 1];

        dx = atual[0] - anterior[0];
        dy = atual[1] - anterior[1];

        if (tuple(atual) in obstaculos) or (dx < 0 or dy < 0): #Se o ponto atual for um obstáculo ou se o passo for "para trás" (Left-Down) esse trecho deve ser melhorado
            custoAtual = melhorCusto;
            for mov in (2, 1): #Teste das melhores alternativas, canditados de reparo
                movX, movY = movimentos[mov];
                nx, ny = anterior[0] + movX, anterior[1] + movY;
                if not (0 <= nx < N and 0 <= ny < N): #Fora do limite do tabuleiro
                    continue
                if (nx, ny) in obstaculos: #Caiu no obstaculo
                    continue
                if [nx, ny] == proxima:
                    continue

                rotaTeste = melhorRota[:i] + [[nx, ny]] + melhorRota[i + 1:]; #Cria uma nova rota substituindo as coordenadas problemáticas pela coordenada candidata
                custoTeste = calculaCusto(rotaTeste);
```

➡️ Efeito: corrige pequenos desvios da rota, privilegiando os movimentos Right–Up e reduzindo penalidades desnecessárias.


#### 💡 2. Integração com o GRASP

A busca local é aplicada após cada construção de rota:

```python
custo = calculaCusto(rota)

    for j in range(10):
        rotaBuscaLocal = buscaLocal(rota);
        custoRotaLocal = calculaCusto(rotaBuscaLocal);
        if (custoRotaLocal < custo):
            custo = custoRotaLocal;
            rota = rotaBuscaLocal[:];

    if (custo < melhorCusto): #Verifica se a rota atual é melhor que a rota encontrada até agora
        melhorCusto = custo;
        melhorRota = rota[:];
        iP = 0;
    else:
        iP += 1;
    i += 1;
```

Assim, a cada iteração do GRASP, a solução é:
- Construída aleatoriamente (Right–Up + LCR), ou seja, segue um padrão guiado mas tem flexibilidade inteligente para se desviar de obstáculos.
- Avaliada pela função de custo;
- Refinada pela busca local.

---

### 🧭 Resultado Final

Após várias iterações, o custo médio começa alto e diminui progressivamente conforme as rotas são refinadas.
O algoritmo para quando o melhor custo não melhora em 50 execuções consecutivas (condição de platô), resultando em soluções estáveis com custos próximos de 150.


<div align="center">
        <img width="600" alt="PlotGrasp143VIVA" src="https://github.com/user-attachments/assets/a7fa1b79-9bf1-49fc-b2f9-9297d5c6cbd9" />
</div>







