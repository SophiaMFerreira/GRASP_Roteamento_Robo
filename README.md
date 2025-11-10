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

### Fase Construtiva

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

O cálculo de custos considera os pesos apresentados anteriormente e pode ser representado de forma simplificada como:

```python
def calcular_custo(movimento):
    
    pesos = {"cima": 10, "direita": 10, "baixo": 5, "esquerda": 5}
    return pesos.get(movimento, 0)
```

## Elaborado por: Nadine Vasconcelos e Sophia Ferreira




