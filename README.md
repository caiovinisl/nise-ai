# nise-ai

Solução de problemas reais por meio de Inteligência Artificial

<p align="center">
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/caiovinisl/nise-ai?color=%2304D361">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/caiovinisl/nise-ai">
  
  <a href="https://github.com/caiovinisl/metodos-hashing/commits/main">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/caiovinisl/nise-ai">
  </a>
   
   <a href="https://github.com/caiovinisl/metodos-hashing/stargazers">
    <img alt="Stargazers" src="https://img.shields.io/github/stars/caiovinisl/nise-ai?style=social">
  </a>
  
 
</p>

<h4 align="center"> 
	🚧 NiseAI 🚧
</h4>

<p align="center">
	<img alt="Status Concluído" src="https://img.shields.io/badge/STATUS-CONCLU%C3%8DDO-brightgreen">
</p>

<p align="center">
 <a href="#-sobre-o-projeto">Sobre</a> •
 <a href="#-funcionalidades">Funcionalidades</a> •
 <a href="#-como-executar-o-projeto">Como executar</a> • 
 <a href="#-tecnologias">Tecnologias</a>
</p>

## 💻 Sobre o projeto

📄 NiseAI

### Detalhamento
Problema: Alcançar bem-estar e evitar o burn out nos indivíduos.

Algoritmos escolhidos:
- Q-Learning: Define política ótima
- Busca Gulosa: Define ordenação dos passeios

Especificação: Precisamos decidir a proporção de passeios em um mês, maximizando o bem-estar do indivíduo. Cada passeio gera um gasto financeiro e físico, porém um ganho social. Se uma grande quantidade de passeios for agendada, o indivíduo pode ficar cansado ou sem dinheiro para outros passeios. Precisamos encontrar a proporção ideal de passeios para realizar e maximizar o retorno, mantendo o indivíduo entretido.

Estados: Entediado, Entretido, Cansado, Sem dinheiro e Burn-out.

Ações: Para simplificar, pressupõe que hajam apenas três ações: passear, nao_passear e trabalhar.

Recompensas: O passeio em determinado estado gera recompensas com a tupla {Financeiro, Físico e Social}

Transições de estado: passear em um estado tem maior probabilidade de se mover para um estado com menos dinheiro, disposição física, mas satisfação social. Da mesma forma, a ação nao_passear tem maior probabilidade de passar para o estado de entediado. A ação de trabalhar gera um retorno financeiro, mas gasto físico e social.

Burn-out é um estado final, pois uma vez que um agente indivíduo chega a este estado, ele não pode mais executar quaisquer ações para obter mais recompensas
É um estado do MDP que não tem arestas de saída (sinkstate) 

![MATA64 Inteligência Artificial - Trabalho Final](https://github.com/caiovinisl/nise-ai/assets/31699879/44c15e2b-a27a-450f-8992-4914e143523a)

---

## ⚙️ Funcionalidades

- [x] Gerar Política Ótima
- [x] Gerar Ordenação de Passeios
- [x] Gerar Calendário de Ações do Mês

---

## 🛣️ Como executar o projeto

#### 🎲 Rodando a aplicação

```bash

# Clone este repositório
$ git clone https://github.com/caiovinisl/nise-ai.git

# Acesse a pasta do projeto no terminal/cmd
$ cd nise-ai

# Instale dependências
$ npm install

# Execute frontend
$ npm start

# Execute backend
$ python learning.py > log.txt

#Abra no seu terminal o localhost:3000 e use a aplicação


```

## 🛠 Tecnologias

- **[Python](https://www.python.org/)**
- **[Flask](https://flask.palletsprojects.com/en/3.0.x/)**
- **[React](https://react.dev/)**

---
