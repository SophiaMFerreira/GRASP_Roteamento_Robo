# 🤖 Projeto GRASP – Roteamento de Robô

Este projeto implementa a **metaheurística GRASP** (Greedy Randomized Adaptive Search Procedure) para o problema de movimentação de um robô em um tabuleiro com obstáculos.  
A solução proposta simula a movimentação e a escolha adaptativa de caminhos com base em penalidades e sorteio controlado, **impedindo que o robô saia do tabuleiro** e **garantindo que ele sempre alcance seu destino**.

---

## 📝 Metaheurística Utilizada

- **Tipo:** GRASP (Greedy Randomized Adaptive Search Procedure)  
- **Fase ativa:** Construtiva  
- **Tamanho da LCR:** 3  
<!-- - **Busca local:** ativa. Atua sobre as colisões. -->

---

## ⚙️ Sobre a Solução GRASP

### 🔧 Fase Construtiva

Na fase construtiva, o robô inicia sua trajetória movendo-se **em diagonal (para cima e para a direita)** até encontrar um obstáculo.  
Ao detectar o obstáculo, o sistema gera uma **LCR (Lista de Candidatos Restrita)** contendo as **3 melhores coordenadas** entre as 4 possíveis para o próximo movimento, definidas com base no seguinte **critério de penalidade**:

| Movimento                       | Peso | Qualidade  |
|---------------------------------|------|-------------|
| 1 - Cima                        | 10   | Ótima       |
| 2 - Direita                     | 10   | Ótima       |
| 3 - Baixo                       | 5    | Média       |
| 4 - Esquerda                    | 5    | Média       |
| Cima + Obstáculo ou Retorno     | 1    | OK          |
| Direita + Obstáculo ou Retorno  | 1    | OK          |
| Baixo + Obstáculo ou Retorno    | 0.5  | Ruim        |
| Esquerda + Obstáculo ou Retorno | 0.5  | Ruim        |
| Cima fora do tabuleiro          | 0    | Descartada  |
| Direita fora do tabuleiro       | 0    | Descartada  |
| Baixo fora do tabuleiro         | 0    | Descartada  |
| Esquerda fora do tabuleiro      | 0    | Descartada  |

Em seguida, um movimento é **sorteado entre os candidatos da LCR** com base nos pesos da tabela (quanto maior a qualidade, maior a probabilidade de escolha), e o robô **retoma sua movimentação diagonal** conforme o movimento que havia sido interrompido.

Para que o robô encontre corretamente seu objetivo, ao atingir as coordenadas *x* ou *y* correspondentes ao destino, ele passa a se mover apenas no sentido necessário até alcançá-lo.  
Quando encontra um novo obstáculo, é chamada a função `geraMovimentoAleatorio()` para decidir o próximo passo.

**Observações:**
- O robô **pode colidir com obstáculos**;  
- **Retornos a posições já visitadas** são possíveis, mas penalizados;  
- A **hierarquia de movimentos** orienta a busca sem eliminar a aleatoriedade do processo.

---

### 💰 Cálculo de Custo

O cálculo de custos considera os pesos já apresentados anteriormente e pode ser representado da seguinte forma: 

```python
def calculaCusto(rota):
    custo = 0
    visitadas = set()  #Guarda posições já visitadas (tuplas)

    for i in range(len(rota) - 1):  #Percorre as posições menos a última
        posicaoAtual = rota[i]
        proxima = rota[i + 1]

        if tuple(posicaoAtual) in obstaculos:
            custo += 50   #Penaliza pisar em obstáculo (posição atual)
        else:
            custo += 1    #Custo padrão da posição

        if tuple(posicaoAtual) in visitadas:
            custo += 10   #Penaliza revisita de posição já percorrida

        dx = proxima[0] - posicaoAtual[0]
        dy = proxima[1] - posicaoAtual[1]
        if dx < 0 or dy < 0:
            custo += 10   #Penaliza movimento de retorno (left or down)

        visitadas.add(tuple(posicaoAtual)) #Marca a posição atual como visitada

    return custo
```

---

### 🔎 Busca Local

#### Refinamento 1 — Remoção de Ciclo

```python
#Refinamento 1 - Remove ciclo se a posição atual já apareceu antes na rota corta o trecho do meio
        if rota.count(posicao) > 1:
            primeiraOcorrencia = next(k for k in range(len(rota)-1) if rota[k] == posicao)
            rota = rota[:primeiraOcorrencia + 1]
```

📘 Explicação:
- Se o robô voltar a uma célula que ele já visitou, isso significa que ele está “andando em círculos”;
- Esse trecho intermediário é desnecessário e só aumenta o custo (porque a função calculaCusto penaliza revisitas);
- Então assim que detectamos essa repetição cortamos tudo que estava entre as duas ocorrências.  

➡️ Resultado: a rota fica mais curta e eficiente.

#### Refinamento 2 — Reparo 1-passo

```python
#Refinamento 2 - Reparo 1-passo apenas no último ponto se for "problemático", ou seja,
        #o problema é quando a célula é obstáculo ou passo para trás (anti right-up).
        if len(rota) >= 2:
            anterior = rota[-2]
            atual    = rota[-1]       
            dx = atual[0] - anterior[0]
            dy = atual[1] - anterior[1]
            passo_para_tras = (dx < 0 or dy < 0)
            em_obstaculo    = tuple(atual) in obstaculos
        
            if em_obstaculo or passo_para_tras:
                custo_atual = calculaCusto(rota)     
                candidatos_mov = (2, 1) #Tenta movimentos 1 e 2 (right up) e só aplica se reduzir custo
                aplicado = False
                for mov in candidatos_mov:
                    movX, movY = movimentos[mov]
                    nx, ny = anterior[0] + movX, anterior[1] + movY
        
                    #Regras básicas do tabuleiro e sem obstáculo
                    if not (0 <= nx < N and 0 <= ny < N):
                        continue
                    if (nx, ny) in obstaculos:
                        continue
                    rota_teste = rota[:-1] + [[nx, ny]]
                    if calculaCusto(rota_teste) < custo_atual:
                        rota = rota_teste
                        posicao = rota[-1][:]   
                        aplicado = True
                        break  #Se não aplicar nenhum desvio melhor mantém como está
        custo = calculaCusto(rota)
```

📘 Explicação:
Depois que o robô dá um novo passo, verificamos se ele entrou em uma célula “ruim”:
- **Pisou em obstáculo**, que é muito penalizado (+50 no custo);
- **Andou para trás** (left-down), que fere a heurística right-up (+10 no custo);

Se isso acontecer, testamos somente dois candidatos de desvio a partir do ponto anterior: Direita (2) ou Cima (1). Se alguma dessas opções gerar um custo total menor, substituímos o ponto atual pelo novo.

➡️ Resultado: a rota se ajusta automaticamente, sem recomeçar, e melhora passo a passo.

---

## Elaborado por: Nadine Vasconcellos e Sophia Ferreira




