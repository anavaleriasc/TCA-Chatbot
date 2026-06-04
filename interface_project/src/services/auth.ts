export function login(email: string, password: string) {
  if (
    email === "admin@email.com" &&
    password === "123456"
  ) {
    localStorage.setItem("authenticated", "true");
    return true;
  }

  return false;
}

export function logout() {
  localStorage.removeItem("authenticated");
}

export function isAuthenticated() {
  return localStorage.getItem("authenticated") === "true";
}