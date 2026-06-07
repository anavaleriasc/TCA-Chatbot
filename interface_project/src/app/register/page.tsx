"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function RegisterPage() {
  const router = useRouter();

  // Estados alinhados com o user_model.py (apenas email e senha)
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  
  // Estados para feedbacks e controle de requisição
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      // Fazendo a requisição real para a rota criada no user_router.py
      const response = await fetch("http://localhost:8000/usuarios", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      if (response.ok) {
        // Redireciona para a página de login após o cadastro bem-sucedido
        router.push("/login");
      } else {
        const data = await response.json();
        // Captura a mensagem de erro do FastAPI (ex: email já cadastrado)
        const errorMessage = data.detail?.[0]?.msg || data.detail || "Erro ao tentar cadastrar o usuário. Verifique os dados.";
        setError(String(errorMessage));
      }
    } catch (err) {
      setError("Erro de conexão. Verifique se o servidor backend está rodando.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="landing-page">

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

      <section className="hero-section">
        <div className="hero-left">
          <img src="/opala.png" alt="Logo Opala" />
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
            <h2>Criar Conta</h2>

            <form onSubmit={handleRegister} style={{ display: "flex", flexDirection: "column", width: "100%" }}>
              
              {error && (
                <div style={{ color: "#ff4d4f", marginBottom: "10px", fontSize: "14px", textAlign: "center" }}>
                  {error}
                </div>
              )}

              {/* Input de Nome removido para espelhar o backend */}

              <input
                className="auth-input"
                placeholder="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />

              <input
                className="auth-input"
                placeholder="Senha"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />

              <button 
                className="auth-button" 
                type="submit"
                disabled={isLoading}
              >
                {isLoading ? "Cadastrando..." : "Cadastrar"}
              </button>
            </form>

            <p className="auth-footer-text" style={{ marginTop: "15px", fontSize: "14px", textAlign: "center" }}>
              Já possui uma conta?{" "}
              <Link href="/login" style={{ color: "#0070f3", textDecoration: "underline", fontWeight: "500" }}>
                Login
              </Link>
            </p>

          </div>
        </div>
      </section>

      <section id="sobre" className="presentation-section">
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

      <section id="tecnologias" className="tech-section">
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

      <footer className="footer">
        <div className="logo">
          <img src="/opala.png" alt="Logo" />
        </div>
        <p>OPALA ChatBot © 2026</p>
      </footer>

    </main>
  );
}