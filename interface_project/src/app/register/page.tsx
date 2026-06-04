export default function RegisterPage() {
  return (
    <main className="auth-page">

      <div className="auth-card">

        <h1 className="auth-title">
          Criar Conta
        </h1>

        <div className="auth-form">

          <input
            className="auth-input"
            placeholder="Nome"
          />

          <input
            className="auth-input"
            placeholder="Email"
          />

          <input
            className="auth-input"
            placeholder="Senha"
            type="password"
          />

          <button className="auth-button">
            Cadastrar
          </button>

        </div>

      </div>

    </main>
  );
}