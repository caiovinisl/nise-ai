from flask import Flask, request, jsonify
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

learning_active = True
politica_otima = {}

estados = ['Entediado', 'Entretido', 'Cansado', 'Sem dinheiro', 'Burn Out']

acoes = ['Passear', 'Nao Passear', 'Trabalhar']

# Array de passeios com as respectivas recompensas
passeios = {
    'Museu': (-200, -200, 500),
    'Parque': (-150, -150, 300),
    'Cinema': (-100, -100, 200),
    'Shopping': (-250, -250, 400),
    'Praia': (-300, -300, 600)
}

# Lista para controlar os passeios já realizados
passeios_realizados = {passeio: 0 for passeio in passeios}

# Tabela de transições e recompensas Ação(Recompensa Financeira, Recompensa Física, Recompensa Social)
transicoes = {
    'Entediado': {
        'Nao Passear': {'Entediado': (0, 0, 0)},
        'Passear': {'Entretido': (-500, -500, 500), 'Entediado': (-500, -500, 500)},
        'Trabalhar':{'Entediado': (500,-500,0), 'Cansado': (500,-100,0)}
    },
    'Entretido': {
        'Nao Passear': {'Entediado': (0, 5, -5), 'Entretido': (0, 5, -5)},
        'Passear': {'Entretido': (-500, -100, 10), 'Cansado': (-500, -100, 10), 'Sem dinheiro': (-1000, 500, 100)},
        'Trabalhar': {'Entediado': (1000,-100,0), 'Cansado': (1000, -100,0)}
    },
    'Cansado': {
        'Nao Passear': {'Cansado': (0, 500, -500), 'Entretido': (0, 500, -500), 'Entediado': (0, 500, -500)},
        'Passear': {'Cansado': (-500, -150, -500)},
        'Trabalhar': {'Burn Out': (200,-150,0)}
    },
    'Sem dinheiro': {
        'Nao Passear': {'Sem dinheiro': (0, 0, 0)},
        'Passear': {'Burn Out': (-500,-150,0)},
        'Trabalhar': {'Entediado': (500, -150, 0), 'Burn Out': (200, -150,0)},
    },
    'Burn Out': {
        'Nao Passear': {'Burn Out': (-10000,-10000,-10000)},
        'Passear': {'Burn Out': (-10000,-10000,-10000)},
        'Trabalhar': {'Burn Out': (-10000,-10000,-10000)},
    }
}

probabilidades = {
    'Entediado': {
        'Nao Passear': {'Entediado': 1.0},
        'Passear': {'Entretido': 0.3, 'Entediado': 0.7},
        'Trabalhar': {'Entediado': 0.7, 'Cansado': 0.3}
    },
    'Entretido': {
        'Nao Passear': {'Entediado': 0.7, 'Entretido': 0.3},
        'Passear': {'Entretido': 0.7, 'Cansado': 0.25, 'Sem dinheiro': 0.05},
        'Trabalhar': {'Entediado': 0.5, 'Cansado': 0.5}
    },
    'Cansado': {
        'Nao Passear': {'Cansado': 0.05, 'Entretido': 0.25, 'Entediado': 0.7},
        'Passear': {'Cansado': 1.0},
        'Trabalhar': {'Burn Out': 1.0}
    },
    'Sem dinheiro': {
        'Nao Passear': {'Sem dinheiro': 1.0},
        'Passear': {'Burn Out': 1.0},
        'Trabalhar': {'Entediado': 0.7, 'Burn Out': 0.3},
    },
    'Burn Out': {
        'Nao Passear': {'Burn Out': 1},
        'Passear': {'Burn Out': 1},
        'Trabalhar': {'Burn Out': 1},
    }
}

# Função para determinar a ordem ideal dos passeios
def ordem_passeios():
    return sorted(passeios.keys(), key=lambda x: (-passeios[x][0], passeios[x][1], -passeios[x][2]))

# Função para escolher um passeio de acordo com a abordagem de busca gulosa
def escolher_passeio_guloso():
    ordem_passeios_atual = ordem_passeios()
    for passeio in ordem_passeios_atual:
        if passeios_realizados[passeio] == 0:
            passeios_realizados[passeio] = 1
            return passeio
    return None

