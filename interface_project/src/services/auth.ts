export const login = async (email: string, password: string) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Mudamos para JSON
      },
      body: JSON.stringify({
        email: email, // Ajuste para o nome do campo que o seu Pydantic espera
        password: password
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(JSON.stringify(errorData));
    }

    return await response.json();
  } catch (error) {
    console.error("Erro no login:", error);
    throw error;
  }
};

export function logout() {
  localStorage.removeItem("authenticated");
}

export function isAuthenticated() {
  return localStorage.getItem("authenticated") === "true";
}