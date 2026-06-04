from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router
import os

# Inicializa o FastAPI
app = FastAPI(title="Chatbot Multiusuário com Gemini")

# Registra os roteadores definidos no arquivo routes.py
app.include_router(router)

# Garantindo que a pasta static exista caso seja rodado num local vazio
os.makedirs("static", exist_ok=True)

# Monta a pasta 'static' para servir o Frontend web (HTML, CSS, JS) na raiz ("/")
# A opção html=True faz com que ao acessar a raiz ele busque automaticamente o index.html
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # Na AWS EC2, host='0.0.0.0' é necessário para expor publicamente na rede
    # reload=False para produção. Deixei True para facilitar o desenvolvimento local
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