# Tabela Q (inicialmente vazia)
Q = {}
for estado in estados:
    Q[estado] = {}
    for acao in acoes:
        Q[estado][acao] = [0, 0, 0]

# Parâmetros do algoritmo de aprendizado
alpha = 0.1  #Taxa de aprendizado
gamma = 0.1  #Fator de desconto
epsilon = 0.1  #Taxa de exploração

# print("Politica otima antes de enviar:", politica_otima)

@app.route('/start_q_learning', methods=['POST'])
def start_q_learning():
    global learning_active
    global alpha
    global gamma
    global epsilon

    alpha = float(request.json.get('alpha'))
    gamma = float(request.json.get('gamma'))
    epsilon = float(request.json.get('epsilon'))

    total_iterations = 10000
    total_states_visited = set()

    for i in range(total_iterations):
        if not learning_active:
            break  # Se learning_active for False, saia do loop
        estado_atual = np.random.choice(estados)
        total_states_visited.add(estado_atual)
        print(f"Iteracao {i + 1}")
        while estado_atual != 'Burn Out':
            print(f"Estado atual: {estado_atual}")
            acoes_validas = list(transicoes[estado_atual].keys())
            
            if np.random.uniform(0, 1) < epsilon:
                acao_escolhida = np.random.choice(acoes_validas)
                print(f"Acao escolhida aleatoriamente: {acao_escolhida}")
            else:
                acoes_q = {acao: sum(Q[estado_atual][acao]) for acao in acoes_validas}
                acao_escolhida = max(acoes_q, key=acoes_q.get)
                print(f"Acao escolhida com base no Q-Value: {acao_escolhida}")
            
            if acao_escolhida in transicoes[estado_atual]:
                prox_estado_probs = probabilidades[estado_atual][acao_escolhida]
                prox_estados = list(prox_estado_probs.keys())
                probs = list(prox_estado_probs.values())
                
                prox_estado = np.random.choice(prox_estados, p=probs)
                print(f"Proximo estado: {prox_estado}")

                if prox_estado != 'Burn Out':
                    q_antigo = Q[estado_atual][acao_escolhida]
                    prox_acoes = Q[prox_estado]
                    
                    max_prox_acao = max(prox_acoes, key=lambda k: sum(prox_acoes[k]))
                    prox_recompensa = transicoes[estado_atual][acao_escolhida][prox_estado]

                    q_novo = q_antigo[0] + alpha * (prox_recompensa[0] + gamma * Q[prox_estado][max_prox_acao][0] - q_antigo[0])
                    Q[estado_atual][acao_escolhida][0] = q_novo
                    estado_atual = prox_estado
                    total_states_visited.add(estado_atual)
                else:
                    print("Estado final alcancado: Burn Out")
                    break

                 # Escolher o passeio caso a ação seja 'Passear'
                if acao_escolhida == 'Passear':
                    global passeios_realizados
                    passeio_escolhido = escolher_passeio_guloso()
                    if passeio_escolhido:
                        print(f"Passeio escolhido: {passeio_escolhido}")
                    # else:
                    #     print("Todos os passeios foram realizados 3 vezes. Reiniciando contagem.")
                    #     passeios_realizados = {passeio: 0 for passeio in passeios}
            else:
                print("Acao invalida. Procurando por uma acao valida para este estado")
                acoes_validas = [acao for acao in transicoes[estado_atual].keys() if acao in Q[estado_atual]]
                
                if acoes_validas:
                    # Escolhe a primeira ação válida encontrada
                    acao_escolhida = np.random.choice(acoes_validas)
                    # print(f"Ação válida escolhida: {acao_escolhida}")
                    
                    # Continua para o próximo estado com a ação válida escolhida
                    prox_estado_probs = probabilidades[estado_atual][acao_escolhida]
                    prox_estados = list(prox_estado_probs.keys())
                    probs = list(prox_estado_probs.values())
                    prox_estado = np.random.choice(prox_estados, p=probs)
                    print(f"Proximo estado: {prox_estado}")
                    
                    # Atualiza os valores do Q-table
                    if prox_estado != 'Burn Out':
                        q_antigo = Q[estado_atual][acao_escolhida]
                        prox_acoes = Q[prox_estado]
                        max_prox_acao = max(prox_acoes, key=lambda k: sum(prox_acoes[k]))
                        prox_recompensa = transicoes[estado_atual][acao_escolhida][prox_estado]
                        q_novo = q_antigo[0] + alpha * (prox_recompensa[0] + gamma * Q[prox_estado][max_prox_acao][0] - q_antigo[0])
                        Q[estado_atual][acao_escolhida][0] = q_novo
                        estado_atual = prox_estado
                        total_states_visited.add(estado_atual)
                    else:
                        print("Estado final alcancado: Burn Out")
                        break
                else:
                    print("Nao ha acoes validas para este estado. Terminando o episodio.")
                    break

    num_unique_states_visited = len(total_states_visited)
    average_states_per_iteration = num_unique_states_visited / total_iterations if total_iterations > 0 else 0

    percentage_visits_per_state = {}
    for estado in estados:
        state_visits = len([s for s in total_states_visited if s == estado])
        percentage_visits_per_state[estado] = state_visits / total_iterations * 100

    metrics = {
        'alpha': alpha,
        'gamma': gamma,
        'epsilon': epsilon,
        'qTabel': Q,
        'totalIterations': total_iterations,
        'totalUniqueStatesVisited': num_unique_states_visited,
        'averageStatesVisitedPerIteration': average_states_per_iteration,
        'percentageVisitsPerState': percentage_visits_per_state
    }

    for estado, acoes_q in Q.items():
        acoes_validas = list(transicoes[estado].keys())
        acoes_q_validas = {acao: sum(acoes_q[acao]) for acao in acoes_validas}
        politica_otima[estado] = max(acoes_q_validas, key=acoes_q_validas.get)
        print(f"Estado: {estado}, Política Ótima: {politica_otima[estado]}")


    print("Enviando politica otima:", politica_otima)
    return jsonify({'message': 'Learning completed', 'metrics': metrics})    

