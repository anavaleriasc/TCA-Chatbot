"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/services/auth";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleLogin() {
    const success = login(email, password);

    if (success) {
      router.push("/chat");
    } else {
      alert("Credenciais inválidas");
    }
  }

  return (
    <main className="auth-page">
      <div className="auth-card">

        <h1 className="auth-title">
          OPALA
        </h1>

        <div className="auth-form">

          <input
            className="auth-input"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
          />

          <input
            className="auth-input"
            type="password"
            placeholder="Senha"
            value={password}
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
    </main>
  );
}