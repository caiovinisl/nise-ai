# nise-ai

Solução de problemas reais por meio de Inteligência Artificial

<p align="center">
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/caiovinisl/hoje-e-onde?color=%2304D361">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/caiovinisl/hoje-e-onde">
  
  <a href="https://github.com/caiovinisl/metodos-hashing/commits/main">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/caiovinisl/hoje-e-onde">
  </a>
   
   <a href="https://github.com/caiovinisl/metodos-hashing/stargazers">
    <img alt="Stargazers" src="https://img.shields.io/github/stars/caiovinisl/hoje-e-onde?style=social">
  </a>
  
 
</p>

<h4 align="center"> 
	🚧 Hoje é onde 🚧
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

📄 Inteligência Artificial de recomendação de passseios

### Detalhamento

Alcançar bem estar a partir das diferentes saúdes.

Especificação: Precisamos decidir a proporção de passeios em um mês, maximizando o bem-estar do indivíduo. Cada passeio gera um gasto financeiro e físico, porém um ganho social. Se uma grande quantidade de passeios for agendada, o indivíduo pode ficar cansado ou sem dinheiro para outros passeios. Precisamos encontrar a proporção ideal de passeios para realizar e maximizar o retorno, mantendo o indivíduo entretido.

Estados: Entediado, Entretido, Cansado e Sem dinheiro

Ações: Para simplificar, pressupõe que hajam apenas duas
ações: passear e nao_passear.
Para o estado cansado, a única ação possível é nao_passear;
Para o estado sem dinheiro, é necessário trabalhar para recuperar o dinheiro necessário para outros passeios.

Recompensas: O passeio em determinado estado gera recompensas com a tupla {Financeiro, Físico e Social}
Ação de passear gera recompensa Financeira e Física negativa e Social positiva;
Ação de não passar gera recompensa Social negativa, Financeira = 0 e Física alterna dependendo do estado atual.

Transições de estado: passear em um estado tem maior probabilidade de se mover para um estado com menos dinheiro, disposição física, mas satisfação social. Da mesma forma, a ação nao_passear tem maior probabilidade de passar para o estado de entediado.

Estado, Ação, Probabilidade, {Recompensa Financeira, Recompensa Física, Recompensa Social} -> Estado que transaciona
Entediado, Não passear, 1, {0,0,0} -> Entediado
Entediado, Passear, 0.7, {-500,-5,5} -> Entretido
Entediado, Passear, 0.3, {-500,-5,5} -> Entediado
Entretido, Passear, 0.7, {-500, -10, +10} -> Entretido
Entretido, Passear, 0.25,{-500, -10, +10} -> Cansado
Entretido, Passear, 0.05, {-1000, 5, +10} -> Sem dinheiro
Entretido, Não Passear, 0.7, {0, 5, -5} -> Entediado
Entretido, Não Passear, 0.3, {0, +5, -5} -> Entretido
Sem dinheiro, Trabalhar, 1, {3000, -10, 0} -> Entediado
Cansado, Não Passear, 0.05, {0, 5, -5} -> Cansado
Cansado, Não Passear, 0.25, {0, +5, -5} -> Entretido
Cansado, Não Passear, 0.7, {0, +5, -5} -> Entediado

Especificação: Precisamos decidir a proporção de passeios em um mês, maximizando o bem-estar do indivíduo. Cada passeio gera um gasto financeiro e físico, porém um ganho social. Se uma grande quantidade de passeios for agendada, o indivíduo pode ficar cansado ou sem dinheiro para outros passeios. Precisamos encontrar a proporção ideal de passeios para realizar e maximizar o retorno, mantendo o indivíduo entretido.

Estados: Entediado, Entretido, Cansado e Sem dinheiro

Ações: Para simplificar, pressupõe que hajam apenas duas
ações: passear e nao_passear.
Para o estado cansado, a única ação possível é nao_passear;
Para o estado sem dinheiro, é necessário trabalhar para recuperar o dinheiro necessário para outros passeios.

Recompensas: O passeio em determinado estado gera recompensas com a tupla {Financeiro, Físico e Social}
Ação de passear gera recompensa Financeira e Física negativa e Social positiva;
Ação de não passar gera recompensa Social negativa, Financeira = 0 e Física alterna dependendo do estado atual.

Transições de estado: passear em um estado tem maior probabilidade de se mover para um estado com menos dinheiro, disposição física, mas satisfação social. Da mesma forma, a ação nao_passear tem maior probabilidade de passar para o estado de entediado.

Estado, Ação, Probabilidade, {Recompensa Financeira, Recompensa Física, Recompensa Social} -> Estado que transaciona
Entediado, Não passear, 1, {0,0,0} -> Entediado
Entediado, Passear, 0.7, {-500,-5,5} -> Entretido
Entediado, Passear, 0.3, {-500,-5,5} -> Entediado
Entretido, Passear, 0.7, {-500, -10, +10} -> Entretido
Entretido, Passear, 0.25,{-500, -10, +10} -> Cansado
Entretido, Passear, 0.05, {-1000, 5, +10} -> Sem dinheiro
Entretido, Não Passear, 0.7, {0, 5, -5} -> Entediado
Entretido, Não Passear, 0.3, {0, +5, -5} -> Entretido
Sem dinheiro, Trabalhar, 1, {3000, -10, 0} -> Entediado
Cansado, Não Passear, 0.05, {0, 5, -5} -> Cansado
Cansado, Não Passear, 0.25, {0, +5, -5} -> Entretido
Cansado, Não Passear, 0.7, {0, +5, -5} -> Entediado

---

## ⚙️ Funcionalidades

- [ ]

---

## 🛣️ Como executar o projeto

#### 🎲 Rodando a aplicação

```bash

# Clone este repositório
$ git clone https://github.com/caiovinisl/hoje-e-onde.git

# Acesse a pasta do projeto no terminal/cmd
$ cd hoje-e-onde

# Execute


```

## 🛠 Tecnologias

- **[Python](https://www.python.org/)**

---
