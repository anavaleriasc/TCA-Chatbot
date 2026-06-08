export const login = async (email: string, password: string) => {
  try {
    const response = await fetch("http://52.67.190.156:8000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        password: password
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(JSON.stringify(errorData));
    }

    const data = await response.json();
    // Armazena o token JWT
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("authenticated", "true");
    return data;
  } catch (error) {
    console.error("Erro no login:", error);
    throw error;
  }
};

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("authenticated");
}

export function isAuthenticated() {
  return localStorage.getItem("authenticated") === "true";
}

export function getToken() {
  return localStorage.getItem("access_token");
}