@app.route('/result_q_learning', methods=['POST'])
def result_q_learning():
    global learning_active
    learning_active = False
    policy = {}
    order_of_tours = []  # Lista para armazenar a ordem dos passeios realizados

    if politica_otima:
        for estado, acao in politica_otima.items():
            policy[estado] = acao
        print(f"Politica: {policy}")

        # Encontrar os passeios realizados
        for passeio, vezes_realizado in passeios_realizados.items():
            if vezes_realizado > 0:
                order_of_tours.append(passeio)

        print("Enviando politica otima:", politica_otima)
        print("Enviando ordem dos passeios:", order_of_tours)

        return jsonify({'policy': policy, 'orderOfTours': order_of_tours})
    else:
        return jsonify({'policy': {}, 'orderOfTours': []})

@app.route('/calendario', methods=['GET'])
def obter_calendario():
    calendario = []
    estado_atual = np.random.choice(estados)
    global epsilon

    for dia in range(30):
        acoes_validas = list(transicoes[estado_atual].keys())

        if np.random.uniform(0, 1) < epsilon:
            acao_escolhida = np.random.choice(acoes_validas)
        else:
            acao_escolhida = max(acoes_validas, key=lambda a: sum(Q[estado_atual][a]))

        calendario.append(f"{dia + 1} - {acao_escolhida}")

        # Obter o próximo estado com base na ação escolhida
        prox_estado_probs = probabilidades[estado_atual][acao_escolhida]
        prox_estados = list(prox_estado_probs.keys())
        probs = list(prox_estado_probs.values())
        prox_estado = np.random.choice(prox_estados, p=probs)

        # Atualizar o estado atual
        estado_atual = prox_estado

        # Se o próximo estado for 'Burn Out', escolha um novo estado aleatório para continuar
        if estado_atual == 'Burn Out':
            estado_atual = np.random.choice(estados)

    return jsonify({'calendario': calendario})


if __name__ == '__main__':
    app.run(debug=True)
