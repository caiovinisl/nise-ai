import numpy as np

# Estados possíveis: Entediado, Entretido, Cansado e Sem dinheiro
estados = ['Entediado', 'Entretido', 'Cansado', 'Sem dinheiro']

# Ações possíveis: passear e nao_passear
acoes = ['Passear', 'Não Passear']

# Tabela de transições e recompensas
transicoes = {
    'Entediado': {
        'Não Passear': {'Entediado': (0, 0, 0)},
        'Passear': {'Entretido': (-500, -5, 5), 'Entediado': (-500, -5, 5)}
    },
    'Entretido': {
        'Não Passear': {'Entediado': (0, 5, -5), 'Entretido': (0, 5, -5)},
        'Passear': {'Entretido': (-500, -10, 10), 'Cansado': (-500, -10, 10), 'Sem dinheiro': (-1000, 5, 10)}
    },
    'Cansado': {
        'Não Passear': {'Entediado': (0, 5, -5), 'Entretido': (0, 5, -5), 'Cansado': (0, 5, -5)}
    },
    'Sem dinheiro': {
        'Trabalhar': {'Entediado': (3000, -10, 0)}
    }
}

# Tabela Q (inicialmente vazia)
Q = {}
for estado in estados:
    Q[estado] = {}
    for acao in acoes:
        Q[estado][acao] = [0, 0, 0]

# Parâmetros do algoritmo de aprendizado
alpha = 0.1  # Taxa de aprendizado
gamma = 0.9  # Fator de desconto
epsilon = 0.2  # Taxa de exploração

# Algoritmo Q-learning
for i in range(10000):  # Número de iterações de aprendizado
    estado_atual = np.random.choice(estados)
    while estado_atual != 'Entediado':  # Continua até atingir o estado 'Entediado'
        if np.random.uniform(0, 1) < epsilon:
            acao_escolhida = np.random.choice(acoes)  # Exploração
        else:
            acoes_q = Q[estado_atual]
            acao_escolhida = max(acoes_q, key=lambda k: sum(acoes_q[k]))  # Ação com maior valor Q

        recompensa = transicoes[estado_atual][acao_escolhida]
        prox_estado = np.random.choice(list(recompensa.keys()), p=[prob for prob in np.array(list(recompensa.values()))[:, 0]])

        q_antigo = Q[estado_atual][acao_escolhida]
        melhor_prox_acao = max(Q[prox_estado], key=lambda k: sum(Q[prox_estado][k]))
        q_novo = q_antigo + alpha * (sum(recompensa[prox_estado]) + gamma * sum(Q[prox_estado][melhor_prox_acao]) - sum(q_antigo))
        Q[estado_atual][acao_escolhida] = q_novo
        estado_atual = prox_estado

# Encontrar a política ótima (ações para cada estado)
politica_otima = {}
for estado, acoes_q in Q.items():
    politica_otima[estado] = max(acoes_q, key=lambda k: sum(acoes_q[k]))

print("Política ótima:")
for estado, acao in politica_otima.items():
    print(f"Estado: {estado} - Ação: {acao}")
