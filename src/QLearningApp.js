// Exemplo de um componente React para iniciar o algoritmo Q-learning
import React, { useEffect, useState } from "react";
import axios from "axios";
import Lottie from "react-lottie";
import "./style.css";
import logo from "./Assets/logo.png";
import animationData from "./Assets/loading.json";

const QLearningApp = () => {
  const [policy, setPolicy] = useState({});
  const [learning, setLearning] = useState(false);
  const [orderOfTours, setOrderOfTours] = useState({});
  const [calendario, setCalendario] = useState([]);
  const [alpha, setAlpha] = useState(0.1);
  const [gamma, setGamma] = useState(0.1);
  const [epsilon, setEpsilon] = useState(0.1);

  const [policyVisible, setPolicyVisible] = useState(true);
  const [orderVisible, setOrderVisible] = useState(true);

  const togglePolicyVisibility = () => {
    setPolicyVisible(!policyVisible);
  };

  const toggleOrderVisibility = () => {
    setOrderVisible(!orderVisible);
  };

  const handleAlphaChange = (e) => {
    setAlpha(parseFloat(e.target.value));
  };

  const handleGammaChange = (e) => {
    setGamma(parseFloat(e.target.value));
  };

  const handleEpsilonChange = (e) => {
    setEpsilon(parseFloat(e.target.value));
  };

  const startQLearning = async () => {
    try {
      setLearning(true);
      console.log("Iniciou o Aprendizado");
      const response = await axios.post(
        "http://localhost:5000/start_q_learning",
        {
          alpha: alpha,
          gamma: gamma,
          epsilon: epsilon,
        }
      );
      console.log("Resposta recebida:", response.data);
      setPolicy(response.data.policy);
    } catch (error) {
      console.error("Erro ao iniciar o Aprendizado:", error);
    }
  };

  const getResultQLearning = async () => {
    try {
      setLearning(false);
      const response = await axios.post(
        "http://localhost:5000/result_q_learning"
      );
      console.log("Parou o Aprendizado");
      console.log("Resposta recebida:", response.data);
      setPolicy(response.data.policy);

      if (response.data.orderOfTours) {
        console.log(
          "Ordem dos passeios realizados:",
          response.data.orderOfTours
        );
        setOrderOfTours(response.data.orderOfTours);
      }
    } catch (error) {
      console.error("Erro ao parar o Aprendizado:", error);
    }
  };

  const obterCalendario = async () => {
    try {
      const response = await axios.get("http://localhost:5000/calendario");
      setCalendario(response.data.calendario);

      if (response.data.calendario) {
        console.log("Calendário:", response.data.calendario);

        // Mapeamento de substituição
        const abreviacoes = {
          "Nao Passear": "NP",
          Passear: "P",
          Trabalhar: "T",
        };

        const calendarioAbreviado = response.data.calendario.map((item) => {
          Object.keys(abreviacoes).forEach((chave) => {
            item = item.replace(chave, abreviacoes[chave]);
          });
          return item;
        });
        setCalendario(calendarioAbreviado);
        console.log("Calendário Abreviado:", calendarioAbreviado);
      }
    } catch (error) {
      console.error("Erro ao obter o calendário:", error);
    }
  };

  console.log("Estado de learning:", learning);

  return (
    <div>
      <img src={logo}></img> <br />
      <h4>Caminho para o bem-estar</h4>
      <div className="config-container">
        <p>Configurações do aprendizado</p>
        <div className="inputs">
          <label className="config-label" htmlFor="alpha-input" data-label="α:">
            <input
              className="config-input"
              type="number"
              step="0.1"
              max="1"
              min="0.1"
              value={alpha}
              onChange={handleAlphaChange}
            />
          </label>
          <label className="config-label" htmlFor="gamma-input" data-label="γ:">
            <input
              className="config-input"
              type="number"
              step="0.1"
              max="1"
              min="0.1"
              value={gamma}
              onChange={handleGammaChange}
            />
          </label>
          <label
            className="config-label"
            htmlFor="epsilon-input"
            data-label="ε:"
          >
            <input
              className="config-input"
              type="number"
              step="0.1"
              max="1"
              min="0.1"
              value={epsilon}
              onChange={handleEpsilonChange}
            />
          </label>
        </div>
      </div>
      {learning ? (
        policy ? (
          <div id="loading">
            <button id="resultado-indisponivel">
              <Lottie
                options={{
                  loop: true,
                  autoplay: true,
                  animationData: animationData,
                }}
                height={200}
                width={200}
              />
            </button>
          </div>
        ) : (
          <button id="resultado-disponivel" onClick={getResultQLearning}>
            Obter Resultado
          </button>
        )
      ) : (
        <button id="iniciar" onClick={startQLearning}>
          Iniciar Aprendizado
        </button>
      )}
      <div>
        {policy && Object.keys(policy).length > 0 ? (
          <div>
            <button id="obter-calendario" onClick={obterCalendario}>
              Obter Calendário
            </button>
            <h2 onClick={togglePolicyVisibility}>Política Ótima</h2>
            {policyVisible ? (
              <ul>
                {Object.keys(policy).map((state) => (
                  <li key={state}>
                    {state} - Ação: {policy[state]}
                  </li>
                ))}
              </ul>
            ) : (
              <></>
            )}
          </div>
        ) : (
          <p>Ainda não há dados de política disponíveis.</p>
        )}
        {orderOfTours && Object.keys(orderOfTours).length > 0 ? (
          <div>
            <h2 onClick={toggleOrderVisibility}>Ordem dos passeios</h2>
            {orderVisible ? (
              <ul className="orderOfTours">
                {Object.keys(orderOfTours).map((key) => (
                  <li key={key}>{orderOfTours[key]}</li>
                ))}
              </ul>
            ) : (
              <></>
            )}
          </div>
        ) : (
          <></>
        )}

        {calendario.length > 0 ? (
          <div id="calendar">
            <h2>Calendário de 30 Dias</h2>
            <ul>
              {calendario.map((dia, index) => (
                <li key={index} className={dia.toLowerCase().replace(" ", "")}>
                  {index + 1}
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <></>
        )}
      </div>
    </div>
  );
};

export default QLearningApp;
