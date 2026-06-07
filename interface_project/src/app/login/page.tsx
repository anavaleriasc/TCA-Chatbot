"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/services/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // function handleLogin() {
  //   const success = login(email, password);

  //   if (success) {
  //     router.push("/chat");
  //   } else {
  //     alert("Credenciais inválidas");
  //   }
  // }

  async function handleLogin() {
    const result = await login(email, password); // await é obrigatório aqui!

    if (result.success) {
      router.push("/chat");
    } else {
      alert("Erro: " + result.error);
    }
}

  return (
    <main className="landing-page">

      {/* Background e Header */}
      <div className="background-glow"></div>
      <header className="landing-header">
        <div className="logo">
          <img src="/opala.png" alt="Logo" />
        </div>

        <nav>
          <a href="#sobre">Sobre</a>
          <a href="#tecnologias">Tecnologias</a>
        </nav>
      </header>

      {/* Hero e Login */}
      <section className="hero-section">

        <div className="hero-left">
          <img src="/opala.png"/>
          <h2> ChatBot Project </h2>

          <p>
            Ambiente desenvolvido para a
            disciplina de Tópicos em
            Computação Aplicada utilizando
            FastAPI, LangChain, PostgreSQL
            e Next.js.
          </p>
        </div>

        <div className="hero-right">
          <div className="login-card">
            <h2>Entrar</h2>
            <input
              className="auth-input"
              placeholder="Email"
              onChange={(e) =>
                setEmail(e.target.value)
              }
            />

            <input
              className="auth-input"
              type="password"
              placeholder="Senha"
              onChange={(e) =>
                setPassword(e.target.value)
              }
            />

            <button
              className="auth-button"
              onClick={handleLogin}
            >
              Entrar
            </button>

          </div>
        </div>
      </section>

      {/* Sobre */}
      <section
        id="sobre"
        className="presentation-section"
      >

        <h2>Sobre o Projeto</h2>

        <p>
          O sistema consiste em uma
          plataforma web de chatbot
          inteligente capaz de gerenciar
          múltiplas sessões de conversa,
          autenticação de usuários e
          integração com modelos de
          linguagem através do LangChain.
        </p>

      </section>

      {/* Tecnologias */}
      <section
        id="tecnologias"
        className="tech-section"
      >

        <h2>Tecnologias Utilizadas</h2>

        <div className="tech-grid">
          <div>Next.js</div>
          <div>FastAPI</div>
          <div>LangChain</div>
          <div>PostgreSQL</div>
          <div>Docker</div>
          <div>AWS</div>
        </div>

      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="logo">
          <img src="/opala.png" alt="Logo" />
        </div>
        <p>OPALA ChatBot © 2026</p>
      </footer>

    </main>
  );
}